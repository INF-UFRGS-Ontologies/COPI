# Generates copi-core-v2.ttl from the spec "Spec copi-core v2" (rev. 2026-11-03c).
# Run: python3 -I gen.py > copi-core-v2.ttl
import textwrap

OUT = []
def w(s=""): OUT.append(s)

PREFIXES = """@prefix copi: <https://www.inf.ufrgs.br/ontologies/copi/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix iof-av: <https://spec.industrialontologies.org/ontology/annotation/> .
@prefix iof-constr: <https://spec.industrialontologies.org/ontology/construct/> .
@prefix obo: <http://purl.obolibrary.org/obo/> .
@prefix ro: <http://purl.obolibrary.org/obo/> .
@prefix meno: <https://raw.githubusercontent.com/stap-m/midlevel-energy-ontology/main/ontology/src/midlevel-energy.owl/> .
@prefix fb: <https://www.inf.ufrgs.br/ontologies/copi/fb/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
"""

# BFO / RO / IOF handles
PROCESS="obo:BFO_0000015"; QUALITY="obo:BFO_0000019"; MATENT="obo:BFO_0000040"; OBJECT="obo:BFO_0000030"
REALIZED_IN="obo:BFO_0000054"; REALIZES="obo:BFO_0000055"; HAS_PART_OCC="obo:BFO_0000117"
HAS_PARTICIPANT="obo:BFO_0000057"; BEARER_OF="obo:BFO_0000196"; INHERES_IN="obo:BFO_0000197"; CONCRETIZES="obo:BFO_0000059"
NEG_REG="ro:RO_0019002"; POS_REG="ro:RO_0019001"; CAUSALLY="ro:RO_0002410"
DF="iof-constr:DesignedFunction"; MA="iof-constr:MaterialArtifact"; ICE="iof-constr:InformationContentEntity"
DESC_ICE="iof-constr:DescriptiveInformationContentEntity"; DIR_ICE="iof-constr:DirectiveInformationContentEntity"
DESCRIBES="iof-constr:describes"; PRESCRIBES="iof-constr:prescribes"; ISABOUT="iof-constr:isAbout"
HASVALEXP="iof-constr:hasValueExpressionAtAllTimes"; MVE="iof-constr:MeasuredValueExpression"
# existing COPI
PORTION_FLUID="copi:COPI_0000037"; PORTION_LIQ="copi:COPI_0000038"; PORTION_GAS="copi:COPI_0000039"; PORTION_SOLID="copi:COPI_0000040"
CONTAINMENT_FN="copi:COPI_0000025"; FLOWCTRL_FN="copi:COPI_0000026"; INDICATION_FN="copi:COPI_0000028"; INSTR_FN="copi:COPI_0000029"
SIGTX_FN="copi:COPI_0000030"; RELIEF_FN="copi:COPI_0000032"; INSTRUMENT="copi:COPI_0000091"; MEAS_INSTR="copi:COPI_0000024"
PRESSURE_Q="copi:COPI_0000053"

ids = {}
_next = [1000]
def nid(key):
    ids[key] = f"copi:COPI_{_next[0]:07d}"; _next[0]+=1; return ids[key]

def esc(s): return s.replace('\\','\\\\').replace('"','\\"')

def cls(key, en, pt, supers=(), equiv=None, nld=None, sfd=None, note=None, adapted=None, primitive=True, source="ODR-024", close=None, related=None, extra=()):
    iri = ids.get(key) or nid(key)
    w(f"{iri} a owl:Class ;")
    w(f'    rdfs:label "{esc(en)}"@en , "{esc(pt)}"@pt-br ;')
    w(f'    dcterms:source "{source}" ;')
    w(f"    rdfs:isDefinedBy copi:copi-core ;")
    for s in supers: w(f"    rdfs:subClassOf {s} ;")
    if equiv: w(f"    owl:equivalentClass {equiv} ;")
    if nld: w(f'    iof-av:naturalLanguageDefinition "{esc(nld)}"@en ;')
    if sfd: w(f'    iof-av:semiFormalNaturalLanguageDefinition "{esc(sfd)}"@en ;')
    if note: w(f'    iof-av:explanatoryNote "{esc(note)}"@en ;')
    if adapted: w(f'    iof-av:adaptedFrom "{esc(adapted)}" ;')
    if close: w(f"    skos:closeMatch {close} ;")
    if related: w(f"    skos:relatedMatch {related} ;")
    for e in extra: w(f"    {e} ;")
    w(f"    iof-av:isPrimitive {'true' if primitive else 'false'} .")
    w()
    return iri

