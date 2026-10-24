"""Shared bounded offline IO. Reuses fix2's trusted-root/final-handle checks."""
import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from datetime import datetime, timezone
from check_literature_record import SecureReader, value_sha, identifier, norm, evaluate, source_context

def timestamp(text):
    t = datetime.fromisoformat(text.replace('Z', '+00:00'))
    if t.tzinfo is None:
        raise ValueError('Timestamp requires timezone')
    return t.astimezone(timezone.utc).isoformat()

def stable(value):
    """Paths relocate; content/anchor/units and all other semantics remain bound."""
    if isinstance(value, dict):
        return {k:stable(v) for k,v in value.items() if k != 'path'}
    if isinstance(value, list):
        return [stable(v) for v in value]
    return value

def raw_ref(reader, ref, base):
    return reader.evidence(dict(ref, format='bytes'), base)

def save_new(reader, path, value):
    path = Path(path)
    if path.exists() or path.is_symlink():
        raise ValueError('Output already exists; history cannot be overwritten')
    path = reader.inside(path.parent.resolve(strict=True)) / path.name
    with path.open('x', encoding='utf-8', newline='\n') as fp:
        reader.inside(reader.opened_path(fp.fileno()))
        json.dump(value, fp, ensure_ascii=False, indent=2, allow_nan=False)

def cli(fn, description):
    p = argparse.ArgumentParser(description=description)
    p.add_argument('--input', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--allowed-root', required=True)
    args = p.parse_args()
    reader = SecureReader(args.allowed_root)
    src = Path(args.input)
    raw = reader.read_path(src)
    try:
        result = fn(json.loads(raw), src.parent, reader)
    except (ValueError, KeyError, TypeError, IndexError, OSError, SyntaxError, ImportError) as error:
        result = {'status':'REVIEW_REQUIRED', 'errors':[str(error)], 'claim_support':'Unknown'}
    if reader.read_path(src) != raw:
        raise ValueError('Input changed during execution')
    result['input_sha256'] = hashlib.sha256(raw).hexdigest()
    result['file_checks'] = reader.audit
    save_new(reader, args.output, result)
    return 2 if result.get('errors') else 0

def entry(fn, description):
    try:
        sys.exit(cli(fn, description))
    except (ValueError, KeyError, TypeError, IndexError, OSError) as error:
        print(type(error).__name__ + ': ' + str(error), file=sys.stderr)
        sys.exit(2)

def source_binding(source, base, reader):
    """Artifact location alone never establishes scientific or publisher identity."""
    if not source.get('SRC-ID') or source.get('kind') not in {'synthetic','local_artifact','external'}:
        raise ValueError('Explicit SRC-ID and artifact kind required')
    raw = raw_ref(reader, source['document_ref'], base)
    binding = {'SRC-ID':source['SRC-ID'], 'kind':source['kind'],
               'document_sha256':source['document_ref']['sha256'], 'source_identity':'UNVERIFIED',
               'publication_status':'NOT_CHECKED', 'claim_support':'Unknown'}
    if source['kind'] in {'synthetic','local_artifact'}:
        if not source.get('description'):
            raise ValueError('Local/synthetic artifact requires declared provenance')
        binding['source_identity'] = 'LOCAL_ARTIFACT_ONLY'
    if source.get('literature_ref'):
        rp = reader.resolve_ref(source['literature_ref']['path'], base)
        record = reader.evidence(source['literature_ref'], base)
        checked = evaluate(record, rp.parent, reader.root)
        if record['SRC-ID'] != source['SRC-ID'] or checked['identity']['status'] != 'MATCH' or checked['errors']:
            raise ValueError('Existing literature binding is invalid or belongs to another SRC')
        docs = record.get('source_documents', [])
        matching = [d for d in docs if d['raw_ref']['sha256']==source['document_ref']['sha256']]
        # Only the existing helper's actually validated reading bindings certify attribution.
        if checked['reading'].get('binding_status') != 'VALIDATED' or not matching:
            raise ValueError('Document not in existing validated reading bindings')
        binding.update(source_identity='BOUND_BY_EXISTING_REVIEW',
                       publication_status=checked['publication_status'],
                       literature_context_sha256=source_context(record, checked))
    elif source['kind']=='external':
        if not source.get('canonical_identifier') or not source.get('acquisition_ref'):
            raise ValueError('External location needs declared source and actual acquisition')
        access = reader.evidence(source['acquisition_ref'], base)
        if access.get('sha256') != source['document_ref']['sha256'] or access.get('status_code')!=200:
            raise ValueError('External artifact differs from acquisition')
        timestamp(access['checked_at'])
        binding.update(canonical_identifier=source['canonical_identifier'], acquisition=stable(access),
                       source_identity='ACQUIRED_ARTIFACT_ATTRIBUTION_REQUIRES_REVIEW')
    return raw, binding
