# Annotations of the function classes of copi-core-v2 (root, 8 primaries, 20 secondaries, 6 genera).
# Fields: nld_pt, sfd_en, sfd_pt, ex_en, ex_pt, note_pt, fol, rat_en, rat_pt, sources (list), adapted.
# English nld and explanatoryNote are kept in gen.py; everything here completes them.
from ann_refs import *

ANN = {}
def A(key, **f): ANN[key] = f

# ---------------------------------------------------------------- root
A("FlowOperatingFunction",
  nld_pt="função projetada de um artefato ou sistema de engenharia que consiste em realizar uma operação sobre um fluxo de material, energia ou sinal que atravessa a fronteira do portador",
  sfd_en="if f is a 'flow-operating function' then f is a 'designed function' and every process p in which f is 'realized' is a 'process' that 'has inflow' some 'flow' or 'has outflow' some 'flow'",
  sfd_pt="se f é uma 'função sobre fluxo' então f é uma 'função projetada' e todo processo p em que f é 'realizada' é um 'processo' que 'tem fluxo de entrada' algum 'fluxo' ou 'tem fluxo de saída' algum 'fluxo'",
  fol="∀f (FlowOperatingFunction(f) → DesignedFunction(f) ∧ ∀p (realizedIn(f,p) → Process(p) ∧ ∃x (Flow(x) ∧ (hasInflow(p,x) ∨ hasOutflow(p,x)))))",
  ex_en="The pumping function of a centrifugal pump (a conversion function on a liquid flow); the containment function of a storage tank (a storing function); the sensing function of a pressure transmitter (a signalling function).",
  ex_pt="A função de bombeamento de uma bomba centrífuga (função de conversão sobre um fluxo de líquido); a função de contenção de um tanque de armazenamento (função de armazenamento); a função de sensoriamento de um transmissor de pressão (função de sinalização).",
  note_pt="A Functional Basis (Hirtz et al. 2002) não nomeia esta raiz: julga um termo de função 'pelo fato de descrever ou não uma operação que um produto ou dispositivo executa sobre um fluxo' e chama as oito primárias de 'classes de função'. iof:DesignedFunction é mais ampla (cobre funções pretendidas que não operam sobre fluxo algum, como a função identificadora de uma plaqueta); esta classe é onde vive a hipótese da Functional Basis. A linhagem são as funções geralmente válidas de Pahl & Beitz.",
  rat_en="The root is primitive: 'operating on a flow' is characterized by a necessary condition on the realizing processes, not defined, because the Functional Basis itself treats the function/flow pairing as the primitive of its vocabulary and the eight primaries exhaust it only by stipulation.",
  rat_pt="A raiz é primitiva: 'operar sobre um fluxo' é caracterizado por uma condição necessária sobre os processos realizadores, não definido, porque a própria Functional Basis trata o par função/fluxo como o primitivo do seu vocabulário e as oito primárias só o esgotam por estipulação.",
  sources=["ODR-024 §1", HIRTZ_T5, STONE, BORGO, PAHL], adapted=HIRTZ + ", §2 and Appendix B; " + PAHL)

