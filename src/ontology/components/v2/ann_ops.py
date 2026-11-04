# Annotations: device genera, instruments, operations (defined classes), leaves, annotation properties, header.
from ann_refs import *
from ann_functions import ANN, A
import ann_flows  # noqa: F401 (registers its entries)

# ---------------------------------------------------------------- device genera (FOMI categories redefined, ODR-025 §4)
_DEV = {
 "copi:COPI_0000016": ("momentum-transfer device","FluidMachineFunction","fluid machine function","função de máquina de fluxo",
   "A centrifugal pump; a reciprocating compressor; a gas turbine; a fan.",
   "Uma bomba centrífuga; um compressor alternativo; uma turbina a gás; um ventilador.",
   "Bombas, compressores, ventiladores, turbinas: o gênero das máquinas de fluxo. A partição bomba × compressor (AllDisjointClasses) pende aqui."),
 "copi:COPI_0000017": ("heat-transfer device","HeatTransferFunction","heat transfer function","função de transferência de calor",
   "A shell-and-tube heat exchanger; a plate heat exchanger; an air cooler.",
   "Um trocador de calor casco-e-tubo; um trocador de placas; um resfriador a ar.",
   "Todo tipo de trocador de calor é instância deste gênero por portar a função de gênero diretamente (tipos construtivos)."),
 "copi:COPI_0000018": ("mass-transfer device","MassTransferFunction","mass transfer function","função de transferência de massa",
   "An absorber; a stripper; a distillation column.",
   "Um absorvedor; um esgotador; uma coluna de destilação.", ""),
 "copi:COPI_0000019": ("mechanical-separation device","MechanicalSeparationFunction","mechanical separation function","função de separação mecânica",
   "A three-phase separator; a hydrocyclone; a filter.",
   "Um separador trifásico; um hidrociclone; um filtro.", ""),
 "copi:COPI_0000020": ("chemical reactor","ChemicalReactionFunction","chemical reaction function","função de reação química",
   "A fixed-bed reactor; a hydrotreater; a Claus reactor.",
   "Um reator de leito fixo; uma unidade de hidrotratamento; um reator Claus.", ""),
 "copi:COPI_0000021": ("phase-change device","PhaseChangeFunction","phase change function","função de mudança de fase",
   "A reboiler; a condenser; a flash drum.",
   "Um refervedor; um condensador; um vaso de flash.", ""),
 "copi:COPI_0000022": ("containment device","ContainmentFunction","containment function","função de contenção",
   "A storage tank; a pressure vessel; a drain sump.",
   "Um tanque de armazenamento; um vaso de pressão; um sumidouro de drenagem.",
   "A função de contenção (copi-vocab COPI_0000025) é reparentada sob armazenar/conter (Provision)."),
 "copi:COPI_0000023": ("flow-control device","FlowControlFunction","flow control function","função de controle de fluxo",
   "A control valve (regulate); a gate valve in isolation service (stop); a relief valve.",
   "Uma válvula de controle (regular); uma válvula gaveta em serviço de bloqueio (interromper); uma válvula de alívio.",
   "A função de controle de fluxo (copi-vocab COPI_0000026) é reparentada sob controle de magnitude: cobre regular e interromper."),
}
_DEV_PT = {"momentum-transfer device":"dispositivo de transferência de quantidade de movimento","heat-transfer device":"dispositivo de transferência de calor","mass-transfer device":"dispositivo de transferência de massa","mechanical-separation device":"dispositivo de separação mecânica","chemical reactor":"reator químico","phase-change device":"dispositivo de mudança de fase","containment device":"dispositivo de contenção","flow-control device":"dispositivo de controle de fluxo"}
for iri,(en,fnkey,fn_en,fn_pt,ex_en,ex_pt,note_extra) in _DEV.items():
    A(iri, nld_pt=f"artefato material que porta uma {fn_pt}",
      sfd_en=f"x is a '{en}' if and only if x is a 'material artifact' that is 'bearer of' some '{fn_en}'",
      sfd_pt=f"x é um '{_DEV_PT[en]}' se e somente se x é um 'artefato material' que é 'portador de' alguma '{fn_pt}'",
      fol=f"∀x ({fnkey.replace('Function','')}Device(x) ↔ MaterialArtifact(x) ∧ ∃f ({fnkey}(f) ∧ bearerOf(x,f)))",
      ex_en=ex_en, ex_pt=ex_pt,
      note_pt="Classe definida: redefinição da categoria do FOMI 2026 (ODR-011/012) sobre sua função de gênero em vez da sua operação; mantém o IRI. As partições (AllDisjointClasses) entre suas espécies são declaradas onde o qualificador é exclusivo. " + note_extra,
      sources=["ODR-025 §4", "ODR-012 (superseded: categories by operation)", "ODR-011 (superseded)", MCCABE], adapted=MCCABE + " (unit-operation categories of the FOMI 2026 paper, now by function)")
