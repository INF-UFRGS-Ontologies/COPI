# copi-core v2 — rascunho verificado (2026-11-03)

Arquivos nesta pasta (`src/ontology/components/v2/`), gerados a partir da spec "Spec copi-core v2" (rev. 2026-11-03c, doc do projeto copi-ufo). **Não substituem ainda** `components/copi-core.ttl` (congelado, FOMI 2026); a troca é o passo seguinte, junto com o ajuste de `copi-vocab.ttl` listado abaixo.

| Arquivo | O que é |
|---|---|
| `copi-core-v2.ttl` | a ontologia core v2: 88 classes, 6 propriedades de objeto, 4 de anotação; ids COPI_0001000–0001071 (faixa nova, `copi-idranges` range 1). Anotada no padrão do `copi-core.ttl` congelado (ver abaixo) |
| `gen.py` | gerador do TTL (fonte de verdade para regenerar; `python3 -I gen.py > copi-core-v2.ttl 2> ids.txt`; falha com `MISSING ANNOTATIONS` se alguma entidade ficar sem campo) |
| `ann_refs.py`, `ann_functions.py`, `ann_flows.py`, `ann_ops.py` | tabelas de anotação consumidas por `gen.py`: referências bibliográficas; funções (raiz, 8 primárias, 20 secundárias, 6 gêneros); fluxos, propriedades, energia, sinal; dispositivos, instrumentos, operações, folhas, propriedades de anotação e cabeçalho |
| `ids.txt` | mapa nome → id gerado |
| `test-terms.ttl` | termos de teste (bomba, compressor, reboiler, trocador, transmissor de pressão, controlador, linha traceada) e uma instância de bomba com fluxos, para o reasoner |
| `check.py` | as 20 verificações: 19 inferências sobre `reasoned-test.owl` + o padrão de anotação sobre `copi-core-v2.ttl` |

## Como foi verificado

ROBOT 1.9.8 + HermiT, no container, sobre `copi-core-v2.ttl` + `copi-vocab.ttl` (sem o `owl:imports`) + mirror `iof-core.owl` 202603 (sem imports) + `bfo-2020.ttl` + `ro-extracted.owl` do MENO:

```
grep -v owl:imports copi-core-v2.ttl > core-noimp.ttl        # o cabeçalho importa BFO 2020 e IOF Core; offline, use as cópias locais
robot merge -i core-noimp.ttl -i vocab-noimp.ttl -i iof-noimp.owl -i bfo-2020.ttl -i ro-extracted.owl -o merged.owl
robot reason -i merged.owl --reasoner HermiT --axiom-generators "SubClass" -o reasoned.owl          # passo 0+1
robot merge -i merged.owl -i test-terms.ttl -o merged-test.owl
robot reason -i merged-test.owl --reasoner HermiT --axiom-generators "SubClass ClassAssertion PropertyAssertion" -o reasoned-test.owl
python3 -I check.py                                                                                   # 20/20
```

## Padrão de anotação (2026-11-04)

Igual ao do `copi-core.ttl` congelado, verificado pelo `check.py` em todas as 98 entidades (classes, propriedades de objeto, propriedades de anotação): `rdfs:label`, `iof-av:naturalLanguageDefinition` e `rdfs:comment`, `iof-av:semiFormalNaturalLanguageAxiom`/`Definition`, `skos:example` (três equipamentos da cobertura), `iof-av:explanatoryNote` — todos em en e pt-br; `iof-av:firstOrderLogicAxiom`/`Definition`; `iof-av:isPrimitive` com `primitiveRationale` bilíngue nas primitivas; `iof-av:adaptedFrom`; `dcterms:source` com o ODR e a referência completa (Hirtz et al. 2002 com tabela/apêndice, Stone & Wood 2000, Borgo et al. 2011, Vermaas 2007, MENO, OEO, IOF Core 202603, BFO 2020, RO, ISA 5.1, ISO 14224, McCabe-Smith-Harriott, Mizoguchi-Kitamura-Borgo 2016); `rdfs:isDefinedBy`. Cabeçalho com `versionIRI`, títulos, `comment` e `usageNote` bilíngues, criadores, licença, `maturity`, fontes. O esquema SKOS `fb:` traz os 8 + 20 + 24 termos com `prefLabel` en/pt-br e a definição de Hirtz nos primários e secundários.