# ---------------------------------------------------------------- primaries
_PRIM_EX = {
 "Branching": ("A gas–liquid separator (separate); a distribution manifold (distribute); a strainer (separate/remove).",
               "Um separador gás–líquido (separar); um manifold de distribuição (distribuir); um filtro-cesto (separar/remover)."),
 "Channelling": ("A pipe (transfer/transport); a cable (transfer/transmit); an inlet nozzle (import); a guide vane (guide).",
                 "Um tubo (transferir/transportar); um cabo (transferir/transmitir); um bocal de entrada (importar); uma palheta guia (guiar)."),
 "Connecting": ("A flange pair (couple/join); a shaft coupling (couple/link); a static mixer (mix).",
                "Um par de flanges (acoplar/unir); um acoplamento de eixo (acoplar/ligar); um misturador estático (misturar)."),
 "MagnitudeControl": ("A control valve (regulate); a gate valve (stop); an orifice plate (change); a solenoid valve (actuate).",
                      "Uma válvula de controle (regular); uma válvula gaveta (interromper); uma placa de orifício (mudar); uma válvula solenoide (atuar)."),
 "Conversion": ("A pump (mechanical energy → pressurized liquid); an electric motor (electrical → mechanical energy); a reboiler (liquid → vapour).",
                "Uma bomba (energia mecânica → líquido pressurizado); um motor elétrico (energia elétrica → mecânica); um refervedor (líquido → vapor)."),
 "Provision": ("A storage tank (store/contain); a drain sump (store/collect); a battery or an accumulator (supply).",
               "Um tanque de armazenamento (armazenar/conter); um sumidouro de drenagem (armazenar/coletar); uma bateria ou um acumulador (suprir)."),
 "Signalling": ("A pressure transmitter (sense/measure); a level gauge (indicate/display); a controller (process).",
                "Um transmissor de pressão (sentir/medir); um indicador de nível (indicar/exibir); um controlador (processar)."),
 "Support": ("A pipe support (secure); a bearing (position); a stiffener or a vibration damper (stabilize).",
             "Um suporte de tubulação (fixar); um mancal (posicionar); um reforçador ou um amortecedor de vibração (estabilizar)."),
}
_PRIM_PT = {
 "Branching": ("função de fazer com que um fluxo deixe de estar unido ou misturado, ou de distribuí-lo",
   "Classe primária 'Branch' da Functional Basis. Disjunta das outras sete primárias; suas secundárias são aspectos, não alternativas, e não são declaradas disjuntas."),
 "Channelling": ("função de fazer um fluxo mover-se de um lugar a outro",
   "Classe primária 'Channel' da Functional Basis. Disjunta das outras sete primárias; suas secundárias são aspectos, não alternativas, e não são declaradas disjuntas."),
 "Connecting": ("função de reunir dois ou mais fluxos",
   "Classe primária 'Connect' da Functional Basis. Disjunta das outras sete primárias; suas secundárias são aspectos, não alternativas, e não são declaradas disjuntas."),
 "MagnitudeControl": ("função de alterar ou governar o tamanho ou a amplitude de um fluxo",
   "Classe primária 'Control magnitude' da Functional Basis. Disjunta das outras sete primárias; suas secundárias são aspectos, não alternativas, e não são declaradas disjuntas. A função de controle de fluxo do copi-vocab (COPI_0000026) é reparentada aqui, porque cobre regular (válvulas de controle) e interromper (válvulas de bloqueio)."),
 "Conversion": ("função de mudar um fluxo de uma forma para outra",
   "Classe primária 'Convert' da Functional Basis, a única sem secundárias. Recebe a única caracterização formal além do verbo: é realizada só em processos que têm como parte uma transformação interna (de energia, de fase ou de composição); sem isso seria indistinguível de canalizar/transferir para um trocador com mudança de fase."),
 "Provision": ("função de acumular ou fornecer um fluxo",
   "Classe primária 'Provision' da Functional Basis. Disjunta das outras sete primárias; suas secundárias são aspectos, não alternativas, e não são declaradas disjuntas. A função de contenção do copi-vocab (COPI_0000025) é reparentada sob armazenar."),
 "Signalling": ("função de fornecer informação sobre um fluxo: sentir, indicar ou processar um sinal",
   "Classe primária 'Signal' da Functional Basis. Disjunta das outras sete primárias; suas secundárias são aspectos, não alternativas, e não são declaradas disjuntas. 'Instrumento' (COPI_0000091) é definido como artefato material que porta uma função de sinalização (ODR-023, leitura A)."),
 "Support": ("função de fixar firmemente um fluxo (um objeto) numa posição definida, ou de prendê-lo ou posicioná-lo",
   "Classe primária 'Support' da Functional Basis. É o único caso em que o 'fluxo' é um operando estático (o tubo que o suporte segura); a realização é o processo de o objeto permanecer em posição. Disjunta das outras sete primárias."),
}
_PRIM_SFD = {
 "Branching": "to cause a flow to no longer be joined or mixed, or to be distributed",
 "Channelling": "to cause a flow to move from one location to another",
 "Connecting": "to bring two or more flows together",
 "MagnitudeControl": "to alter or govern the size or amplitude of a flow",
 "Conversion": "to change a flow from one form to another, in a process that has as part some 'transformation'",
 "Provision": "to accumulate or provide a flow",
 "Signalling": "to provide information on a flow",
 "Support": "to fix, secure or position a flow that is an object",
}
_PRIM_SFD_PT = {
 "Branching": "fazer um fluxo deixar de estar unido ou misturado, ou distribuí-lo",
 "Channelling": "fazer um fluxo mover-se de um lugar a outro",
 "Connecting": "reunir dois ou mais fluxos",
 "MagnitudeControl": "alterar ou governar o tamanho ou a amplitude de um fluxo",
 "Conversion": "mudar um fluxo de uma forma para outra, num processo que tem como parte alguma 'transformação'",
 "Provision": "acumular ou fornecer um fluxo",
 "Signalling": "fornecer informação sobre um fluxo",
 "Support": "fixar, prender ou posicionar um fluxo que é um objeto",
}
_OTHERS = lambda k: [p for p in _PRIM_PT if p != k]
for k,(nld_pt,note_pt) in _PRIM_PT.items():
    ex_en, ex_pt = _PRIM_EX[k]
    others = " ∧ ".join(f"¬{o}Function(f)" for o in _OTHERS(k))
    fol = f"∀f ({k}Function(f) → FlowOperatingFunction(f) ∧ {others})"
    if k == "Conversion":
        fol += " ∧ ∀f (ConversionFunction(f) → ∀p (realizedIn(f,p) → ∃t (Transformation(t) ∧ hasOccurrentPart(p,t))))"
    A(k+"Function", nld_pt=nld_pt, note_pt=note_pt, ex_en=ex_en, ex_pt=ex_pt, fol=fol,
      sfd_en=f"if f is a '{k.lower() if k!='MagnitudeControl' else 'magnitude control'} function' then f is a 'flow-operating function' whose operation on the flow is {_PRIM_SFD[k]}, and f is not an instance of any of the other seven primary function classes",
      sfd_pt=f"se f é uma função desta classe então f é uma 'função sobre fluxo' cuja operação sobre o fluxo é {_PRIM_SFD_PT[k]}, e f não é instância de nenhuma das outras sete classes primárias de função",
      rat_en="Primitive: the Functional Basis gives the eight classes by enumeration and natural-language definition; what distinguishes them is the kind of operation on the flow, which OWL cannot express as a sufficient condition without reifying the operation. Disjointness among the eight is the only formal commitment, and it is what disjointness among artifact types is derived from (ODR-025).",
      rat_pt="Primitiva: a Functional Basis dá as oito classes por enumeração e definição em linguagem natural; o que as distingue é o tipo de operação sobre o fluxo, que OWL não expressa como condição suficiente sem reificar a operação. A disjunção entre as oito é o único compromisso formal, e é dela que deriva a disjunção entre tipos de artefato (ODR-025).",
      sources=["ODR-024 §1", "ODR-025 §3 (disjointness by primary)", HIRTZ_T5], adapted=HIRTZ + ", Appendix B")

