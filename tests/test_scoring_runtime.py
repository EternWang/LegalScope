import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

ROOT=Path(__file__).resolve().parents[1]
def module(name,file):
    spec=importlib.util.spec_from_file_location(name,ROOT/'evaluation'/file)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

runtime=module('score_runtime','score.py');builder=module('score_preparation','prepare.py')
generation=module('generation_runtime','generate.py')

class ScoringRuntimeTests(unittest.TestCase):
    def test_generation_sends_only_prompt_and_excludes_hidden_thoughts(self):
        configs=json.loads((ROOT/'evaluation/generation_configs.json').read_text(encoding='utf8'))['configurations']
        google=next(c for c in configs if c['provider']=='google')
        url,key,payload=generation.request_spec(google,'Question',32768)
        self.assertEqual(payload['contents'],[{'role':'user','parts':[{'text':'Question'}]}])
        data={'candidates':[{'content':{'parts':[{'text':'Hidden','thought':True},{'text':'Answer'}]},'finishReason':'STOP'}]}
        self.assertEqual(generation.response_text(google,data)[0],'Answer')
        router=next(c for c in configs if c['provider']=='openrouter')
        payload=generation.request_spec(router,'Question',4096)[2]
        self.assertEqual(payload['messages'],[{'role':'user','content':'Question'}])
        self.assertEqual(payload['temperature'],0)

    def setUp(self):
        self.prompts=[dict(review_id='R1',document_id='D1',issue_id='I1',prompt='Analyze only these facts.',core_issue='Whether a duty arose',position_original='Support')]
        self.refs=[dict(review_id='R1',document_id='D1',issue_id='I1',citation_basis='Statute 1',supported_proposition='A duty arose',review_constraints='Closed book',old_score=4)]
        self.responses=[dict(item_id='R1',model_group='SecretModel',response='Candidate text',old_score=0)]
        self.rubric=json.loads((ROOT/'evaluation/rubrics/case_joint_aug2026.json').read_text(encoding='utf8'))

    def build(self):
        return builder.prepare(self.prompts,self.refs,self.responses,['SecretModel'],['R1'],self.rubric,'joint')

    def test_prompt_excludes_model_identity_and_prior_scores(self):
        tasks,index=self.build();text=runtime.build_prompt('cn',tasks[0],self.rubric)
        self.assertNotIn('SecretModel',text);self.assertNotIn('old_score',text)
        self.assertEqual(index[0]['model_group'],'SecretModel')
        self.assertIn('Candidate text',text)

    def test_input_hashes_are_verified(self):
        tasks,_=self.build()
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp);(p/'rubric.json').write_text(json.dumps(self.rubric),encoding='utf8')
            (p/'scoring_tasks.jsonl').write_text(json.dumps(tasks[0]),encoding='utf8')
            self.assertEqual(runtime.load_inputs(p)[0],'cn')
            tasks[0]['scoring_input']['candidate_answer']='Changed answer'
            (p/'scoring_tasks.jsonl').write_text(json.dumps(tasks[0]),encoding='utf8')
            with self.assertRaisesRegex(ValueError,'Answer hash'):runtime.load_inputs(p)

    def test_unknown_join_or_duplicate_answer_fails(self):
        self.responses*=2
        with self.assertRaisesRegex(ValueError,'Duplicate'):self.build()
        self.responses=self.responses[:1];self.refs[0]['document_id']='Other'
        with self.assertRaisesRegex(ValueError,'join'):self.build()

    def test_resume_rejects_changed_reference(self):
        tasks,_=self.build();task=tasks[0]
        result=dict(status='success',task_id=task['task_id'],
                    scoring_input_sha256=runtime.canonical_sha(task['scoring_input']),
                    runtime_sha256=runtime.RUNTIME_SHA256,prompt_sha256=task['prompt_sha256'],
                    answer_sha256=task['answer_sha256'],rubric_sha256=task['rubric_sha256'],
                    scorer_provider=runtime.SCORER_PROVIDER,requested_model=runtime.MODEL,
                    reasoning_effort=runtime.REASONING_EFFORT,stateless_execution=runtime.STATELESS_MARKER,
                    score_type='cn',A=4,B=4,C=4,review_notes='A: Relevant authority; B: Constraints met; C: Valid argument.',
                    cap_rules_triggered=[],audit_flags=[])
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'scores.jsonl';path.write_text(json.dumps(result),encoding='utf8')
            self.assertEqual(len(runtime.load_existing(path,{task['task_id']:task},task['rubric_sha256'],'cn')),1)
            task['scoring_input']['citation_basis']='Changed reference'
            with self.assertRaisesRegex(ValueError,'metadata mismatch'):
                runtime.load_existing(path,{task['task_id']:task},task['rubric_sha256'],'cn')
        original_id=tasks[0]['task_id'];self.refs[0]['citation_basis']='Changed reference'
        self.assertNotEqual(self.build()[0][0]['task_id'],original_id)

    def test_runner_rejects_tool_activity(self):
        result=SimpleNamespace(returncode=0,stderr='',stdout=json.dumps({'type':'item.started','item':{'type':'command_execution','command':'anything'}}))
        with patch.object(runtime.subprocess,'run',return_value=result):
            with self.assertRaisesRegex(runtime.RunFailure,'Tool activity'):runtime.invoke('Prompt',10,'cn')

    def test_cap_and_schema_validation(self):
        score=dict(A=0,B=3,C=2,review_notes='A: NO_EXPLICIT_AUTHORITY_A_ZERO_BC_MAX_2; B: Limited; C: Limited.',cap_rules_triggered=['NO_EXPLICIT_AUTHORITY_A_ZERO_BC_MAX_2'],audit_flags=[])
        with self.assertRaisesRegex(runtime.RunFailure,'cap'):runtime.validate_cn(score)
        score['B']=2;self.assertEqual(runtime.validate_cn(score)['B'],2)
        score['A']=True
        with self.assertRaises(runtime.RunFailure):runtime.validate_cn(score)