def restr(prop, kind, filler): return f"[ a owl:Restriction ; owl:onProperty {prop} ; owl:{kind} {filler} ]"
def inter(*xs): return "[ owl:intersectionOf ( " + " ".join(xs) + " ) ]"
def union(*xs): return "[ owl:unionOf ( " + " ".join(xs) + " ) ]"
SOME="someValuesFrom"; ONLY="allValuesFrom"

# ---------------------------------------------------------------- header
w(PREFIXES)
w("""copi:copi-core a owl:Ontology ;
    rdfs:label "COPI core (v2) — functions of the Functional Basis, three flows, identity and scope"@en ;
    dcterms:source "Spec copi-core v2 (rev. 2026-11-03c); ODR-024 (flow and function root), ODR-025 (identity and disjointness), ODR-026 (equipment × system)" ;
    rdfs:comment "Replaces the unit-operation anchoring of the FOMI 2026 paper (ODR-009/011/012) by function classes whose genus is a Functional Basis verb applied to a flow. No COPI process class carries identity; flows are occurrents; energy is a quality of its bearer; signal content is concretized by a signal flow or by a quality of its bearer."@en ;
    owl:versionInfo "2.0.0-draft-2026-11-03" .
""")

# ---------------------------------------------------------------- object properties kept from v1 (copied verbatim semantics)
w("""copi:COPI_0000002 a owl:ObjectProperty ;
    rdfs:label "functionally participates in"@en , "participa funcionalmente em"@pt-br ;
    rdfs:domain iof-constr:MaterialArtifact ;
    rdfs:range obo:BFO_0000015 ;
    dcterms:source "ODR-011 §4" ;
    rdfs:isDefinedBy copi:copi-core ;
    rdfs:subPropertyOf obo:BFO_0000056 ;
    owl:propertyChainAxiom ( iof-constr:hasFunction obo:BFO_0000054 ) ;
    iof-av:isPrimitive false .

copi:COPI_0000805 a owl:ObjectProperty ;
    rdfs:label "has functional participant"@en , "tem participante funcional"@pt-br ;
    rdfs:domain obo:BFO_0000015 ;
    rdfs:range iof-constr:MaterialArtifact ;
    dcterms:source "ODR-011 §4" ;
    rdfs:isDefinedBy copi:copi-core ;
    rdfs:subPropertyOf obo:BFO_0000057 ;
    owl:inverseOf copi:COPI_0000002 ;
    iof-av:isPrimitive false .
""")

# ---------------------------------------------------------------- flows (declared first: the root restriction uses them)
FLOW = nid("Flow"); MFLOW=nid("MaterialFlow"); EFLOW=nid("EnergyFlow"); SFLOW=nid("SignalFlow")
HAS_INFLOW=nid("hasInflow"); HAS_OUTFLOW=nid("hasOutflow"); HAS_INP=nid("hasInflowParticipant"); HAS_OUTP=nid("hasOutflowParticipant")
ENERGY=nid("Energy"); EDEC=nid("EnergyDecrease"); EINC=nid("EnergyIncrease")
SBEARER=nid("SignalBearer")

for p,en,pt,note in [
  (HAS_INFLOW,"has inflow","tem fluxo de entrada","flow, occurrent part of the process that realizes a function, that crosses an interface of the bearer inwards"),
  (HAS_OUTFLOW,"has outflow","tem fluxo de saída","flow, occurrent part of the process that realizes a function, that crosses an interface of the bearer outwards")]:
    w(f"""{p} a owl:ObjectProperty ;
    rdfs:label "{en}"@en , "{pt}"@pt-br ;
    rdfs:subPropertyOf {HAS_PART_OCC} ;
    rdfs:domain {PROCESS} ;
    rdfs:range {FLOW} ;
    dcterms:source "ODR-024" ;
    rdfs:isDefinedBy copi:copi-core ;
    iof-av:naturalLanguageDefinition "{note}"@en ;
    iof-av:isPrimitive true .
""")
for p,chain,en,pt,rel in [
  (HAS_INP,HAS_INFLOW,"has inflow participant","tem participante de fluxo de entrada","iof-constr:hasInput"),
  (HAS_OUTP,HAS_OUTFLOW,"has outflow participant","tem participante de fluxo de saída","iof-constr:hasOutput")]:
    w(f"""{p} a owl:ObjectProperty ;
    rdfs:label "{en}"@en , "{pt}"@pt-br ;
    owl:propertyChainAxiom ( {chain} {HAS_PARTICIPANT} ) ;
    dcterms:source "ODR-024" ;
    rdfs:isDefinedBy copi:copi-core ;
    skos:relatedMatch {rel} ;
    iof-av:explanatoryNote "Chain {chain} ∘ has participant. Declared as a COPI property because the chain into {rel} is not regular in OWL 2 DL given {rel} ⊑ has participant (IOF Core 202603); for the same reason this property is NOT declared a sub-property of has participant (that would close the cycle hasParticipant ≺ this ≺ hasParticipant, as HermiT reports). The export materializes {rel} and has participant from this property by SPARQL CONSTRUCT."@en ;
    iof-av:isPrimitive false .
""")

