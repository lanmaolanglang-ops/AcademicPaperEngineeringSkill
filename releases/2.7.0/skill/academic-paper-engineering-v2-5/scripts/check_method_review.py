"""Bound method observations and limited dimensional arithmetic, not scientific certification."""
import ast
import math
from workflow_io import *

OUTCOMES={'SUPPORTED','PARTIALLY_SUPPORTED','INTERNAL_CONTRADICTION','NOT_REPORTED',
          'INSUFFICIENT_MATERIAL','NOT_APPLICABLE','EXPERT_REVIEW'}
# SI dimensions: mass, length, time, temperature. Offsets (Celsius) unsupported.
UNITS={'1':(1,(0,0,0,0)),'kg':(1,(1,0,0,0)),'g':(.001,(1,0,0,0)),
       'm':(1,(0,1,0,0)),'cm':(.01,(0,1,0,0)),'mm':(.001,(0,1,0,0)),
       's':(1,(0,0,1,0)),'min':(60,(0,0,1,0)),'h':(3600,(0,0,1,0)),
       'K':(1,(0,0,0,1)),'J':(1,(1,2,-2,0)),'kJ':(1000,(1,2,-2,0)),
       'W':(1,(1,2,-3,0)),'kW':(1000,(1,2,-3,0)),'Pa':(1,(1,-1,-2,0))}

class Q:
    def __init__(self,v,d=(0,0,0,0),g=None):
        self.v=float(v);self.d=tuple(d);self.g=g or {}
        if not math.isfinite(self.v):raise ValueError('Nonfinite numeric input/result')
    def calc(self,b,op):
        keys=set(self.g)|set(b.g)
        if isinstance(op,(ast.Add,ast.Sub)):
            if self.d!=b.d:raise ValueError('DIMENSION_MISMATCH: addition/subtraction')
            sign=1 if isinstance(op,ast.Add) else -1
            return Q(self.v+sign*b.v,self.d,{k:self.g.get(k,0)+sign*b.g.get(k,0) for k in keys})
        if isinstance(op,ast.Mult):
            return Q(self.v*b.v,[x+y for x,y in zip(self.d,b.d)],{k:self.g.get(k,0)*b.v+b.g.get(k,0)*self.v for k in keys})
        if isinstance(op,ast.Div):
            if b.v==0:raise ValueError('Division by zero')
            return Q(self.v/b.v,[x-y for x,y in zip(self.d,b.d)],{k:self.g.get(k,0)/b.v-self.v*b.g.get(k,0)/b.v**2 for k in keys})
        if isinstance(op,ast.Pow):
            if b.d!=(0,0,0,0) or b.g or int(b.v)!=b.v or abs(b.v)>4:raise ValueError('Only constant integer powers -4..4')
            n=int(b.v)
            if self.v==0 and n<0:raise ValueError('Negative power of zero')
            return Q(self.v**n,[x*n for x in self.d],{k:0 if n==0 else n*self.v**(n-1)*v for k,v in self.g.items()})
        raise ValueError('Unsupported operator')

def expression(text,variables):
    if not isinstance(text,str) or len(text)>500:raise ValueError('Expression too long/invalid')
    tree=ast.parse(text,mode='eval')
    if sum(1 for _ in ast.walk(tree))>100:raise ValueError('Expression too complex')
    def visit(n):
        if isinstance(n,ast.Expression):return visit(n.body)
        if isinstance(n,ast.Name) and n.id in variables:return variables[n.id]
        if isinstance(n,ast.Constant) and type(n.value) in (int,float):return Q(n.value)
        if isinstance(n,ast.BinOp):return visit(n.left).calc(visit(n.right),n.op)
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,(ast.UAdd,ast.USub)):
            return Q(1 if isinstance(n.op,ast.UAdd) else -1).calc(visit(n.operand),ast.Mult())
        raise ValueError('Unknown variable or forbidden expression node')
    return visit(tree)

