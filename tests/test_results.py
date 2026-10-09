import copy
import unittest
from pathlib import Path
from legalscope.results import aggregate, compare, read_csv


class ResultsTests(unittest.TestCase):
    def test_released_scores_reproduce_all_published_values(self):
        root=Path(__file__).resolve().parents[1]
        models=[r['model_group'] for r in read_csv(root/'data/metadata/model_groups.csv')]
        rows=read_csv(root/'data/results/answer_scores.csv.gz')
        self.assertEqual(len(rows),34636)
        self.assertEqual(compare(aggregate(rows,models),read_csv(root/'data/metadata/model_performance.csv')),[])

    def setUp(self):
        self.pools = {('exam','automatic'):2, ('exam','exam_review'):1,
                      ('case','automatic'):2, ('case','lawyer_1'):1, ('case','lawyer_2'):1}
        self.rows = []
        for (track,ev),n in self.pools.items():
            for i in range(n):
                row = dict(track=track,evaluation=ev,item_id=str(i),model_group='M',score='',A='',B='',C='')
                if track=='exam': row['score'] = 4 if ev=='automatic' else 2
                else: row.update(A=0,B=2,C=4)
                self.rows.append(row)

    def test_weighting_is_equal_across_tracks_not_question_counts(self):
        actual=aggregate(self.rows,['M'],self.pools)[0]
        self.assertEqual(actual['public_exam_auto'],100)
        self.assertEqual(actual['citation'],0)
        self.assertEqual(actual['real_case_auto'],50)
        self.assertEqual(actual['overall_auto'],75)
        self.assertEqual(actual['overall_human'],50)

    def test_bad_coverage_duplicates_or_out_of_range_fail(self):
        for rows in [self.rows[:-1], self.rows+self.rows[:1]]:
            with self.assertRaises(ValueError):aggregate(rows,['M'],self.pools)
        for value in (True,1.5,-1,5,'NaN'):
            rows=copy.deepcopy(self.rows);rows[0]['score']=value
            with self.subTest(value=value),self.assertRaises(ValueError):aggregate(rows,['M'],self.pools)

    def test_same_count_wrong_review_item_is_rejected(self):
        rows=copy.deepcopy(self.rows);rows[-1]['item_id']='unseen'
        with self.assertRaises(ValueError):aggregate(rows,['M'],self.pools)

    def test_published_rounding_and_nonfinite_values(self):
        rows=aggregate(self.rows,['M'],self.pools)
        self.assertEqual(compare(rows,rows),[])
        published=copy.deepcopy(rows);published[0]['overall_auto']=75.1
        self.assertEqual(len(compare(rows,published)),1)
        published[0]['overall_auto']='nan'
        self.assertEqual(len(compare(rows,published)),1)
