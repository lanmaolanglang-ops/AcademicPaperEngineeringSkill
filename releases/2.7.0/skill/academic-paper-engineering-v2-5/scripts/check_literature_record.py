"""Check one hash-bound SRC view offline; never infer scientific support.

No requests, dependency installation, history writes or paper acceptance.
Run --help. Schema, authority limits and manual review: literature_verification.md.
"""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path, PureWindowsPath
import re
import stat
import sys
import unicodedata
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

RELATIONS = {'Verified', 'Partial Verified', 'Unsupported', 'Need Source', 'Unknown'}
READING = {'NOT_READ', 'METADATA', 'ABSTRACT', 'PARTIAL_FULL_TEXT', 'FULL_TEXT'}
EVENTS = {'retraction': 'RETRACTED', 'correction': 'CORRECTED',
          'expression_of_concern': 'EXPRESSION_OF_CONCERN'}


class SecureReader:
    """Trusted caller root, final-handle checks, one buffer for hash and parse."""

    def __init__(self, allowed_root):
        self.root = Path(allowed_root).resolve(strict=True)
        if not self.root.is_dir():
            raise ValueError('Allowed root must be an existing directory')
        self.audit = []

    def inside(self, path):
        try:
            path.relative_to(self.root)
        except ValueError:
            raise ValueError('Reference path escapes allowed root') from None
        return path

    def resolve_ref(self, value, base):
        if not isinstance(value, str) or not value or '\x00' in value:
            raise ValueError('Reference needs a nonempty relative path')
        windows = PureWindowsPath(value)
        if windows.drive or windows.root or Path(value).is_absolute():
            raise ValueError('Absolute, drive, UNC or device references are not allowed')
        # Interpret both separators; reject Windows device aliases and ADS.
        value = value.replace('\\', '/')
        for part in value.split('/'):
            if part in ('', '.', '..'):
                continue
            if ':' in part or part.endswith((' ', '.')) or re.fullmatch(r'(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?', part, re.I):
                raise ValueError('Device, stream or ambiguous path component')
        base = self.inside(Path(base).resolve(strict=True))
        return self.inside((base / value).resolve(strict=True))

    @staticmethod
    def opened_path(fd):
        if os.name == 'nt':
            import ctypes
            from ctypes import wintypes
            import msvcrt
            api = ctypes.WinDLL('kernel32', use_last_error=True).GetFinalPathNameByHandleW
            api.argtypes = [wintypes.HANDLE, wintypes.LPWSTR, wintypes.DWORD, wintypes.DWORD]
            api.restype = wintypes.DWORD
            size = 512
            while True:
                buf = ctypes.create_unicode_buffer(size)
                length = api(msvcrt.get_osfhandle(fd), buf, size, 0)
                if not length:
                    raise OSError(ctypes.get_last_error(), 'Cannot verify opened file final path')
                if length < size:
                    text = buf.value
                    if text.startswith('\\\\?\\UNC\\'):
                        text = '\\\\' + text[8:]
                    elif text.startswith('\\\\?\\'):
                        text = text[4:]
                    return Path(text)
                size = length + 1
        proc = Path('/proc/self/fd') / str(fd)
        if proc.exists():
            return Path(os.readlink(proc))
        raise ValueError('Final opened-path verification unavailable on this platform')

    @staticmethod
    def identity(info):
        return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns)

    def read_path(self, path):
        path = self.inside(Path(path).resolve(strict=True))
        before = path.stat()
        if not stat.S_ISREG(before.st_mode):
            raise ValueError('Evidence must be a regular file')
        flags = os.O_RDONLY | getattr(os, 'O_BINARY', 0) | getattr(os, 'O_NOFOLLOW', 0)
        fd = os.open(path, flags)
        try:
            # Validate the handle before reading even one content byte.
            actual = self.inside(self.opened_path(fd))
            first = os.fstat(fd)
            if actual != path or self.identity(first) != self.identity(before):
                raise ValueError('File changed between path validation and open')
            with os.fdopen(fd, 'rb', closefd=False) as stream:
                raw = stream.read()
            last = os.fstat(fd)
            path_after = path.stat()
            if (self.identity(last) != self.identity(first) or last.st_ctime_ns != first.st_ctime_ns or
                    self.inside(self.opened_path(fd)) != actual or
                    self.inside(path.resolve(strict=True)) != actual or
                    self.identity(path_after) != self.identity(before) or path_after.st_ctime_ns != before.st_ctime_ns):
                raise ValueError('File/path changed while reading; result rejected')
        finally:
            os.close(fd)
        self.audit.append({'path':actual.relative_to(self.root).as_posix(),
                           'sha256':hashlib.sha256(raw).hexdigest(), 'final_handle_checked':True})
        return raw

    def evidence(self, ref, base):
        path = self.resolve_ref(ref['path'], base)
        raw = self.read_path(path)
        if hashlib.sha256(raw).hexdigest() != ref['sha256']:
            raise ValueError('Snapshot SHA256 mismatch')
        return parse_evidence(ref, path, raw)


