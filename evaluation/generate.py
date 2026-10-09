"""Generate case responses using a recorded provider configuration.

Dry run is the default. Each request contains only one public case prompt.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


def digest(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def request_spec(config, prompt, budget):
    params = dict(config['parameters'])
    if config['provider'] == 'openrouter':
        params['max_tokens'] = budget
        return ('https://openrouter.ai/api/v1/chat/completions', 'OPENROUTER_API_KEY',
                {'model':config['model_id'], 'messages':[{'role':'user','content':prompt}], **params})
    if config['provider'] == 'google':
        params['maxOutputTokens'] = budget
        model = urllib.parse.quote(config['model_id'], safe='')
        return (f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent', 'GEMINI_API_KEY',
                {'contents':[{'role':'user','parts':[{'text':prompt}]}], 'generationConfig':params})
    raise ValueError('Unsupported provider')


def response_text(config, data):
    if config['provider'] == 'openrouter':
        choice = (data.get('choices') or [{}])[0]
        text = (choice.get('message') or {}).get('content')
        return text if isinstance(text,str) else '', str(choice.get('finish_reason','')), data.get('model'), data.get('usage',{})
    choice = (data.get('candidates') or [{}])[0]
    text = ''.join(p.get('text','') for p in choice.get('content',{}).get('parts',[]) if not p.get('thought'))
    return text, str(choice.get('finishReason','')), data.get('modelVersion'), data.get('usageMetadata',{})


def call(config, prompt, attempts):
    provider = config['provider']
    budget = config['parameters'].get('max_tokens',config['parameters'].get('maxOutputTokens'))
    maximum = config['maximum_output_budget']
    for attempt in range(1,attempts+1):
        url,key_name,payload = request_spec(config,prompt,budget)
        token = os.environ.get(key_name)
        if not token: raise RuntimeError(f'Set {key_name} in the environment')
        headers={'Content-Type':'application/json'}
        headers['Authorization' if provider=='openrouter' else 'x-goog-api-key'] = 'Bearer '+token if provider=='openrouter' else token
        req=urllib.request.Request(url,data=json.dumps(payload,ensure_ascii=False).encode('utf-8'),headers=headers)
        try:
            with urllib.request.urlopen(req,timeout=600) as response:
                data=json.loads(response.read().decode('utf-8-sig'))
            text,finish,returned,usage=response_text(config,data)
            if text.strip() and finish.lower()=='stop':
                return dict(response=text,answer_sha256=digest(text),requested_model=config['model_id'],
                            returned_model=returned,finish_reason=finish,attempts=attempt,output_budget=budget,usage=usage)
            if finish.lower() in ('length','max_tokens','max_tokens_reached'):
                budget=min(maximum,max(budget+2048,int(budget*1.5)) if provider=='openrouter' else budget*2)
            else:
                raise RuntimeError('Provider returned no complete response')
        except urllib.error.HTTPError as error:
            if error.code not in (408,409,425,429,500,502,503,504):
                raise RuntimeError(f'Provider HTTP {error.code}') from None
        except (urllib.error.URLError,TimeoutError,json.JSONDecodeError):
            pass
        if attempt<attempts:time.sleep(min(20,2**attempt))
    raise RuntimeError('No complete response within the attempt limit')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--prompts',type=Path,required=True)
    ap.add_argument('--config-file',type=Path,default=Path(__file__).with_name('generation_configs.json'))
    ap.add_argument('--model',required=True)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--limit',type=int)
    ap.add_argument('--max-attempts',type=int,default=6)
    ap.add_argument('--execute',action='store_true')
    args=ap.parse_args()
    if args.max_attempts<1 or (args.limit is not None and args.limit<0):ap.error('Invalid attempt limit or record limit')
    configs=json.loads(args.config_file.read_text(encoding='utf-8'))['configurations']
    matches=[c for c in configs if c['model_group']==args.model]
    if len(matches)!=1:ap.error('Model must identify exactly one configuration')
    cfg=matches[0]
    rows=[json.loads(l) for l in args.prompts.read_text(encoding='utf-8-sig').splitlines() if l.strip()]
    if len({r['review_id'] for r in rows})!=len(rows):ap.error('Duplicate review IDs')
    if any(not isinstance(r.get('prompt'),str) or not r['prompt'].strip() for r in rows):ap.error('Empty prompt')
    if args.limit is not None:rows=rows[:args.limit]
    budget=cfg['parameters'].get('max_tokens',cfg['parameters'].get('maxOutputTokens'))
    for r in rows:request_spec(cfg,r['prompt'],budget)
    print(json.dumps(dict(mode='execute' if args.execute else 'dry_run',model=args.model,records=len(rows))))
    if not args.execute or not rows:return
    args.out.mkdir(parents=True,exist_ok=False)
    manifest=dict(configuration=cfg,input_sha256=hashlib.sha256(args.prompts.read_bytes()).hexdigest(),
                  runtime_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),records=len(rows),max_attempts=args.max_attempts)
    (args.out/'run.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    with (args.out/'responses.jsonl').open('w',encoding='utf-8') as f:
        for r in rows:
            result=call(cfg,r['prompt'],args.max_attempts)
            f.write(json.dumps(dict(item_id=r['review_id'],model_group=args.model,prompt_sha256=digest(r['prompt']),**result),ensure_ascii=False)+'\n');f.flush()


if __name__=='__main__':main()