A("copi:COPI_0000091",
  nld_pt="artefato material que porta uma função de sinalização: sentir, indicar ou processar um sinal",
  sfd_en="x is an 'instrument' if and only if x is a 'material artifact' that is 'bearer of' some 'signalling function'",
  sfd_pt="x é um 'instrumento' se e somente se x é um 'artefato material' que é 'portador de' alguma 'função de sinalização'",
  fol="∀x (Instrument(x) ↔ MaterialArtifact(x) ∧ ∃f (SignallingFunction(f) ∧ bearerOf(x,f)))",
  ex_en="A pressure transmitter; a level gauge; a controller; a limit switch; a control valve positioner.",
  ex_pt="Um transmissor de pressão; um indicador de nível; um controlador; uma chave fim de curso; um posicionador de válvula de controle.",
  note_pt="ISA 5.1: instrumentos incluem elementos primários, indicadores, controladores, elementos finais de controle e chaves. Instrumentos de medição são o subconjunto que sente e emite conteúdo de medição. Fecha o ODR-023 pela leitura A: instrumento ⊒ instrumento de medição, como a ISA 5.1 e a ISO 15926 leem.",
  sources=["ODR-023 (reading A)", "ODR-025 §5", ISA51, ISO15926], adapted=ISA51 + ": instrument")
A("copi:COPI_0000024",
  nld_pt="instrumento que porta uma função de sensoriamento realizada num processo cujo fluxo de saída é um fluxo de sinal que concretiza conteúdo de medição",
  sfd_en="x is a 'measurement instrument' if and only if x is a 'material artifact' that is 'bearer of' some 'sensing function' that is 'realized in' some process that 'has outflow' some 'signal flow' that 'concretizes' some 'measurement content'",
  sfd_pt="x é um 'instrumento de medição' se e somente se x é um 'artefato material' que é 'portador de' alguma 'função de sensoriamento' que é 'realizada em' algum processo que 'tem fluxo de saída' algum 'fluxo de sinal' que 'concretiza' algum 'conteúdo de medição'",
  fol="∀x (MeasurementInstrument(x) ↔ MaterialArtifact(x) ∧ ∃f (SensingFunction(f) ∧ bearerOf(x,f) ∧ ∃p (realizedIn(f,p) ∧ ∃s (SignalFlow(s) ∧ hasOutflow(p,s) ∧ ∃c (MeasurementContent(c) ∧ concretizes(s,c))))))",
  ex_en="A pressure transmitter; a temperature element with its transmitter; a Coriolis flow meter.",
  ex_pt="Um transmissor de pressão; um elemento de temperatura com seu transmissor; um medidor de vazão Coriolis.",
  note_pt="'Instrumento de medição ⊑ instrumento' passa a ser inferido no sentido em que a ISA 5.1 e a ISO 15926 leem. Sua realização é um bfo:Process, não iof:MeasurementProcess (planejado): sensoriamento contínuo não é medição planejada (ODR-009 §4 superseded). Um controlador (processar), uma chave (sentir com conteúdo de estado) e um elemento final (regular com entrada de controle) são instrumentos sem ser de medição. O guard check_tsensor_subclass_mesinstr.sparql continua válido.",
  sources=["ODR-023 (reading A)", "ODR-025 §5", "ODR-009 §4 (superseded)", ISA51, IOF + ": MeasurementProcess (planned)"], adapted=ISA51 + ": measuring instrument; " + ISO15926)