def identifier(value):
    value = str(value).strip()
    doi = re.sub(r'^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)', '', value, flags=re.I)
    if re.match(r'^10\.\d{4,9}/\S+$', doi):
        return doi.lower()
    return value  # Do not lowercase arbitrary URLs, ISBNs or official IDs.


def norm(value):
    return ' '.join(unicodedata.normalize('NFKC', str(value)).casefold().split())


def pointer(data, path):
    for key in path.strip('/').split('/') if path else []:
        key = key.replace('~1', '/').replace('~0', '~')
        data = data[int(key)] if isinstance(data, list) else data[key]
    return data


def evidence(ref, base, allowed_root=None):
    return SecureReader(allowed_root or base).evidence(ref, base)


def parse_evidence(ref, path, raw):
    if ref.get('format') == 'bytes':
        return raw
    if 'pointer' in ref:
        value = pointer(json.loads(raw), ref['pointer'])
        text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    elif path.suffix.lower() == '.json' or ref.get('format') == 'json':
        value = json.loads(raw)
        text = json.dumps(value, ensure_ascii=False)
    elif 'xml_path' in ref:
        nodes = ET.fromstring(raw).findall(ref['xml_path'])
        if not nodes:
            raise ValueError('Missing XML anchor: ' + ref['xml_path'])
        text = ' '.join(' '.join(n.itertext()) for n in nodes)
        value = text
    else:
        text = raw.decode(ref.get('encoding', 'utf-8'))
        if 'line_start' in ref:
            lines = text.splitlines()
            start, end = ref['line_start'], ref.get('line_end', ref['line_start'])
            if type(start) is not int or type(end) is not int or start < 1 or end < start or end > len(lines):
                raise ValueError('Invalid source line range')
            text = '\n'.join(lines[start - 1:end])
        value = text
    if 'quote' in ref and norm(ref['quote']) not in norm(text):
        raise ValueError('Quote absent at actual anchor: ' + ref['path'])
    return value


