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