Resultado: hierarquia de propriedades regular; nenhuma classe insatisfazível; 18/18 inferências esperadas (`MeasurementInstrument ⊑ Instrument`; transmissor ⊑ instrumento de medição; controlador ⊑ instrumento e não ⊑ instrumento de medição; bomba/compressor ⊑ momentum-transfer device; reboiler em dois gêneros sem inconsistência; linha traceada coexistindo com trocador; cadeias `hasInflowParticipant`/`hasOutflowParticipant` disparando na instância; `proc1` classificado como momentum transfer e conversion operation).

## Dois achados do reasoner que mudaram a spec

1. **Regularidade.** `hasInflowParticipant ⊑ has participant` + cadeia `hasInflow ∘ has participant ⊑ hasInflowParticipant` é cíclico (HermiT: "not regular"). As duas propriedades de cadeia ficam **sem** `subPropertyOf`; `has participant` e `iof:hasInput/hasOutput` são materializados delas no export por CONSTRUCT.
2. **`signal transmission function` (COPI_0000030)** não pode ser reparentada sob *Transferring* (Channel): no vocab ela é filha de *instrumentation function*, que no v2 vira *Sensing* (Signal), e as primárias são disjuntas. Ficou sob Sensing até 2026-11-18, quando passou para *Processing*, que também está sob Signal (ver a revisão dessa data).

## O que o v2 faz com o que já existe (mesmos IRIs)

- Os nove dispositivos (COPI_0000016–24) viram classes definidas `MaterialArtifact ⊓ ∃bearerOf.<função de gênero>`; os oito tipos de operação (0000003–10) viram classes definidas `Process ⊓ ∃realizes.<função de gênero>`; as folhas (11, 12, 13, 14, 89) ficam como subclasses e recebem equivalência no export.
- `copi:Operation ⊑ PlannedProcess` (COPI_0000001) **sai**.
- `Instrument` (0000091) ≡ `MaterialArtifact ⊓ ∃bearerOf.SignallingFunction`; `MeasurementInstrument` (0000024) ≡ … `SensingFunction` com `SignalFlow` que concretiza `MeasurementContent` (fecha o ODR-023 pela leitura A).
- Funções do vocab reparentadas (assertado no v2; a declaração continua no vocab): containment (25) ⊑ Storing; flow control (26) ⊑ Regulating; indication (28) ⊑ Indicating; instrumentation (29) ⊑ Sensing; safety relief (32) ⊑ Regulating. **Ajuste pendente em `copi-vocab.ttl`:** remover de COPI_0000029 o `realizedIn some/only iof:MeasurementProcess`; e os processos 0000035/36 (`⊑ iof:MeasurementProcess`) devem passar a `⊑ bfo:Process`.

## Pendências antes de trocar o arquivo congelado

- Ajuste do `copi-vocab.ttl` acima.
- `copi-enriched.owl`: export v2 (funções de termo sob as funções de gênero; `realizedIn only` com fluxos; partições; sem os 16 axiomas par a par).
- Guard novo: `signal transmission function` sob Processing (desde 2026-11-18); nenhuma função de termo sem gênero primário.
- ODR-024/025/026 (em `COPIeditor/docs/ontology-decisions/`).
- Subclasses da `containment function` nos terciários: storage function (COPI_0000197) fica sob a 0025; pressure containment function (COPI_0000381) vai para `containing function` (COPI_0001091); gravity collection function (COPI_0000754) e sample collection function (COPI_0000777) vão para `collecting function` (COPI_0001092). A migração do banco do editor está commitada (`COPIeditor/migration/odr024_fb_tertiary_parents.py`) e **só é aplicada quando o export v2 virar o padrão** do `regen_enriched_owl.py` e do `verify_owl.sh`: no caminho v1 o alocador cunharia números novos, duplicatas da 1091 e da 1092.