def value_sha(value):
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def publication_context(record, canonical, base, reader):
    """Check acquired Crossref records, not arbitrary notice text or live authority."""
    def stable_ref(ref):
        return {k: v for k, v in ref.items() if k in {'sha256', 'pointer', 'xml_path', 'line_start', 'line_end', 'format'}}

    def stamp(text):
        from datetime import datetime, timezone
        if not isinstance(text, str) or not text:
            raise ValueError('Acquisition/check time needs an explicit timestamp')
        value = datetime.fromisoformat(text.replace('Z', '+00:00'))
        if value.tzinfo is None:
            raise ValueError('Acquisition/check time needs an explicit timezone')
        return value.astimezone(timezone.utc).isoformat()

    def url(text):
        parsed = urlsplit(text)
        if parsed.scheme not in {'http', 'https'} or not parsed.hostname or parsed.username or parsed.password or parsed.fragment:
            raise ValueError('Invalid acquisition/source URL')
        return parsed._replace(scheme=parsed.scheme.lower(), netloc=parsed.netloc.lower()).geturl()

    def acquired(access_ref, raw_ref):
        access = reader.evidence(access_ref, base)
        if not isinstance(access, dict):
            raise ValueError('Access record must be an object')
        request = url(access['url'])
        at = stamp(access['checked_at'])
        status = access.get('status_code')
        info = {'access_sha256': access_ref['sha256'], 'request_url': request,
                'checked_at': at, 'status_code': status, 'simulated': bool(access.get('simulated', False))}
        if status != 200:
            if raw_ref:
                raise ValueError('Failed access cannot supply a successful response/notice')
            return info, None
        final = url(access.get('final_url', access['url']))
        cursor = request
        redirects = []
        for step in access.get('redirects', []):
            source, target = url(step['from']), url(step['to'])
            if source != cursor or step.get('status_code') not in {301, 302, 303, 307, 308}:
                raise ValueError('Broken recorded redirect chain')
            redirects.append({'from': source, 'to': target, 'status_code': step['status_code']})
            cursor = target
        if cursor != final:
            raise ValueError('Different final URL needs the actual ordered redirect chain')
        if not raw_ref:
            raise ValueError('Successful publication check needs its raw response_ref')
        raw = reader.evidence(dict(raw_ref, format='bytes'), base)
        if access.get('sha256') != raw_ref['sha256'] or ('bytes' in access and access['bytes'] != len(raw)):
            raise ValueError('Response bytes differ from their acquisition record')
        parsed = urlsplit(final)
        simulated = info['simulated']
        if not simulated and not (parsed.scheme == 'https' and parsed.hostname == 'api.crossref.org' and parsed.path.startswith('/works')):
            raise ValueError('Unsupported publication response origin; needs actual manual verification')
        body = json.loads(raw)
        if not isinstance(body, dict) or 'message' not in body:
            raise ValueError('Not the supported acquired Crossref envelope')
        info.update(final_url=final, redirects=redirects, response_sha256=raw_ref['sha256'],
                    representation='raw-crossref-json', authority_scope='synthetic' if simulated else 'recorded Crossref response; authenticity not certified')
        return info, body

    events, coverage, attempts, problems = [], [], [], []
    checked = unavailable = False
    for check in record.get('authority_record', []):
        attempt = {'declared': {k: check.get(k) for k in ('url', 'checked_at', 'complete')},
                   'refs': {k: stable_ref(check[k]) for k in ('access_ref', 'response_ref', 'notice_ref', 'notice_access_ref') if k in check},
                   'source_mapping': check.get('source_mapping')}
        cov = check.get('coverage')
        attempt['declared']['coverage'] = {k: v for k, v in cov.items() if k != 'description'} if isinstance(cov, dict) else cov
        try:
            if not isinstance(cov, dict) or set(cov) - {'kind', 'scope', 'pointer', 'description'}:
                raise ValueError('Coverage needs bounded kind/scope/pointer; free-text claims require review')
            if check.get('complete', False):
                raise ValueError('One returned response cannot certify exhaustive publication coverage')
            raw_ref = check.get('response_ref')
            # A legacy notice can itself be the acquired response, only with the same actual hash.
            if raw_ref is None and check.get('notice_ref'):
                raw_ref = check['notice_ref']
            chain, body = acquired(check['access_ref'], raw_ref)
            attempt['source'] = chain
            declared_url = url(check['url'])
            nodes = {chain['request_url'], chain.get('final_url', chain['request_url'])}
            nodes.update(s[k] for s in chain.get('redirects', []) for k in ('from', 'to'))
            if declared_url not in nodes:
                mapping = check.get('source_mapping', {})
                own = body.get('message', {}).get('DOI') if body and isinstance(body.get('message'), dict) else None
                if (mapping.get('kind') != 'doi-via-crossref' or not own or identifier(mapping.get('canonical_identifier', '')) != identifier(own) or
                        identifier(declared_url) != identifier(own)):
                    raise ValueError('Authority URL has no acquired redirect or verified DOI/API mapping')
            if stamp(check['checked_at']) != chain['checked_at']:
                raise ValueError('Declared check time differs from its actual acquisition event')
            attempt['declared']['checked_at'] = chain['checked_at']
            attempt['declared']['url'] = declared_url
            if body is None:
                if cov != {'kind': 'failed_attempt', 'scope': 'attempt_only'} and {k:v for k,v in cov.items() if k != 'description'} != {'kind':'failed_attempt', 'scope':'attempt_only'}:
                    raise ValueError('Failed acquisition cannot claim checked metadata/full text')
                if check.get('notice_ref') or check.get('notice_access_ref'):
                    raise ValueError('Failed authority attempt cannot silently borrow a notice')
                unavailable = True
            else:
                kind, scope, anchor = cov.get('kind'), cov.get('scope'), cov.get('pointer')
                projection = pointer(body, anchor) if isinstance(anchor, str) else None
                if kind in {'metadata', 'notice_metadata'} and scope == 'returned_record' and anchor == '/message':
                    if not isinstance(projection, dict) or not projection.get('DOI'):
                        raise ValueError('Coverage does not select an acquired work record')
                    if kind == 'metadata' and identifier(projection['DOI']) != canonical:
                        raise ValueError('Acquired metadata describes a different paper')
                elif kind == 'query_results' and scope == 'returned_items' and anchor == '/message/items':
                    if not isinstance(projection, list):
                        raise ValueError('Query coverage does not select returned items')
                else:
                    raise ValueError('Coverage exceeds supported acquired metadata scope')
                chain['projection'] = {'pointer': anchor, 'sha256': value_sha(projection)}
                notice_ref = check.get('notice_ref')
                if kind == 'notice_metadata' and not notice_ref:
                    raise ValueError('Notice coverage needs its explicit anchored notice')
                local_events = []
                if notice_ref:
                    nchain, nbody = (acquired(check['notice_access_ref'], notice_ref) if check.get('notice_access_ref') else (dict(chain), body))
                    if nbody is None or notice_ref['sha256'] != nchain.get('response_sha256'):
                        raise ValueError('Notice snapshot is not bound to its own actual acquisition')
                    anchor = notice_ref.get('pointer', '')
                    if not re.fullmatch(r'/message(?:/items/\d+)?', anchor):
                        raise ValueError('Notice must select its own acquired Crossref work record')
                    notice = reader.evidence(notice_ref, base)
                    if notice != pointer(nbody, anchor) or not isinstance(notice, dict) or not notice.get('DOI'):
                        raise ValueError('Notice projection differs from its actual acquired record')
                    updates = notice.get('update-to')
                    if not isinstance(updates, list) or not updates:
                        raise ValueError('Notice lacks explicit update-to relationship evidence')
                    nchain['projection'] = {'pointer': anchor, 'sha256': value_sha(notice)}
                    attempt['notice'] = nchain
                    for index, update in enumerate(updates):
                        if not isinstance(update, dict) or not update.get('DOI') or not update.get('type'):
                            raise ValueError('Malformed notice target/type')
                        if identifier(update['DOI']) == canonical:
                            local_events.append({'type': EVENTS.get(update['type'], 'OTHER_UPDATE'), 'raw_type': update['type'],
                                'notice_identifier': identifier(notice['DOI']), 'target_identifier': canonical,
                                'authority_record': nchain['final_url'], 'checked_at': nchain['checked_at'],
                                'source_chain': nchain, 'relation_pointer': anchor + '/update-to/' + str(index),
                                'relation_sha256': value_sha(update)})
                    if not local_events:
                        raise ValueError('Notice has no explicit relationship to the target paper')
                # Commit observations only after the entire attempt is consistent.
                events.extend(local_events)
                checked = True
            attempt['binding_status'] = 'VALIDATED'
            coverage.append({'url': declared_url, 'checked_at': chain['checked_at'], 'coverage': attempt['declared']['coverage'], 'source_chain': chain})
        except (OSError, ValueError, KeyError, TypeError, ET.ParseError, IndexError) as error:
            attempt['binding_status'] = 'REVIEW_REQUIRED'
            attempt['error'] = str(error)
            problems.append('UNVERIFIED_PUBLICATION_SOURCE: ' + str(error))
        attempts.append(attempt)
    result = {'status': 'NOTICES_FOUND' if events else 'NO_NOTICE_FOUND_IN_CHECKED_SOURCES' if checked else 'UNAVAILABLE' if unavailable else 'NOT_CHECKED',
              'events': events, 'coverage': coverage, 'coverage_complete': False,
              'unavailable_attempts_present': unavailable, 'unverified_attempts_present': bool(problems), 'attempts': attempts}
    # Paths and display-only description/labels are excluded; acquired/anchored identities remain.
    result['context_sha256'] = value_sha({'canonical_identifier': canonical, 'attempts': attempts, 'events': events})
    return result, problems