_PRIM_NOTE_EN = {
 "MagnitudeControl": "Primary class 'Control magnitude' of the Functional Basis. Disjoint from the other seven primaries; its secondaries are aspects, not alternatives, and are not declared disjoint. The flow control function of copi-vocab (COPI_0000026) is re-parented here, because it covers regulating (control valves) and stopping (block valves).",
 "Conversion": "Primary class 'Convert' of the Functional Basis, the only one without secondaries. It receives the only formal characterization beyond the verb: it is realized only in processes that have an internal transformation as part (of energy, phase or composition); without it, it would be indistinguishable from channelling/transferring for an exchanger with phase change.",
 "Provision": "Primary class 'Provision' of the Functional Basis. Disjoint from the other seven primaries; its secondaries are aspects, not alternatives, and are not declared disjoint. The containment function of copi-vocab (COPI_0000025) is re-parented under storing.",
 "Signalling": "Primary class 'Signal' of the Functional Basis. Disjoint from the other seven primaries; its secondaries are aspects, not alternatives, and are not declared disjoint. 'Instrument' (COPI_0000091) is defined as a material artifact bearing a signalling function (ODR-023, reading A).",
 "Support": "Primary class 'Support' of the Functional Basis. The only case in which the 'flow' is a static operand (the pipe the support holds); the realization is the process of the object staying in place. Disjoint from the other seven primaries.",
}
for k, v in _PRIM_NOTE_EN.items():
    ANN[k + "Function"]["note_en"] = v