cls("Flow","flow","fluxo", supers=[PROCESS, restr(HAS_PARTICIPANT,SOME,MATENT)],
    nld="process in which some material entity crosses one interface of an artifact or engineered system, carrying with it some material, energy or information content",
    note="One flow per interface crossing. What happens inside the artifact (transformation, mixing, separation) is not a flow but another occurrent part of the process that realizes the function. The same flow may be an outflow of one artifact's process and an inflow of the next one's: it is the crossing of the interface they share. The Functional Basis leaves open whether a flow is the operand or its change over time; COPI takes the occurrent reading for the reasons recorded in ODR-024.",
    adapted="Functional Basis: operation on flows of material, energy and signal (Stone & Wood 2000; Hirtz et al. 2002); formalization in Borgo, Carrara, Garbacz & Vermaas (2011)", close="fb:Flow")
cls("MaterialFlow","material flow","fluxo de material", supers=[FLOW, restr(HAS_PARTICIPANT,SOME,union(PORTION_FLUID,PORTION_SOLID,OBJECT))],
    nld="flow whose participant is a portion of fluid, a portion of solid or an object: the material itself is what crosses the interface",
    note="A process stream (OntoCAPE Stream, ISO 15926 Stream, CFIHOS) is a material flow in steady state at a given interface.",
    close="iof-constr:MaterialLocationChangeProcess")
cls("EnergyFlow","energy flow","fluxo de energia", supers=[FLOW, restr(HAS_PART_OCC,SOME,EDEC), restr(HAS_PART_OCC,SOME,EINC)],
    nld="flow that is an energy transfer across the interface: a decrease of some energy quality in the bearer on one side causally related to an increase of an energy quality of the same kind in the bearer on the other side",
    note="Energy transformation (different kinds, same bearer) is not a flow; see energy transformation. No participant restriction 'bearer of some energy' is stated because every material entity satisfies it; what distinguishes an energy flow is its decrease/increase parts.",
    adapted="MENO (Stappel & Neuhaus, FOIS 2024): energy transfer", close="meno:MENO_01002")
cls("SignalFlow","signal flow","fluxo de sinal", supers=[FLOW, union(restr(CONCRETIZES,SOME,ICE), restr(HAS_PARTICIPANT,SOME,inter(SBEARER, restr(BEARER_OF,SOME,restr(CONCRETIZES,SOME,ICE)))))],
    nld="flow that concretizes an information content entity, directly (BFO 2020 admits a process as concretizer) or through a quality of its signal bearer, and transmits it between artifacts",
    note="The short form (the flow concretizes the content) answers whether a signal exists; the long form (a quality of the bearer concretizes it) answers through which bearer it passed.",
    adapted="IAO/CCO: content concretized in a bearer; BFO 2020 concretizes (BFO_0000059)")
w("# flows are not disjoint: a pressurized liquid stream is a material flow and an energy flow (carrier flow, Nagel et al. 2007)\n")

# ---------------------------------------------------------------- function root and the eight primaries
ROOT = cls("FlowOperatingFunction","flow-operating function","função sobre fluxo",
    supers=[DF, restr(REALIZED_IN,ONLY, inter(PROCESS, union(restr(HAS_INFLOW,SOME,FLOW), restr(HAS_OUTFLOW,SOME,FLOW))))],
    nld="designed function of an artifact or engineered system that consists in performing an operation on a flow of material, energy or signal that crosses the bearer's boundary",
    sfd="every instance of 'flow-operating function' is an instance of 'designed function' that is 'realized in' only processes that have as occurrent part some 'flow' crossing the bearer's boundary inwards or outwards",
    note="The Functional Basis (Hirtz et al. 2002) does not name this root: it judges a function term 'based on whether or not it describes an operation that a product or device carries out on a flow', and calls the eight primaries 'function classes'. iof:DesignedFunction is wider (it covers intended functions that operate on no flow, e.g. the identifying function of a tag plate); this class is where the Functional Basis assumption lives. The lineage is Pahl & Beitz's generally valid functions.",
    adapted="Hirtz, Stone, McAdams, Szykman & Wood (2002), Research in Engineering Design 13(2); Stone & Wood (2000), J. Mech. Des. 122(4); Borgo, Carrara, Garbacz & Vermaas (2011), JCISE 11(3)", close="fb:Function")

