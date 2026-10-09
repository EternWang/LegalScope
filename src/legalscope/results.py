"""Reproduce reported model means from the released answer-level score table."""
from __future__ import annotations
import argparse
import csv
import json
import gzip
from pathlib import Path
from statistics import mean

METRICS = ('public_exam_auto', 'public_exam_human', 'citation', 'constraint',
           'argument', 'real_case_auto', 'real_case_human', 'overall_auto', 'overall_human')
POOLS = {('exam', 'automatic'):861, ('case', 'automatic'):276,
         ('exam', 'exam_review'):80, ('case', 'lawyer_1'):10, ('case', 'lawyer_2'):10}

def aggregate(rows: list[dict], models: list[str], pools=None) -> list[dict]:
    pools = POOLS if pools is None else pools
    if not models or len(models) != len(set(models)):
        raise ValueError('Model roster must be nonempty and unique')
    grouped={}; keys=set(); ids={}
    for row in rows:
        pool=(row['track'], row['evaluation']); model=row['model_group']; rid=row['item_id']
        if pool not in pools or model not in models or not rid:
            raise ValueError('Unknown pool/model or empty item ID')
        key=(*pool,model,rid)
        if key in keys: raise ValueError('Duplicate answer score')
        keys.add(key)
        fields=('score',) if pool[0]=='exam' else ('A','B','C')
        values=[]
        for field in fields:
            value=row.get(field)
            if isinstance(value,bool) or str(value) not in ('0','1','2','3','4'):
                raise ValueError(f'{field} must be an integer from 0 to 4')
            values.append(int(value))
        excluded=('A','B','C') if pool[0]=='exam' else ('score',)
        if any(row.get(f) not in (None,'') for f in excluded):
            raise ValueError('Score fields do not match the track')
        grouped.setdefault((*pool,model),[]).append(values)
        ids.setdefault((*pool,model),set()).add(rid)
    for pool,count in pools.items():
        for model in models:
            item_ids=ids.get((*pool,model),set())
            if len(item_ids)!=count or item_ids!=ids.get((*pool,models[0]),set()):
                raise ValueError('Missing answers or inconsistent item coverage')
    for model in models:
        if ids[('case','lawyer_1',model)]!=ids[('case','lawyer_2',model)]:
            raise ValueError('Lawyer subsets do not match')
        for track,ev in [('case','lawyer_1'),('case','lawyer_2'),('exam','exam_review')]:
            if not ids[(track,ev,model)]<=ids[(track,'automatic',model)]:
                raise ValueError('Review subset is not part of automatic track')
    out=[]
    for model in models:
        def dims(track,evaluation):
            return [mean(v)*25 for v in zip(*grouped[(track,evaluation,model)])]
        ea=dims('exam','automatic')[0]; eh=dims('exam','exam_review')[0]
        a,b,c=dims('case','automatic'); ca=mean([a,b,c])
        ch=mean(dims('case','lawyer_1')+dims('case','lawyer_2'))
        out.append(dict(zip(('model_group',*METRICS),(model,ea,eh,a,b,c,ca,ch,(ea+ca)/2,(eh+ch)/2))))
    return out

def compare(actual, published):
    by_model={r['model_group']:r for r in actual}
    if len(published)!=len(by_model) or {r['model_group'] for r in published}!=set(by_model):
        raise ValueError('Published model roster differs')
    differences=[]
    for row in published:
        for metric in METRICS:
            recorded=float(row[metric]); computed=by_model[row['model_group']][metric]
            if not 0<=recorded<=100 or abs(recorded-computed)>0.050001:
                differences.append(dict(model=row['model_group'],metric=metric,published=recorded,computed=computed))
    return differences

def read_csv(path):
    path=Path(path)
    opener=gzip.open if path.suffix=='.gz' else open
    with opener(path,'rt',encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scores',type=Path,required=True)
    parser.add_argument('--roster',type=Path,required=True)
    parser.add_argument('--published',type=Path,required=True)
    args=parser.parse_args()
    models=[r['model_group'] for r in read_csv(args.roster)]
    actual=aggregate(read_csv(args.scores),models)
    differences=compare(actual,read_csv(args.published))
    print(json.dumps(dict(models=len(models),values_checked=len(models)*len(METRICS),differences=differences),indent=2))
    if differences: raise SystemExit(1)

if __name__=='__main__': main()
