import rdflib, sys
from rdflib import RDF,RDFS,OWL,URIRef,Namespace
g=rdflib.Graph(); g.parse(sys.argv[1] if len(sys.argv)>1 else 'reasoned-test.owl')
C=Namespace("https://www.inf.ufrgs.br/ontologies/copi/"); T=Namespace("https://www.inf.ufrgs.br/ontologies/copi/test/")
def supers(c): return {s for s in g.transitive_objects(c,RDFS.subClassOf) if isinstance(s,URIRef) and s!=c}
def closure(i):
    ts={t for t in g.objects(i,RDF.type) if isinstance(t,URIRef)}; cl=set(ts)
    for t in ts: cl|=supers(t)
    return cl
conv=next(iter(g.subjects(RDFS.label, rdflib.Literal('conversion operation',lang='en'))))
checks=[
 ("PressureTransmitter ⊑ measurement instrument", C.COPI_0000024 in supers(T.PressureTransmitter)),
 ("PressureTransmitter ⊑ instrument", C.COPI_0000091 in supers(T.PressureTransmitter)),
 ("measurement instrument ⊑ instrument", C.COPI_0000091 in supers(C.COPI_0000024)),
 ("Controller ⊑ instrument", C.COPI_0000091 in supers(T.Controller)),
 ("Controller not ⊑ measurement instrument", C.COPI_0000024 not in supers(T.Controller)),
 ("Pump ⊑ momentum-transfer device", C.COPI_0000016 in supers(T.Pump)),
 ("Compressor ⊑ momentum-transfer device", C.COPI_0000016 in supers(T.Compressor)),
 ("HeatExchanger ⊑ heat-transfer device", C.COPI_0000017 in supers(T.HeatExchanger)),
 ("Reboiler ⊑ phase-change device", C.COPI_0000021 in supers(T.Reboiler)),
 ("Reboiler ⊑ mechanical-separation device", C.COPI_0000019 in supers(T.Reboiler)),
 ("Reboiler satisfiable", OWL.Nothing not in supers(T.Reboiler)),
 ("TraceHeatedLine satisfiable", OWL.Nothing not in supers(T.TraceHeatedLine)),
 ("line1 TraceHeatedLine and HeatExchanger", (T.line1,RDF.type,T.HeatExchanger) in g),
 ("proc1 hasInflowParticipant liquidA", (T.proc1, C.COPI_0001006, T.liquidA) in g),
 ("proc1 hasOutflowParticipant liquidB", (T.proc1, C.COPI_0001007, T.liquidB) in g),
 ("proc1 conversion operation (closure)", conv in closure(T.proc1)),
 ("proc1 momentum transfer", (T.proc1,RDF.type,C.COPI_0000003) in g),
 ("pump1 momentum-transfer device (closure)", C.COPI_0000016 in closure(T.pump1)),
 ("no unsatisfiable classes", not any(True for _ in g.subjects(RDFS.subClassOf,OWL.Nothing))),
 # review of 2026-11-17: control valves share the control signal, not the verb
 ("process-controlled flow function ⊑ magnitude control", C.COPI_0001016 in supers(C.COPI_0000027)),
 ("process-controlled flow function not ⊑ regulating", C.COPI_0001030 not in supers(C.COPI_0000027)),
 ("on-off (binary) function not ⊑ regulating", C.COPI_0001030 not in supers(T.BinaryFlowControlFunction)),
 ("on-off (binary) function satisfiable", OWL.Nothing not in supers(T.BinaryFlowControlFunction)),
 ("modulating function ⊑ regulating", C.COPI_0001030 in supers(T.ModulatingFlowControlFunction)),
]
# ---- annotation standard of copi-core-v2.ttl (same as the frozen v1: bilingual definition, comment, semiformal,
# example, explanatory note; FOL; isPrimitive with bilingual rationale when primitive; adaptedFrom or source)
from rdflib import Namespace as _NS, Graph
_AV=_NS("https://spec.industrialontologies.org/ontology/annotation/"); _SK=_NS("http://www.w3.org/2004/02/skos/core#"); _DC=_NS("http://purl.org/dc/terms/")
_core=Graph(); _core.parse("copi-core-v2.ttl", format="turtle")
_subj=[s for s in set(_core.subjects(RDF.type,None)) if isinstance(s,URIRef) and str(s).startswith(str(C)) and
       ((_core.value(s,RDF.type) in (OWL.Class, OWL.ObjectProperty, OWL.AnnotationProperty)) and (s,RDFS.isDefinedBy,None) in _core)]