PRIM = {}
prim_defs = [
 ("Branching","branching function","função de ramificação","Branch","function to cause a flow to no longer be joined or mixed, or to be distributed", ["Separating","Distributing"]),
 ("Channelling","channelling function","função de canalização","Channel","function to cause a flow to move from one location to another", ["Importing","Exporting","Transferring","Guiding"]),
 ("Connecting","connecting function","função de conexão","Connect","function to bring two or more flows together", ["Coupling","Mixing"]),
 ("MagnitudeControl","magnitude control function","função de controle de magnitude","Control magnitude","function to alter or govern the size or amplitude of a flow", ["Actuating","Regulating","Changing","Stopping"]),
 ("Conversion","conversion function","função de conversão","Convert","function to change a flow from one form to another", []),
 ("Provision","provision function","função de provisão","Provision","function to accumulate or provide a flow", ["Storing","Supplying"]),
 ("Signalling","signalling function","função de sinalização","Signal","function to provide information on a flow: to sense, indicate or process a signal", ["Sensing","Indicating","Processing"]),
 ("Support","support function","função de suporte","Support","function to firmly fix a flow (an object) into a defined location, or secure or position it", ["Stabilizing","Securing","Positioning"]),
]
sec_nld = {
 "Separating":("separating function","função de separação","Separate","function to isolate a flow into distinct components; tertiary: divide, extract, remove"),
 "Distributing":("distributing function","função de distribuição","Distribute","function to cause a flow to break up and spread over an area"),
 "Importing":("importing function","função de importação","Import","function to bring a flow in from outside the system boundary"),
 "Exporting":("exporting function","função de exportação","Export","function to send a flow out across the system boundary"),
 "Transferring":("transferring function","função de transferência","Transfer","function to shift or convey a flow from one place to another; tertiary: transport, transmit"),
 "Guiding":("guiding function","função de guia","Guide","function to direct the course of a flow along a specific path; tertiary: translate, rotate, allow degree of freedom"),
 "Coupling":("coupling function","função de acoplamento","Couple","function to join or bring together flows; tertiary: join, link"),
 "Mixing":("mixing function","função de mistura","Mix","function to combine two flows into a single, uniform homogeneous mass"),
 "Actuating":("actuating function","função de atuação","Actuate","function to commence the flow of energy, signal or material in response to an imported control signal"),
 "Regulating":("regulating function","função de regulação","Regulate","function to adjust a flow in response to a control signal; tertiary: increase, decrease"),
 "Changing":("changing function","função de mudança","Change","function to adjust a flow in a predetermined and fixed manner; tertiary: increment, decrement, shape, condition"),
 "Stopping":("stopping function","função de interrupção","Stop","function to cease, or prevent, the transfer of a flow; tertiary: prevent, inhibit"),
 "Storing":("storing function","função de armazenamento","Store","function to accumulate a flow; tertiary: contain, collect"),
 "Supplying":("supplying function","função de suprimento","Supply","function to provide a flow from storage"),
 "Sensing":("sensing function","função de sensoriamento","Sense","function to perceive, or become aware of, a flow; tertiary: detect, measure"),
 "Indicating":("indicating function","função de indicação","Indicate","function to make something known to the user about a flow; tertiary: track, display"),
 "Processing":("processing function","função de processamento de sinal","Process","function to submit a signal to a particular treatment or method having a set number of operations or steps"),
 "Stabilizing":("stabilizing function","função de estabilização","Stabilize","function to prevent an object from changing course or location"),
 "Securing":("securing function","função de fixação","Secure","function to firmly fix an object to a location"),
 "Positioning":("positioning function","função de posicionamento","Position","function to place an object into a specific location or orientation"),
}
for key,en,pt,fb,nld,secs in prim_defs:
    PRIM[key] = cls(key+"Function", en, pt, supers=[ROOT], nld=nld,
        note=f"Primary class '{fb}' of the Functional Basis. Disjoint from the other seven primaries; its secondaries are aspects, not alternatives, and are not declared disjoint.",
        adapted=f"Hirtz et al. (2002), Appendix B, class '{fb}'", close=f"fb:{fb.replace(' ','')}")
for key,en,pt,fb,nld,secs in prim_defs:
    for sk in secs:
        sen,spt,sfb,snld = sec_nld[sk]
        cls(sk+"Function", sen, spt, supers=[PRIM[key]], nld=snld, adapted=f"Hirtz et al. (2002), Appendix B, secondary '{sfb}' under '{fb}'", close=f"fb:{sfb.replace(' ','')}",
            note="Tertiary terms of the Functional Basis are kept in the SKOS scheme fb: (skos:narrower), not as classes.")
