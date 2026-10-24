"""Opt-in bounded Crossref GET collection. TLS stays enabled; no hidden retries."""
import argparse
import hashlib
import json
import platform
import time
import urllib.request
import urllib.error
from urllib.parse import urlencode
from workflow_io import *

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        return None

def collect(config, folder, reader, timeout=20):
    for field in ('search_run_id','question','purpose','scope','query','limits'):
        if not config.get(field):raise ValueError('Missing field '+field)
    pages=config['limits']['max_pages'];rows=config['limits']['rows']
    if type(pages)!=int or not 1<=pages<=3 or type(rows)!=int or not 1<=rows<=20:
        raise ValueError('Collector bounded to 1-3 pages and 1-20 rows per page')
    query=config['query'];syntax=query['syntax']
    if not isinstance(syntax,str) or not syntax or len(syntax)>2000:raise ValueError('Invalid query')
    if set(query)-{'syntax','language','history','filter','sort','order','select'}:raise ValueError('Unknown query option')
    if query.get('sort') in {'issued','published','published-print','published-online'}:
        raise ValueError('Crossref cursor does not support publication-date sorts; choose another explicit ordering')
    folder=Path(folder);reader.inside(folder.parent.resolve(strict=True));folder.mkdir(exist_ok=False)
    reader.inside(folder.resolve(strict=True))
    def store_bytes(name,data):
        target=reader.inside(folder.resolve(strict=True))/name
        with target.open('xb') as f:
            reader.inside(reader.opened_path(f.fileno()));f.write(data)
        return {'path':name,'sha256':hashlib.sha256(data).hexdigest()}
    def store_json(name,data):
        return store_bytes(name,json.dumps(data,ensure_ascii=False,indent=2).encode('utf-8'))
    run=copy.deepcopy(config);run.update(started_at=datetime.now(timezone.utc).isoformat(),pages=[],claim_complete=False,
        tool={'name':'collect_search.py','version':'2.7.0','python':platform.python_version(),
              'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
        license_note='Crossref bibliographic facts reusable; abstracts retain original copyright. This collector requests bibliographic fields, not abstracts or full text. https://www.crossref.org/documentation/retrieve-metadata/')
    # Never request abstracts or full-text links. Exact submitted syntax/filters remain recorded.
    selection=query.get('select','DOI,title,author,issued,relation,URL,type')
    allowed={'DOI','title','author','issued','relation','URL','type'}
    if not set(selection.split(','))<=allowed:raise ValueError('Only bibliographic fields allowed')
    run['query']['select']=selection
    cursor='*';opener=urllib.request.build_opener(NoRedirect())
    for index in range(pages):
        params={'query':syntax,'rows':str(rows),'cursor':cursor,'select':selection}
        params.update({k:query[k] for k in ('filter','sort','order') if k in query})
        url='https://api.crossref.org/works?'+urlencode(params)
        at=datetime.now(timezone.utc).isoformat();started=time.monotonic()
        access={'url':url,'checked_at':at,'simulated':False,'retry_attempt':0,'status_code':None}
        response=None;body=None
        try:
            request=urllib.request.Request(url,headers={'User-Agent':'AcademicPaperEngineeringSkill/2.7.0 (bounded research audit)','Accept':'application/json'})
            with opener.open(request,timeout=timeout) as r:
                raw=r.read(20_000_001)
                if len(raw)>20_000_000:raise ValueError('Response exceeded 20MB limit; not complete')
                access.update(status_code=r.status,final_url=r.url,bytes=len(raw),
                              headers={k:v for k,v in r.headers.items() if k.lower() in {'content-type','date','retry-after','x-rate-limit-limit','x-rate-limit-interval','x-concurrency-limit'}},sha256=hashlib.sha256(raw).hexdigest())
                response=store_bytes(f'page-{index+1}.response.json',raw)
                body=json.loads(raw)
        except urllib.error.HTTPError as e:
            access.update(status_code=e.code,error=str(e),retry_after=e.headers.get('Retry-After'),final_url=e.url)
            error_raw=e.read(65536)
            access['error_body_ref']=store_bytes(f'page-{index+1}.error-body',error_raw)
        except (urllib.error.URLError,TimeoutError,OSError,ValueError) as e:
            access['error']=type(e).__name__+': '+str(e)
            # A parse failure retains bytes, but cannot claim a usable result page.
            if response:access['unparsed_response_ref']=response;response=None;access['status_code']=None
        access['elapsed_seconds']=time.monotonic()-started
        aref=store_json(f'page-{index+1}.access.json',access)
        page={'access_ref':aref,'format':'crossref'}
        if response:page['response_ref']=response
        run['pages'].append(page)
        store_json(f'checkpoint-{index+1}.json',run)
        if access['status_code']!=200:break
        items=body.get('message',{}).get('items')
        if not isinstance(items,list):break
        if len(items)<rows:break
        cursor=body['message'].get('next-cursor')
        if not cursor:break
        if index+1<pages:time.sleep(1)
    store_json('run.json',run)
    return run

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',required=True);p.add_argument('--output-dir',required=True);p.add_argument('--allowed-root',required=True)
    a=p.parse_args();r=SecureReader(a.allowed_root);raw=r.read_path(a.input);config=json.loads(raw)
    collect(config,a.output_dir,r)
    if r.read_path(a.input)!=raw:raise ValueError('Config changed during acquisition; retained artifacts require review')
    print('Collection recorded. Run check_search_run.py; success here is not complete retrieval.')

if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,TypeError,OSError) as error:
        print(type(error).__name__+': '+str(error),file=sys.stderr);sys.exit(2)
