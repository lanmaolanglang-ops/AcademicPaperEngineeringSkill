"""Rebuild bounded search exports and screening; never certify exhaustive retrieval."""
import copy
import json
from urllib.parse import urlsplit, parse_qsl
from workflow_io import *

RULE_VERSION = 'stable-id-explicit-version-v1'

def query_url(url, syntax):
    p = urlsplit(url)
    if p.scheme!='https' or p.netloc!='api.crossref.org' or p.path!='/works' or p.fragment:
        raise ValueError('Only explicit Crossref HTTPS /works requests supported')
    pairs = parse_qsl(p.query, keep_blank_values=True)
    if len(dict(pairs)) != len(pairs):
        raise ValueError('Duplicate request parameters')
    params = dict(pairs)
    if set(params)-{'query','rows','cursor','filter','sort','order','select'}:
        raise ValueError('Undeclared query parameters require an explicit supported mapping')
    if params.get('query') != syntax:
        raise ValueError('Recorded syntax differs from submitted query')
    return params

def key(item, occurrence):
    if item.get('DOI'):
        return 'doi:' + identifier(item['DOI'])
    if item.get('official_id'):
        return 'official:' + str(item.get('database','')) + ':' + str(item['official_id'])
    if item.get('URL'):
        return 'url:' + item['URL']
    return 'unresolved:' + occurrence