# ---------------------------------------------------------------- secondaries
_SEC = {
 # key: (nld_pt, ex_en, ex_pt, note_pt_extra)
 "Separating": ("função de isolar um fluxo em componentes distintos; terciários: dividir, extrair, remover",
   "A three-phase separator (divide); an absorber (extract); a strainer or a filter (remove).",
   "Um separador trifásico (dividir); um absorvedor (extrair); um filtro-cesto ou um filtro (remover).", ""),
 "Distributing": ("função de fazer um fluxo se repartir e espalhar por uma área",
   "A distribution manifold; a pipe tee; a spray nozzle.", "Um manifold de distribuição; um tê de tubulação; um bico aspersor.", ""),
 "Importing": ("função de trazer um fluxo de fora da fronteira do sistema",
   "An inlet nozzle; a suction strainer at a tank inlet; an air intake.", "Um bocal de entrada; um filtro de sucção na entrada de um tanque; uma tomada de ar.", ""),
 "Exporting": ("função de enviar um fluxo para fora da fronteira do sistema",
   "An outlet nozzle; a vent; a discharge header.", "Um bocal de saída; um respiro; um coletor de descarga.", ""),
 "Transferring": ("função de deslocar ou conduzir um fluxo de um lugar a outro; terciários: transportar, transmitir",
   "A pipe or a hose (transport a fluid); a drive shaft (transmit mechanical energy); an electrical cable (transmit electrical energy).",
   "Um tubo ou um mangote (transportar um fluido); um eixo de acionamento (transmitir energia mecânica); um cabo elétrico (transmitir energia elétrica).",
   " Transferir energia térmica entre dois fluidos sem transformação é a função de gênero dos trocadores de calor (COPI_0001055)."),
 "Guiding": ("função de dirigir o curso de um fluxo ao longo de um caminho específico; terciários: transladar, rotacionar, permitir grau de liberdade",
   "A pipe elbow or bend; a guide vane; a bearing's guiding of a rotating shaft (allow degree of freedom).",
   "Uma curva ou cotovelo de tubulação; uma palheta guia; a guia de um eixo girante por um mancal (permitir grau de liberdade).", ""),
 "Coupling": ("função de unir ou juntar fluxos; terciários: unir, ligar",
   "A flange pair or a fitting (join); a shaft coupling (link); a tubing hanger coupling a string to a head.",
   "Um par de flanges ou uma conexão (unir); um acoplamento de eixo (ligar); um suspensor de coluna acoplando a coluna à cabeça.", ""),
 "Mixing": ("função de combinar dois fluxos numa única massa uniforme e homogênea",
   "A static mixer; an agitator; an aerator.", "Um misturador estático; um agitador; um aerador.",
   " A função de mistura enriquecida do misturador (COPI_0000578) foi fundida nesta classe em 2026-11-04."),
 "Actuating": ("função de iniciar o fluxo de energia, sinal ou material em resposta a um sinal de controle importado",
   "A solenoid valve; an on-off control valve; a motor starter.", "Uma válvula solenoide; uma válvula de controle liga-desliga; um contator de partida de motor.", ""),
 "Regulating": ("função de ajustar um fluxo em resposta a um sinal de controle; terciários: aumentar, diminuir",
   "A control valve; a choke valve; a pressure relief valve (decrease); a variable-speed drive (increase/decrease).",
   "Uma válvula de controle; uma válvula choke; uma válvula de alívio de pressão (diminuir); um inversor de frequência (aumentar/diminuir).",
   " A função de fluxo controlado por processo do copi-vocab (COPI_0000027) e a função de alívio de segurança (COPI_0000032) são reparentadas aqui."),
 "Changing": ("função de ajustar um fluxo de maneira predeterminada e fixa; terciários: incrementar, decrementar, dar forma, condicionar",
   "A restriction orifice (decrement); a gearbox (change speed and torque); a power transformer (change voltage); a filter conditioning a fluid.",
   "Uma placa de orifício de restrição (decrementar); uma caixa de engrenagens (mudar rotação e torque); um transformador de potência (mudar tensão); um filtro condicionando um fluido.", ""),
 "Stopping": ("função de cessar, ou impedir, a transferência de um fluxo; terciários: impedir, inibir",
   "A gate valve or a ball valve in isolation service; a check valve (prevent backflow); a gasket (prevent leakage).",
   "Uma válvula gaveta ou esfera em serviço de bloqueio; uma válvula de retenção (impedir refluxo); uma junta (impedir vazamento).", ""),
 "Storing": ("função de acumular um fluxo; terciários: conter, coletar",
   "A storage tank (contain); a pressure vessel (contain); a drain sump (collect).",
   "Um tanque de armazenamento (conter); um vaso de pressão (conter); um sumidouro de drenagem (coletar).",
   " A função de contenção do copi-vocab (COPI_0000025) é reparentada aqui (conter)."),
 "Supplying": ("função de fornecer um fluxo a partir de armazenamento",
   "A hydraulic accumulator supplying pressure; a battery or a UPS supplying electrical energy; a chemical injection tank.",
   "Um acumulador hidráulico fornecendo pressão; uma bateria ou um no-break fornecendo energia elétrica; um tanque de injeção de produto químico.", ""),
 "Sensing": ("função de perceber, ou tomar conhecimento de, um fluxo; terciários: detectar, medir",
   "A pressure transmitter or a temperature element (measure); a flame detector or a level switch (detect).",
   "Um transmissor de pressão ou um elemento de temperatura (medir); um detector de chama ou uma chave de nível (detectar).",
   " A função de instrumentação do copi-vocab (COPI_0000029) é reparentada aqui (ODR-023, leitura A); 'instrumento de medição' (COPI_0000024) é definido sobre ela com um fluxo de sinal que concretiza conteúdo de medição."),
 "Indicating": ("função de tornar algo conhecido ao usuário sobre um fluxo; terciários: rastrear, exibir",
   "A pressure gauge; a level sight glass; a local indicator or a display (display); a totalizer (track).",
   "Um manômetro; um visor de nível; um indicador local ou um mostrador (exibir); um totalizador (rastrear).",
   " A função de indicação do copi-vocab (COPI_0000028) é reparentada aqui."),
 "Processing": ("função de submeter um sinal a um tratamento ou método particular com um número definido de operações ou passos",
   "A controller; a transducer converting a sensor signal to a standard output; a relay or a logic solver.",
   "Um controlador; um transdutor convertendo o sinal do sensor numa saída padrão; um relé ou um solucionador lógico.",
   " Controladores e transdutores são instrumentos sem ser instrumentos de medição (ODR-025 §5)."),
 "Stabilizing": ("função de impedir que um objeto mude de curso ou de posição",
   "A stiffener; a vibration damper; a guy wire or a brace.", "Um reforçador; um amortecedor de vibração; um estai ou uma escora.", ""),
 "Securing": ("função de fixar firmemente um objeto a uma posição",
   "A pipe support or a clamp; an anchor bolt; a transmitter housing securing the electronics.",
   "Um suporte de tubulação ou uma braçadeira; um chumbador; a caixa de um transmissor fixando a eletrônica.", ""),
 "Positioning": ("função de colocar um objeto numa posição ou orientação específica",
   "A bearing positioning a rotating shaft; a spacer; an alignment pin.",
   "Um mancal posicionando um eixo girante; um espaçador; um pino de alinhamento.",
   " A função de suporte enriquecida do mancal (COPI_0000659) foi fundida nesta classe em 2026-11-04; o segundo verbo do mancal (guiar/rotacionar) é assertado no artefato."),
}
_SEC_PARENT = {"Separating":"Branching","Distributing":"Branching","Importing":"Channelling","Exporting":"Channelling","Transferring":"Channelling","Guiding":"Channelling",
  "Coupling":"Connecting","Mixing":"Connecting","Actuating":"MagnitudeControl","Regulating":"MagnitudeControl","Changing":"MagnitudeControl","Stopping":"MagnitudeControl",
  "Storing":"Provision","Supplying":"Provision","Sensing":"Signalling","Indicating":"Signalling","Processing":"Signalling","Stabilizing":"Support","Securing":"Support","Positioning":"Support"}
