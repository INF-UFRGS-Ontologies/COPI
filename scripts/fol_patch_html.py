# scripts/fol_patch_html.py
"""Patch First-Order Logic Theory blocks in COPI HTML documentation files."""
import re
import pathlib
from fol_gen import (
    label_to_pred, fix_fol_annotation, fix_dl_in_fol,
    gen_genus_axiom, gen_some_restriction, gen_all_restriction,
    gen_disjointness, render_fol_block, _fresh_var,
)

# Regex that matches the entire First-Order Logic Theory axiom-block div
_FOL_BLOCK_RE = re.compile(
    r'(<div class="axiom-block">\s*'
    r'<div class="axiom-label"><span class="t-en">First-Order Logic Theory</span>'
    r'<span class="t-pt">Teoria em Lógica de Primeira Ordem</span></div>\s*'
    r'<div style="[^"]*">)'   # group 1: opening tags
    r'(.*?)'                   # group 2: inner content to replace
    r'(</div>\s*</div>)',      # group 3: closing tags
    re.DOTALL
)


def build_axioms_for_ttl_class(cls_data: dict) -> list:
    """Build a list of (label, fol_string) from TTL class data.

    Args:
        cls_data: a single class dict (one value from extract_class_data result).

    Returns:
        List of (label, fol_string) tuples.
    """
    axioms = []
    pred = cls_data['pred']

    if cls_data.get('fol_def'):
        fol = fix_dl_in_fol(fix_fol_annotation(cls_data['fol_def']))
        axioms.append(('Definition', fol))
    elif cls_data.get('fol_axiom'):
        fol = fix_dl_in_fol(fix_fol_annotation(cls_data['fol_axiom']))
        axioms.append(('Necessary condition', fol))
    else:
        # Derive from genus + restrictions
        parent_preds = [label_to_pred(p) for p in cls_data.get('parents', []) if p]
        if parent_preds:
            genus = parent_preds[0]
            # Build combined necessary condition: genus ∧ ∃-restrictions
            parts = [f'{genus}(x)']
            for prop, filler in cls_data.get('some_restrictions', []):
                filler_pred = label_to_pred(filler)
                v = _fresh_var(prop)
                parts.append(f'∃{v} ({filler_pred}({v}) ∧ {prop}(x,{v}))')
            if len(parts) == 1:
                axioms.append(('Necessary condition', f'∀x ({pred}(x) → {parts[0]})'))
            else:
                rhs = ' ∧ '.join(parts)
                axioms.append(('Necessary condition', f'∀x ({pred}(x) → {rhs})'))
        elif cls_data.get('some_restrictions'):
            # No parents but has some_restrictions
            parts = []
            for prop, filler in cls_data.get('some_restrictions', []):
                filler_pred = label_to_pred(filler)
                v = _fresh_var(prop)
                parts.append(f'∃{v} ({filler_pred}({v}) ∧ {prop}(x,{v}))')
            rhs = ' ∧ '.join(parts)
            axioms.append(('Necessary condition', f'∀x ({pred}(x) → {rhs})'))

        # Additional universal restrictions (allValuesFrom)
        for prop, filler in cls_data.get('all_restrictions', []):
            filler_pred = label_to_pred(filler)
            axioms.append(
                (f'Universal restriction: {filler_pred}',
                 gen_all_restriction(pred, prop, filler_pred))
            )

    # Disjointness axioms
    for other_label in cls_data.get('disjoint_with', []):
        other_pred = label_to_pred(other_label)
        axioms.append(('Disjointness', gen_disjointness(pred, other_pred)))

    return axioms


def _extract_existing_axioms_from_html(html_content: str) -> list:
    """Extract existing fol-line spans from the HTML FOL block.

    Returns list of (label, fol_string) tuples with DL notation and ∀x fixed.
    """
    m = _FOL_BLOCK_RE.search(html_content)
    if not m:
        return []
    inner = m.group(2)
    # Match each fol-line span: label + fol text (stripping trailing comment span)
    line_re = re.compile(
        r'<span class="fol-line">'
        r'<span class="fol-label">\[([^\]]+)\]</span>'
        r'(.*?)'
        r'(?:<span\s+style="[^"]*">.*?</span>)?'
        r'\s*</span>',
        re.DOTALL
    )
    axioms = []
    for lm in line_re.finditer(inner):
        label = lm.group(1).strip()
        # Strip any remaining HTML tags from the fol text
        fol_raw = re.sub(r'<[^>]+>', '', lm.group(2)).strip()
        fol_fixed = fix_dl_in_fol(fix_fol_annotation(fol_raw))
        axioms.append((label, fol_fixed))
    return axioms


def patch_fol_block_in_html(html_content: str, ttl_data: dict, html_label: str,
                              _override_inner: str = None) -> str:
    """Replace the FOL Theory block in html_content.

    If html_label (lowercase) is found in ttl_data, derives axioms from TTL.
    Otherwise fixes syntax errors in existing HTML axioms.

    Args:
        html_content: full HTML file content.
        ttl_data: result of extract_class_data (dict keyed by lowercase label).
        html_label: lowercase label for this HTML page (used to look up ttl_data).
        _override_inner: if provided, use this directly as the inner div content
                         (used in tests to inject arbitrary content).

    Returns:
        Patched HTML string.
    """
    if _override_inner is not None:
        new_inner = _override_inner
    elif html_label in ttl_data:
        axioms = build_axioms_for_ttl_class(ttl_data[html_label])
        new_inner = render_fol_block(axioms)
    else:
        axioms = _extract_existing_axioms_from_html(html_content)
        new_inner = render_fol_block(axioms)

    def replacer(m):
        return m.group(1) + new_inner + m.group(3)

    return _FOL_BLOCK_RE.sub(replacer, html_content, count=1)


def patch_html_file(path: str, ttl_data: dict) -> bool:
    """Patch the FOL block in the HTML file at path. Returns True if changed."""
    p = pathlib.Path(path)
    original = p.read_text(encoding='utf-8')

    # Extract HTML label from <title> tag (format: "COPI · ClassName")
    m = re.search(r'<title>COPI\s*[·•]\s*(.*?)</title>', original, re.IGNORECASE)
    html_label = m.group(1).strip().lower() if m else ''

    patched = patch_fol_block_in_html(original, ttl_data, html_label)
    if patched != original:
        p.write_text(patched, encoding='utf-8')
        return True
    return False


if __name__ == '__main__':
    import sys
    sys.path.insert(0, str(pathlib.Path(__file__).parent))
    from fol_extract import extract_class_data
    repo_root = pathlib.Path(__file__).parent.parent
    ttl_path = str(repo_root / 'copi-full.ttl')
    html_dir = repo_root / 'docs' / 'classes'

    print('Loading TTL data...')
    ttl_data = extract_class_data(ttl_path)
    print(f'Loaded {len(ttl_data)} classes from TTL')

    changed = 0
    for html_file in sorted(html_dir.glob('*.html')):
        if patch_html_file(str(html_file), ttl_data):
            changed += 1
            print(f'  patched: {html_file.name}')

    print(f'\nDone: {changed} files changed out of {len(list(html_dir.glob("*.html")))} total')
