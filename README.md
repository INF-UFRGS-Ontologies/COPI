# COPPP — Core Ontology for Petroleum Production Plants

**COPPP** is a domain ontology focused on **Petroleum Production Plants**, designed as a **core semantic artifact** to support interoperability, reasoning, and data integration across heterogeneous industrial standards and data sources.

This repository is maintained under the scope of academic research at **UFRGS**, with a strong emphasis on **formal ontology engineering**, **semantic interoperability**, and **industrial applicability**.

---

## 🎯 Scope and Motivation

Industrial petroleum production environments rely on multiple overlapping standards and data models (e.g., ISO 15926, DEXPI, CFIHOS), each addressing specific viewpoints such as engineering design, operations, or asset management.

COPPP aims to:

- Provide a **precisely scoped core ontology** for petroleum production plants
- Act as a **semantic bridge**, not a replacement, for existing standards
- Enable **formal reasoning**, querying, and integration over heterogeneous data sources
- Support both **virtualized** and **materialized** knowledge graph deployments

COPPP is **not intended** to fully replicate or reimplement any existing industrial standard.

---

## 🧩 Interoperability Targets

COPPP is designed to be **correlatable and alignable** with the following standards and initiatives:

- **ISO 15926-4** — Reference Data Library (RDL)
- **DEXPI** — Data Exchange in the Process Industry
- **CFIHOS** — Capital Facilities Information Handover Specification
- **POSC Caesar Association**
- **IDO (Industrial Data Ontologies)**
- **Energistics standards**
- **PPDM (Professional Petroleum Data Management)**

Alignments are expected to be:
- *partial*
- *explicit*
- *use-case driven*

---

## 🧠 Ontology Design Principles

The development of COPPP follows these principles:

- **Strict domain scoping**
- **Clear separation between core concepts and extensions**
- **OWL 2 DL compliance**, enabling automated reasoning
- **Minimal ontological commitment**, favoring reuse and alignment
- **Compatibility with Ontology Development Kit (ODK)**
- **Methodological grounding**, aligned with LOT (Linked Ontology Toolset)

---

## 📁 Repository Structure

COPPP/
├── src/            # Ontology source files (OWL, TTL, imports)
├── docs/           # Documentation, scope definitions, ORSD, diagrams
├── requirements/   # Competency questions, requirements, constraints
├── tests/          # Ontology tests, SPARQL queries, reasoning checks
├── LICENSE         # MIT License
└── README.md

---

## 🛠 Tooling and Technologies

- **OWL / RDF**
- **SPARQL**
- **Ontology Development Kit (ODK)**
- **Reasoners** (e.g., HermiT, Pellet)
- **Virtual Knowledge Graphs (Ontop)**

---

## 📌 Intended Use Cases

- Semantic integration of industrial plant data
- Knowledge graph construction (virtual or materialized)
- Formal reasoning over plant structure and assets
- Support for NLP-to-SPARQL and neuro-symbolic pipelines
- Academic research in applied ontologies and semantic technologies

---

## 📄 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for details.

---

## 📬 Contact and Attribution

This ontology is developed and maintained as part of academic research at **Universidade Federal do Rio Grande do Sul (UFRGS)**.

Contributions, discussions, and alignment proposals are welcome via issues and pull requests.