_SEC_FB = {"Separating":"Separate","Distributing":"Distribute","Importing":"Import","Exporting":"Export","Transferring":"Transfer","Guiding":"Guide","Coupling":"Couple","Mixing":"Mix","Actuating":"Actuate","Regulating":"Regulate","Changing":"Change","Stopping":"Stop","Storing":"Store","Supplying":"Supply","Sensing":"Sense","Indicating":"Indicate","Processing":"Process","Stabilizing":"Stabilize","Securing":"Secure","Positioning":"Position"}
for k,(nld_pt,ex_en,ex_pt,extra) in _SEC.items():
    p = _SEC_PARENT[k]
    A(k+"Function", nld_pt=nld_pt, ex_en=ex_en, ex_pt=ex_pt,
      note_pt="Termo secundário '"+_SEC_FB[k]+"' da Functional Basis sob '"+p+"'. Os termos terciários ficam no esquema SKOS fb: (skos:narrower), não como classes. Secundárias irmãs não são disjuntas: um mesmo artefato pode portar duas (Vermaas 2007; cobertura COPI 2026-10-23)."+extra,
      sfd_en=f"if f is a '{k.lower()} function' then f is a '{'magnitude control' if p=='MagnitudeControl' else p.lower()} function' whose operation on the flow is the secondary term '{_SEC_FB[k]}' of the Functional Basis",
      sfd_pt=f"se f é uma função desta classe então f é uma função primária '{p}' cuja operação sobre o fluxo é o termo secundário '{_SEC_FB[k]}' da Functional Basis",
      fol=f"∀f ({k}Function(f) → {p}Function(f))",
      rat_en="Primitive, like its primary: the secondary term names a kind of operation on the flow that is distinguished in natural language only. Secondaries of one primary are not declared disjoint because the coverage data show them co-occurring on one artifact (separate + distribute; sense + indicate).",
      rat_pt="Primitiva, como sua primária: o termo secundário nomeia um tipo de operação sobre o fluxo distinguido só em linguagem natural. Secundárias de uma mesma primária não são declaradas disjuntas porque os dados da cobertura as mostram coocorrendo num mesmo artefato (separar + distribuir; sentir + indicar).",
      sources=["ODR-024 §1", HIRTZ_T5, VERMAAS], adapted=HIRTZ + ", Appendix B, secondary '" + _SEC_FB[k] + "'")

