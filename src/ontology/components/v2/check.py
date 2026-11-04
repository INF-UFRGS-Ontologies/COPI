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
checks.append((f"annotation standard on {len(_subj)} entities" + (f" — gaps: {_gaps[:8]}" if _gaps else ""), not _gaps))

bad=0
for n,ok in checks:
    print(("PASS" if ok else "FAIL"), n); bad+= (not ok)
sys.exit(bad)