w("[] a owl:AllDisjointClasses ;\n    owl:members ( " + " ".join(PRIM[k] for k,*_ in prim_defs) + " ) .\n")

# ConversionFunction: internal transformation
TRANSF = nid("Transformation")
w(f"{PRIM['Conversion']} rdfs:subClassOf {restr(REALIZED_IN,ONLY, inter(PROCESS, restr(HAS_PART_OCC,SOME,TRANSF)))} .\n")

# ---------------------------------------------------------------- energy
cls("Energy","energy","energia", supers=[QUALITY, restr(INHERES_IN,SOME,MATENT)],
    nld="quality of a material entity whose magnitude can decrease in its bearer as a causally related quality of the same kind increases in another bearer (transfer), or as a quality of a different kind increases in the same bearer (transformation)",
    note="As a specifically dependent continuant, an energy quality never migrates between bearers; 'transfer' is the pair decrease-here/increase-there (MENO). Kinds follow the Functional Basis flow taxonomy used in the COPI coverage; MENO is aligned, not imported (its IRIs are raw GitHub URLs, it imports BFO 2.0, and it lacks mechanical, hydraulic and pneumatic energy).",
    adapted="MENO (Stappel & Neuhaus, FOIS 2024): energy ⊑ bfo:quality, quality of some material entity; OEO (Stappel et al., JOWO 2022)", close="meno:MENO_01001")
for key,en,pt,note,close,related in [
 ("MechanicalEnergy","mechanical energy","energia mecânica","kinetic plus potential energy of a body or shaft; broader than MENO kinetic energy",None,"meno:MENO_01007"),
 ("HydraulicEnergy","hydraulic energy","energia hidráulica","Functional Basis carrier-based kind: pressure-volume energy of a liquid; an engineering distinction by bearer, not a physical kind. No MENO counterpart.",None,None),
 ("PneumaticEnergy","pneumatic energy","energia pneumática","as hydraulic energy, for a gas",None,None),
 ("ThermalEnergy","thermal energy","energia térmica",None,"meno:MENO_01011",None),
 ("ElectricalEnergy","electrical energy","energia elétrica",None,"meno:MENO_01006",None),
 ("ChemicalEnergy","chemical energy","energia química",None,"meno:MENO_01005",None),
 ("ElectromagneticEnergy","electromagnetic energy","energia eletromagnética","radiative energy in MENO",None,"meno:MENO_01009")]:
    cls(key,en,pt,supers=[ENERGY], nld=f"{en} as a kind of energy quality of its bearer, in the sense of the Functional Basis flow taxonomy", note=note, close=close, related=related, adapted="Hirtz et al. (2002), Table 3 (energy flows)")
cls("EnergyDecrease","energy decrease","decréscimo de energia", supers=[PROCESS, restr(NEG_REG,SOME,ENERGY)],
    nld="process that negatively regulates an energy quality of its bearer", adapted="MENO: energy decrease (quality decrease)", close="meno:MENO_01013")
cls("EnergyIncrease","energy increase","acréscimo de energia", supers=[PROCESS, restr(POS_REG,SOME,ENERGY)],
    nld="process that positively regulates an energy quality of its bearer", adapted="MENO: energy increase (quality increase)", close="meno:MENO_01014")
cls("Transformation","transformation","transformação", supers=[PROCESS],
    nld="process, occurrent part of the realization of a conversion function, in which the form of the operand changes inside the artifact: the kind of energy borne, the phase, or the chemical composition",
    note="Does not cross an interface; therefore not a flow. It is the formal mark of ConversionFunction, which is otherwise indistinguishable from channelling/transferring.")
cls("EnergyTransformation","energy transformation","transformação de energia", supers=[TRANSF, restr(HAS_PART_OCC,SOME,EDEC), restr(HAS_PART_OCC,SOME,EINC)],
    nld="transformation in which an energy quality of one kind decreases and, causally related, an energy quality of a different kind increases in the same bearer",
    adapted="MENO: energy transformation", close="meno:MENO_01003")
cls("MaterialTransformation","material transformation","transformação de material", supers=[TRANSF],
    nld="transformation in which the phase or the chemical composition of the material operand changes inside the artifact")