## Revisão de 2026-11-17 (baixo risco)

Duas mudanças saídas da revisão da assinatura do passo 5 (`COPIeditor/eval/fb-signature-*`):

1. **Identidade.** O cabeçalho e a anotação `identity function` passam a admitir uma diferença declarada fora da assinatura (construtiva, posicional ou paramétrica) quando tipos irmãos têm a mesma assinatura. Só anotação. A emenda do ODR-025 §1 está pendente.
2. **Control valves.** `process-controlled flow function` (COPI_0000027) deixa de ser assertada sob *Regulating*: toda control valve a porta, e a on-off control valve aciona e bloqueia mas não regula. Ela continua sob *Magnitude control* via `flow control function`. O que as control valves têm em comum é o sinal de controle, agora assertado no processo de realização: `process-controlled flow process` (COPI_0000033) ⊑ ∃hasInflow.(SignalFlow ⊓ ∃concretizes.ControlContent).

Verificação: mesma receita acima, com ROBOT 1.9.8 + HermiT. O commit anterior deu 20/20 e este dá 25/25; as cinco verificações novas do `check.py` cobrem a função das control valves (não ⊑ regulating, ⊑ magnitude control, função on-off satisfazível e fora de regulating, função moduladora sob regulating). Os guards 02 e 06 não são afetados, porque leem `control valve ⊑ valve` e `COPI_0000027 ⊑ flow control function`, que não mudaram.

Fica de fora, por depender de verificação ainda aberta: o novo rótulo da função (candidato: "final control function", termo da ISO 15926-4), o transmissor sob *Processing*, os campos novos da anotação `signature` e a tabela de fluxos do Hirtz.

## Revisão de 2026-11-17 — Functional Basis só em OWL

Decisão: a ontologia fica num formalismo só. O esquema SKOS `fb:` paralelo saiu.

- **Origem no Hirtz em cada classe.** A anotação nova `Functional Basis term` (COPI_0001072) guarda o caminho do termo na sua tabela: `Function/Branch/Separate/Remove`, `Flow`. Ela substitui o `skos:closeMatch` para os conceitos `fb:`. As 53 classes de função e a classe `flow` a carregam.
- **Os 24 terciários viraram classes**, subclasses das suas secundárias (COPI_0001073 a COPI_0001096). Foram alocados depois de todas as entidades anteriores, então nenhum IRI existente mudou (`ids.txt`). As definições adaptam o Apêndice B do Hirtz à forma "function to …" das secundárias.
- **Regra de asserção.** Uma função de termo é afirmada no terciário só quando a sua definição traz o termo; caso contrário fica na secundária. A `containment function` do copi-vocab (COPI_0000025) **não** desce para `containing function`, apesar do nome: as subclasses dela no `copi-enriched` cobrem Store (storage function), Contain (pressure containment function) e Collect (gravity collection function, sample collection function). Ela fica sob `storing function`, como já estava. Reparentar as quatro subclasses nos terciários e renomear a 0025 ficam para o lado do editor.
- **Tabela de cobertura.** `hirtz-coverage.csv` tem uma linha por termo do Hirtz com status `adotada`, `adaptada`, `não adotada` ou `extensão`. O `check.py` confere a tabela contra a ontologia, e `hirtz_coverage.resolve()` devolve o IRI de um termo adotado e levanta `NotAdopted` nos outros casos. O export deve usá-lo para nunca aproximar um termo não adotado.

Um exemplo foi corrigido para acompanhar os correspondentes do próprio Hirtz: filtro e filtro-cesto passam de *remove* para *extract* ("filter, strain" estão sob Extract; "cut, drill" sob Remove). Vale conferir se essa leitura é a desejada.