# ---------------------------------------------------------------- operations (defined classes over functions)
_OPS = {
 "copi:COPI_0000003": ("momentum transfer","transferência de quantidade de movimento","FluidMachineFunction","fluid machine function","função de máquina de fluxo",
   "The pumping of a liquid; the compression of a gas; the expansion of a gas through a turbine.",
   "O bombeamento de um líquido; a compressão de um gás; a expansão de um gás numa turbina."),
 "copi:COPI_0000004": ("heat transfer","transferência de calor","HeatTransferFunction","heat transfer function","função de transferência de calor",
   "Cooling a product stream against seawater; preheating crude against a hot product; condensing overheads against cooling water.",
   "Resfriar uma corrente de produto contra água do mar; pré-aquecer óleo cru contra um produto quente; condensar o topo contra água de resfriamento."),
 "copi:COPI_0000005": ("mass transfer","transferência de massa","MassTransferFunction","mass transfer function","função de transferência de massa",
   "Absorbing CO2 into amine; stripping H2S; dehydrating gas with glycol.",
   "Absorver CO2 em amina; esgotar H2S; desidratar gás com glicol."),
 "copi:COPI_0000006": ("mechanical separation","separação mecânica","MechanicalSeparationFunction","mechanical separation function","função de separação mecânica",
   "Separating oil, gas and water by gravity; removing sand in a hydrocyclone; filtering solids from a liquid.",
   "Separar óleo, gás e água por gravidade; remover areia num hidrociclone; filtrar sólidos de um líquido."),
 "copi:COPI_0000007": ("chemical reaction","reação química","ChemicalReactionFunction","chemical reaction function","função de reação química",
   "Hydrodesulphurization; the Claus reaction; combustion in a burner.",
   "Hidrodessulfurização; a reação de Claus; combustão num queimador."),
 "copi:COPI_0000008": ("phase change","mudança de fase","PhaseChangeFunction","phase change function","função de mudança de fase",
   "Vaporizing the bottoms of a column in a reboiler; condensing overheads; flashing a liquid at reduced pressure.",
   "Vaporizar o fundo de uma coluna num refervedor; condensar o topo; expandir um líquido em flash a pressão reduzida."),
 "copi:COPI_0000009": ("material containment","contenção de material","ContainmentFunction","containment function","função de contenção",
   "Holding crude in a storage tank; holding gas in a surge vessel; collecting drains in a sump.",
   "Manter óleo cru num tanque de armazenamento; manter gás num vaso pulmão; coletar drenos num sumidouro."),
 "copi:COPI_0000010": ("flow control","controle de fluxo","FlowControlFunction","flow control function","função de controle de fluxo",
   "Throttling a flow with a control valve; isolating a line with a gate valve; relieving overpressure through a relief valve.",
   "Estrangular um fluxo com uma válvula de controle; bloquear uma linha com uma válvula gaveta; aliviar sobrepressão por uma válvula de alívio."),
}
for iri,(en,pt,fnkey,fn_en,fn_pt,ex_en,ex_pt) in _OPS.items():
    A(iri, nld_pt=f"processo que realiza uma {fn_pt}",
      sfd_en=f"p is a '{en}' if and only if p is a 'process' that 'realizes' some '{fn_en}'",
      sfd_pt=f"p é uma '{pt}' se e somente se p é um 'processo' que 'realiza' alguma '{fn_pt}'",
      fol=f"∀p ({''.join(w.capitalize() for w in en.split())}(p) ↔ Process(p) ∧ ∃f ({fnkey}(f) ∧ realizes(p,f)))",
      ex_en=ex_en, ex_pt=ex_pt,
      note_pt="Classe definida sobre a função de gênero. Não carrega identidade (ODR-011 superseded); copi:Operation ⊑ PlannedProcess (COPI_0000001) é removida; o caráter planejado é ortogonal (ODR-009 §2). Mantém rótulo, definição e adaptedFrom do FOMI 2026 (McCabe-Smith-Harriott) como classe de consulta.",
      sources=["ODR-024 §3", "ODR-009 §2", "ODR-011 (superseded)", MCCABE], adapted=MCCABE)
