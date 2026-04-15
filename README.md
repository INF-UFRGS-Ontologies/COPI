# COPI — Core Ontology of Petroleum Installations

**IRI:** `https://www.inf.ufrgs.br/ontologies/copi`  
**License:** [MIT](LICENSE)

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

---

## Repository structure

```
COPI/
├── src/ontology/       # Ontology source (OWL, imports, mirrors, Makefile)
├── docs/               # Static HTML documentation, class pages
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
