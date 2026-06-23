# scripts/fol_gen.py
"""FOL string generation utilities for COPI documentation."""
import re


def label_to_pred(label: str) -> str:
    """Convert English label to CamelCase FOL predicate name.
    'flow-control device' → 'FlowControlDevice'
    'MomentumTransfer' → 'MomentumTransfer' (already CamelCase, returned as-is)
    """
    if re.match(r'^[A-Z][A-Za-z0-9]*$', label):
        return label
    return ''.join(w.capitalize() for w in re.split(r'[\s\-]+', label))


def fix_fol_annotation(s: str) -> str:
    """Add ∀v (...) wrapper if the annotation is a bare implication or biconditional.
    'FlowControl(x) → Process(x)' → '∀x (FlowControl(x) → Process(x))'
    'GasAbsorption(p) ↔ ...' → '∀p (GasAbsorption(p) ↔ ...)'
    '∀x (...)' → unchanged
    """
    s = s.strip()
    if s.startswith('∀'):
        return s
    # Bare: ClassPred(v) → ... or ClassPred(v) ↔ ... where v is a single letter
    m = re.match(r'^[A-Z]\w+\(([a-z])\)\s*(→|↔)', s)
    if m:
        v = m.group(1)
        return f'∀{v} ({s})'
    return s


def fix_dl_in_fol(s: str, outer_var: str = "x") -> str:
    """Replace DL-style existential notation (∃prop.Class) with proper FOL."""
    patterns = [
        (
            r'∃(bearerOf|hasFunction)\.([A-Z][A-Za-z0-9]+)',
            lambda m, v=outer_var: f'∃f ({m.group(2)}(f) ∧ {m.group(1)}({v},f))'
        ),
        (
            r'∃hasComponentPartAtAllTimes\.([A-Z][A-Za-z0-9]+)',
            lambda m, v=outer_var: f'∃p ({m.group(1)}(p) ∧ hasComponentPartAtAllTimes({v},p))'
        ),
    ]
    for pattern, replacement in patterns:
        s = re.sub(pattern, replacement, s)
    return s


# Variable name selection by property type
_PROP_VARS = {
    'realizedIn': 'p',
    'hasFunction': 'f',
    'bearerOf': 'f',
    'describes': 'q',
    'hasComponentPartAtAllTimes': 'p',
    'hasInput': 'm',
    'hasOutput': 'm',
}


def _fresh_var(prop: str) -> str:
    return _PROP_VARS.get(prop, 'y')


def gen_genus_axiom(class_pred: str, parent_pred: str) -> str:
    """∀x (C(x) → P(x))"""
    return f'∀x ({class_pred}(x) → {parent_pred}(x))'


def gen_some_restriction(class_pred: str, prop: str, filler_pred: str) -> str:
    """∀x (C(x) → ∃v (F(v) ∧ prop(x,v)))"""
    v = _fresh_var(prop)
    return f'∀x ({class_pred}(x) → ∃{v} ({filler_pred}({v}) ∧ {prop}(x,{v})))'


def gen_all_restriction(class_pred: str, prop: str, filler_pred: str) -> str:
    """∀x ∀v (C(x) ∧ prop(x,v) → F(v))"""
    v = _fresh_var(prop)
    return f'∀x ∀{v} ({class_pred}(x) ∧ {prop}(x,{v}) → {filler_pred}({v}))'


def gen_disjointness(pred_a: str, pred_b: str) -> str:
    """∀x ¬(A(x) ∧ B(x))"""
    return f'∀x ¬({pred_a}(x) ∧ {pred_b}(x))'


def render_fol_block(axioms: list) -> str:
    """Render a list of (label, fol_string) tuples as HTML fol-line spans.
    Returns the content to put inside the background div.
    """
    lines = []
    for label, fol in axioms:
        lines.append(
            f'<span class="fol-line">'
            f'<span class="fol-label">[{label}]</span>'
            f'{fol}'
            f'</span>'
        )
    return '\n'.join(lines) + '\n'
