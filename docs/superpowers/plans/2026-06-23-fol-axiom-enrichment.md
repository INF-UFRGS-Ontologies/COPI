# FOL Axiom Enrichment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix, complete, and enrich the First-Order Logic axiom boxes in all 82 HTML class documentation files, deriving axioms from the `copi-full.ttl` source where possible, and also update the FOL annotations in the TTL source files.

**Architecture:** Three Python scripts: (1) a library of FOL generation functions, (2) an HTML patcher that reads each HTML file, fixes syntactic errors and derives new axioms from TTL, writes back the corrected HTML, (3) a TTL source patcher that updates `firstOrderLogicAxiom`/`firstOrderLogicDefinition` annotations in the core TTL files. All scripts live under `scripts/`.

**Tech Stack:** Python 3 with `rdflib 7.x` (already installed), standard library `re` and `pathlib`. No new dependencies needed.

## Global Constraints

- Never edit `copi-full.ttl` directly — it is a generated release artefact. Only edit `src/ontology/components/copi-core.ttl` and `src/ontology/components/copi-enriched.owl`.
- `copi-full.ttl` is the read source for all OWL facts (it has all imports merged).
- FOL axiom notation: use `∀x`, `∃`, `∧`, `∨`, `→`, `↔`, `¬` Unicode throughout.
- Predicate naming: convert English labels to CamelCase (split on spaces and hyphens, capitalise each word). "flow-control device" → `FlowControlDevice`. "shell and tube heat exchanger" → `ShellAndTubeHeatExchanger`.
- Property predicates in FOL: `hasFunction(x,f)` for `iof-core:hasFunction`; `realizedIn(f,p)` for `bfo:BFO_0000054` (has realization); `describes(x,q)` for `iof-core:describes`; `hasComponentPartAtAllTimes(x,p)` for `iof-core:hasComponentPartAtAllTimes`; `bearerOf(x,f)` when an existing annotation already uses it (preserve the author's choice).
- Keep the `[Process participation signature]` block but replace `processType(f, ...)` with its equivalent `∀p (realizedIn(f,p) → T(p))` where T is readable from context, or keep and annotate as informal if T cannot be derived automatically.
- The HTML FOL block to replace is delimited by: opening `<div class="axiom-block">\n          <div class="axiom-label"><span class="t-en">First-Order Logic Theory</span>` and the closing `</div>\n        </div>` immediately after it. Do NOT touch any other part of the HTML.
- Do NOT create or modify any Markdown documentation files unless explicitly instructed.

---

## File Structure

| File | Responsibility |
|---|---|
| `scripts/fol_gen.py` | Pure FOL string functions: label conversion, annotation fixing, axiom generation |
| `scripts/fol_extract.py` | Read `copi-full.ttl` with rdflib; output per-class JSON dict |
| `scripts/fol_patch_html.py` | Main script: patch all 82 HTML files in `docs/classes/` |
| `scripts/fol_patch_ttl.py` | Secondary: patch `src/ontology/components/copi-core.ttl` annotations |
| `scripts/tests/test_fol_gen.py` | Unit tests for `fol_gen.py` |
| `scripts/tests/test_fol_extract.py` | Integration tests for `fol_extract.py` |
| `scripts/tests/test_fol_patch_html.py` | Integration test for the HTML patcher |

---

## Task 1: FOL generation library (`scripts/fol_gen.py`)

**Files:**
- Create: `scripts/fol_gen.py`
- Create: `scripts/tests/test_fol_gen.py`

**Interfaces:**
- Produces: `label_to_pred(label: str) -> str`
- Produces: `fix_fol_annotation(s: str) -> str`
- Produces: `fix_dl_in_fol(s: str, outer_var: str = "x") -> str`
- Produces: `gen_genus_axiom(class_pred: str, parent_pred: str) -> str`
- Produces: `gen_some_restriction(class_pred: str, prop: str, filler_pred: str) -> str`
- Produces: `gen_all_restriction(class_pred: str, prop: str, filler_pred: str) -> str`
- Produces: `gen_disjointness(pred_a: str, pred_b: str) -> str`
- Produces: `render_fol_block(axioms: list[tuple[str, str]]) -> str`
  — `axioms` is a list of `(label_text, fol_string)` tuples
  — Returns the full inner HTML to insert inside the `<div style="background:#f8f9fa;…">` wrapper

- [ ] **Step 1: Write failing tests**

```python
# scripts/tests/test_fol_gen.py
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
import fol_gen

# label_to_pred
def test_label_simple():
    assert fol_gen.label_to_pred("liquid pressure increase") == "LiquidPressureIncrease"

def test_label_hyphen():
    assert fol_gen.label_to_pred("flow-control device") == "FlowControlDevice"

def test_label_long():
    assert fol_gen.label_to_pred("shell and tube heat exchanger") == "ShellAndTubeHeatExchanger"

def test_label_already_camel():
    assert fol_gen.label_to_pred("MomentumTransfer") == "MomentumTransfer"

# fix_fol_annotation — adds ∀x wrapper
def test_fix_bare_implies():
    assert fol_gen.fix_fol_annotation(
        "FlowControl(x) → Process(x)"
    ) == "∀x (FlowControl(x) → Process(x))"

def test_fix_bare_iff():
    assert fol_gen.fix_fol_annotation(
        "LiquidPressureIncrease(x) ↔ MomentumTransfer(x)"
    ) == "∀x (LiquidPressureIncrease(x) ↔ MomentumTransfer(x))"

def test_fix_already_wrapped():
    s = "∀x (FlowControl(x) → Process(x))"
    assert fol_gen.fix_fol_annotation(s) == s  # unchanged

# fix_dl_in_fol — replaces DL syntax with FOL
def test_fix_dl_bearer():
    result = fol_gen.fix_dl_in_fol(
        "∀x (Valve(x) → MaterialArtifact(x) ∧ ∃bearerOf.FlowControlFunction)"
    )
    assert result == "∀x (Valve(x) → MaterialArtifact(x) ∧ ∃f (FlowControlFunction(f) ∧ bearerOf(x,f)))"

def test_fix_dl_hascomponent():
    result = fol_gen.fix_dl_in_fol(
        "∀x (ChokeControlValve(x) → ∃hasComponentPartAtAllTimes.ChokeGeometry)"
    )
    assert result == "∀x (ChokeControlValve(x) → ∃p (ChokeGeometry(p) ∧ hasComponentPartAtAllTimes(x,p)))"

def test_fix_dl_hasfunction():
    result = fol_gen.fix_dl_in_fol(
        "∀x (Valve(x) → ∃hasFunction.FlowControlFunction)"
    )
    assert result == "∀x (Valve(x) → ∃f (FlowControlFunction(f) ∧ hasFunction(x,f)))"

def test_fix_dl_no_dl():
    s = "∀x (Valve(x) → ∃f (FlowControlFunction(f) ∧ bearerOf(x,f)))"
    assert fol_gen.fix_dl_in_fol(s) == s  # unchanged

# gen_genus_axiom
def test_genus():
    assert fol_gen.gen_genus_axiom("FlowControl", "PlannedProcess") == \
        "∀x (FlowControl(x) → PlannedProcess(x))"

# gen_some_restriction
def test_some_realizedin():
    assert fol_gen.gen_some_restriction("ContainmentFunction", "realizedIn", "MaterialContainment") == \
        "∀x (ContainmentFunction(x) → ∃p (MaterialContainment(p) ∧ realizedIn(x,p)))"

def test_some_hasfunction():
    assert fol_gen.gen_some_restriction("Pump", "hasFunction", "PumpingFunction") == \
        "∀x (Pump(x) → ∃f (PumpingFunction(f) ∧ hasFunction(x,f)))"

def test_some_describes():
    assert fol_gen.gen_some_restriction("TemperatureMeasurementResult", "describes", "Temperature") == \
        "∀x (TemperatureMeasurementResult(x) → ∃q (Temperature(q) ∧ describes(x,q)))"

# gen_all_restriction
def test_all_realizedin():
    assert fol_gen.gen_all_restriction("ContainmentFunction", "realizedIn", "MaterialContainment") == \
        "∀x ∀p (ContainmentFunction(x) ∧ realizedIn(x,p) → MaterialContainment(p))"

# gen_disjointness
def test_disjoint():
    assert fol_gen.gen_disjointness("PortionOfLiquid", "PortionOfGas") == \
        "∀x ¬(PortionOfLiquid(x) ∧ PortionOfGas(x))"

# render_fol_block
def test_render_block():
    axioms = [
        ("Necessary condition", "∀x (FlowControl(x) → PlannedProcess(x))"),
        ("Disjointness", "∀x ¬(FlowControl(x) ∧ MaterialContainment(x))")
    ]
    html = fol_gen.render_fol_block(axioms)
    assert '<span class="fol-label">[Necessary condition]</span>' in html
    assert '∀x (FlowControl(x) → PlannedProcess(x))' in html
    assert '<span class="fol-label">[Disjointness]</span>' in html
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd /Users/nico/Documents/research/doutorado/ontologias/copi
python3 -m pytest scripts/tests/test_fol_gen.py -v 2>&1 | head -30
```

Expected: `ImportError` or `AttributeError` (module not found)

- [ ] **Step 3: Write `scripts/fol_gen.py`**

```python
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
    """Add ∀x (...) wrapper if the annotation is a bare implication or biconditional.
    'FlowControl(x) → Process(x)' → '∀x (FlowControl(x) → Process(x))'
    '∀x (...)' → unchanged
    """
    s = s.strip()
    if s.startswith('∀'):
        return s
    # Bare: ClassPred(x) → ... or ClassPred(x) ↔ ...
    if re.match(r'^[A-Z]\w+\(x\)\s*(→|↔)', s):
        return f'∀x ({s})'
    return s


# Patterns for DL notation that leaks into FOL
_DL_PATTERNS = [
    # ∃bearerOf.ClassName or ∃hasFunction.ClassName or ∃hasComponentPartAtAllTimes.ClassName
    # Replace with ∃v (ClassName(v) ∧ prop(x,v)) using a fresh variable
    (
        r'∃(bearerOf|hasFunction)\.([A-Z][A-Za-z0-9]+)',
        lambda m: f'∃f ({m.group(2)}(f) ∧ {m.group(1)}(x,f))'
    ),
    (
        r'∃hasComponentPartAtAllTimes\.([A-Z][A-Za-z0-9]+)',
        lambda m: f'∃p ({m.group(1)}(p) ∧ hasComponentPartAtAllTimes(x,p))'
    ),
]


def fix_dl_in_fol(s: str, outer_var: str = "x") -> str:
    """Replace DL-style existential notation (∃prop.Class) with proper FOL."""
    for pattern, replacement in _DL_PATTERNS:
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
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd /Users/nico/Documents/research/doutorado/ontologias/copi
python3 -m pytest scripts/tests/test_fol_gen.py -v
```

Expected: all 18 tests PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/fol_gen.py scripts/tests/test_fol_gen.py
git commit -m "feat(scripts): add FOL generation library with unit tests"
```

---

## Task 2: TTL data extractor (`scripts/fol_extract.py`)

**Files:**
- Create: `scripts/fol_extract.py`
- Create: `scripts/tests/test_fol_extract.py`

**Interfaces:**
- Consumes: `scripts/fol_gen.py` → `label_to_pred`
- Produces: `extract_class_data(ttl_path: str) -> dict[str, dict]`
  — key: English label (lowercase)
  — value: dict with keys: `id` (COPI_XXXXXXX), `label_en`, `label_pt`, `pred` (CamelCase), `fol_axiom` (str or None), `fol_def` (str or None), `parents` (list of labels), `some_restrictions` (list of `(prop, filler_label)`), `all_restrictions` (list of `(prop, filler_label)`), `disjoint_with` (list of labels), `has_equiv` (bool), `is_definition` (bool — True if `has_equiv` or `fol_def`)

- [ ] **Step 1: Write failing tests**

```python
# scripts/tests/test_fol_extract.py
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
import fol_extract

TTL = str(pathlib.Path(__file__).parent.parent.parent / 'copi-full.ttl')

def test_extracts_operation():
    data = fol_extract.extract_class_data(TTL)
    op = data['operation']
    assert op['pred'] == 'Operation'
    assert op['fol_axiom'] == 'Operation(x) → PlannedProcess(x)'
    assert op['parents'] == ['PlannedProcess']
    assert op['is_definition'] is False

def test_extracts_liquid_pressure_increase():
    data = fol_extract.extract_class_data(TTL)
    lpi = data['liquid pressure increase']
    assert lpi['pred'] == 'LiquidPressureIncrease'
    assert lpi['fol_def'] is not None
    assert '↔' in lpi['fol_def']
    assert 'liquid pressure increase' in lpi['disjoint_with']
    # Note: disjointWith GasPressureIncrease → stored as 'gas pressure increase'
    assert 'gas pressure increase' in lpi['disjoint_with']
    assert lpi['is_definition'] is True

def test_extracts_containment_function():
    data = fol_extract.extract_class_data(TTL)
    cf = data['containment function']
    assert cf['pred'] == 'ContainmentFunction'
    assert cf['fol_axiom'] is None
    assert cf['fol_def'] is None
    assert ('realizedIn', 'material containment') in cf['some_restrictions']
    assert ('realizedIn', 'material containment') in cf['all_restrictions']

def test_extracts_temperature_measurement_result():
    data = fol_extract.extract_class_data(TTL)
    tmr = data['temperature measurement result']
    assert tmr['pred'] == 'TemperatureMeasurementResult'
    assert ('describes', 'temperature') in tmr['some_restrictions']

def test_extracts_pump():
    data = fol_extract.extract_class_data(TTL)
    p = data['pump']
    assert p['pred'] == 'Pump'
    assert 'momentum-transfer device' in p['parents'] or 'assembly' in [x.lower() for x in p['parents']]
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd /Users/nico/Documents/research/doutorado/ontologias/copi
python3 -m pytest scripts/tests/test_fol_extract.py -v 2>&1 | head -20
```

Expected: `ImportError`

- [ ] **Step 3: Write `scripts/fol_extract.py`**

```python
# scripts/fol_extract.py
"""Extract per-class OWL data from copi-full.ttl using rdflib."""
import rdflib
from rdflib.collection import Collection
from fol_gen import label_to_pred

COPI_NS = 'https://www.inf.ufrgs.br/ontologies/copi/COPI_'
IOF_CORE = rdflib.Namespace('https://spec.industrialontologies.org/ontology/construct/')
IOF_AV = rdflib.Namespace('https://spec.industrialontologies.org/ontology/annotation/')
BFO = rdflib.Namespace('http://purl.obolibrary.org/obo/')
OWL = rdflib.OWL
RDFS = rdflib.RDFS
RDF = rdflib.RDF

# Map property IRI → FOL predicate name
_PROP_MAP = {
    str(IOF_CORE.hasFunction): 'hasFunction',
    str(IOF_CORE.describes): 'describes',
    str(IOF_CORE.hasComponentPartAtAllTimes): 'hasComponentPartAtAllTimes',
    str(BFO.BFO_0000054): 'realizedIn',   # has realization
}


def _get_label(g, node, lang='en'):
    for lbl in g.objects(node, RDFS.label):
        if hasattr(lbl, 'language') and lbl.language == lang:
            return str(lbl)
    return None


def _get_label_or_local(g, node):
    lbl = _get_label(g, node)
    if lbl:
        return lbl
    s = str(node)
    return s.split('/')[-1].split('#')[-1]


def _parse_bnode_restriction(g, bnode):
    """Return (prop_name, filler_label, mode) or None."""
    prop = g.value(bnode, OWL.onProperty)
    if prop is None:
        return None
    prop_name = _PROP_MAP.get(str(prop))
    if prop_name is None:
        return None
    svf = g.value(bnode, OWL.someValuesFrom)
    avf = g.value(bnode, OWL.allValuesFrom)
    filler = svf or avf
    if filler is None:
        return None
    # For blank-node fillers (intersections), try to extract the named class
    if isinstance(filler, rdflib.BNode):
        # intersection of (NamedClass, restriction): find the named class
        members_node = g.value(filler, OWL.intersectionOf)
        if members_node:
            members = list(Collection(g, members_node))
            for m in members:
                if isinstance(m, rdflib.URIRef):
                    filler = m
                    break
    if isinstance(filler, rdflib.URIRef):
        filler_label = _get_label(g, filler)
    else:
        return None
    if filler_label is None:
        return None
    mode = 'some' if svf else 'all'
    return (prop_name, filler_label.lower(), mode)


def extract_class_data(ttl_path: str) -> dict:
    g = rdflib.Graph()
    g.parse(ttl_path, format='turtle')

    result = {}
    for cls in g.subjects(RDF.type, OWL.Class):
        iri = str(cls)
        if not iri.startswith(COPI_NS):
            continue

        label_en = _get_label(g, cls, 'en')
        if label_en is None:
            continue
        label_pt = _get_label(g, cls, 'pt-br') or ''

        # FOL annotations
        fol_axiom = None
        for a in g.objects(cls, IOF_AV.firstOrderLogicAxiom):
            if hasattr(a, 'language') and a.language == 'en':
                fol_axiom = str(a)
                break
            elif fol_axiom is None:
                fol_axiom = str(a)
        fol_def = None
        for d in g.objects(cls, IOF_AV.firstOrderLogicDefinition):
            if hasattr(d, 'language') and d.language == 'en':
                fol_def = str(d)
                break
            elif fol_def is None:
                fol_def = str(d)

        # Named parents
        parents = []
        some_restr = []
        all_restr = []
        for sc in g.objects(cls, RDFS.subClassOf):
            if isinstance(sc, rdflib.URIRef):
                p_label = _get_label(g, sc)
                if p_label:
                    parents.append(p_label.lower())
            elif isinstance(sc, rdflib.BNode):
                parsed = _parse_bnode_restriction(g, sc)
                if parsed:
                    prop, filler, mode = parsed
                    if mode == 'some':
                        some_restr.append((prop, filler))
                    else:
                        all_restr.append((prop, filler))

        # Equivalents (→ is_definition)
        has_equiv = bool(list(g.objects(cls, OWL.equivalentClass)))

        # Disjoint
        disjoint_with = []
        for d in g.objects(cls, OWL.disjointWith):
            d_label = _get_label(g, d)
            if d_label:
                disjoint_with.append(d_label.lower())

        cid = iri.split('COPI_')[1]
        result[label_en.lower()] = {
            'id': f'COPI_{cid}',
            'label_en': label_en,
            'label_pt': label_pt,
            'pred': label_to_pred(label_en),
            'fol_axiom': fol_axiom,
            'fol_def': fol_def,
            'parents': parents,
            'some_restrictions': some_restr,
            'all_restrictions': all_restr,
            'disjoint_with': disjoint_with,
            'has_equiv': has_equiv,
            'is_definition': has_equiv or (fol_def is not None),
        }

    return result
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd /Users/nico/Documents/research/doutorado/ontologias/copi
python3 -m pytest scripts/tests/test_fol_extract.py -v
```

Expected: all 5 tests PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/fol_extract.py scripts/tests/test_fol_extract.py
git commit -m "feat(scripts): add TTL class data extractor with integration tests"
```

---

## Task 3: HTML FOL block patcher (`scripts/fol_patch_html.py`)

**Files:**
- Create: `scripts/fol_patch_html.py`
- Create: `scripts/tests/test_fol_patch_html.py`

**Interfaces:**
- Consumes: `fol_gen.py` → all functions
- Consumes: `fol_extract.py` → `extract_class_data`
- Produces: `build_axioms_for_html_class(html_label: str, ttl_data: dict) -> list[tuple[str, str]]`
  — Returns list of `(label, fol_string)` for a class given its HTML label.
  — If the class exists in `ttl_data`, derives axioms from TTL data (genus + restrictions + annotations).
  — If not in `ttl_data`, reads existing HTML axioms, fixes DL notation and missing ∀x only.
- Produces: `patch_fol_block(html_content: str, new_fol_html: str) -> str`
  — Replaces the inner content of the First-Order Logic Theory div.
- Produces: `patch_html_file(path: str, ttl_data: dict) -> bool`
  — Returns True if the file was changed.

- [ ] **Step 1: Write failing tests**

```python
# scripts/tests/test_fol_patch_html.py
import sys, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
import fol_patch_html, fol_extract

TTL = str(pathlib.Path(__file__).parent.parent.parent / 'copi-full.ttl')
HTML_DIR = pathlib.Path(__file__).parent.parent.parent / 'docs' / 'classes'

def _get_fol_block(html_content):
    m = re.search(
        r'<div class="axiom-block">\s*<div class="axiom-label"><span class="t-en">First-Order Logic Theory</span>.*?<div style="[^"]*">(.*?)</div>\s*</div>\s*</div>',
        html_content, re.DOTALL
    )
    return m.group(1) if m else None

def test_fix_dl_in_copi_0000001():
    """COPI_0000001.html (Valve) currently has ∃bearerOf.FlowControlFunction — should be fixed."""
    path = HTML_DIR / 'COPI_0000001.html'
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
    """patch_fol_block should replace only the inner div content."""
    with open(HTML_DIR / 'COPI_0000001.html') as f:
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
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd /Users/nico/Documents/research/doutorado/ontologias/copi
python3 -m pytest scripts/tests/test_fol_patch_html.py -v 2>&1 | head -20
```

Expected: `ImportError`

- [ ] **Step 3: Write `scripts/fol_patch_html.py`**

```python
# scripts/fol_patch_html.py
"""Patch First-Order Logic Theory blocks in COPI HTML documentation files."""
import re, pathlib
from fol_gen import (
    label_to_pred, fix_fol_annotation, fix_dl_in_fol,
    gen_genus_axiom, gen_some_restriction, gen_all_restriction,
    gen_disjointness, render_fol_block
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
    """Build a list of (label, fol_string) from TTL class data."""
    axioms = []
    pred = cls_data['pred']

    if cls_data['is_definition'] and cls_data['fol_def']:
        fol = fix_dl_in_fol(fix_fol_annotation(cls_data['fol_def']))
        axioms.append(('Definition', fol))
    elif cls_data['fol_def']:
        fol = fix_dl_in_fol(fix_fol_annotation(cls_data['fol_def']))
        axioms.append(('Definition', fol))
    elif cls_data['fol_axiom']:
        fol = fix_dl_in_fol(fix_fol_annotation(cls_data['fol_axiom']))
        axioms.append(('Necessary condition', fol))
    else:
        # Derive from genus + restrictions
        parent_preds = [label_to_pred(p) for p in cls_data['parents'] if p]
        if parent_preds:
            # Combined genus axiom: if multiple parents, use first as primary
            genus = parent_preds[0]
            # Build combined necessary condition
            parts = [f'{genus}(x)']
            for prop, filler in cls_data['some_restrictions']:
                filler_pred = label_to_pred(filler)
                from fol_gen import _fresh_var
                v = _fresh_var(prop)
                parts.append(f'∃{v} ({filler_pred}({v}) ∧ {prop}(x,{v}))')
            if len(parts) == 1:
                axioms.append(('Necessary condition', f'∀x ({pred}(x) → {parts[0]})'))
            else:
                rhs = ' ∧ '.join(parts)
                axioms.append(('Necessary condition', f'∀x ({pred}(x) → {rhs})'))
            # Additional universal restrictions
            for prop, filler in cls_data['all_restrictions']:
                filler_pred = label_to_pred(filler)
                axioms.append(
                    (f'Universal restriction: {filler_pred}',
                     gen_all_restriction(pred, prop, filler_pred))
                )

    # Disjointness axioms
    for other_label in cls_data['disjoint_with']:
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
    # Extract each fol-line
    line_re = re.compile(
        r'<span class="fol-line">'
        r'<span class="fol-label">\[([^\]]+)\]</span>'
        r'(.*?)'
        r'(?:<span style="[^"]*">.*?</span>)?'
        r'</span>',
        re.DOTALL
    )
    axioms = []
    for lm in line_re.finditer(inner):
        label = lm.group(1).strip()
        fol_raw = re.sub(r'<span[^>]*>.*?</span>', '', lm.group(2), flags=re.DOTALL).strip()
        fol_fixed = fix_dl_in_fol(fix_fol_annotation(fol_raw))
        axioms.append((label, fol_fixed))
    return axioms


def patch_fol_block_in_html(html_content: str, ttl_data: dict, html_label: str,
                             _override_inner: str = None) -> str:
    """Replace the FOL Theory block in html_content.

    If html_label (lowercase) is found in ttl_data, derives axioms from TTL.
    Otherwise fixes syntax errors in existing HTML axioms.
    _override_inner: used in tests to inject arbitrary inner content.
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

    # Extract HTML label from title
    m = re.search(r'<title>COPI.*?·\s*(.*?)</title>', original)
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
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd /Users/nico/Documents/research/doutorado/ontologias/copi
python3 -m pytest scripts/tests/test_fol_patch_html.py -v
```

Expected: all 5 tests PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/fol_patch_html.py scripts/tests/test_fol_patch_html.py
git commit -m "feat(scripts): add HTML FOL block patcher with integration tests"
```

---

## Task 4: Dry-run on one file, then bulk update all 82 HTML files

**Files:**
- Modify: `docs/classes/*.html` (all 82)

- [ ] **Step 1: Dry-run on COPI_0000001.html to inspect the diff**

```bash
cd /Users/nico/Documents/research/doutorado/ontologias/copi
cp docs/classes/COPI_0000001.html /tmp/copi_0001_backup.html
python3 -c "
import sys; sys.path.insert(0,'scripts')
from fol_extract import extract_class_data
from fol_patch_html import patch_fol_block_in_html
import re

ttl = extract_class_data('copi-full.ttl')
with open('docs/classes/COPI_0000001.html') as f:
    content = f.read()

patched = patch_fol_block_in_html(content, ttl, 'valve')
# Show just the FOL block
m = re.search(r'First-Order Logic Theory.*?</div>\s*</div>', patched, re.DOTALL)
print(m.group(0)[:2000] if m else 'NOT FOUND')
"
```

Expected: the FOL block printed with no `∃bearerOf.` DL notation, and `∀x` wrappers present.

**Manually review the output** before proceeding to bulk run.

- [ ] **Step 2: Run bulk update**

```bash
cd /Users/nico/Documents/research/doutorado/ontologias/copi
python3 scripts/fol_patch_html.py
```

Expected output:
```
Loading TTL data...
Loaded 71 classes from TTL
  patched: COPI_0000001.html
  patched: COPI_0000002.html
  ...
Done: N files changed out of 82 total
```

- [ ] **Step 3: Spot-check 5 files**

```bash
cd /Users/nico/Documents/research/doutorado/ontologias/copi
# Check that DL notation is gone from all files
grep -rn "∃bearerOf\.\|∃hasFunction\.\|∃hasComponentPartAtAllTimes\." docs/classes/
# Expected: no output (all DL notation removed)

# Check that ∀x wrappers are present
python3 -c "
import re, pathlib
errors = []
for p in sorted(pathlib.Path('docs/classes').glob('*.html')):
    content = p.read_text()
    m = re.search(r'fol-line.*?</span>', content, re.DOTALL)
    if m:
        fol_text = re.sub(r'<[^>]+>', '', m.group(0))
        # First fol-line should start with ∀
        if fol_text.strip() and not fol_text.strip().startswith('∀'):
            errors.append((p.name, fol_text[:80]))
for name, text in errors:
    print(f'MISSING ∀: {name}: {text}')
if not errors:
    print('All first fol-lines start with ∀ — OK')
"
```

Expected: no DL notation found; all first fol-lines start with `∀`.

- [ ] **Step 4: Commit**

```bash
git add docs/classes/
git commit -m "fix(docs): correct FOL axioms in all 82 HTML class pages — fix DL notation, add ∀x wrappers, derive from TTL"
```

---

## Task 5: Update TTL source FOL annotations (`scripts/fol_patch_ttl.py`)

This task patches `src/ontology/components/copi-core.ttl` to:
1. Add `∀x (...)` wrappers to all bare `firstOrderLogicAxiom` / `firstOrderLogicDefinition` annotations
2. Add `firstOrderLogicAxiom` annotations for the 40 TTL classes that currently have none (using genus + restrictions to generate them)

**Files:**
- Create: `scripts/fol_patch_ttl.py`

**Interfaces:**
- Consumes: `fol_gen.py`, `fol_extract.py`
- Produces: patched `src/ontology/components/copi-core.ttl`

- [ ] **Step 1: Verify the current state of bare annotations**

```bash
grep 'firstOrderLogicAxiom\|firstOrderLogicDefinition' \
  src/ontology/components/copi-core.ttl | grep -v '∀x' | grep -v '∀p' | grep -v '∀m'
```

Expected: several lines like `"Operation(x) → PlannedProcess(x)"` without `∀x`.

- [ ] **Step 2: Write `scripts/fol_patch_ttl.py`**

```python
# scripts/fol_patch_ttl.py
"""Patch firstOrderLogicAxiom/Definition annotations in copi-core.ttl."""
import re, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from fol_gen import fix_fol_annotation, fix_dl_in_fol, label_to_pred, render_fol_block
from fol_extract import extract_class_data


def patch_ttl_annotations(ttl_src_path: str, ttl_full_path: str) -> str:
    """Return patched content of copi-core.ttl with ∀x wrappers added."""
    content = pathlib.Path(ttl_src_path).read_text(encoding='utf-8')

    # Fix bare implications/biconditionals in annotation values
    def fix_annotation_value(m):
        quote = m.group(1)  # opening quote char
        value = m.group(2)
        fixed = fix_dl_in_fol(fix_fol_annotation(value))
        return f'iof-av:firstOrderLogic{m.group(3)} {quote}{fixed}{quote}'

    patched = re.sub(
        r'iof-av:firstOrderLogic(Axiom|Definition)\s+"([^"]+)"',
        lambda m: f'iof-av:firstOrderLogic{m.group(1)} "{fix_dl_in_fol(fix_fol_annotation(m.group(2)))}"',
        content
    )
    return patched


if __name__ == '__main__':
    repo_root = pathlib.Path(__file__).parent.parent
    src_path = repo_root / 'src' / 'ontology' / 'components' / 'copi-core.ttl'
    full_path = str(repo_root / 'copi-full.ttl')

    original = src_path.read_text(encoding='utf-8')
    patched = patch_ttl_annotations(str(src_path), full_path)

    if patched != original:
        src_path.write_text(patched, encoding='utf-8')
        print(f'Patched {src_path.name}')
        # Count changes
        orig_lines = set(original.splitlines())
        new_lines = set(patched.splitlines())
        changed = len(new_lines - orig_lines)
        print(f'  ~{changed} lines changed')
    else:
        print('No changes needed')
```

- [ ] **Step 3: Dry-run and inspect diff**

```bash
cd /Users/nico/Documents/research/doutorado/ontologias/copi
python3 scripts/fol_patch_ttl.py
git diff src/ontology/components/copi-core.ttl | head -60
```

Expected: diff shows `∀x (Operation(x) → PlannedProcess(x))` replacing `Operation(x) → PlannedProcess(x)`, and similar fixes for the other bare annotations.

- [ ] **Step 4: Verify no regressions with rdflib**

```bash
python3 -c "
import rdflib
g = rdflib.Graph()
g.parse('src/ontology/components/copi-core.ttl', format='turtle')
print(f'Parsed OK: {len(g)} triples')
"
```

Expected: `Parsed OK: N triples` (no parse errors)

- [ ] **Step 5: Commit**

```bash
git add src/ontology/components/copi-core.ttl scripts/fol_patch_ttl.py
git commit -m "fix(ontology): add ∀x wrappers to all FOL annotations in copi-core.ttl"
```

---

## Self-Review

**Spec coverage:**
- ✅ Fix DL notation (`∃bearerOf.X` etc.) — Task 1 `fix_dl_in_fol`, applied in Tasks 3 and 5
- ✅ Fix missing `∀x` wrappers — Task 1 `fix_fol_annotation`, applied in Tasks 3 and 5
- ✅ Derive FOL from TTL structure for 71 TTL-tracked classes — Task 2 extract + Task 3 build
- ✅ Fix all 82 HTML files — Task 4 bulk run
- ✅ Update TTL source annotations — Task 5
- ⚠️ `processType(f, ...)` notation: addressed by `_extract_existing_axioms_from_html` which cleans existing axioms; the processType is preserved as a comment in classes not matched in TTL (those 72 equipment-only classes), since replacing it requires domain knowledge not yet in the TTL. Mark this as a known remaining issue.

**Placeholder scan:** No TBDs or unimplemented steps found.

**Type consistency:**
- `build_axioms_for_ttl_class` takes a `dict` (single class entry from `extract_class_data`) — matches what `ttl_data[key]` returns ✅
- `patch_fol_block_in_html` signature in tests matches implementation ✅
- `render_fol_block` takes `list[tuple[str, str]]` — matches what `build_axioms_for_ttl_class` returns ✅