_OPSV = {"Branching":("branching operation","operação de ramificação","Separating a mixture into phases; distributing a flow through a manifold."," Separar uma mistura em fases; distribuir um fluxo por um manifold."),
 "Channelling":("channelling operation","operação de canalização","Conveying crude through a pipeline; transmitting shaft power; guiding a flow through an elbow."," Transportar óleo cru por um oleoduto; transmitir potência de eixo; guiar um fluxo por uma curva."),
 "Connecting":("connecting operation","operação de conexão","Mixing two streams; coupling two shafts; joining two pipe ends."," Misturar duas correntes; acoplar dois eixos; unir duas pontas de tubo."),
 "MagnitudeControl":("magnitude control operation","operação de controle de magnitude","Throttling a flow; isolating a line; reducing a pressure through an orifice."," Estrangular um fluxo; bloquear uma linha; reduzir uma pressão por um orifício."),
 "Conversion":("conversion operation","operação de conversão","Pumping; compressing; generating electricity; vaporizing."," Bombear; comprimir; gerar eletricidade; vaporizar."),
 "Provision":("provision operation","operação de provisão","Storing crude; collecting drains; supplying hydraulic pressure from an accumulator."," Armazenar óleo cru; coletar drenos; suprir pressão hidráulica de um acumulador."),
 "Signalling":("signalling operation","operação de sinalização","Sensing a pressure; indicating a level; processing a control loop."," Sentir uma pressão; indicar um nível; processar uma malha de controle."),
 "Support":("support operation","operação de suporte","Supporting a pipe; positioning a shaft in a bearing; stabilizing a vessel against vibration."," Sustentar um tubo; posicionar um eixo num mancal; estabilizar um vaso contra vibração.")}
for k,(en,pt,ex_en,ex_pt) in _OPSV.items():
    fn_pt = {"Branching":"função de ramificação","Channelling":"função de canalização","Connecting":"função de conexão","MagnitudeControl":"função de controle de magnitude","Conversion":"função de conversão","Provision":"função de provisão","Signalling":"função de sinalização","Support":"função de suporte"}[k]
    A(k+"Operation", nld_pt=f"processo que realiza alguma {fn_pt}",
      sfd_en=f"p is a '{en}' if and only if p is a 'process' that 'realizes' some '{en.replace(' operation',' function')}'",
      sfd_pt=f"p é uma '{pt}' se e somente se p é um 'processo' que 'realiza' alguma '{fn_pt}'",
      fol=f"∀p ({k}Operation(p) ↔ Process(p) ∧ ∃f ({k}Function(f) ∧ realizes(p,f)))",
      ex_en=ex_en, ex_pt=ex_pt.strip(),
      note_pt="Classe definida pelo verbo primário, para as CQs do core (CQ24) e para o padrão do MENO. Não é um universal de processo da COPI: é uma classe de consulta.",
      sources=["ODR-024 §3", HIRTZ_T5], adapted=HIRTZ + " (function classes as operations on flows)")
# leaves kept from v1
_LEAVES = {
 "copi:COPI_0000011": ("liquid pressure increase","aumento de pressão de líquido","Pumping crude from a separator to a header; boosting water for injection.","Bombear óleo cru de um separador para um coletor; elevar a pressão da água de injeção."),
 "copi:COPI_0000012": ("gas pressure increase","aumento de pressão de gás","Compressing gas for export; boosting fuel gas; compressing instrument air.","Comprimir gás para exportação; elevar a pressão do gás combustível; comprimir ar de instrumento."),
 "copi:COPI_0000013": ("gas absorption","absorção de gás","Absorbing CO2 into amine; absorbing water into glycol.","Absorver CO2 em amina; absorver água em glicol."),
 "copi:COPI_0000014": ("vaporization","vaporização","Vaporizing column bottoms in a reboiler; vaporizing LNG in a vaporizer.","Vaporizar o fundo de uma coluna num refervedor; vaporizar GNL num vaporizador."),
 "copi:COPI_0000089": ("heat exchange","troca térmica","Exchanging heat between a hot product and cold crude in a shell-and-tube exchanger.","Trocar calor entre um produto quente e óleo cru frio num trocador casco-e-tubo."),
}
for iri,(en,pt,ex_en,ex_pt) in _LEAVES.items():
    A(iri, nld_pt=f"{pt}: folha de operação mantida do v1; sua equivalência a 'processo que realiza alguma <função de termo>' é emitida pelo export",
      sfd_en=f"if p is a '{en}' then p is an instance of its parent operation; the export states p is a '{en}' if and only if p realizes the corresponding term function",
      sfd_pt=f"se p é uma '{pt}' então p é instância da sua operação pai; o export afirma que p é uma '{pt}' se e somente se p realiza a função de termo correspondente",
      fol=f"∀p ({''.join(w.capitalize() for w in en.split())}(p) → Process(p))",
      ex_en=ex_en, ex_pt=ex_pt,
      note_pt="Folha de operação do FOMI 2026 mantida pelo IRI; deixa de carregar identidade. A equivalência à função de termo (ex.: aumento de pressão de líquido ≡ processo que realiza alguma função de bombeamento) vem do export enriquecido.",
      rat_en="Kept primitive in the core; the export adds the defining equivalence from the enriched term function.",
      rat_pt="Mantida primitiva no core; o export acrescenta a equivalência definidora a partir da função de termo enriquecida.",
      sources=["ODR-011 (leaf kept)", "ODR-024 §3", MCCABE], adapted=MCCABE)
