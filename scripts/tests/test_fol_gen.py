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
