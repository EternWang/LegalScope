import copy
from pathlib import Path
import tempfile
import unittest

from legalscope.review import prepare, validate_results, write_bundle, load_index


class OfflineReviewTests(unittest.TestCase):
    def setUp(self):
        self.prompts = [dict(review_id='R1', document_id='D1', issue_id='I1', prompt='Argue this case.')]
        self.refs = [dict(review_id='R1', document_id='D1', issue_id='I1', scoring_prompt='Support',
                          citation_basis='Old article', supported_proposition='Rule', review_constraints='Facts only',
                          old_score=4, model='must not leak')]
        self.answers = [dict(review_id='R1', model=m, response='An answer.', A=4, previous_notes='must not leak')
                        for m in ('Alpha', 'Beta')]

    def build(self, **kwargs):
        args = dict(prompts=self.prompts, references=self.refs, responses=self.answers,
                    models=['Alpha','Beta'], selection=['R1'], run_id='test', variant='original')
        args.update(kwargs)
        return prepare(**args)

    def test_allowlist_preserves_text_without_score_or_identity_metadata(self):
        packets, index, _ = self.build()
        for p in packets:
            self.assertEqual(set(p), {'response_id','prompt','response','reference'})
            self.assertEqual(set(p['reference']), {'scoring_prompt','citation_basis','supported_proposition','review_constraints'})
            self.assertEqual(p['response'],'An answer.')
        self.assertEqual({r['model'] for r in index},{'Alpha','Beta'})

    def test_missing_duplicate_and_unknown_answers_fail(self):
        for answers in (self.answers[:1], self.answers + self.answers[:1],
                        self.answers + [dict(review_id='bad',model='Alpha',response='a')]):
            with self.subTest(answers=answers), self.assertRaises(ValueError):
                self.build(responses=answers)

    def test_empty_and_duplicate_selection_fail(self):
        for selected in ([], ['R1','R1'], ['unknown']):
            with self.subTest(selected=selected), self.assertRaises(ValueError):
                self.build(selection=selected)

    def test_wrong_join_fails_even_with_existing_id(self):
        refs=copy.deepcopy(self.refs);refs[0]['issue_id']='wrong'
        with self.assertRaisesRegex(ValueError,'join'): self.build(references=refs)

    def test_duplicate_reference_fails(self):
        with self.assertRaisesRegex(ValueError,'Duplicate'): self.build(references=self.refs*2)

    def test_patch_is_explicit_and_requires_exact_old_text(self):
        patch=[dict(review_id='R1',before='Old article',after='Corrected article')]
        packets,_,_=self.build(patches=patch,variant='corrected')
        self.assertTrue(all(p['reference']['citation_basis']=='Corrected article' for p in packets))
        self.assertEqual(self.refs[0]['citation_basis'],'Old article')
        patch[0]['before']='different'
        with self.assertRaisesRegex(ValueError,'historical'): self.build(patches=patch)

    def test_variants_have_different_opaque_ids(self):
        a,_,_=self.build();b,_,_=self.build(variant='corrected')
        self.assertFalse({p['response_id'] for p in a} & {p['response_id'] for p in b})

    def test_validation_and_normalization(self):
        _,index,_=self.build()
        results=[dict(response_id=r['response_id'],A=4,B=2,C=0,notes='Reason') for r in index]
        summary=validate_results(results,index)
        self.assertEqual(summary[0]['case_mean'],50)
        self.assertEqual(summary[0]['citation'],100)
        self.assertEqual(summary[0]['n'],1)
        for bad in (results[:1],results+results[:1]):
            with self.assertRaises(ValueError):validate_results(bad,index)
        for value in (True,1.0,-1,5,'4'):
            bad=copy.deepcopy(results);bad[0]['A']=value
            with self.subTest(value=value),self.assertRaises(ValueError):validate_results(bad,index)

    def test_bundle_cannot_overwrite_or_accept_tampering(self):
        with tempfile.TemporaryDirectory() as folder:
            dest=Path(folder)/'new'
            values=self.build()
            write_bundle(dest,*values,{})
            self.assertEqual(len(load_index(dest)),2)
            with self.assertRaises(FileExistsError):write_bundle(dest,*values,{})
            with (dest/'packets.jsonl').open('a') as f:f.write('\n')
            with self.assertRaisesRegex(ValueError,'hash'):load_index(dest)