def unit(text):
    if text in UNITS:
        v,d=UNITS[text];return Q(v,d)
    return expression(text,{k:Q(v,d) for k,(v,d) in UNITS.items() if k!='1'})

def review(record,base,reader):
    for k in ('method_review_id','CLM-ID','target','research_type','selection_reason'):
        if not record.get(k):raise ValueError('Missing method field '+k)
    sources={};evidence={};data={};input_errors=[]
    for s in record.get('sources',[]):
        sid=s['SRC-ID']
        if sid in sources:raise ValueError('Duplicate SRC-ID')
        _,binding=source_binding(s,base,reader);sources[sid]=binding
    for e in record.get('evidence',[]):
        sid=e['SRC-ID'];eid=e['EVID-ID']
        if eid in evidence or sid not in sources:raise ValueError('Duplicate evidence or unknown source')
        if e['ref']['sha256']!=sources[sid]['document_sha256']:raise ValueError('Evidence substituted from another source document')
        if not any(k in e['ref'] for k in ('line_start','pointer','xml_path')):raise ValueError('Explicit evidence location required')
        raw=reader.evidence(e['ref'],base)
        evidence[eid]={'SRC-ID':sid,'anchor':stable(e['ref']),'value':raw,'anchor_sha256':value_sha(raw)}
    for d in record.get('data',[]):
        did=d['DATA-ID'];eid=d['EVID-ID']
        if did in data or eid not in evidence:raise ValueError('Untraceable or duplicate DATA-ID')
        original=evidence[eid]['value']
        if not isinstance(original,dict) or original.get('DATA-ID')!=did or original.get('value')!=d['value'] or original.get('unit')!=d['unit']:
            raise ValueError('Data value/unit differs from actual source field')
        u=unit(d['unit']);q=Q(d['value']).calc(u,ast.Mult())
        if 'standard_uncertainty' in d:
            if d['standard_uncertainty']!=original.get('standard_uncertainty') or d['standard_uncertainty']<0:raise ValueError('Uncertainty differs from source or is negative')
        data[did]={'record':d,'si_value':q.v,'dimension':q.d,'scale':u.v}
    findings=[]
    for f in record.get('findings',[]):
        if f.get('outcome') not in OUTCOMES:raise ValueError('Method status must remain separate from Gate/support')
        if not all(f.get(k) for k in ('dimension','reason','scope','reviewer','reviewed_at')):raise ValueError('Method finding lacks reasoning/actual scope/reviewer')
        timestamp(f['reviewed_at'])
        ids=f.get('EVID-IDs',[])
        if any(e not in evidence for e in ids):raise ValueError('Finding refers to unknown evidence')
        if f['outcome'] in {'SUPPORTED','PARTIALLY_SUPPORTED','INTERNAL_CONTRADICTION','NOT_REPORTED'} and not ids:
            raise ValueError('Reported/absent/contradictory finding needs actual reviewed evidence scope')
        if f.get('asserted_event') in {'did_not_happen','fabricated','fraud'} and f['outcome'] in {'NOT_REPORTED','INSUFFICIENT_MATERIAL'}:
            raise ValueError('Missing reporting cannot prove nonoccurrence or fabrication')
        findings.append(copy.deepcopy(f))
    computations=[]
    for c in record.get('calculations',[]):
        result={'calculation_id':c['calculation_id'],'CLM-ID':record['CLM-ID'],'expression':c['expression'],'status':'CHECKED',
                'scientific_applicability':'EXPERT_REVIEW','claim_support':'Unknown'}
        try:
            if not c.get('variable_definitions') or not c.get('applicability'):
                raise ValueError('Variable definitions and applicability required')
            variables={};uncertainties={};seen_data=set()
            for name,did in c['variables'].items():
                if did not in data or name not in c['variable_definitions']:raise ValueError('Untraceable variable or missing definition')
                if did in seen_data:raise ValueError('One DATA-ID must use one variable; repeated use stays correlated')
                seen_data.add(did);d=data[did];variables[name]=Q(d['si_value'],d['dimension'],{name:1})
                if 'standard_uncertainty' in d['record']:uncertainties[name]=d['record']['standard_uncertainty']*d['scale']
            q=expression(c['expression'],variables);expected_unit=unit(c['reported_unit'])
            if q.d!=expected_unit.d:raise ValueError('DIMENSION_MISMATCH: result/report unit')
            value=q.v/expected_unit.v;tolerance=c.get('absolute_tolerance',0)
            if not math.isfinite(tolerance) or tolerance<0:raise ValueError('Nonnegative finite tolerance required')
            result.update(value=value,unit=c['reported_unit'],si_value=q.v,dimensions=q.d,
                          inputs=[data[did]['record'] for did in c['variables'].values()],
                          arithmetic_matches=math.isclose(value,float(c['reported_value']),abs_tol=tolerance,rel_tol=0),
                          tolerance=tolerance,precision_note=c.get('precision_note','Significant figures require review; no automatic certification'))
            if c['applicability'].get('status')=='NOT_MET':result['scientific_applicability']='NOT_MET'
            else:result['scientific_applicability']='SUPPLIED_ASSUMPTIONS_REQUIRE_EXPERT_REVIEW'
            if c.get('uncertainty_method'):
                if c['uncertainty_method']!='independent-first-order' or c.get('independence')!='explicit_assumption':
                    result['uncertainty']={'status':'EXPERT_REVIEW','reason':'Only explicit independent first-order propagation implemented'}
                elif set(q.g)-set(uncertainties):
                    result['uncertainty']={'status':'INSUFFICIENT_MATERIAL','missing':sorted(set(q.g)-set(uncertainties))}
                else:
                    variance=sum((grad*uncertainties[k])**2 for k,grad in q.g.items())
                    result['uncertainty']={'status':'COMPUTED_UNDER_ASSUMPTIONS','standard_uncertainty':math.sqrt(variance)/expected_unit.v,
                        'unit':c['reported_unit'],'derivatives_SI':q.g,'scope':'First order only; independence and model validity not established'}
            if not result['arithmetic_matches']:result['status']='INTERNAL_CONTRADICTION'
        except (ValueError,KeyError,TypeError,ZeroDivisionError,SyntaxError,OverflowError) as error:
            result.update(status='REVIEW_REQUIRED',reason=str(error))
        computations.append(result)
    context={'method_review_id':record['method_review_id'],'CLM-ID':record['CLM-ID'],'target':record['target'],
             'research_type':record['research_type'],'selection_reason':record['selection_reason'],
             'sources':sources,'evidence':evidence,'data':data,'calculations':record.get('calculations',[]),'findings':findings}
    fingerprint=value_sha(stable(context));review_state='NOT_SUPPLIED';errors=[]
    if record.get('review_ref'):
        saved=reader.evidence(record['review_ref'],base)
        if saved.get('context_sha256')!=fingerprint or saved.get('method_review_id')!=record['method_review_id'] or not all(saved.get(k) for k in ('reviewer','reviewed_at','reason')):
            review_state='REVIEW_REQUIRED';errors.append('Old method review does not match current claim/data/units/source context')
        else:
            timestamp(saved['reviewed_at']);review_state='CURRENT'
    return {'method_review_id':record['method_review_id'],'CLM-ID':record['CLM-ID'],'target':record['target'],
            'status':'CHECKED_NOT_SCIENTIFICALLY_CERTIFIED','review_status':review_state,'context_sha256':fingerprint,
            'findings':findings,'findings_basis':'Supplied scoped observations; independent review fingerprint governs reuse, not scientific truth',
            'calculations':computations,'source_bindings':sources,'traceable_data_ids':list(data),'errors':errors,
            'claim_support':'Unknown','paper_gate':'NOT RUN','fabrication_inference':False,
            'history':copy.deepcopy(record.get('history',[])),
            'limits':'No missing conditions invented. Unsupported units, correlated errors, significant figures and scientific applicability need actual expert review.'}

if __name__=='__main__':entry(review,__doc__)
