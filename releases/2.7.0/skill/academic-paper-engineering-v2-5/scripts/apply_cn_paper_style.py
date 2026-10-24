"""Apply the optional CN-PAPER-DEFAULT-1 profile to explicitly mapped paragraphs.

Requires an already available lxml. No installation is performed.
This is a formatting helper, not a manuscript or submission validator.
The caller supplies a hash-bound role map; no paragraph roles are guessed.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys
import zipfile
try:
    from lxml import etree as ET
except ImportError:
    print('lxml unavailable: stop; use an authorized existing renderer/library', file=sys.stderr)
    sys.exit(2)

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
ET.register_namespace('w', W)


def q(name):
    return '{' + W + '}' + name


# Chinese font, points, bold, alignment, first line points, left points,
# before points, after points, line multiplier, keep-next.
PROFILE = {
    'Title': ('黑体', 18, True, 'center', 0, 0, 0, 12, 1.5, True),
    'Heading1': ('黑体', 16, True, 'left', 0, 0, 12, 6, 1.5, True),
    'Heading2': ('黑体', 14, True, 'left', 0, 0, 6, 6, 1.5, True),
    'Heading3': ('黑体', 12, True, 'left', 0, 0, 6, 0, 1.5, True),
    'Body': ('宋体', 12, False, 'both', 24, 0, 0, 0, 1.5, False),
    'AbstractBody': ('宋体', 12, False, 'both', 24, 0, 0, 0, 1.5, False),
    'Keywords': ('宋体', 12, False, 'left', 0, 0, 0, 0, 1.5, False),
    'TableText': ('宋体', 10.5, False, 'left', 0, 0, 0, 0, 1.15, False),
    'Caption': ('宋体', 10.5, False, 'center', 0, 0, 6, 6, 1.15, False),
    'References': ('宋体', 10.5, False, 'both', -21, 21, 0, 0, 1.25, False),
    'Footer': ('宋体', 10.5, False, 'center', 0, 0, 0, 0, 1, False),
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def el(name, **attrs):
    return ET.Element(q(name), {q(k): str(v) for k, v in attrs.items()})


def properties(role):
    cn, size, bold, align, first, left, before, after, line, keep = PROFILE[role]
    rpr = el('rPr')
    rpr.append(el('rFonts', ascii='Times New Roman', hAnsi='Times New Roman',
                  eastAsia=cn, cs='Times New Roman'))
    for tag in ('b', 'bCs'):
        rpr.append(el(tag, val=int(bold)))
    rpr.append(el('color', val='000000'))
    for tag in ('sz', 'szCs'):
        rpr.append(el(tag, val=round(size * 2)))
    rpr.append(el('lang', val='en-US', eastAsia='zh-CN', bidi='en-US'))
    ppr = el('pPr')
    ppr.append(el('keepNext', val=int(keep)))
    ppr.append(el('keepLines', val=int(keep)))
    ppr.append(el('pageBreakBefore', val=0))
    ppr.append(el('widowControl', val=1))
    ppr.append(el('suppressAutoHyphens', val=1))
    ppr.append(el('snapToGrid', val=0))
    ppr.append(el('spacing', before=round(before*20), after=round(after*20),
                  beforeAutospacing=0, afterAutospacing=0,
                  line=round(line*240), lineRule='auto'))
    ind = el('ind', left=round(left*20), right=0)
    ind.set(q('hanging' if first < 0 else 'firstLine'), str(round(abs(first)*20)))
    ppr.append(ind)
    ppr.append(el('jc', val=align))
    if role.startswith('Heading'):
        ppr.append(el('outlineLvl', val=int(role[-1])-1))
    else:
        ppr.append(el('outlineLvl', val=9))
    return ppr, rpr


def replace_selected(parent, replacement, tags):
    # Remove only typography/paragraph properties governed by this profile.
    for node in list(parent):
        if node.tag in {q(tag) for tag in tags}:
            parent.remove(node)
    for node in replacement:
        parent.append(copy.deepcopy(node))


def owned_nodes(paragraph, tag):
    # A nested textbox paragraph is a separate authorization boundary.
    for node in paragraph.iter(tag):
        if next(node.iterancestors(q('p')), None) is paragraph:
            yield node


def run(args):
    src, dst, report = Path(args.input), Path(args.output), Path(args.report)
    if (dst.exists() or report.exists() or len({p.resolve() for p in
            (src, dst, report, Path(args.mapping))}) != 4):
        raise ValueError('Refuse overwrite: use new output and report paths')
    mapping = json.loads(Path(args.mapping).read_text(encoding='utf-8'))
    raw = src.read_bytes()
    if sha(raw) != mapping['input_sha256']:
        raise ValueError('Input SHA256 differs from role-map identity')
    if mapping.get('authority') != 'product-default-no-template':
        raise ValueError('Default helper cannot replace a user/institution template')
    entries = mapping['paragraphs']
    if not entries:
        raise ValueError('Empty paragraph map')
    with zipfile.ZipFile(src) as pack:
        if pack.testzip() is not None:
            raise ValueError('Input ZIP CRC failed')
        infos = pack.infolist()
        if len({i.filename.casefold() for i in infos}) != len(infos):
            raise ValueError('Duplicate ZIP members')
        if any(i.filename.startswith('_xmlsignatures/') for i in infos):
            raise ValueError('Signed DOCX: do not invalidate signatures')
        data = {i.filename: pack.read(i) for i in infos}
    roots = {}
    selected = set()
    for row in entries:
        part, index, role = row['part'], row['paragraph_index'], row['role']
        if role not in PROFILE or type(index) is not int or index < 1:
            raise ValueError('Invalid role or one-based paragraph index')
        if part != 'word/document.xml' and not (
            part.startswith(('word/header', 'word/footer')) and part.endswith('.xml')
        ):
            raise ValueError('Unsupported part: ' + part)
        if (part, index) in selected:
            raise ValueError('Duplicate paragraph mapping')
        selected.add((part, index))
        if part not in roots:
            roots[part] = ET.fromstring(data[part])
        paras = list(roots[part].iter(q('p')))
        if index > len(paras):
            raise ValueError('Paragraph index out of range')
        p = paras[index-1]
        if any(next(owned_nodes(p, q(x)), None) is not None
               for x in ('ins', 'del', 'smartTag')):
            raise ValueError('Resolve revision/semantic markup before normalization')
        # Changing a paragraph style also changes inherited formatting in these
        # objects. Do not guess effective math/symbol/link typography. Reject only
        # a selected paragraph containing them; unselected content remains usable.
        special = ('hyperlink', 'sym')
        math_ns = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
        if (any(next(owned_nodes(p, q(x)), None) is not None for x in special) or
                any(next(owned_nodes(p, '{' + math_ns + '}' + x), None) is not None
                    for x in ('oMath', 'oMathPara'))):
            raise ValueError('Unsupported mapped hyperlink/math/symbol paragraph: '
                             + part + '#' + str(index)
                             + '; leave it unmapped or use a dedicated formatter')
        ppr, rpr = properties(role)
        current = p.find(q('pPr'))
        if current is None:
            current = el('pPr'); p.insert(0, current)
        replace_selected(current, ppr, (
            'pStyle', 'keepNext', 'keepLines', 'pageBreakBefore', 'widowControl',
            'suppressAutoHyphens', 'snapToGrid', 'spacing', 'ind', 'jc',
            'outlineLvl', 'pBdr', 'shd', 'tabs', 'contextualSpacing',
        ))
        current.insert(0, el('pStyle', val='APE' + role))
        # A paragraph mark can itself inherit a theme font.
        mark = current.find(q('rPr'))
        if mark is None:
            mark = el('rPr'); current.append(mark)
        replace_selected(mark, rpr, ('rFonts', 'sz', 'szCs', 'b', 'bCs', 'color', 'lang'))
        for r in owned_nodes(p, q('r')):
            # Only runs owned by this mapped paragraph. Nested paragraphs require
            # their own explicit map. Drawing-only runs remain untouched.
            if not any(r.find(q(x)) is not None for x in ('t', 'instrText', 'fldChar')):
                continue
            props = r.find(q('rPr'))
            if props is None:
                props = el('rPr'); r.insert(0, props)
            replace_selected(props, rpr, ('rFonts', 'sz', 'szCs', 'b', 'bCs', 'color', 'lang'))
    styles = ET.fromstring(data['word/styles.xml'])
    roles = sorted({row['role'] for row in entries})
    for role in roles:
        sid = 'APE' + role
        old = [s for s in styles.findall(q('style')) if s.get(q('styleId')) == sid]
        # Prefix collisions could otherwise overwrite a user's style silently.
        if old:
            raise ValueError('Style prefix collision: ' + sid)
        s = el('style', type='paragraph', customStyle=1, styleId=sid)
        s.append(el('name', val='APE ' + role)); s.append(el('qFormat'))
        ppr, rpr = properties(role); s.extend((ppr, rpr)); styles.append(s)
    roots['word/styles.xml'] = styles
    if args.page_default:
        for sec in roots['word/document.xml'].iter(q('sectPr')):
            oldsize, oldmargin = sec.find(q('pgSz')), sec.find(q('pgMar'))
            if oldsize is not None: sec.remove(oldsize)
            if oldmargin is not None: sec.remove(oldmargin)
            sec.insert(0, el('pgSz', w=11906, h=16838))
            sec.insert(1, el('pgMar', top=1417, bottom=1417, left=1417,
                             right=1417, header=709, footer=709, gutter=0))
    for part, root in roots.items():
        data[part] = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    # Detect text or field loss before any write. XML whitespace is not document text.
    def text_nodes(content):
        root = ET.fromstring(content)
        return [(e.tag, e.text) for e in root.iter() if e.tag in (q('t'), q('instrText'))]
    with zipfile.ZipFile(src) as pack:
        for part in roots:
            if part != 'word/styles.xml' and text_nodes(pack.read(part)) != text_nodes(data[part]):
                raise ValueError('Text/field identity changed: ' + part)
    if sha(src.read_bytes()) != mapping['input_sha256']:
        raise ValueError('Source identity changed before output')
    created = []
    try:
        with dst.open('xb') as fp:
            created.append(dst)
            with zipfile.ZipFile(fp, 'w', compression=zipfile.ZIP_DEFLATED) as pack:
                for info in infos:
                    pack.writestr(info, data[info.filename])
        if sha(src.read_bytes()) != mapping['input_sha256']:
            raise ValueError('Source identity changed during operation')
        result = {'execution': 'APPLIED_NOT_ACCEPTED', 'profile': 'CN-PAPER-DEFAULT-1',
                  'input_sha256': sha(raw), 'output_sha256': sha(dst.read_bytes()),
                  'mapped_paragraphs': len(entries), 'modified_parts': sorted(roots),
                  'page_default': args.page_default, 'source_unchanged': True,
                  'font_availability': 'NOT RUN', 'effective_font_check': 'NOT RUN',
                  'render_and_page_review': 'NOT RUN', 'formal_submission_gate': 'NOT RUN',
                  'limits': 'Explicit mapped plain-text typography only; mapped hyperlinks/math/symbols rejected. No role inference, '
                            'template validation, table geometry, TOC update or scientific audit.'}
        with report.open('x', encoding='utf-8') as fp:
            created.append(report)
            json.dump(result, fp, ensure_ascii=False, indent=2)
        print(json.dumps(result, ensure_ascii=False))
    except BaseException:
        for created_path in reversed(created):
            created_path.unlink(missing_ok=True)
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('input', 'output', 'mapping', 'report'):
        parser.add_argument('--' + name, required=True)
    parser.add_argument('--page-default', action='store_true',
                        help='Use A4/25mm margins only under no-template default authority')
    try:
        run(parser.parse_args())
    except (ValueError, KeyError, OSError, zipfile.BadZipFile, ET.ParseError) as error:
        print(type(error).__name__ + ': ' + str(error), file=sys.stderr)
        sys.exit(2)