def rebuild(run, base, reader):
    for field in ('search_run_id','question','purpose','scope','query','limits','tool','license_note'):
        if not run.get(field):raise ValueError('Missing search field: '+field)
    if run.get('claim_complete'):
        raise ValueError('Retrieved counts cannot establish complete literature coverage')
    timestamp(run['started_at'])
    if run.get('processing_version', RULE_VERSION) != RULE_VERSION:
        raise ValueError('Unsupported processing rule; preserve old output for comparison')
    syntax = run['query']['syntax']
    if not isinstance(syntax,str) or not syntax:raise ValueError('Raw query syntax required')
    if not run['query'].get('language') or not isinstance(run['query'].get('history'),list):
        raise ValueError('Declare database syntax and query modification history')
    for h in run['query']['history']:
        timestamp(h['at'])
        if not h.get('syntax') or not h.get('reason'):raise ValueError('Incomplete query history')
    records=[];attempts=[];ended=False;resume=None;totals=[];failed=False
    expected_cursor='*'
    if len(run.get('pages',[]))>run['limits']['max_pages']:raise ValueError('Recorded page count exceeds declared acquisition limit')
    for index,page in enumerate(run.get('pages',[])):
        if ended:raise ValueError('Extra pages after recorded end')
        access=reader.evidence(page['access_ref'],base)
        timestamp(access['checked_at'])
        mode=page.get('format','crossref')
        if mode=='crossref':
            params=query_url(access['url'],syntax)
            final=access.get('final_url',access['url'])
            if final!=access['url']:raise ValueError('Search redirect unsupported; record/review actual chain separately')
            if params.get('cursor')!=expected_cursor:raise ValueError('Missing page or wrong recorded resume cursor')
            for k in ('filter','sort','order','select'):
                if params.get(k)!=run['query'].get(k):raise ValueError('Actual database option differs: '+k)
            rows=int(params['rows'])
            if rows!=run['limits']['rows'] or rows<1:raise ValueError('Actual rows differ from declared limit')
        elif mode=='manual-export-v1':
            if not page.get('export_note'):raise ValueError('Manual export needs provenance/limits; not a live query')
            rows=None
        else:raise ValueError('Unsupported result format')
        attempt={'access':stable(access),'response_sha256':page.get('response_ref',{}).get('sha256'),'format':mode}
        if access.get('status_code')!=200:
            if page.get('response_ref'):raise ValueError('Failed attempt cannot provide successful result records')
            attempt['error']=access.get('error','HTTP '+str(access.get('status_code')))
            failed=True;resume=access['url'];attempts.append(attempt)
            # A bounded collector stops. Subsequent retries belong to another run/history.
            if index!=len(run['pages'])-1:raise ValueError('Failure must end this run; resume in a new recorded run')
            break
        raw=raw_ref(reader,page['response_ref'],base)
        if access.get('sha256')!=page['response_ref']['sha256'] or access.get('bytes')!=len(raw):
            raise ValueError('Raw results do not match their acquisition/export record')
        body=json.loads(raw)
        if mode=='crossref':
            msg=body['message'];items=msg['items'];total=msg.get('total-results')
            if not isinstance(items,list) or len(items)>rows:raise ValueError('Malformed result page')
            totals.append(total)
            ended=len(items)<rows
            expected_cursor=msg.get('next-cursor')
            if not ended and not expected_cursor:raise ValueError('Full page missing next cursor; cannot reconstruct')
            resume=None if ended else {'cursor':expected_cursor,'syntax':syntax}
        else:
            items=body['records'];ended=True;attempt['scope']='supplied export only; original retrieval unverified'
        for j,item in enumerate(items):
            oid=f'p{index+1}-r{j+1}'
            records.append({'occurrence_id':oid,'stable_id':key(item,oid),'raw':item,
                            'origin':{'response_sha256':page['response_ref']['sha256'],
                                      'pointer':('/message/items/' if mode=='crossref' else '/records/')+str(j),
                                      'access_sha256':page['access_ref']['sha256']}})
        attempts.append(attempt)
    if not attempts:raise ValueError('No actual request/export attempt')
    groups={}
    for r in records:groups.setdefault(r['stable_id'],[]).append(r)
    unique=[];conflicts=[]
    for sid,members in groups.items():
        # Same identifier is a duplicate record, but conflicting deposited metadata stays visible.
        if len({norm(m['raw'].get('title','')) for m in members})>1:conflicts.append(sid)
        unique.append({'SRC-ID':'SRC-'+value_sha(sid)[:16],'stable_id':sid,'members':members,
                       'title':members[0]['raw'].get('title',[]), 'identity':'DISCOVERY_ONLY'})
    byid={r['stable_id']:r for r in unique};parent={x:x for x in byid};relations=[]
    def find(x):
        while parent[x]!=x:x=parent[x]
        return x
    for r in records:
        rel=r['raw'].get('relation',{})
        for kind in ('is-preprint-of','has-preprint'):
            for target in rel.get(kind,[]):
                tid='doi:'+identifier(target.get('id',''))
                if target.get('id-type')!='doi' or tid not in byid:continue
                parent[find(tid)]=find(r['stable_id'])
                relations.append({'from':r['stable_id'],'to':tid,'kind':kind,'basis':r['origin'],
                                  'meaning':'metadata-linked versions; not content equivalence'})
    studies={}
    for sid in byid:studies.setdefault(find(sid),[]).append(sid)
    titles={}
    for r in unique:titles.setdefault(norm(r['title']),[]).append(r['stable_id'])
    ambiguous=[v for t,v in titles.items() if t and len(v)>1 and len({find(i) for i in v})>1]
    # Decision logs are not inferred from presence/absence of abstracts or full text.
    decisions=[];latest={};screen_errors=[]
    for decision in run.get('screening',[]):
        d=copy.deepcopy(decision)
        if d.get('stable_id') not in byid:raise ValueError('Screening record absent from retrieved set')
        if d.get('stage') not in {'metadata','abstract','full_text','final'}:raise ValueError('Invalid screening stage')
        if d.get('decision') not in {'include','exclude','pending'}:raise ValueError('Invalid screening decision')
        if not d.get('reason') or not d.get('reviewer') or not d.get('read_scope'):raise ValueError('Screening reason/reviewer/actual range missing')
        timestamp(d['reviewed_at'])
        if d['stage'] in {'full_text','final'} and d.get('reading_level') not in {'PARTIAL_FULL_TEXT','FULL_TEXT'}:
            if d['decision']!='pending':raise ValueError('Unavailable full text cannot be treated as full screening or irrelevant')
        refs=d.get('evidence',[])
        if d['decision']!='pending' and not refs:raise ValueError('Screening judgement lacks read evidence')
        allowed={m['origin']['response_sha256'] for m in byid[d['stable_id']]['members']}
        for e in refs:
            reader.evidence(e,base)
            if d['stage'] in {'metadata','abstract'} and e['sha256'] not in allowed:
                raise ValueError('Screening metadata belongs to another retrieved record')
            if d['stage'] in {'metadata','abstract'}:
                valid={m['origin']['pointer'] for m in byid[d['stable_id']]['members'] if m['origin']['response_sha256']==e['sha256']}
                if e.get('pointer') not in valid:raise ValueError('Screening anchor points at another item')
                if d['stage']=='abstract':
                    viewed=reader.evidence(e,base)
                    if not isinstance(viewed,dict) or not viewed.get('abstract') or d.get('reading_level')!='ABSTRACT':
                        raise ValueError('Abstract screening needs an actual abstract in the viewed record')
        if d['stage'] in {'full_text','final'} and d['decision']!='pending':
            src=d.get('source')
            if not src:raise ValueError('Full text requires existing source binding, not arbitrary local text')
            _,binding=source_binding(src,base,reader)
            if binding['source_identity']!='BOUND_BY_EXISTING_REVIEW':raise ValueError('Full text attribution is not validated')
            rp=reader.resolve_ref(src['literature_ref']['path'],base)
            literature=reader.evidence(src['literature_ref'],base)
            if 'doi:'+identifier(literature['citation']['canonical_identifier'])!=d['stable_id'] and 'url:'+literature['citation']['canonical_identifier']!=d['stable_id']:
                raise ValueError('Full text source differs from screening record')
            if any(e['sha256']!=src['document_ref']['sha256'] for e in refs):raise ValueError('Screening evidence differs from bound full text')
        previous=latest.get((d['stable_id'],d['stage']))
        if previous and d.get('supersedes')!=previous['decision_id']:raise ValueError('Repeated screening decision needs review history')
        if not d.get('decision_id') or any(x['decision_id']==d['decision_id'] for x in decisions):raise ValueError('Unique decision ID required')
        latest[(d['stable_id'],d['stage'])]=d;decisions.append(d)
    counts={stage:{state:sum(d['stage']==stage and d['decision']==state for d in latest.values()) for state in ('include','exclude','pending')} for stage in ('metadata','abstract','full_text','final')}
    out={'search_run_id':run['search_run_id'],'status':'INCOMPLETE' if failed or not ended else 'RECORDED_RANGE_COMPLETE',
         'exhaustive_literature_coverage':False,'request_attempts':attempts,'resume_from':resume,
         'reported_totals':totals,'counts':{'retrieved_occurrences':len(records),'deduplicated_records':len(unique),
         'duplicate_occurrences':len(records)-len(unique),'linked_study_groups':len(studies),'screening':counts},
         'records':unique,'version_relations':relations,'study_groups':list(studies.values()),
         'ambiguous_title_groups':ambiguous,'metadata_conflicts':conflicts,'screening_history':decisions,
         'query':run['query'],'scope':run['scope'],'limits':run['limits'],'processing_version':RULE_VERSION,
         'claim_support':'Unknown','publication_status':'NOT_CHECKED','errors':[],
         'limits_note':'Study groups are metadata links, unresolved records are not certified independent studies; no scientific or full-text claim.'}
    out['request_context_sha256']=value_sha(stable({'query':{k:v for k,v in run['query'].items() if k!='history'},'scope':run['scope'],'limits':run['limits']}))
    out['raw_context_sha256']=value_sha([a['response_sha256'] for a in attempts])
    out['processing_sha256']=value_sha({'version':RULE_VERSION,'screening':stable(decisions)})
    out['context_sha256']=value_sha(stable(out))
    if run.get('compare_ref'):
        old=reader.evidence(run['compare_ref'],base)
        old_conditions=value_sha(stable({'query':{k:v for k,v in old['query'].items() if k!='history'},'scope':old['scope'],'limits':old['limits']}))
        out['comparison']={'query_changed':old_conditions!=out['request_context_sha256'],
                           'raw_responses_changed':old['raw_context_sha256']!=out['raw_context_sha256'],
                           'local_processing_changed':old['processing_sha256']!=out['processing_sha256'],
                           'prior_search_run_id':old['search_run_id'],
                           'interpretation':'Raw change may be metadata/order/access/time differences; it alone does not establish a scientific change.'}
    return out

if __name__=='__main__':entry(rebuild,__doc__)