# ---------------------------------------------------------------- genus-level functions (ODR-025 §4)
A("FluidMachineFunction",
  nld_pt="função de conversão realizada num processo com um fluxo de entrada de energia mecânica, uma transformação interna de energia, e um fluxo de saída que é ao mesmo tempo fluxo de material e fluxo de energia hidráulica ou pneumática (um carrier flow)",
  sfd_en="if f is a 'fluid machine function' then f is a 'conversion function' and every process in which f is 'realized' 'has outflow' some flow that is both a 'material flow' and an 'energy flow'",
  sfd_pt="se f é uma 'função de máquina de fluxo' então f é uma 'função de conversão' e todo processo em que f é 'realizada' 'tem fluxo de saída' algum fluxo que é ao mesmo tempo 'fluxo de material' e 'fluxo de energia'",
  fol="∀f (FluidMachineFunction(f) → ConversionFunction(f) ∧ ∀p (realizedIn(f,p) → ∃x (MaterialFlow(x) ∧ EnergyFlow(x) ∧ hasOutflow(p,x))))",
  ex_en="The pumping function of a pump; the compression function of a compressor; the function of a fan or a blower; the expansion function of a turbine (energy in the opposite direction).",
  ex_pt="A função de bombeamento de uma bomba; a função de compressão de um compressor; a função de um ventilador ou soprador; a função de expansão de uma turbina (energia no sentido oposto).",
  note_pt="Função de gênero da COPI: o pai das funções de termo (ex.: função de bombeamento) de um gênero de artefato. Refina uma classe da Functional Basis; não pertence a ela. É o gênero em que pendura a partição bomba × compressor (qualificador exclusivo: líquido × gás como fluxo primário). Redefine a categoria 'transferência de quantidade de movimento' do FOMI 2026 (MomentumTransfer, McCabe-Smith-Harriott) pela função, não pela operação.",
  rat_en="Primitive with a necessary condition (the carrier outflow). A sufficient condition would have to name the energy transformation inside the machine, which the term functions below it specify (mechanical → hydraulic for a pump).",
  rat_pt="Primitiva com uma condição necessária (o fluxo de saída portador). Uma condição suficiente teria de nomear a transformação de energia dentro da máquina, que as funções de termo abaixo dela especificam (mecânica → hidráulica para uma bomba).",
  sources=["ODR-025 §4", "ODR-011 (MomentumTransfer, superseded)", MCCABE, HIRTZ_T3], adapted=MCCABE + " (fluid-flow operations); carrier flows after Nagel et al. (2007)")
