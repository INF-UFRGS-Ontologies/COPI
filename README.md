# COPI — Core Ontology of Petroleum Installations

**IRI:** `https://www.inf.ufrgs.br/ontologies/copi`  
**License:** [CC BY 4.0](LICENSE)

COPI is a domain-core ontology for petroleum production plants. It provides a domain-level semantic backbone by specializing [BFO 2020](https://github.com/bfo-ontology/bfo-2020) and [IOF-Core](https://spec.industrialontologies.org/ontology/202601/core/Core/), supporting semantic interoperability across heterogeneous industrial standards and datasets.

---

## Scope

**In scope:**

- Material entities composing petroleum production plants
- Functional locations used to organize and manage physical assets
- Information artifacts describing assets, locations, and plant documentation

**Out of scope:**

- Real-time control logic
- Numerical simulation models
- Business process modeling beyond asset lifecycle representation

---

## Intended uses

- Semantic integration of heterogeneous plant data sources
- Support for querying asset hierarchies and functional locations
- Alignment and comparison between industrial standards
- Serving as a semantic foundation for domain-specific application ontologies

**Intended end-users:** ontology engineers, asset integrity engineers, maintenance engineers, and industrial data integration specialists.

---

## Method — enriching flat reference data with BFO/IOF-Core axioms

Standards such as ISO 15926-4, CFIHOS, and DEXPI each provide equipment classes for the same physical
things — a pump, a valve, a separator — but their definitions are natural-language tautologies with no
formal axioms. ISO 15926-4's own definition of `PUMP` is representative: *"A `<PUMP>` is a
`<FunctionalObject>` that is capable of `<PUMPING>` but may require parts and subsystems for that
capability."* This tells a reasoner nothing about what the class necessarily has or how it differs from
a compressor or a valve, and it gives no principled way to compare the same class across standards.

COPI classes are produced by an **enrichment method** that grounds each equipment universal in [BFO
2020](https://github.com/bfo-ontology/bfo-2020), using [IOF-Core](https://spec.industrialontologies.org/ontology/202601/core/Core/)
as the mid-level vocabulary. Two constructs do the work:

- **Identity-giving function** — a subtype of `DesignedFunction` that grounds the identity of the
  equipment universal in its designed purpose, rather than in an arbitrary taxonomic label.
- **Process participation signature** — the typed pattern of inputs, outputs, and transformation that
  the process realizing that function exhibits.

Together these give a **principled disjointness criterion**: two equipment universals are disjoint when
their signatures are physically incompatible, not by stipulation. In practice, each equipment cluster is
axiomatized in five steps — identity-giving function, genus (most specific known superclass), differentia
(the OWL restriction distinguishing it from genus siblings), necessary parts
(`hasComponentPartAtAllTimes` restrictions universal to every instance), and the process participation
signature — using [COPIeditor](https://github.com/n0santos/COPIeditor), an LLM-assisted axiomatization
workbench built for this project, with every proposal reviewed by a domain expert before release. See
[`PIPELINE.md`](PIPELINE.md) for the full editing-to-release workflow.

The method is described in full, and evaluated against ten petroleum-production equipment types, in the
paper below.

---

## Publications

### Axiomatizing Industrial Reference Data

> **Nicolau Oyhenard dos Santos, Cauã Antunes, Mara Abel, João Netto.**
> *Axiomatizing Industrial Reference Data: A BFO/IOF-Core Enrichment of ISO 15926-4 Equipment Classes.*
> To appear in *Formal Ontology in Information Systems (FOIS 2026)*, Frontiers in Artificial
> Intelligence and Applications, IOS Press. (Accepted; camera-ready submitted — a DOI/link will be
> added once the proceedings are published.)

The paper presents the enrichment method summarized above and applies it to ten equipment types central
to petroleum production (pump, valve, separator, heat exchanger, compressor, sensor, pressure vessel,
filter, pipe, column), producing a proof-of-concept OWL 2 DL ontology with 95 named classes, 16
disjointness axioms, and SKOS links to ISO 15926-4, DEXPI, and CFIHOS — evaluated through consistency
checking, instance-level classification tests, and competency questions. The full COPI ontology in this
repository extends that proof of concept to the broader equipment population described below.

```bibtex
@inproceedings{santos2026axiomatizing,
  author    = {Santos, Nicolau O. and Antunes, Cau{\~a} and
               Abel, Mara and Netto, Jo{\~a}o},
  title     = {Axiomatizing Industrial Reference Data: A {BFO}/{IOF-Core}
               Enrichment of {ISO}~15926-4 Equipment Classes},
  booktitle = {Formal Ontology in Information Systems (FOIS 2026)},
  series    = {Frontiers in Artificial Intelligence and Applications},
  publisher = {IOS Press},
  year      = {2026},
  note      = {Forthcoming}
}
```

### An Ontology Design Pattern for Functional Locations

> **Nicolau Oyhenard dos Santos, Haroldo Rojas, Cauã Roca Antunes, Fabrício H. Rodrigues, Régis Romeu,
> Rafael H. Petry, Mara Abel, João César Netto.**
> *An Ontology Design Pattern for Functional Locations in Industrial Asset Management.*
> To appear in *Formal Ontology in Information Systems (FOIS 2026)*, Frontiers in Artificial
> Intelligence and Applications, IOS Press. (Accepted; to be presented 21–25 September 2026 in
> Vitória, ES, Brazil — a DOI/link will be added once the proceedings are published.)

A companion FOIS 2026 paper proposing a reusable BFO/IOF-aligned ODP for functional locations in
industrial asset management. The pattern's ontology is published separately at
[`inf.ufrgs.br/ontologies/odp/functional-location`](https://www.inf.ufrgs.br/ontologies/odp/functional-location)
([Zenodo DOI](https://doi.org/10.5281/zenodo.21072929)) and remains the citable form of the pattern.
It has since been migrated into COPI as the **`copi-floc`** module — see
[Functional location module](#functional-location-module-copi-floc) below.

```bibtex
@inproceedings{santos2026functionallocations,
  author    = {Santos, Nicolau O. and Rojas, Haroldo and
               Antunes, Cau{\~a} Roca and Rodrigues, Fabr{\'i}cio H. and
               Romeu, R{\'e}gis and Petry, Rafael H. and Abel, Mara and
               Netto, Jo{\~a}o C{\'e}sar},
  title     = {An Ontology Design Pattern for Functional Locations in
               Industrial Asset Management},
  booktitle = {Formal Ontology in Information Systems (FOIS 2026)},
  series    = {Frontiers in Artificial Intelligence and Applications},
  publisher = {IOS Press},
  year      = {2026},
  note      = {Forthcoming}
}
```

See also [`CITATION.cff`](CITATION.cff) for citing the ontology artefact itself.

---

## Functional location module (`copi-floc`)

`copi-floc` carries the functional-location pattern inside COPI. A functional location is a
persistent **site** whose boundaries are fixed by delimiting material entities, not by the
equipment occupying it, which is what lets a position keep its identity, its history and its data
across equipment replacement.

The module keeps four concerns apart: the site and its hierarchy; the two identifiers that
designate it (the location code — *where* in the breakdown — and the equipment tag — *what kind*
of item is expected); the specification stating what the position requires; and the installation
periods through which artifacts occupy the site over time.

It imports **BFO 2020 and IOF-Core 202603 only** — no equipment classes, no observation
vocabulary, no maintenance records — so it can be imported on its own by ontologies outside oil
and gas, and it is also merged into the `copi-*` release artefacts as a COPI component.

| Resource | Location |
|---|---|
| Term reference (EN/PT-BR) | [`copi/docs/copi-floc.html`](https://www.inf.ufrgs.br/ontologies/copi/docs/copi-floc.html) |
| Standalone artefact | `copi-floc.owl` / `copi-floc.ttl` |
| Editable component | `src/ontology/components/copi-floc.ttl` |
| Correspondence with ODP-FL v0.8 | `src/ontology/copi-floc-odp-map.sssom.tsv` |

The module is **provisional** (`iof-av:maturity iof-ind:Provisional`). Two gaps are recorded in
the header of the component file and are not resolved: identifiers still commit to a designated
site, which misrepresents a position that is designed but never built; and the content of a
position's requirement — a class plus property-value pairs with units and a revision, in the
shape CFIHOS and SAP PM classification give it — is not modelled yet.

Regenerate the term reference after editing the component:

```bash
python3 scripts/gen_floc_docs.py           # writes docs/copi-floc.html
python3 scripts/gen_floc_docs.py --check   # fails if the page is stale
```

---

## Standards alignment

COPI is designed to be correlatable and alignable with:

| Standard | Description |
|---|---|
| ISO 15926-4 | Reference Data Library (RDL) |
| ISO 14224 | Reliability and maintenance of equipment |
| CFIHOS | Capital Facilities Information Handover Specification |
| DEXPI | Data Exchange in the Process Industry |
| POSC Caesar RDL | Reference Data Library |

---

## Release artefacts

Artefacts are published at `https://www.inf.ufrgs.br/ontologies/copi/` and generated automatically on every push to `main` via GitHub Actions using [ODK](https://github.com/INCATools/ontology-development-kit).

| File | Description |
|---|---|
| `copi.owl` / `copi.ttl` | Primary release (full) |
| `copi-base.owl` / `copi-base.ttl` | Base artefact (no imports merged) |
| `copi-full.owl` / `copi-full.ttl` | Full artefact (imports merged) |
| `copi-simple.owl` / `copi-simple.ttl` | Simplified artefact |
| `copi-floc.owl` / `copi-floc.ttl` | Functional location module, standalone (imports **not** merged) |

---

## Repository structure

```
COPI/
├── src/ontology/       # Ontology source (OWL, imports, mirrors, Makefile)
├── scripts/            # Helper scripts (FOL enrichment, module documentation)
├── docs/               # Static HTML documentation, class pages, module reference
├── requirements/       # ORSD, competency questions (cqs.csv)
├── LICENSE
└── README.md
```

---

## Development

This ontology is developed using the [Ontology Development Kit (ODK)](https://github.com/INCATools/ontology-development-kit) and follows the [LOT methodology](https://lot.linkeddata.es/).

To regenerate release artefacts locally:

```bash
cd src/ontology
./run.sh make prepare_release IMP=false PAT=false MIR=false COMP=false
```

See [`src/ontology/README-editors.md`](src/ontology/README-editors.md) for editor setup instructions.

For a full description of the development and release pipeline — from editing classes in COPIeditor, through the automated GitHub Actions workflow, to IRI deployment on the UFRGS server — see **[`PIPELINE.md`](PIPELINE.md)**.

---

## Contributors

- Nicolau Oyhenard dos Santos (author)
- Haroldo Rojas
- Mara Abel
- Cauã Roca Antunes

Universidade Federal do Rio Grande do Sul (UFRGS) — Instituto de Informática
