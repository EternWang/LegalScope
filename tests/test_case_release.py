"""Case-publication checks use synthetic records, never private judgments."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('prepare_hf_tables', ROOT / 'scripts/prepare_hf_tables.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CaseReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.package = Path(self.temp.name)
        self.cases = self.package / 'data/cases'
        self.cases.mkdir(parents=True)
        self.prompts = [dict(review_id=f'R{i}', document_id='D1', issue_id='I1', stance=s)
                        for i,s in enumerate(('support','oppose'))]
        self.refs = [{k:v for k,v in p.items() if k != 'stance'} for p in reversed(self.prompts)]
        self.write_fixture()

    def write_fixture(self):
        manifest = dict(case_prompts=2, scoring_references=2, issues=1, judgments=1,
                        stance_counts={'support':1,'oppose':1}, files={})
        for name, rows in [('case_prompts',self.prompts),('case_scoring_references',self.refs)]:
            path = self.cases / f'{name}.jsonl'
            path.write_text(''.join(json.dumps(r)+'\n' for r in rows), encoding='utf-8')
            manifest['files'][path.name] = dict(rows=len(rows), sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        (self.cases/'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')

    def test_join_uses_ids_not_order(self):
        tables, _ = module.read_case_tables(self.package)
        self.assertEqual(len(tables),2)

    def test_changed_reviewed_text_is_rejected(self):
        with (self.cases/'case_prompts.jsonl').open('a',encoding='utf-8') as handle:
            handle.write('\n')
        with self.assertRaisesRegex(ValueError,'reviewed manifest'):
            module.read_case_tables(self.package)

    def test_rehashed_reference_for_wrong_case_is_rejected(self):
        self.refs[0]['document_id']='wrong-case'
        self.write_fixture()
        with self.assertRaisesRegex(ValueError,'joins do not match'):
            module.read_case_tables(self.package)

    def test_rehashed_duplicate_ids_are_rejected(self):
        self.refs[0]['review_id']=self.refs[1]['review_id']
        self.write_fixture()
        with self.assertRaisesRegex(ValueError,'Duplicate'):
            module.read_case_tables(self.package)

    def test_missing_opposing_stance_is_rejected(self):
        self.prompts[1]['stance']='support'
        self.write_fixture()
        with self.assertRaisesRegex(ValueError,'paired stances'):
            module.read_case_tables(self.package)