Verificação: ROBOT 1.9.8 + HermiT, 36/36 no `check.py` (nenhuma classe insatisfazível; 123 entidades no padrão de anotação). O `check.py` agora precisa de `hirtz_coverage.py` e `hirtz-coverage.csv` ao lado.

## Revisão de 2026-11-17 — fluxos, sensores e extensões à Functional Basis

**Fluxos de material: reaproveita o copi-vocab.** Gás, líquido, sólido e mistura do Hirtz são as porções de matéria do copi-vocab, participantes do `material flow`, e não subclasses de fluxo. O caminho do Hirtz é assertado aqui sobre COPI_0000038, 0039, 0040 e 0808. A única classe nova é `portion of mixture` (COPI_0000808, no copi-vocab): o Mixture do Hirtz inclui misturas com sólido (dryer e filter press na amostra) e a COPI_0000044 só cobria mistura fluida. A 0044 passa a ser subclasse das duas, `portion of fluid` e `portion of mixture`, e o `material flow` aceita a classe nova como participante. Convenção de nome para o que é incontável: "portion of X" (Arp, Smith & Spear). Dois rótulos mudaram no copi-vocab, com o antigo guardado em `iof-av:synonym`:

| IRI | Antes | Agora |
|---|---|---|
| COPI_0000044 | fluid mixture | portion of fluid mixture |
| COPI_0000393 | fuel portion | portion of fuel |

**Resto da tabela de fluxos: sob demanda.** `hirtz-coverage.csv` lista as 3 classes de fluxo e os 42 termos do Hirtz: 4 adotados, 14 adaptados (tipos de energia como qualidade do portador, conteúdos de sinal como conteúdo de informação, materiais como participantes) e 28 não adotados. Classe nova só quando um termo precisar. `hirtz_coverage.resolve()` levanta `NotAdopted` para um fluxo não adotado: o export deve alertar, nunca aproximar para o valor mais próximo. `python3 -I hirtz_coverage.py` confere a tabela contra o TTL sem reasoner e sai com status 1 em caso de falha, pronto para entrar no CI.

**Sensores: a grandeza medida é uma qualidade.** Ela não é fluxo de entrada. É o alvo do `describes` do `measurement content` (COPI_0001051):

```
função do sensor ⊑ sensing function ⊓ ∃realizedIn.∃hasOutflow.(
    signal flow ⊓ ∃concretizes.(measurement content ⊓ ∃describes.(
        <qualidade X> ⊓ ∃inheresIn.portion of fluid)))
```

A anotação `signature` ganhou o campo `measured quantity`, preenchido só quando a saída é sinal de medição. Valores controlados: temperature, pressure, flow rate e level do copi-vocab (COPI_0000052–55), mais duas classes novas pedidas pela amostra, `differential pressure` (COPI_0000806) e `moisture` (COPI_0000807). As duas ficam no copi-vocab, ao lado das outras qualidades, como pede a regra de hospedagem do ODR-022 §10.3. A identidade do portador pelo lugar (o fluido "no ponto do PT-101") não entra no passo 5: fica para o módulo de functional locations.

**Extensões da COPI à Functional Basis, num lugar só.** São as linhas `extensão` de `hirtz-coverage.csv`: `portion of fluid` (o Hirtz só tem Gas e Liquid) com a sua subclasse `portion of fluid mixture`, `measurement content` (no Hirtz a medida cai em Status) e a grandeza medida. Sem elas, level element e level switch, e os elementos de pressão diferencial, nível e umidade, ficam com a mesma assinatura. As classes de extensão não carregam caminho da Functional Basis.

**Números do copi-vocab.** As três classes novas do vocab (806 a 808) seguem o registro do COPIeditor, `enrichment/ontologies/copi-context/copi-iri-map.tsv`, cujo maior número era 805. O editor não aloca números para o vocab: a linha no mapa é posta à mão, e o `PROTECTED_EXTRA` de `scripts/regen_enriched_owl.py` precisa incluir 806 a 808 e o bloco da core v2 até 1096. O alocador do editor (maior número do mapa mais um) não enxerga o bloco 1000 em diante e o alcançaria depois de 191 alocações.