A("copi:COPI_0000015",
  nld_pt="processo em que material contido deixa seu dispositivo de contenção por outra via que não um fluxo de saída da sua função de armazenamento",
  sfd_en="if p is a 'loss of containment' then p is a 'process' in which contained material leaves its 'containment device' other than through an 'outflow' of the realization of its 'storing function'",
  sfd_pt="se p é uma 'perda de contenção' então p é um 'processo' em que material contido deixa seu 'dispositivo de contenção' por outra via que não um 'fluxo de saída' da realização da sua 'função de armazenamento'",
  fol="∀p (LossOfContainment(p) → Process(p))",
  ex_en="A leak at a flange; a tank overflow; a pipeline rupture.",
  ex_pt="Um vazamento num flange; o transbordamento de um tanque; a ruptura de um oleoduto.",
  note_pt="Processo não planejado, mantido do ODR-009 §3 para as CQs de integridade (CQ34, propagação de falhas). Não é a realização de função alguma: é um fluxo de material que não é fluxo de saída de nenhuma função — a definição em linguagem natural o diz pela negativa.",
  rat_en="Primitive: 'other than through an outflow' is a negation OWL cannot state over an open world.",
  rat_pt="Primitiva: 'por outra via que não um fluxo de saída' é uma negação que OWL não enuncia em mundo aberto.",
  sources=["ODR-009 §3", ISO14224 + " (failure modes: external leakage)"], adapted=ISO14224)

# ---------------------------------------------------------------- annotation properties used by the export
_AP = {
 "signature": ("signature","assinatura","assinatura JSON de uma função de termo: verbo, secundário, terciário, fluxos de entrada, fluxos de saída, fluxo primário, interface",
   "On the pumping function: {verb: Convert, inflows: [liquid, mechanical energy], outflows: [liquid+hydraulic energy], primary_flow: liquid}.",
   "Na função de bombeamento: {verbo: Convert, entradas: [líquido, energia mecânica], saídas: [líquido+energia hidráulica], fluxo primário: líquido}.",
   "Espelha o process_signature do enrichment.db; é o que a regra de compatibilidade do ODR-025 §3 lê."),
 "primaryFunction": ("primary function","função primária","IRI da função que dá ao artefato sua caixa (convenção de curadoria; contexto de projeto)",
   "On the reboiler: the phase change function (Convert), not the mechanical separation function (Branch).",
   "No refervedor: a função de mudança de fase (Convert), não a de separação mecânica (Branch).",
   "A célula de verbo transformativo; se nenhuma, a que a definição da norma nomeia primeiro. Convenção de curadoria, não compromisso ontológico: um contexto de projeto no sentido de Mizoguchi, Kitamura & Borgo (2016)."),
 "identityFunction": ("identity function","função de identidade","IRI da função de termo cuja assinatura individua o tipo de artefato",
   "On the pump: the pumping function, whose signature ⟨Convert, liquid + mechanical energy in, liquid + hydraulic energy out⟩ is what makes a pump a pump.",
   "Na bomba: a função de bombeamento, cuja assinatura ⟨Convert, líquido + energia mecânica entrando, líquido + energia hidráulica saindo⟩ é o que faz de uma bomba uma bomba.",
   "OWL não expressa 'exatamente uma função identitária' sem reificar; a anotação registra a escolha (ODR-025 §1)."),
 "constructiveType": ("constructive type","tipo construtivo","differentia construtiva do termo (gaveta, esfera, casco-e-tubo), mantida como anotação, nunca como subclasse funcional",
   "On the gate valve: 'gate'; on the shell-and-tube heat exchanger: 'shell and tube'.",
   "Na válvula gaveta: 'gaveta'; no trocador casco-e-tubo: 'casco e tubo'.",
   "Separa o aspecto construtivo do funcional (ODR-026 §5): tipos construtivos portam a função do gênero e são primitivos."),
}
_AP_NOTE_EN = {
 "signature": "Mirrors the process_signature of enrichment.db; it is what the compatibility rule of ODR-025 §3 reads.",
 "primaryFunction": "The transformative cell; if none, the one the standard's definition names first. A curation convention, not an ontological commitment: a design context in the sense of Mizoguchi, Kitamura & Borgo (2016).",
 "identityFunction": "OWL does not express 'exactly one identity-giving function' without reification; the annotation records the choice (ODR-025 §1).",
 "constructiveType": "Separates the constructive aspect from the functional one (ODR-026 §5): constructive types bear the genus function and are primitive.",
}
for k,(en,pt,nld_pt,ex_en,ex_pt,note_pt) in _AP.items():
    A(k, label_pt=pt, nld_pt=nld_pt, ex_en=ex_en, ex_pt=ex_pt, note_en=_AP_NOTE_EN[k], note_pt=note_pt, sources=["ODR-025 §1–2", KITAMURA], adapted=KITAMURA if k=="primaryFunction" else None)