def _has(s,p,lang): return any(getattr(o,"language",None)==lang for o in _core.objects(s,p))
_gaps=[]
for s in _subj:
    isap=(s,RDF.type,OWL.AnnotationProperty) in _core
    need=[(RDFS.label,"en"),(RDFS.label,"pt-br"),(_AV.naturalLanguageDefinition,"en"),(_AV.naturalLanguageDefinition,"pt-br"),(_SK.example,"en"),(_SK.example,"pt-br"),(_AV.explanatoryNote,"en"),(_AV.explanatoryNote,"pt-br")]
    for p,l in need:
        if not _has(s,p,l): _gaps.append(f"{s.rsplit('/',1)[-1]} {p.rsplit('/',1)[-1].rsplit('#',1)[-1]}@{l}")
    if not isap:
        for l in ("en","pt-br"):
            if not (_has(s,_AV.semiFormalNaturalLanguageAxiom,l) or _has(s,_AV.semiFormalNaturalLanguageDefinition,l)): _gaps.append(f"{s.rsplit('/',1)[-1]} semiformal@{l}")
        if not ((s,_AV.firstOrderLogicAxiom,None) in _core or (s,_AV.firstOrderLogicDefinition,None) in _core): _gaps.append(f"{s.rsplit('/',1)[-1]} FOL")
        if (s,RDF.type,OWL.Class) in _core:
            prim=_core.value(s,_AV.isPrimitive)
            if prim is None: _gaps.append(f"{s.rsplit('/',1)[-1]} isPrimitive")
            elif bool(prim) and not (_has(s,_AV.primitiveRationale,"en") and _has(s,_AV.primitiveRationale,"pt-br")): _gaps.append(f"{s.rsplit('/',1)[-1]} primitiveRationale")
    if (s,_DC.source,None) not in _core: _gaps.append(f"{s.rsplit('/',1)[-1]} dcterms:source")
# ---- Functional Basis in OWL only (review of 2026-11-17): no SKOS scheme; hirtz-coverage.csv lists every term of
# Hirtz with its status and is checked against the ontology; the path hierarchy is the class hierarchy
import os as _os
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))   # -I drops the script dir; hirtz_coverage.py lives beside check.py
import hirtz_coverage as _hc
_cov=_hc.load()
_res,_by_path=_hc.verify(_core,_cov)
checks.extend(_res)
_U=lambda c: URIRef(str(C)+c.split(":",1)[1])
_hier=[p for p,v in _by_path.items() if p.startswith("Function/") and p.rsplit("/",1)[0] in _by_path and _U(_by_path[p.rsplit("/",1)[0]][0]) not in supers(_U(v[0]))]
checks.append((f"function path hierarchy = class hierarchy ({sum(p.startswith('Function') for p in _by_path)} function classes)" + (f" — {_hier[:5]}" if _hier else ""), not _hier))
checks.append(("containment function ⊑ storing, not ⊑ containing", C.COPI_0001033 in supers(C.COPI_0000025) and C.COPI_0001091 not in supers(C.COPI_0000025)))
checks.append(("term function at a tertiary ⊑ its secondary and primary", C.COPI_0001021 in supers(T.DehydrationFunction) and C.COPI_0001013 in supers(T.DehydrationFunction)))
def _refused(path):
    try: _hc.resolve(path,_cov); return False
    except _hc.NotAdopted: return True