Pontos abertos, registrados na tabela e não decididos aqui:

- `differential pressure` como qualidade de uma porção de fluido ou como qualidade relacional (BFO_0000145).
- A definição de `level` no copi-vocab põe o portador no vaso; o padrão do sensor o põe numa porção de fluido.
- ~~Renomear a `containment function` (COPI_0000025)~~ (2026-11-18): agora `material storing function`. Reparentar as quatro subclasses dela nos terciários continua pendente, do lado do editor.
- ~~Fundir a `detection function` (COPI_0000465, copi-enriched) na `detecting function`~~ (2026-11-18): o export v2 do editor a funde pelo `MERGED_INTO_CORE` (a 465 fica como stub depreciado ⊑ COPI_0001093) e o rótulo PT da 1093 volta a "função de detecção". Com HermiT, detector, flame detector e gas detector continuam instrument; o detector genérico deixa de ser measurement instrument, e o `detection process` (COPI_0000466) fica sem função que se realize nele.
- Outras classes de material do copi-vocab fora da convenção "portion of X": absorbent phase, rich absorbent, hydraulic fluid, exhaust gas, depleted fluid, hydrocarbon fluid, formation fluid, drilling fluid, combustion product, heat transfer medium, carrier fluid, rock cuttings.
- O `copi-enriched.owl` ainda cita os rótulos antigos em 9 definições e 3 axiomas em FOL; muda no próximo export.

Verificação: ROBOT 1.9.8 + HermiT, 48/48 no `check.py`. Os testes novos mostram que as funções de level element, level switch, elemento de pressão diferencial e elemento de umidade caem cada uma na sua classe-sonda e em nenhuma outra, que o level element é inferido como measurement instrument e que o level switch é instrument mas não measurement instrument. O `copi-core.ttl` congelado não foi tocado.

## Revisão de 2026-11-18 — transmissor sob Processing

Decisão 3 do documento de revisão, opção B.

- **`signal transmission function` (COPI_0000030) ⊑ `processing function`.** As definições do gênero transmitter falam em receber o sinal dos sensores e convertê-lo num sinal padronizado, e seis das sete espécies dizem "through an internal or external measuring element". Sentir só vale quando o elemento é interno; processar vale nos dois casos. No copi-vocab a 0030 deixa de ser subclasse de `instrumentation function`. Sensing e Processing estão as duas sob Signal, então nenhuma primária é cruzada.
- **`measurement instrument` (COPI_0000024) redefinido.** Passa a ser o artefato que porta uma função *Signalling* (antes: *Sensing*) realizada num processo cujo fluxo de sinal de saída concretiza conteúdo de medição. O transmissor com elemento externo continua instrumento de medição, pelo conteúdo do sinal que emite.
- **Inferência nova, esperada.** Um indicador cujo processo emite conteúdo de medição passa a ser instrumento de medição. Um indicador sem fluxo de sinal declarado, um controller (conteúdo de controle) e uma chave (conteúdo de status) continuam só instrumento.
- **Transmissor sem conteúdo declarado.** Uma função sob a 0030 só leva a `measurement instrument` quando o processo dela declara o conteúdo de medição. Hoje só o de pressão (COPI_0000036) declara; os de vazão, condutividade e posição dependem do export.

Do lado do editor, o processo do transmissor não volta a ser `MeasurementProcess`. O gate de ancoragem e a verificação do ODR-009 do `verify_owl.sh`, que hoje falham por isso, precisam ser portados para a v2 em vez de corrigidos no baseline.

Verificação: ROBOT 1.9.8 + HermiT, nenhuma classe insatisfazível, 53/53 no `check.py`.

## Revisão de 2026-11-18 — renome da COPI_0000025