# ---------------------------------------------------------------- signal
cls("SignalBearer","signal bearer","portador de sinal", supers=[MATENT],
    nld="material entity (a current loop, a cable, a pneumatic line, a network segment) some quality of which, or some signal flow through which, concretizes an information content entity transmitted between artifacts",
    note="IOF Core 202603 has no information-bearer class; this is COPI's. The bearer answers 'through which cable'; the content answers 'about what'.",
    adapted="IAO material information bearer; CCO information bearing entity")
cls("MeasurementContent","measurement content","conteúdo de medição", supers=[DESC_ICE, restr(DESCRIBES,SOME,QUALITY), restr(HASVALEXP,SOME,MVE)],
    nld="descriptive information content entity, produced by continuous sensing, that describes a quality of the observed entity and has a measured value expression",
    note="Sibling, not equivalent, of iof:MeasurementInformationContentEntity: the IOF class requires being the output of some (planned) MeasurementProcess, which continuous sensing is not. Same describes / value-expression pattern.",
    close="iof-constr:MeasurementInformationContentEntity")
cls("ControlContent","control content","conteúdo de controle", supers=[DIR_ICE, restr(PRESCRIBES,SOME,QUALITY)],
    nld="directive information content entity that prescribes a quality of the actuated artifact (a valve opening, a pump speed)",
    note="Interlock and trip contents are control contents.")
cls("StatusContent","status content","conteúdo de estado", supers=[DESC_ICE, restr(DESCRIBES,SOME,QUALITY)],
    nld="descriptive information content entity whose content is discrete: that a quality has crossed a limit (high level, flame detected) or the condition of an artifact (pump running)",
    note="Alarms are status contents with reference to a limit. Switches and detectors produce status content.")

# ---------------------------------------------------------------- genus-level functions (COPI refinements of FB classes) and the nine device genera
GEN = {}
genus_fns = [
 ("FluidMachineFunction","fluid machine function","função de máquina de fluxo",PRIM["Conversion"],
  "conversion function realized in a process with an inflow of mechanical energy, an internal energy transformation, and an outflow that is both a material flow and an energy flow of hydraulic or pneumatic energy (a carrier flow)",
  [restr(REALIZED_IN,ONLY, inter(PROCESS, restr(HAS_OUTFLOW,SOME,inter(MFLOW,EFLOW))))]),
 ("HeatTransferFunction","heat transfer function","função de transferência de calor","Transferring",
  "transferring function realized in a process with two material inflows and two material outflows, one pair carrying a thermal energy decrease and the other a thermal energy increase, and no transformation", []),
 ("MassTransferFunction","mass transfer function","função de transferência de massa","Separating",
  "separating function that isolates a component of a fluid mixture by transferring it to another phase (extract)", []),
 ("MechanicalSeparationFunction","mechanical separation function","função de separação mecânica","Separating",
  "separating function that isolates phases or particles of a mixture by mechanical means", []),
 ("ChemicalReactionFunction","chemical reaction function","função de reação química",PRIM["Conversion"],
  "conversion function whose internal transformation changes the chemical composition of the material operand", []),
 ("PhaseChangeFunction","phase change function","função de mudança de fase",PRIM["Conversion"],
  "conversion function whose internal transformation changes the phase of the material operand", []),
]
for key,en,pt,parent,nld,extra_supers in genus_fns:
    p = parent if parent.startswith("copi:") else ids[parent+"Function"]
    GEN[key]=cls(key,en,pt,supers=[p]+extra_supers, nld=nld, note="Genus-level function of COPI: the parent of the term functions (e.g. pumping function) of one artifact genus. Refines a Functional Basis class; not itself in the Functional Basis.", source="ODR-025")

# re-parenting of existing vocab functions (asserted here; copi-vocab keeps their declarations)
w(f"{CONTAINMENT_FN} rdfs:subClassOf {ids['StoringFunction']} .    # containment function ⊑ storing (contain)")
w(f"{FLOWCTRL_FN} rdfs:subClassOf {ids['RegulatingFunction']} .    # flow control function ⊑ regulating")
w(f"{INDICATION_FN} rdfs:subClassOf {ids['IndicatingFunction']} .  # indication function ⊑ indicating")
w(f"{INSTR_FN} rdfs:subClassOf {ids['SensingFunction']} .          # instrumentation function ⊑ sensing (ODR-023, reading A; its allValuesFrom MeasurementProcess is removed in copi-vocab)")
w(f"# {SIGTX_FN} (signal transmission function) stays under instrumentation/sensing function in copi-vocab: a transmitter senses and emits; re-parenting it under transferring (Channel) would cross two disjoint primaries (HermiT, 3/11)")
w(f"{RELIEF_FN} rdfs:subClassOf {ids['RegulatingFunction']} .      # safety relief function ⊑ regulating (decrease)")
# the vocab realization processes of the transmitter functions (COPI_0000035/36, now ⊑ bfo:Process) get their
# signal outflow here, so that 'pressure transmission function' (COPI_0000031) reaches MeasurementInstrument
# through the vocab IRIs the iri-map aliases the enriched terms to (finding of 4/11: the export's own process
# with the signal flow got a fresh IRI nobody references)
w(f"copi:COPI_0000035 rdfs:subClassOf {restr(HAS_OUTFLOW,SOME,SFLOW)} .   # signal transmission process: emits a signal flow")
w(f"copi:COPI_0000036 rdfs:subClassOf copi:COPI_0000035 , {restr(HAS_OUTFLOW,SOME, inter(SFLOW, restr(CONCRETIZES,SOME,ids['MeasurementContent'])))} .   # pressure measurement and transmission process: the signal carries measurement content")
w()