A("HeatTransferFunction",
  nld_pt="função de transferência realizada num processo com dois fluxos de material de entrada e dois de saída, um par carregando um decréscimo de energia térmica e o outro um acréscimo, sem transformação",
  sfd_en="if f is a 'heat transfer function' then f is a 'transferring function' and every process in which f is 'realized' 'has inflow' some flow that is a 'material flow' and an 'energy flow' with an 'energy decrease' of 'thermal energy', and 'has outflow' some flow that is a 'material flow' and an 'energy flow' with an 'energy increase' of 'thermal energy'",
  sfd_pt="se f é uma 'função de transferência de calor' então f é uma 'função de transferência' e todo processo em que f é 'realizada' 'tem fluxo de entrada' algum fluxo que é 'fluxo de material' e 'fluxo de energia' com um 'decréscimo de energia' térmica, e 'tem fluxo de saída' algum fluxo que é 'fluxo de material' e 'fluxo de energia' com um 'acréscimo de energia' térmica",
  fol="∀f (HeatTransferFunction(f) → TransferringFunction(f) ∧ ∀p (realizedIn(f,p) → ∃i (MaterialFlow(i) ∧ EnergyFlow(i) ∧ hasInflow(p,i) ∧ ∃d (EnergyDecrease(d) ∧ hasOccurrentPart(i,d) ∧ ∃q (ThermalEnergy(q) ∧ negativelyRegulatesCharacteristic(d,q)))) ∧ ∃o (MaterialFlow(o) ∧ EnergyFlow(o) ∧ hasOutflow(p,o) ∧ ∃n (EnergyIncrease(n) ∧ hasOccurrentPart(o,n) ∧ ∃r (ThermalEnergy(r) ∧ positivelyRegulatesCharacteristic(n,r))))))",
  ex_en="The function of a shell-and-tube, plate, air-cooled or finned-tube heat exchanger; of a cooler; of a condenser without phase change on the cooled side.",
  ex_pt="A função de um trocador de calor casco-e-tubo, de placas, resfriado a ar ou de tubos aletados; de um resfriador; de um condensador sem mudança de fase do lado resfriado.",
  note_pt="Função de gênero da COPI; é a função de todo tipo de trocador de calor: os tipos diferem só construtivamente e portam este gênero diretamente (a função de termo enriquecida COPI_0000068 foi fundida aqui em 2026-11-04). Refina 'transferir' (Channel) da Functional Basis: calor é transferido, não convertido — um trocador com mudança de fase (refervedor, condensador) porta além disso uma função de mudança de fase.",
  rat_en="Primitive with the exchanger template as necessary condition; the condition is not sufficient because a trace-heated line also transfers thermal energy into a material flow without being a heat exchanger (its primary flow is the conveyed liquid).",
  rat_pt="Primitiva com o template de trocador como condição necessária; a condição não é suficiente porque uma linha com traceamento também transfere energia térmica para um fluxo de material sem ser um trocador (seu fluxo primário é o líquido transportado).",
  sources=["ODR-025 §4", "ODR-024 §5 (energy transfer)", MCCABE, MENO], adapted=MCCABE + " (heat transfer); " + MENO + " (energy transfer as decrease/increase)")
A("MassTransferFunction",
  nld_pt="função de separação que isola um componente de uma mistura fluida transferindo-o para outra fase (extrair)",
  sfd_en="if f is a 'mass transfer function' then f is a 'separating function' whose operation isolates a component of a fluid mixture by transfer to another phase",
  sfd_pt="se f é uma 'função de transferência de massa' então f é uma 'função de separação' cuja operação isola um componente de uma mistura fluida por transferência a outra fase",
  fol="∀f (MassTransferFunction(f) → SeparatingFunction(f))",
  ex_en="The absorption function of a gas absorber; the function of a stripper; of a distillation column; of a glycol contactor.",
  ex_pt="A função de absorção de um absorvedor de gás; a função de um esgotador; de uma coluna de destilação; de um contactor de glicol.",
  note_pt="Função de gênero da COPI: redefine a categoria 'transferência de massa' do FOMI 2026 pela função. Refina 'separar/extrair' (Branch) da Functional Basis; o critério que a distingue da separação mecânica é o mecanismo (equilíbrio entre fases vs. força mecânica), registrado só em linguagem natural.",
  rat_en="Primitive: the mechanism (interphase equilibrium) is not expressible as a restriction over flows; both mass transfer and mechanical separation have a mixture inflow and phase outflows.",
  rat_pt="Primitiva: o mecanismo (equilíbrio entre fases) não é exprimível como restrição sobre fluxos; tanto a transferência de massa quanto a separação mecânica têm uma mistura na entrada e fases na saída.",
  sources=["ODR-025 §4", "ODR-011 (MassTransfer, superseded)", MCCABE], adapted=MCCABE + " (mass transfer and its applications)")
