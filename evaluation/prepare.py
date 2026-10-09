"""Prepare anonymous case scoring tasks from public inputs and supplied answers."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path


def sha(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def read(path):
    return [json.loads(line) for line in Path(path).read_text(encoding='utf-8-sig').splitlines() if line.strip()]


def unique(rows, field):
    result = {}
    for row in rows:
        key = row.get(field)
        if not isinstance(key, str) or not key or key in result:
            raise ValueError(f'Missing or duplicate {field}')
        result[key] = row
    return result


def prepare(prompts, references, responses, models, selected, rubric, mode):
    if mode not in ('joint', 'b'):
        raise ValueError('Mode must be joint or b')
    if not models or len(set(models)) != len(models) or not selected or len(set(selected)) != len(selected):
        raise ValueError('Model and item selections must be nonempty and unique')
    ps, rs = unique(prompts, 'review_id'), unique(references, 'review_id')
    if set(ps) != set(rs) or not set(selected) <= set(ps):
        raise ValueError('Prompt/reference coverage differs or selection is unknown')
    for rid in ps:
        if any(ps[rid][k] != rs[rid][k] for k in ('document_id', 'issue_id')):
            raise ValueError('Prompt/reference join mismatch')
    answers = {}
    for row in responses:
        key = (row.get('item_id'), row.get('model_group'))
        if key in answers or key[0] not in ps:
            raise ValueError('Duplicate or unknown answer')
        value = row.get('response')
        if not isinstance(value, str) or not value.strip():
            raise ValueError('Answer must be nonempty text')
        if row.get('answer_sha256', sha(value)) != sha(value):
            raise ValueError('Answer hash mismatch')
        answers[key] = value
    rubric_sha = sha(json.dumps(rubric, ensure_ascii=False, sort_keys=True, separators=(',', ':')))
    tasks, index = [], []
    for rid in sorted(selected):
        p, r = ps[rid], rs[rid]
        for model in models:
            if (rid, model) not in answers:
                raise ValueError('Missing selected model answer')
            answer = answers[(rid, model)]
            inputs = dict(prompt=p['prompt'], citation_basis=r['citation_basis'],
                          cited_supported_proposition=r['supported_proposition'],
                          review_constraints=r['review_constraints'],
                          position=p['position_original'], core_issue=p['core_issue'],
                          candidate_answer=answer)
            if any(not isinstance(v, str) or not v.strip() for v in inputs.values()):
                raise ValueError('Empty scoring input')
            tid = ('SCN-' if mode == 'joint' else 'SCNB-') + sha(json.dumps([rid, model, inputs, rubric_sha], sort_keys=True, ensure_ascii=False))
            tasks.append(dict(task_id=tid, prompt_sha256=sha(p['prompt']), answer_sha256=sha(answer),
                              rubric_sha256=rubric_sha, scoring_input=inputs))
            index.append(dict(task_id=tid, review_id=rid, model_group=model))
    return tasks, index


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for field in ('prompts', 'references', 'responses', 'out'):
        ap.add_argument('--' + field, type=Path, required=True)
    ap.add_argument('--models', nargs='+', required=True)
    ap.add_argument('--review-ids', nargs='+')
    ap.add_argument('--mode', choices=['joint', 'b'], default='joint')
    args = ap.parse_args()
    rubric_path = Path(__file__).parent/'rubrics'/('case_joint_aug2026.json' if args.mode == 'joint' else 'case_b_aug2026.json')
    rubric = json.loads(rubric_path.read_text(encoding='utf-8'))
    prompts = read(args.prompts)
    tasks, index = prepare(prompts, read(args.references), read(args.responses), args.models,
                           args.review_ids or [r['review_id'] for r in prompts], rubric, args.mode)
    args.out.mkdir(parents=True, exist_ok=False)
    (args.out/'rubric.json').write_bytes(rubric_path.read_bytes())
    for name, rows in [('scoring_tasks.jsonl', tasks), ('identity_map.jsonl', index)]:
        (args.out/name).write_text(''.join(json.dumps(r, ensure_ascii=False)+'\n' for r in rows), encoding='utf-8')
    print(json.dumps(dict(tasks=len(tasks),mode=args.mode)))


if __name__ == '__main__':
    main()