HEADER = {
 "title_en": "COPI Core (v2): a process-industry core layer in BFO — functions of the Functional Basis, three flows, identity and scope",
 "title_pt": "COPI Núcleo (v2): uma camada núcleo para indústrias de processo em BFO — funções da Functional Basis, três fluxos, identidade e escopo",
 "comment_en": "COPI Core is the top-level layer of the Core Ontology for Petroleum Installations (COPI). It specializes BFO 2020 and IOF Core 202603 with the classes every COPI equipment universal is anchored in. Version 2 replaces the unit-operation anchoring of the FOMI 2026 paper (ODR-009/011/012) by function classes whose genus is a verb of the Functional Basis (Hirtz et al. 2002) applied to a flow of material, energy or signal: a flow-operating function under iof:DesignedFunction with eight disjoint primaries and twenty secondaries; flows as occurrents (the crossing of one interface), with material, energy and signal flows not disjoint; energy as a quality of its bearer, transferred by decrease/increase (MENO) and transformed inside the artifact; signal content concretized by the flow or by a quality of its bearer; the nine FOMI equipment categories and eight operations kept on their IRIs as defined classes over the genus-level functions. Identity of an equipment type is its term function's signature; its box is its primary function; disjointness among artifacts is by partition under a functional genus (ODR-025). Equipment at the ISO 14224 equipment-unit level receives a function with a signature; systems do not (ODR-026).",
 "comment_pt": "COPI Núcleo é a camada de topo da Ontologia Núcleo para Instalações de Petróleo (COPI). Especializa o BFO 2020 e o IOF Core 202603 com as classes em que todo universal de equipamento da COPI é ancorado. A versão 2 substitui a ancoragem em operações unitárias do artigo do FOMI 2026 (ODR-009/011/012) por classes de função cujo gênero é um verbo da Functional Basis (Hirtz et al. 2002) aplicado a um fluxo de material, energia ou sinal: uma função sobre fluxo sob iof:DesignedFunction com oito primárias disjuntas e vinte secundárias; fluxos como ocorrentes (o atravessar de uma interface), com fluxos de material, energia e sinal não disjuntos; energia como qualidade do portador, transferida por decréscimo/acréscimo (MENO) e transformada dentro do artefato; conteúdo de sinal concretizado pelo fluxo ou por uma qualidade do portador; as nove categorias de equipamento e as oito operações do FOMI mantidas nos seus IRIs como classes definidas sobre as funções de gênero. A identidade de um tipo de equipamento é a assinatura da sua função de termo; sua caixa é a função primária; a disjunção entre artefatos é por partição sob um gênero funcional (ODR-025). Equipamento no nível de unidade de equipamento da ISO 14224 recebe função com assinatura; sistemas não (ODR-026).",
 "usage_en": "Load in Protégé; map the IOF import IRI to the local Core.rdf (202603 mirror in copi/src/ontology/mirror/) and ensure BFO 2020 resolves. Reason with HermiT (ELK does not support allValuesFrom and property chains together). copi-vocab.ttl asserts the declarations of the vocab functions and processes this file re-parents (COPI_0000025–36). The property chains of 'has inflow participant' / 'has outflow participant' are not sub-properties of 'has participant' (regularity); materialize 'has participant' and iof:hasInput/hasOutput on instance data with the CONSTRUCT shipped in COPIeditor/scripts/sparql/materialize_participants.rq.",
 "usage_pt": "Carregue no Protégé; mapeie o IRI de importação da IOF para o Core.rdf local (mirror 202603 em copi/src/ontology/mirror/) e garanta que o BFO 2020 resolve. Raciocine com HermiT (o ELK não suporta allValuesFrom e cadeias de propriedade juntos). O copi-vocab.ttl asserta as declarações das funções e processos do vocab que este arquivo reparenta (COPI_0000025–36). As cadeias de 'tem participante de fluxo de entrada' / 'de saída' não são subpropriedades de 'tem participante' (regularidade); materialize 'tem participante' e iof:hasInput/hasOutput sobre instâncias com o CONSTRUCT em COPIeditor/scripts/sparql/materialize_participants.rq.",
 "versionInfo": "2.0.0-draft (copi-core v2; ODR-024/025/026; Functional Basis anchoring, flows as occurrents, identity by signature; 2026-11-04)",
 "sources": ["Spec copi-core v2 (project doc copi-ufo, rev. 2026-11-04)", "ODR-024 (function root, flows as occurrents, three flow patterns)", "ODR-025 (identity by signature, box by primary function, disjointness by partition)", "ODR-026 (equipment × system: who receives a cell)", "ODR-023 (closed, reading A)", HIRTZ, STONE, BORGO, VERMAAS, PAHL, MENO, OEO, IOF, BFO, RO, ISA51, ISO14224, MCCABE, KITAMURA],
}