devices = [
 ("copi:COPI_0000016","momentum-transfer device","dispositivo de transferência de quantidade de movimento",GEN["FluidMachineFunction"],"Pumps, compressors, fans, turbines: the fluid-machine genus."),
 ("copi:COPI_0000017","heat-transfer device","dispositivo de transferência de calor",GEN["HeatTransferFunction"],None),
 ("copi:COPI_0000018","mass-transfer device","dispositivo de transferência de massa",GEN["MassTransferFunction"],None),
 ("copi:COPI_0000019","mechanical-separation device","dispositivo de separação mecânica",GEN["MechanicalSeparationFunction"],None),
 ("copi:COPI_0000020","chemical reactor","reator químico",GEN["ChemicalReactionFunction"],None),
 ("copi:COPI_0000021","phase-change device","dispositivo de mudança de fase",GEN["PhaseChangeFunction"],None),
 ("copi:COPI_0000022","containment device","dispositivo de contenção",CONTAINMENT_FN,None),
 ("copi:COPI_0000023","flow-control device","dispositivo de controle de fluxo",FLOWCTRL_FN,None),
]
for iri,en,pt,fn,note in devices:
    ids[iri]=iri
    cls(iri,en,pt,supers=[MA], equiv=inter(MA, restr(BEARER_OF,SOME,fn)), primitive=False, source="ODR-025",
        nld=f"material artifact that bears a {en.replace(' device','').replace('-',' ')} function",
        note=(note or "")+" Defined class: redefinition of the FOMI 2026 category over its genus-level function instead of its operation; keeps its IRI. Partitions (AllDisjointClasses) among its species are declared where the qualifier is exclusive (e.g. pump × compressor).")
ids[INSTRUMENT]=INSTRUMENT
cls(INSTRUMENT,"instrument","instrumento", supers=[MA], equiv=inter(MA, restr(BEARER_OF,SOME,PRIM["Signalling"])), primitive=False, source="ODR-023 (reading A)",
    nld="material artifact that bears a signalling function: sensing, indicating or processing a signal",
    note="ISA 5.1: instruments include primary elements, indicators, controllers, final control elements and switches. Measurement instruments are the sensing subset.")
ids[MEAS_INSTR]=MEAS_INSTR
cls(MEAS_INSTR,"measurement instrument","instrumento de medição", supers=[INSTRUMENT],
    equiv=inter(MA, restr(BEARER_OF,SOME, inter(ids['SensingFunction'], restr(REALIZED_IN,SOME, restr(HAS_OUTFLOW,SOME, inter(SFLOW, restr(CONCRETIZES,SOME,ids['MeasurementContent']))))))),
    primitive=False, source="ODR-023 (reading A)",
    nld="instrument that bears a sensing function realized in a process whose outflow is a signal flow concretizing measurement content",
    note="MeasurementInstrument ⊑ Instrument is now inferred in the direction ISA 5.1 and ISO 15926 read it. Its realization is a bfo:Process, not iof:MeasurementProcess (planned): continuous sensing is not a planned measurement.")