checks.append(("resolve() refuses an unadopted flow and an unknown term", _refused("Flow/Energy/Acoustic") and _refused("Function/NoSuchTerm")))
checks.append(("resolve() returns the class of an adopted flow", _hc.resolve("Flow/Material/Liquid",_cov)=="copi:COPI_0000038"))
# every controlled value of the signature names a class that exists (in copi-core-v2, copi-vocab or BFO)
_known={str(s) for s in g.subjects(RDF.type,OWL.Class)}
_exp=lambda c: str(C)+c.split(":",1)[1] if c.startswith("copi:") else "http://purl.obolibrary.org/obo/"+c.split(":",1)[1]
_gone=[p for p,i in {**_hc.flow_values(_cov),**_hc.measured_quantities(_cov)}.items() if _exp(i) not in _known]
checks.append((f"controlled values of the signature name existing classes ({len(_hc.flow_values(_cov))} flows, {len(_hc.measured_quantities(_cov))} measured quantities)" + (f" — {_gone[:5]}" if _gone else ""), not _gone))

# ---- sensors (review of 2026-11-17): the measured quantity is the quality that the measurement content describes
_sens=[("level element measures level", T.MeasuresLevel in supers(T.LevelSensingFunction)),
 ("level switch signals level status, does not measure it", T.SignalsLevelStatus in supers(T.LevelSwitchingFunction) and T.MeasuresLevel not in supers(T.LevelSwitchingFunction)),
 ("differential pressure element measures differential pressure, not level or pressure", T.MeasuresDifferentialPressure in supers(T.DifferentialPressureSensingFunction) and T.MeasuresLevel not in supers(T.DifferentialPressureSensingFunction) and T.MeasuresPressure not in supers(T.DifferentialPressureSensingFunction)),
 ("moisture element measures moisture, not level", T.MeasuresMoisture in supers(T.MoistureSensingFunction) and T.MeasuresLevel not in supers(T.MoistureSensingFunction)),
 ("the four sensor functions are satisfiable", all(OWL.Nothing not in supers(x) for x in (T.LevelSensingFunction,T.LevelSwitchingFunction,T.DifferentialPressureSensingFunction,T.MoistureSensingFunction))),
 ("LevelElement ⊑ measurement instrument", C.COPI_0000024 in supers(T.LevelElement)),
 ("LevelSwitch ⊑ instrument, not ⊑ measurement instrument", C.COPI_0000091 in supers(T.LevelSwitch) and C.COPI_0000024 not in supers(T.LevelSwitch))]
checks.extend(_sens)

# ---- transmitter under Processing (review of 2026-11-18)
_MI=C.COPI_0000024; _IN=C.COPI_0000091
checks.extend([
 ("signal transmission function ⊑ processing, not ⊑ sensing", C.COPI_0001037 in supers(C.COPI_0000030) and C.COPI_0001035 not in supers(C.COPI_0000030)),
 ("transmitter by the vocab function ⊑ measurement instrument", _MI in supers(T.VocabPressureTransmitter)),
 ("transmitter with no declared signal content ⊑ instrument, not ⊑ measurement instrument", _IN in supers(T.GenericTransmitter) and _MI not in supers(T.GenericTransmitter)),
 ("indicator with no signal outflow ⊑ instrument, not ⊑ measurement instrument", _IN in supers(T.PlainIndicator) and _MI not in supers(T.PlainIndicator)),
 ("indicator emitting measurement content ⊑ measurement instrument", _MI in supers(T.MeasurementIndicator)),
])

checks.append((f"annotation standard on {len(_subj)} entities" + (f" — gaps: {_gaps[:8]}" if _gaps else ""), not _gaps))

bad=0
for n,ok in checks:
    print(("PASS" if ok else "FAIL"), n); bad+= (not ok)
sys.exit(bad)