def check_publication_review(record, result, read_ref, base):
    publication = result['publication_status']
    publication['review_status'] = 'NOT_SUPPLIED'
    if not record.get('publication_review_ref'):
        return
    try:
        review = read_ref(record['publication_review_ref'], base)
        if not isinstance(review, dict) or not all(review.get(k) for k in ('reviewer', 'reviewed_at', 'reason')):
            raise ValueError('Publication review needs actual reviewer/time/reason')
        if (review.get('context_sha256') != publication['context_sha256'] or review.get('status') != publication['status'] or
                publication['unverified_attempts_present']):
            raise ValueError('Old publication review does not match the current acquired context/status')
        publication['review_status'] = 'CURRENT'
        publication['review_ref_sha256'] = record['publication_review_ref']['sha256']
    except (OSError, ValueError, KeyError, TypeError, ET.ParseError, IndexError) as error:
        publication['review_status'] = 'REVIEW_REQUIRED'
        result['review_required'].append('RECHECK_PUBLICATION_CONTEXT: ' + str(error))
        result['errors'].append('Invalid publication review: ' + str(error))


def source_context(source, checked):
    """Bind a judgement to known publication/version/use context, not path spelling."""
    def stable(value):
        if isinstance(value, dict):
            return {k: stable(v) for k, v in value.items() if k != 'path'}
        if isinstance(value, list):
            return [stable(v) for v in value]
        return value
    publication = checked['publication_status']
    context = {
        'SRC-ID': source['SRC-ID'], 'canonical_identifier': checked['canonical_identifier'],
        'publication': {'status': publication['status'],
                        'events': [{k: e.get(k) for k in ('type', 'raw_type', 'notice_identifier', 'target_identifier')}
                                   for e in publication['events']],
                        'coverage_complete': publication.get('coverage_complete', False),
                        'unavailable_attempts_present': publication.get('unavailable_attempts_present', False)},
        'version_relation': stable(checked['version_relation']),
        'purpose': source.get('purpose'), 'update_impact': source.get('update_impact', 'unknown'),
        'update_review_evidence': stable(source.get('update_review_evidence', []))}
    if source.get('authority_record'):
        context['publication_context_sha256'] = publication['context_sha256']
    return value_sha(context)