# ---------------------------------------------------------------- operations as defined classes (keep FOMI IRIs; drop Operation 0000001)
ops = [
 ("copi:COPI_0000003","momentum transfer","transferência de quantidade de movimento",GEN["FluidMachineFunction"]),
 ("copi:COPI_0000004","heat transfer","transferência de calor",GEN["HeatTransferFunction"]),
 ("copi:COPI_0000005","mass transfer","transferência de massa",GEN["MassTransferFunction"]),
 ("copi:COPI_0000006","mechanical separation","separação mecânica",GEN["MechanicalSeparationFunction"]),
 ("copi:COPI_0000007","chemical reaction","reação química",GEN["ChemicalReactionFunction"]),
 ("copi:COPI_0000008","phase change","mudança de fase",GEN["PhaseChangeFunction"]),
 ("copi:COPI_0000009","material containment","contenção de material",CONTAINMENT_FN),
 ("copi:COPI_0000010","flow control","controle de fluxo",FLOWCTRL_FN),
]
for iri,en,pt,fn in ops:
    ids[iri]=iri
    cls(iri,en,pt,supers=[PROCESS], equiv=inter(PROCESS, restr(REALIZES,SOME,fn)), primitive=False, source="ODR-024",
        nld=f"process that realizes a {en} function",
        note="Defined class over the genus-level function. Carries no identity (ODR-011 superseded); copi:Operation ⊑ PlannedProcess (COPI_0000001) is removed; planned-ness is orthogonal (ODR-009).")
for key,en,pt in [("Branching","branching operation","operação de ramificação"),("Channelling","channelling operation","operação de canalização"),("Connecting","connecting operation","operação de conexão"),("MagnitudeControl","magnitude control operation","operação de controle de magnitude"),("Conversion","conversion operation","operação de conversão"),("Provision","provision operation","operação de provisão"),("Signalling","signalling operation","operação de sinalização"),("Support","support operation","operação de suporte")]:
    cls(key+"Operation",en,pt,supers=[PROCESS], equiv=inter(PROCESS, restr(REALIZES,SOME,PRIM[key])), primitive=False, nld=f"process that realizes some {ids[key+'Function']} ({en.replace(' operation','')} function)", note="Defined class by primary verb, for the core CQs (CQ24) and the MENO pattern.")
# leaves kept as subclasses (their term-function definitions come from the enriched export)
for iri,en,pt,parent in [("copi:COPI_0000011","liquid pressure increase","aumento de pressão de líquido","copi:COPI_0000003"),("copi:COPI_0000012","gas pressure increase","aumento de pressão de gás","copi:COPI_0000003"),("copi:COPI_0000013","gas absorption","absorção de gás","copi:COPI_0000005"),("copi:COPI_0000014","vaporization","vaporização","copi:COPI_0000008"),("copi:COPI_0000089","heat exchange","troca térmica","copi:COPI_0000004")]:
    ids[iri]=iri
    cls(iri,en,pt,supers=[parent], nld=f"{en}: operation leaf kept from v1; its equivalence to 'process that realizes some <term function>' is emitted by the export", source="ODR-011 (leaf kept)")
w("copi:COPI_0000011 owl:disjointWith copi:COPI_0000012 .   # liquid × gas pressure increase: exclusive qualifier\n")
ids["copi:COPI_0000015"]="copi:COPI_0000015"
cls("copi:COPI_0000015","loss of containment","perda de contenção", supers=[PROCESS], nld="process in which contained material leaves its containment device other than through an outflow of its storing function", source="ODR-009 §3")

# ---------------------------------------------------------------- SKOS scheme for tertiaries
w("""fb:scheme a skos:ConceptScheme ; rdfs:label "Functional Basis terms (Hirtz et al. 2002)"@en .""")
terts = {"Separate":["Divide","Extract","Remove"],"Transfer":["Transport","Transmit"],"Guide":["Translate","Rotate","AllowDOF"],"Couple":["Join","Link"],"Regulate":["Increase","Decrease"],"Change":["Increment","Decrement","Shape","Condition"],"Stop":["Prevent","Inhibit"],"Store":["Contain","Collect"],"Sense":["Detect","Measure"],"Indicate":["Track","Display"]}
for sec,ts in terts.items():
    for t in ts:
        w(f'fb:{t} a skos:Concept ; skos:inScheme fb:scheme ; skos:prefLabel "{t}"@en ; skos:broader fb:{sec} .')
w()

# ---------------------------------------------------------------- annotation properties used by the export
for key,en,nld in [("signature","signature","JSON signature of a term function: verb, secondary, tertiary, inflows, outflows, primary flow, interface"),
                   ("primaryFunction","primary function","IRI of the function that gives the artifact its box (curation convention; design context)"),
                   ("identityFunction","identity function","IRI of the term function whose signature individuates the artifact type"),
                   ("constructiveType","constructive type","constructive differentia of the term (gate, ball, shell-and-tube), kept as annotation, never as functional subclass")]:
    w(f'{nid(key)} a owl:AnnotationProperty ; rdfs:label "{en}"@en ; iof-av:naturalLanguageDefinition "{nld}"@en ; dcterms:source "ODR-025" .')
w()

print("\n".join(OUT))
import sys
sys.stderr.write("ids: " + ", ".join(f"{k}={v}" for k,v in ids.items() if k not in v) + "\n")
