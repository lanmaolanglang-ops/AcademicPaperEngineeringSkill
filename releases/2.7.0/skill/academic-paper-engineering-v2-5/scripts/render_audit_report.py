"""Three report views from bound records. Preserve all failures and distinct test layers."""
from collections import Counter
from workflow_io import *

STATES={'PASS','FAIL','PARTIAL','BLOCKED','NOT RUN'}
CATEGORIES={'deterministic','real_material','live','regression','historical','repeat','independent','unexecuted'}
ORIGINS={'historical_record','current_record','first_failure','unknown'}
DIMENSIONS={'值','单位','时期','统计对象','地理','口径或情景','事实/预测/假设性质','结论'}

def render(record,base,reader):
    for k in ('report_id','verdict','scope','next_step','limits','workstreams'):
        if not record.get(k):raise ValueError('Missing report decision field '+k)
    rows=[];seen=set();counts={};issues=[]
    for row in record.get('records',[]):
        if row.get('status') not in STATES or row.get('category') not in CATEGORIES:raise ValueError('Unknown result state/layer')
        k=(row['id'],row.get('execution_id'))
        if k in seen:raise ValueError('Duplicate check would inflate counts')
        seen.add(k)
        if not row.get('reason'):raise ValueError('Result needs actual reason/scope')
        if not row.get('evidence_ref'):raise ValueError('Every result needs evidence or actual unrun/blocked declaration')
        actual=reader.evidence(row['evidence_ref'],base)
        if not isinstance(actual,dict) or actual.get('status')!=row['status'] or actual.get('id')!=row['id']:
            raise ValueError('Summary changes the bound original result identity/status')
        if actual.get('category') not in CATEGORIES or not actual.get('reason'):
            raise ValueError('Original evidence needs explicit category and reason; use a separately bound review for legacy raw logs')
        if row['reason']!=actual['reason']:
            raise ValueError('Summary changes the bound original reason')
        origin='unknown'
        if row.get('classification_ref'):
            review=reader.evidence(row['classification_ref'],base)
            expected={'id':actual['id'],'status':actual['status'],'source_sha256':row['evidence_ref']['sha256'],
                      'source_category':actual['category'],'source_reason':actual['reason'],
                      'execution_layer':row['category'],'evidence_origin':row.get('evidence_origin')}
            if any(review.get(k)!=v for k,v in expected.items()) or review.get('evidence_origin') not in ORIGINS:
                raise ValueError('Classification review is not bound to original category/reason and execution layer')
            if not all(review.get(k) for k in ('rationale','reviewer','reviewed_at')):
                raise ValueError('Classification review needs actual scope, reviewer and time')
            timestamp(review['reviewed_at']);origin=review['evidence_origin']
        elif row['category']!=actual['category'] or row.get('evidence_origin','unknown')!='unknown':
            raise ValueError('Execution layer differs from original category without a bound classification review')
        view=copy.deepcopy(row)
        view.update(execution_layer=row['category'],evidence_category=actual['category'],evidence_origin=origin,current_result=actual['status'])
        rows.append(view)
        if row['status']!='PASS':issues.append(row)
        c=counts.setdefault(row['category'],{});c[row['status']]=c.get(row['status'],0)+1
    # Reuse ledger IDs; references do not establish semantic truth.
    inventory_state='INDEX_ONLY_NOT_COMPLETENESS_VERIFIED'
    if record.get('inventory_ref'):
        inventory=reader.evidence(record['inventory_ref'],base)
        project=lambda r:(r['id'],r['status'],r['category'],r.get('execution_id',''))
        if sorted(map(project,inventory))!=sorted(map(project,rows)):
            raise ValueError('Report omits or changes records from bound inventory')
        inventory_state='BOUND_INVENTORY_COMPLETE'
    ledger=record.get('ledger',{});sources=set(ledger.get('SRC-IDs',[]));claims=set(ledger.get('CLM-IDs',[]));evidence=ledger.get('evidence',{})
    for eid,src in evidence.items():
        if src not in sources:raise ValueError('Evidence refers to missing SRC')
    relations=ledger.get('relations',[]);relids=set()
    for rel in relations:
        if rel['id'] in relids:raise ValueError('Duplicate relation')
        relids.add(rel['id'])
        if rel['CLM-ID'] not in claims or evidence.get(rel['EVID-ID'])!=rel['SRC-ID']:raise ValueError('Broken CLM-EVID-SRC relationship')
        if rel.get('status') not in {'Verified','Partial Verified','Unsupported','Need Source','Unknown'}:raise ValueError('Invalid original ledger status')
        if set(rel.get('dimensions',{}))!=DIMENSIONS or any(not v or v in {'同上','见前文'} for v in rel['dimensions'].values()):raise ValueError('Eight self-contained dimensions required')
    cites={};numbers={}
    for c in ledger.get('citations',[]):
        if c['CIT-ID'] in cites or c['SRC-ID'] not in sources:raise ValueError('Duplicate CIT or missing SRC')
        if type(c['number'])!=int or c['number']<1 or c['number'] in numbers and numbers[c['number']]!=c['SRC-ID']:raise ValueError('Citation number reused for another source')
        numbers[c['number']]=c['SRC-ID'];cites[c['CIT-ID']]=c
    occurrence_ids=set()
    for o in ledger.get('occurrences',[]):
        if o['id'] in occurrence_ids or o['CLM-ID'] not in claims or not o.get('location'):raise ValueError('Missing or duplicate claim occurrence')
        occurrence_ids.add(o['id'])
        for cid in o.get('CIT-IDs',[]):
            if cid not in cites:raise ValueError('Dangling citation in occurrence')
            if not any(r['CLM-ID']==o['CLM-ID'] and r['SRC-ID']==cites[cid]['SRC-ID'] for r in relations):raise ValueError('Citation lacks a claim/source relation')
    constraints=['检查记录数不等于独立真实论文数；合成 Gate 不等于真实论文验收。',
                 'HTTP 200、SHA256 匹配和规则通过均不证明科学主张成立；未发现通知不证明绝无撤稿。']
    summary=[str(record['verdict']), '范围：'+record['scope'], '各工作流：'+json.dumps(record['workstreams'],ensure_ascii=False),
             '分层结果：'+json.dumps(counts,ensure_ascii=False), '未关闭/非通过记录：']
    summary.extend(f"- {r['id']} [{r['category']}] {r['status']}：{r['reason']} → {r['evidence_ref']['path']}" for r in issues)
    summary.extend(['限制：']+['- '+x for x in record['limits']]+constraints+['下一步：'+record['next_step']])
    technical=['# 技术验收视图','',record['scope'],'','| ID | 本次执行层 | 原证据分类 / 属性 | 此记录结果 | 原始理由 | 证据 |','|---|---|---|---|---|---|']
    for r in rows:technical.append('| '+' | '.join(str(v).replace('|','\\|').replace('\n',' ') for v in [r['id'],r['execution_layer'],r['evidence_category']+' / '+r['evidence_origin'],r['current_result'],r['reason'],r['evidence_ref']['path']])+' |')
    technical+=['','限制：',*record['limits'],'','关系、出现位置及原状态完整保留在第三层 JSON；只做结构校验。']
    before='\n\n'.join(json.dumps({'common_scope':record['scope'],'common_limits':record['limits'],'result':r},ensure_ascii=False,indent=2) for r in rows)
    after='\n'.join(summary)
    return {'report_id':record['report_id'],'status':'CHECKED_NOT_PAPER_ACCEPTED','errors':[],
            'counts_by_layer':counts,'inventory_state':inventory_state,'nonpass_ids':[r['id'] for r in issues],
            'summary_markdown':after,'technical_markdown':'\n'.join(technical),
            'audit_evidence':{'records':rows,'ledger':ledger,'limits':record['limits'],'workstreams':record['workstreams']},
            'comparison':{'comparison_kind':'Explicit repeated-header baseline built from same records, not historical report bytes',
                          'before_characters':len(before),'summary_characters':len(after),'technical_characters':len('\n'.join(technical)),
                          'before_view':before,'all_nonpass_visible':all(r['id'] in after for r in issues),
                          'all_limits_visible':all(x in after for x in record['limits']),
                          'relation_count':len(relations),'occurrence_count':len(occurrence_ids)},
            'claim_support':'Unknown','paper_gate':'NOT RUN'}

if __name__=='__main__':entry(render,__doc__)