def verify_support(record, base, result, read_ref, evaluate_source):
    """Validate a supplied semantic judgement, never derive one from structure."""
    review = record['support_review']
    uses = review.get('evidence', [])
    if not isinstance(uses, list) or not uses or any(not isinstance(u, dict) or not u.get('EVID-ID') or not u.get('SRC-ID') or not u.get('role') for u in uses):
        raise ValueError('Support needs explicit registered EVID-ID, SRC-ID and contribution role')
    if result['identity']['status'] != 'MATCH':
        raise ValueError('Current citation identity mismatch; support cannot be inherited')
    registry = {record['SRC-ID']: record}
    for source in record.get('support_sources', []):
        sid = source['SRC-ID']
        if sid in registry or source.get('support_sources') or source.get('support_review'):
            raise ValueError('Duplicate or nested support source registration')
        registry[sid] = source
    required = {u['SRC-ID'] for u in uses}
    if not required <= registry.keys():
        raise ValueError('Undeclared support source')
    bound = {}
    result['support_source_checks'] = {}
    for sid in sorted(required):
        source = registry[sid]
        checked = result if sid == record['SRC-ID'] else evaluate_source(source)
        if sid != record['SRC-ID']:
            result['support_source_checks'][sid] = {k: copy.deepcopy(checked[k]) for k in
                                                    ('identity', 'publication_status', 'reading', 'version_relation', 'errors')}
        if checked['identity']['status'] != 'MATCH' or checked['errors']:
            raise ValueError('Invalid dependent source identity: ' + sid)
        event_types = {e['type'] for e in checked['publication_status']['events']}
        if sid != record['SRC-ID'] and (
                checked['publication_status']['status'] == 'CONFLICT' or
                'RETRACTED' in event_types and source.get('purpose') != 'notice_as_object' or
                ('CORRECTED' in event_types or checked['version_relation']['status'] in {'CORRECTED_VERSION', 'MATERIAL_DIFFERENCE'})
                and source.get('update_impact') != 'reviewed_current'):
            raise ValueError('Dependent source needs current update review: ' + sid)
        meta = read_ref(source['metadata_ref'], base)
        documents = {}
        for doc in source.get('source_documents', []):
            did = doc['document_id']
            if did in documents:
                raise ValueError('Duplicate document_id')
            raw_ref = doc['raw_ref']
            raw = read_ref(dict(raw_ref, format='bytes'), base)
            acquisition = read_ref(doc['acquisition_ref'], base)
            if not isinstance(acquisition, dict):
                raise ValueError('Acquisition record must be an object')
            kind = doc.get('representation', 'jats')
            root = None
            acquired_sha = raw_ref['sha256']
            if kind == 'jats':
                root = ET.fromstring(raw)
                # Only the document front matter establishes its own identity.
                doi = root.find('./front/article-meta/article-id[@pub-id-type="doi"]')
                title = root.find('./front/article-meta/title-group/article-title')
                if doi is None or title is None or identifier(doi.text or '') != identifier(meta['canonical_identifier']) or norm(''.join(title.itertext())) != norm(meta['title']):
                    raise ValueError('Raw document front-matter identity differs from registered source: ' + sid)
            elif kind == 'official-limited-json-v1':
                # Existing no-DOI corpus uses an explicitly limited normalized
                # representation, not a redistributed full official publication.
                normalized = json.loads(raw)
                if (not isinstance(normalized, dict) or meta.get('source_kind') != 'official_document' or
                        normalized.get('url') != meta['canonical_identifier'] or norm(normalized.get('title')) != norm(meta['title']) or
                        not isinstance(normalized.get('excerpt'), str) or not normalized['excerpt'] or
                        normalized.get('acquisition') != acquisition):
                    raise ValueError('Official canonical representation differs from registered identity/acquisition')
                index = urlsplit(normalized['url'])
                section = urlsplit(normalized.get('methods_url', ''))
                if (index.scheme != 'https' or section.scheme != 'https' or index.netloc != section.netloc or
                        not section.path.startswith(index.path.rsplit('/', 1)[0] + '/') or
                        acquisition.get('url') != normalized['methods_url'] or not doc.get('conversion_note')):
                    raise ValueError('Official section/canonical representation provenance is not declared')
                acquired_sha = normalized['acquisition'].get('sha256')
            else:
                raise ValueError('Unsupported source representation; requires actual binding review')
            if not isinstance(acquisition, dict) or acquisition.get('status_code') != 200 or acquisition.get('sha256') != acquired_sha or not acquisition.get('url') or not acquisition.get('checked_at'):
                raise ValueError('Raw artifact is not bound to its actual acquisition record')
            if not doc.get('version'):
                raise ValueError('Document needs an explicit version label and raw SHA')
            allowed = {(str((base / raw_ref['path']).resolve()), raw_ref['sha256'])}
            if doc.get('derived_ref'):
                if root is None or doc.get('conversion') != 'jats-body-text-v1':
                    raise ValueError('Unverifiable text conversion')
                derived = read_ref(dict(doc['derived_ref'], format='bytes'), base)
                expected = '\n'.join(''.join(p.itertext()) for p in root.findall('.//body//p')).encode('utf-8')
                if derived != expected:
                    raise ValueError('Derived text does not reproduce the registered raw document')
                allowed.add((str((base / doc['derived_ref']['path']).resolve()), doc['derived_ref']['sha256']))
            documents[did] = (doc, allowed)
        seen = set()
        for ref in source.get('reading', {}).get('evidence', []):
            eid, did = ref.get('EVID-ID'), ref.get('document_id')
            if not eid or eid in seen or did not in documents:
                raise ValueError('Reading evidence lacks a unique registered document/EVID-ID: ' + sid)
            seen.add(eid)
            doc, allowed = documents[did]
            if (str((base / ref['path']).resolve()), ref['sha256']) not in allowed:
                raise ValueError('Reading anchor belongs to a different document/version')
            if not any(k in ref for k in ('xml_path', 'pointer', 'line_start')):
                raise ValueError('Support evidence needs an explicit source anchor')
            value = read_ref(ref, base)
            binding = {'SRC-ID': sid, 'EVID-ID': eid, 'document_id': did,
                       'raw_sha256': doc['raw_ref']['sha256'], 'read_sha256': ref['sha256'],
                       'anchor_sha256': value_sha(value), 'context_sha256': source_context(source, checked)}
            bound[(sid, eid)] = binding
        if sid == record['SRC-ID']:
            result['reading']['binding_status'] = 'VALIDATED'
    selected = []
    seen_uses = set()
    for use in uses:
        key = (use['SRC-ID'], use['EVID-ID'])
        if key in seen_uses or key not in bound:
            raise ValueError('Support does not reference unique actual reading evidence')
        seen_uses.add(key)
        selected.append(dict(bound[key], role=use['role']))
    if review.get('source_sha256') and review['source_sha256'] not in {b['raw_sha256'] for b in selected}:
        raise ValueError('Legacy source SHA differs from actually used source documents')
    result['support_binding_candidates'] = selected
    judgement = read_ref(review['semantic_review_ref'], base)
    if not isinstance(judgement, dict):
        raise ValueError('Semantic review must be a structured review record')
    for key in ('CLM-ID', 'target', 'status'):
        if judgement.get(key) != review[key]:
            raise ValueError('Semantic review does not match current claim/target/status')
    if (not judgement.get('reviewer') or not judgement.get('reviewed_at') or not judgement.get('reason') or
            not judgement.get('reading_scope') or judgement.get('evidence') != selected):
        raise ValueError('Semantic review lacks current reading/anchor/role bindings')
    result['claim_support'] = copy.deepcopy(review)
    result['claim_support']['validated_bindings'] = selected
    result['claim_support']['basis'] = 'Supplied, traceable semantic judgement; structure does not prove scientific meaning or reviewer authenticity'