A("MechanicalSeparationFunction",
  nld_pt="função de separação que isola fases ou partículas de uma mistura por meios mecânicos",
  sfd_en="if f is a 'mechanical separation function' then f is a 'separating function' whose operation isolates phases or particles of a mixture by mechanical means",
  sfd_pt="se f é uma 'função de separação mecânica' então f é uma 'função de separação' cuja operação isola fases ou partículas de uma mistura por meios mecânicos",
  fol="∀f (MechanicalSeparationFunction(f) → SeparatingFunction(f))",
  ex_en="The function of a gravity or a three-phase separator; of a cyclone or a hydrocyclone; of a filter or a strainer; of a centrifuge.",
  ex_pt="A função de um separador gravitacional ou trifásico; de um ciclone ou hidrociclone; de um filtro ou filtro-cesto; de uma centrífuga.",
  note_pt="Função de gênero da COPI: redefine a categoria 'separação mecânica' do FOMI 2026 pela função. Refina 'separar' (Branch) da Functional Basis: dividir (separador), remover (filtro). Um refervedor porta esta função além da de mudança de fase (regra 4 do ODR-025): duas funções de primárias disjuntas sem inconsistência.",
  rat_en="Primitive: see mass transfer function; the two separation genera are told apart by mechanism, not by signature.",
  rat_pt="Primitiva: ver função de transferência de massa; os dois gêneros de separação se distinguem pelo mecanismo, não pela assinatura.",
  sources=["ODR-025 §4", "ODR-011 (MechanicalSeparation, superseded)", MCCABE], adapted=MCCABE + " (mechanical separations)")
A("ChemicalReactionFunction",
  nld_pt="função de conversão cuja transformação interna muda a composição química do operando material",
  sfd_en="if f is a 'chemical reaction function' then f is a 'conversion function' whose internal 'transformation' is a 'material transformation' that changes the chemical composition of the operand",
  sfd_pt="se f é uma 'função de reação química' então f é uma 'função de conversão' cuja 'transformação' interna é uma 'transformação de material' que muda a composição química do operando",
  fol="∀f (ChemicalReactionFunction(f) → ConversionFunction(f) ∧ ∀p (realizedIn(f,p) → ∃t (MaterialTransformation(t) ∧ hasOccurrentPart(p,t))))",
  ex_en="The function of a reactor; of a hydrotreater; of a sulphur recovery unit's reaction furnace; of a fuel cell (chemical → electrical energy).",
  ex_pt="A função de um reator; de uma unidade de hidrotratamento; do forno de reação de uma unidade de recuperação de enxofre; de uma célula a combustível (energia química → elétrica).",
  note_pt="Função de gênero da COPI: redefine a categoria 'reação química' do FOMI 2026 pela função. Refina 'converter' da Functional Basis com uma transformação de material; a composição é a differentia, dita em linguagem natural.",
  rat_en="Primitive: 'change of chemical composition' is a property of the transformation stated in natural language; COPI does not model reactions or species.",
  rat_pt="Primitiva: 'mudança de composição química' é uma propriedade da transformação dita em linguagem natural; a COPI não modela reações nem espécies químicas.",
  sources=["ODR-025 §4", "ODR-011 (ChemicalReaction, superseded)", MCCABE], adapted=MCCABE)
A("PhaseChangeFunction",
  nld_pt="função de conversão cuja transformação interna muda a fase do operando material",
  sfd_en="if f is a 'phase change function' then f is a 'conversion function' whose internal 'transformation' is a 'material transformation' that changes the phase of the operand",
  sfd_pt="se f é uma 'função de mudança de fase' então f é uma 'função de conversão' cuja 'transformação' interna é uma 'transformação de material' que muda a fase do operando",
  fol="∀f (PhaseChangeFunction(f) → ConversionFunction(f) ∧ ∀p (realizedIn(f,p) → ∃t (MaterialTransformation(t) ∧ hasOccurrentPart(p,t))))",
  ex_en="The function of a reboiler or a vaporizer (liquid → vapour); of a condenser (vapour → liquid); of a flash drum; of an evaporator.",
  ex_pt="A função de um refervedor ou vaporizador (líquido → vapor); de um condensador (vapor → líquido); de um vaso de flash; de um evaporador.",
  note_pt="Função de gênero da COPI: redefine a categoria 'mudança de fase' do FOMI 2026 pela função. Refina 'converter' da Functional Basis; é o que distingue um refervedor de um trocador (que só transfere calor).",
  rat_en="Primitive: the phase is a quality of the operand, not modelled as a flow type; the differentia is stated in natural language.",
  rat_pt="Primitiva: a fase é uma qualidade do operando, não modelada como tipo de fluxo; a differentia é dita em linguagem natural.",
  sources=["ODR-025 §4", "ODR-011 (PhaseChange, superseded)", MCCABE], adapted=MCCABE)