# ---------------------------------------------------------------- English explanatory notes for entries whose English note was not in gen.py
_NOTE_EN = {
 "hasInflow": "Direction is relative to the boundary of the artifact whose function the process realizes: 'in' and 'out' are predicated of an occurrent bounded by the interface, not of a portion. Sub-property of 'has occurrent part' (BFO_0000117).",
 "hasOutflow": "See 'has inflow'. The same flow is the outflow of one artifact and the inflow of the next (individuation by interface).",
 "ThermalEnergy": "Transferred between bearers by a heat exchanger; close match to MENO thermal energy.",
 "ElectricalEnergy": "Transferred by cables and bus bars; converted by motors, generators and transformers (the latter change the magnitude, not the kind).",
 "ChemicalEnergy": "Converted to thermal energy by combustion and to electrical energy by fuel cells.",
 "EnergyDecrease": "One half of MENO's transfer/transformation pattern: a decrease here, causally related to an increase there (transfer) or of another kind in the same bearer (transformation). Uses RO's regulates-characteristic relations.",
 "EnergyIncrease": "See energy decrease.",
 "EnergyTransformation": "The decrease and the increase regulate energy qualities of DIFFERENT kinds inhering in the SAME bearer; the decrease is causally related to the increase (RO_0002410). Distinct from transfer (same kind, two bearers), which is an energy flow. An electrical transformer does not transform: it changes the magnitude (voltage) of one kind of energy — magnitude control/change.",
 "MaterialTransformation": "The internal part of the realization of phase change and chemical reaction functions (ODR-025 §4). To be detailed with the portions and qualities of ODR-010 §2 when CQs require phase and composition as qualities.",
 "copi:COPI_0000011": "FOMI 2026 operation leaf kept on its IRI; it no longer carries identity. The equivalence to the term function (liquid pressure increase ≡ process that realizes some pumping function) comes from the enriched export.",
 "copi:COPI_0000012": "FOMI 2026 operation leaf kept on its IRI; it no longer carries identity. The equivalence to the term function (gas pressure increase ≡ process that realizes some compression function) comes from the enriched export.",
 "copi:COPI_0000013": "FOMI 2026 operation leaf kept on its IRI; it no longer carries identity. The equivalence to the term function comes from the enriched export.",
 "copi:COPI_0000014": "FOMI 2026 operation leaf kept on its IRI; it no longer carries identity. The equivalence to the term function comes from the enriched export.",
 "copi:COPI_0000089": "FOMI 2026 operation leaf kept on its IRI; it no longer carries identity. The equivalence to the term function comes from the enriched export.",
 "copi:COPI_0000015": "Unplanned process, kept from ODR-009 §3 for the integrity CQs (CQ34, failure propagation). It is the realization of no function: a material flow that is the outflow of no function — the definition says it by negation.",
}
for k, v in _NOTE_EN.items():
    ANN[k]["note_en"] = v
