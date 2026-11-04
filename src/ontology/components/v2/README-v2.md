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
2. **`signal transmission function` (COPI_0000030)** não pode ser reparentada sob *Transferring* (Channel): no vocab ela é filha de *instrumentation function*, que no v2 vira *Sensing* (Signal), e as primárias são disjuntas. Fica sob Sensing (o transmissor sente e emite).

## O que o v2 faz com o que já existe (mesmos IRIs)

- Os nove dispositivos (COPI_0000016–24) viram classes definidas `MaterialArtifact ⊓ ∃bearerOf.<função de gênero>`; os oito tipos de operação (0000003–10) viram classes definidas `Process ⊓ ∃realizes.<função de gênero>`; as folhas (11, 12, 13, 14, 89) ficam como subclasses e recebem equivalência no export.
- `copi:Operation ⊑ PlannedProcess` (COPI_0000001) **sai**.
- `Instrument` (0000091) ≡ `MaterialArtifact ⊓ ∃bearerOf.SignallingFunction`; `MeasurementInstrument` (0000024) ≡ … `SensingFunction` com `SignalFlow` que concretiza `MeasurementContent` (fecha o ODR-023 pela leitura A).
- Funções do vocab reparentadas (assertado no v2; a declaração continua no vocab): containment (25) ⊑ Storing; flow control (26) ⊑ Regulating; indication (28) ⊑ Indicating; instrumentation (29) ⊑ Sensing; safety relief (32) ⊑ Regulating. **Ajuste pendente em `copi-vocab.ttl`:** remover de COPI_0000029 o `realizedIn some/only iof:MeasurementProcess`; e os processos 0000035/36 (`⊑ iof:MeasurementProcess`) devem passar a `⊑ bfo:Process`.

## Pendências antes de trocar o arquivo congelado

- Ajuste do `copi-vocab.ttl` acima.
- `copi-enriched.owl`: export v2 (funções de termo sob as funções de gênero; `realizedIn only` com fluxos; partições; sem os 16 axiomas par a par).
- Guard novo: `signal transmission function` sob Sensing (já é); nenhuma função de termo sem gênero primário.
- ODR-024/025/026 (em `COPIeditor/docs/ontology-decisions/`).
