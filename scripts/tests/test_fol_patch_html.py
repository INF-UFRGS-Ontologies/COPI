# scripts/tests/test_fol_patch_html.py
import sys
import pathlib
import re

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
import fol_patch_html
import fol_extract

TTL = str(pathlib.Path(__file__).parent.parent.parent / 'copi-full.ttl')
# Note: COPI_0000077.html = Valve (brief referenced COPI_0000001 which does not exist;
# actual HTML IDs start at COPI_0000072 — Valve lives at COPI_0000077)
HTML_DIR = pathlib.Path(__file__).parent.parent.parent / 'docs' / 'classes'


def _get_fol_block(html_content):
    m = re.search(
        r'<div class="axiom-block">\s*<div class="axiom-label"><span class="t-en">First-Order Logic Theory</span>.*?<div style="[^"]*">(.*?)</div>\s*</div>\s*</div>',
        html_content, re.DOTALL
    )
    return m.group(1) if m else None


def test_fix_dl_in_valve_html():
    """COPI_0000077.html (Valve) has ∃bearerOf.FlowControlFunction — should be fixed.

    Brief referenced COPI_0000001 but that file does not exist; Valve is COPI_0000077.
    Valve has no @en label in copi-full.ttl so it uses the HTML-extraction path.
    """
    path = HTML_DIR / 'COPI_0000077.html'
    ttl_data = fol_extract.extract_class_data(TTL)
    with open(path) as f:
        original = f.read()
    patched = fol_patch_html.patch_fol_block_in_html(original, ttl_data, 'valve')
    block = _get_fol_block(patched)
    assert block is not None
    # DL syntax must be gone
    assert '∃bearerOf.' not in block
    assert '∃hasComponentPartAtAllTimes.' not in block
    # Valid FOL must be present
    assert '∀x (Valve(x)' in block


def test_fix_missing_quantifier_in_operation_block():
    """The TTL has 'Operation(x) → PlannedProcess(x)' — should become ∀x (...)."""
    ttl_data = fol_extract.extract_class_data(TTL)
    axioms = fol_patch_html.build_axioms_for_ttl_class(ttl_data['operation'])
    fol_strings = [fol for _, fol in axioms]
    assert any('∀x (Operation(x) → PlannedProcess(x))' in s for s in fol_strings)


def test_gen_axioms_containment_function():
    """containment function has no FOL annotation but has someValuesFrom/allValuesFrom — derive both."""
    ttl_data = fol_extract.extract_class_data(TTL)
    axioms = fol_patch_html.build_axioms_for_ttl_class(ttl_data['containment function'])
    fol_strings = [fol for _, fol in axioms]
    assert any('∃p (MaterialContainment(p) ∧ realizedIn(x,p))' in s for s in fol_strings)
    assert any('realizedIn(x,p) → MaterialContainment(p)' in s for s in fol_strings)


def test_gen_axioms_with_disjointness():
    """liquid pressure increase is disjoint with gas pressure increase."""
    ttl_data = fol_extract.extract_class_data(TTL)
    axioms = fol_patch_html.build_axioms_for_ttl_class(ttl_data['liquid pressure increase'])
    labels = [label for label, _ in axioms]
    fols = [fol for _, fol in axioms]
    assert 'Disjointness' in labels
    assert any('GasPressureIncrease' in s for s in fols)


def test_patch_fol_block_replaces_correctly():
    """patch_fol_block_in_html should replace only the inner div content.

    Brief referenced COPI_0000001 but that file does not exist; using COPI_0000077 (Valve).
    """
    with open(HTML_DIR / 'COPI_0000077.html') as f:
        content = f.read()
    new_inner = '<span class="fol-line">TEST_SENTINEL</span>\n'
    patched = fol_patch_html.patch_fol_block_in_html(
        content,
        fol_extract.extract_class_data(TTL),
        'valve',
        _override_inner=new_inner
    )
    assert 'TEST_SENTINEL' in patched
    block = _get_fol_block(patched)
    assert block is not None
