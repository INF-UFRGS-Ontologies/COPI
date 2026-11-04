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
bad=0
for n,ok in checks:
    print(("PASS" if ok else "FAIL"), n); bad+= (not ok)
sys.exit(bad)