`containment function` passa a `material storing function` ("função de armazenamento de material"), com o rótulo antigo em `iof-av:synonym`. Motivo: ela ficava ao lado de `containing function` com um nome quase idêntico sem ser o terciário Contain. O IRI não muda, e o nome legível `ContainmentFunction` do editor também não. Com isso, `containing function` recebe em português o rótulo "função de contenção" no lugar de "função de confinamento".

Não mudam: `containment device` (COPI_0000022), `material containment` (COPI_0000009) e `loss of containment` (COPI_0000015). O `copi-enriched.owl` e o banco do editor ainda citam o rótulo antigo em prosa; mudam no próximo export e no reenriquecimento.

## Revisão de 2026-11-18 — campos da anotação `signature`

Decisão 4 do documento de revisão. A anotação `signature` ganha três campos, e o `process_signature` do `enrichment.db` precisa espelhá-los.

| Campo | Valores | Regra |
|---|---|---|
| `force` | `functional`, `constructive`, `mixed` | Onde está a diferença do termo em relação ao gênero. Derivada do passo 3 do método, não preenchida à parte |
| `actuation` | um fluxo controlado de `hirtz-coverage.csv`, ou `none` | Só quando o verbo primário é Control magnitude; `not applicable` nos demais |
| `protection` | `yes`, `not declared` | `yes` só quando a definição afirma o propósito de proteção |

Regras que acompanham os campos, das nove questões do confronto às cegas:

- Regulate e Actuate exigem acionamento diferente de `none`; Change exige `none`. O sinal pode ser uma característica do próprio fluxo, e por isso a relief valve é Regulate.
- O propósito de proteção não vira verbo quando é a única evidência. Quando a definição descreve a operação sobre o fluxo (o thermowell como barreira ao fluido), o verbo fica.
- O verbo é "da espécie" quando o texto da espécie o afirma, e "herdado" só quando vem do gênero.
- Herança pela cadeia de gêneros (Questão 7): se a espécie cala, o verbo vem do primeiro gênero da cadeia cuja linha enriquecida o afirma com fonte. O nome do termo ou do gênero nunca autoriza um valor. Se nenhum gênero da cadeia tem linha, o campo fica sem valor e o gênero entra na fila de enriquecimento. Caso que fixou a regra: wafer check valve body herda Provision de valve body, que a ISO 15926-4 define como "CONTAINER that is the main fluid or pressure containing component of a valve", passando por check valve body.
- "Sem valor" na secundária significa a função afirmada na primária; no terciário, na secundária.
- Defeito de definição vale quando a definição não dá diferença nenhuma em relação ao gênero.
- A origem do sinal processado é `not applicable` fora de Signal/Process.

Correspondência com o passo 3 do método (differentia), que é a única fonte; a força e o tipo da diferença fora da assinatura são calculados a partir dele, e o passo 3 admite mais de um desfecho por termo:

| Desfecho do passo 3 | `force` | Diferença fora da assinatura |
|---|---|---|
| funcional | `functional` | nenhuma |
| estrutural | `constructive` | construtiva |
| funcional e estrutural | `mixed` | construtiva |
| de uso | a do gênero | posicional ou paramétrica |
| nenhuma | a do gênero | defeito de definição |

O terciário continua no JSON como o enriquecimento o gravou, mas a identidade lê a classe sob a qual a função de termo é afirmada. Os três campos novos estão nas linhas `extensão` de `hirtz-coverage.csv`.

Pendências que esta decisão cria:

- Acionamento manual pede `Flow/Energy/Human`, que o Hirtz tem e a core não adotou. Pela regra de fluxos sob demanda, a classe entra quando o primeiro termo com acionamento manual for enriquecido.

## ODR-027

As decisões das revisões de 2026-11-17 e 2026-11-18 estão registradas no ODR-027 (`COPIeditor/docs/ontology-decisions/`), que emenda o ODR-024 §1, o ODR-025 §1 e §5 e o ODR-023. As anotações que citavam "ODR pending" passaram a citá-lo.