def evaluate(record, base, allowed_root=None):
    """Return separate dimensions; execution is not a semantic PASS certificate."""
    result = {'SRC-ID': record['SRC-ID'], 'canonical_identifier': None,
              'identity': {'status': 'UNRESOLVED', 'differences': []},
              'publication_status': {'status': 'NOT_CHECKED', 'events': [], 'coverage': []},
              'version_relation': {'status': 'UNKNOWN'},
              'version_correctness': {'status': 'Not Run', 'reason': 'No explicit required version or artifact supplied'},
              'reading': {'level': 'NOT_READ', 'evidence': []},
              'claim_support': {'status': 'Unknown'},
              'citation_format': {'status': 'Not Run'},
              'review_required': [], 'errors': [],
              'history': copy.deepcopy(record.get('history', [])),
              'limits': 'Offline identity/anchor consistency only. Authenticity of acquisition, '
                        'reading completeness, scientific meaning and external style compliance need actual review.'}
    reader = None
    try:
        base = Path(base)
        reader = SecureReader(allowed_root or base)
        evidence = reader.evidence
        metadata = evidence(record['metadata_ref'], base)
        if not isinstance(metadata, dict):
            raise ValueError('Metadata view must be an object with acquisition provenance')
        # Metadata is a documented projection, not an authority merely because
        # this file hashes correctly. Bind every projection to its raw origin.
        for origin in metadata.get('provenance', []):
            evidence(origin, reader.resolve_ref(record['metadata_ref']['path'], base).parent)
        if not metadata.get('provenance'):
            raise ValueError('Metadata has no raw acquisition provenance')
        result['canonical_identifier'] = identifier(metadata['canonical_identifier'])
        citation = record['citation']
        differences = []
        for field in ('canonical_identifier', 'title', 'authors'):
            actual, expected = citation.get(field), metadata.get(field)
            if field == 'authors' and actual is None and expected is None and metadata.get('source_kind') == 'official_document':
                result['identity']['author_limit'] = 'Official document identity only; authorship not supplied or verified'
                continue
            if actual is None or expected is None:
                differences.append({'field': field, 'kind': 'missing', 'citation': actual, 'authority': expected})
            elif field == 'canonical_identifier':
                if identifier(actual) != identifier(expected):
                    differences.append({'field': field, 'kind': 'mismatch', 'citation': actual, 'authority': expected})
            elif norm(actual) != norm(expected):
                differences.append({'field': field, 'kind': 'mismatch', 'citation': actual, 'authority': expected})
        result['identity'].update({'status': 'MISMATCH' if any(d['kind'] == 'mismatch' for d in differences)
                              else 'UNRESOLVED' if differences else 'MATCH', 'differences': differences}
                              )

        checks = record.get('authority_record', [])
        publication, problems = publication_context(record, result['canonical_identifier'], base, reader)
        result['publication_status'] = publication
        result['errors'].extend(problems)
        if problems:
            result['review_required'].append('RECHECK_PUBLICATION_SOURCE_BINDING')
        events = publication['events']
        assertions = record.get('conflicting_assertions', [])
        if assertions:
            facts = []
            for assertion in assertions:
                fact = evidence(assertion['ref'], base)
                if identifier(fact['target_identifier']) != result['canonical_identifier']:
                    raise ValueError('Conflict assertion target differs')
                facts.append(fact['explicit_retraction_assertion'])
            if True in facts and False in facts:
                result['publication_status']['status'] = 'CONFLICT'
                result['review_required'].append('RESOLVE_AUTHORITY_CONFLICT')
        if record.get('publication_not_applicable'):
            if checks or not record.get('not_applicable_reason'):
                raise ValueError('Not applicable needs a reason and no claimed publication check')
            if metadata.get('source_kind') not in {'internal_definition', 'unpublished_record'}:
                raise ValueError('Published literature cannot bypass publication checks as not applicable')
            result['publication_status']['status'] = 'NOT_APPLICABLE'

        version = copy.deepcopy(record.get('version_relation', {'status': 'UNKNOWN'}))
        allowed = {'PREPRINT_ONLY', 'PUBLISHED_COUNTERPART', 'MATERIAL_DIFFERENCE', 'CORRECTED_VERSION',
                   'SUSPECTED_SAME_RESEARCH', 'DIFFERENT_RESEARCH', 'UNKNOWN'}
        if version['status'] not in allowed:
            raise ValueError('Invalid version relation')
        if version['status'] == 'PUBLISHED_COUNTERPART':
            preprint = evidence(version['preprint_ref'], base)
            published = evidence(version['published_ref'], base)
            if identifier(preprint['published']) != identifier(published['DOI']):
                raise ValueError('No matching explicit preprint publication relation')
            version['counting_rule'] = 'Two versions of one linked study; do not count as two independent studies'
            version['content_equivalence'] = 'NOT VERIFIED; metadata relation does not transfer claim support'
        if version['status'] in {'MATERIAL_DIFFERENCE', 'CORRECTED_VERSION'}:
            if not version.get('reason') or not version.get('evidence'):
                raise ValueError('Version change needs actual compared evidence and reason')
            for ref in version['evidence']:
                evidence(ref, base)
            result['review_required'].append('RECHECK_AFFECTED_CLM_DATA_AND_OCCURRENCES')
        result['version_relation'] = version
        def version_identity(value):
            if isinstance(value, dict):
                return {k: version_identity(v) for k, v in value.items() if k != 'path'}
            if isinstance(value, list):
                return [version_identity(v) for v in value]
            return value
        result['publication_status']['context_sha256'] = value_sha({
            'acquired_context': result['publication_status']['context_sha256'],
            'status': result['publication_status']['status'],
            'version_relation': version_identity(version),
            'conflicting_assertions': [{k:v for k,v in a.get('ref', {}).items() if k != 'path'} for a in record.get('conflicting_assertions', [])],
            'not_applicable_reason': record.get('not_applicable_reason')})
        check_publication_review(record, result, evidence, base)


        reading = record.get('reading', {'level': 'NOT_READ', 'evidence': []})
        if reading['level'] not in READING:
            raise ValueError('Invalid reading level')
        for ref in reading.get('evidence', []):
            evidence(ref, base)
        if reading['level'] != 'NOT_READ' and not reading.get('evidence'):
            raise ValueError('Reading claimed without actual evidence')
        result['reading'] = copy.deepcopy(reading)
        requirement = record.get('version_requirement')
        if requirement:
            if not requirement.get('canonical_identifier') or not requirement.get('reason'):
                raise ValueError('Version requirement needs explicit identifier and reason')
            same_id = identifier(requirement['canonical_identifier']) == result['canonical_identifier']
            same_artifact = (not requirement.get('source_sha256') or requirement['source_sha256'] in
                             {ref['sha256'] for ref in reading.get('evidence', [])})
            result['version_correctness'] = {
                'status': 'Passed' if same_id and same_artifact and result['identity']['status'] == 'MATCH' else 'Failed',
                'requirement': copy.deepcopy(requirement),
                'scope': 'Explicit identifier/artifact requirement only; relation does not prove text equivalence'}
        review = record.get('support_review')
        if review:
            if review['status'] not in RELATIONS or not review.get('CLM-ID') or not review.get('target') or not review.get('reason'):
                raise ValueError('Support review needs original relation state, target, CLM and reason')
            refs = reading.get('evidence', [])
            result['claim_support'] = copy.deepcopy(review)
            result['claim_support']['status'] = 'Unknown'
            try:
                verify_support(record, base, result, evidence, lambda source: evaluate(source, base, allowed_root))
            except (OSError, ValueError, KeyError, TypeError, ET.ParseError, IndexError) as error:
                result['review_required'].append('UNVERIFIED_SUPPORT_BINDING: ' + str(error))
                result['errors'].append('Invalid support binding: ' + str(error))
                result['claim_support']['status'] = 'Unknown'
            if result['identity']['status'] != 'MATCH':
                result['claim_support']['status'] = 'Unknown'
                result['review_required'].append('IDENTITY_OR_READING_BINDING_CHANGED')
            elif reading['level'] in {'NOT_READ', 'METADATA'} or (
                    review.get('requires_full_text') and reading['level'] == 'ABSTRACT'):
                result['claim_support']['status'] = 'Need Source'
            elif review['status'] in {'Verified', 'Partial Verified'} and not review.get('evidence'):
                result['claim_support']['status'] = 'Unknown'
                result['review_required'].append('MISSING_SUPPORT_ANCHOR')
        types = {e['type'] for e in events}
        update_affects = record.get('update_impact', 'unknown')
        if 'EXPRESSION_OF_CONCERN' in types:
            result['review_required'].append('ASSESS_EOC_SCOPE_NOT_AUTOMATIC_RETRACTION')
        blocked_use = ('RETRACTED' in types and record.get('purpose') != 'notice_as_object')
        stale_update = ('CORRECTED' in types or version['status'] in {'MATERIAL_DIFFERENCE', 'CORRECTED_VERSION'}) and update_affects != 'reviewed_current'
        if blocked_use or stale_update or result['publication_status']['status'] == 'CONFLICT':
            result['claim_support']['status'] = 'Unknown'
            result['review_required'].append('UNQUALIFIED_OR_STALE_SUPPORT_NOT_ACCEPTED')
        if update_affects == 'reviewed_current':
            if not record.get('update_review_evidence'):
                raise ValueError('Current update review requires bound evidence')
            for ref in record['update_review_evidence']:
                evidence(ref, base)
        # Only this explicit local test/user style is mechanically supported.
        # Other standards need a separate real review, never guessed compliance.
        fmt = record.get('citation_format', {})
        if fmt.get('style') == 'ID-LINE-1':
            parts = fmt.get('rendered', '').split(' | ')
            ok = len(parts) == 4 and bool(re.fullmatch(r'\[\d+\]', parts[0])) and all(parts[1:])
            result['citation_format'] = {'status': 'Passed' if ok else 'Failed',
                                         'style': 'ID-LINE-1', 'scope': 'Four nonempty columns: [n] | author | title | identifier; syntax only'}
    except (OSError, ValueError, KeyError, TypeError, ET.ParseError, IndexError) as error:
        result['errors'].append(type(error).__name__ + ': ' + str(error))
        result['claim_support']['status'] = 'Unknown'
        result['review_required'].append('INVALID_OR_UNVERIFIED_RECORD')
    result['execution'] = 'CHECKED_REVIEW_REQUIRED' if result['review_required'] or result['errors'] else 'CHECKED_NOT_PAPER_ACCEPTED'
    result['file_checks'] = reader.audit if reader else []
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--allowed-root', required=True, help='Trusted caller-selected package root; input cannot expand it')
    args = parser.parse_args()
    src, dst = Path(args.input), Path(args.output)
    if dst.exists() or dst.is_symlink() or src.resolve() == dst.resolve():
        parser.error('Use a new output path; input/history are read-only')
    reader = SecureReader(args.allowed_root)
    original = reader.read_path(src)
    result = evaluate(json.loads(original), src.parent, reader.root)
    result['input_sha256'] = hashlib.sha256(original).hexdigest()
    if reader.read_path(src) != original:
        parser.error('Input changed; no output written')
    dst = reader.inside(dst.parent.resolve(strict=True)) / dst.name
    with dst.open('x', encoding='utf-8', newline='\n') as fp:
        reader.inside(reader.opened_path(fp.fileno()))
        json.dump(result, fp, ensure_ascii=False, indent=2)
    return 2 if result['errors'] else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, TypeError, ET.ParseError, IndexError) as error:
        print(type(error).__name__ + ': ' + str(error), file=sys.stderr)
        sys.exit(2)
