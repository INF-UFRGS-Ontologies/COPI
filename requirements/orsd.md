# Ontology Requirements Specification Document

**COPI – Core Ontology of Petroleum Installations**

**Author(s):** Nicolau Oyhenard dos Santos
**Creation date:** 2026-02-02
**Project(s) related:** COPI Ontology, PhD Research Project

---

## 1. Purpose

The purpose of the COPI ontology is to provide a core ontology for petroleum production plants, supporting semantic interoperability across heterogeneous industrial standards and datasets.

COPI aims to act as a domain-level semantic backbone, specializing BFO and IOF-Core, and enabling alignment with standards such as ISO 15926-4, ISO 14224, CFIHOS, and DEXPI.

---

## 2. Scope

The scope of COPI includes:
* Material entities composing petroleum production plants;
* Functional locations used to organize and manage physical assets;
* Information artifacts describing assets, locations, and plant documentation.

The ontology explicitly excludes:
* Real-time control logic;
* Numerical simulation models;
* Business process modeling beyond asset lifecycle representation.

---

## 3. Implementation Language (optional)

COPI is implemented using **OWL 2 DL**, following best practices for ontology engineering and reasoning compatibility.

---

## 4. Intended End-Users (optional)

* Ontology engineers
* Asset integrity engineers
* Maintenance engineers
* Industrial data integration specialists

---

## 5. Intended Uses

The intended uses of COPI include:
* Semantic integration of heterogeneous plant data sources;
* Support for querying asset hierarchies and functional locations;
* Alignment and comparison between industrial standards;
* Serving as a semantic foundation for domain-specific application ontologies.

---

## 6. Ontology Requirements

### a. Non-Functional Requirements

| ID | Requirement |
| :--- | :--- |
| **NFR-01** | The ontology shall be aligned with BFO as a top-level ontology. |
| **NFR-02** | The ontology shall reuse IOF-Core as a mid-level ontology. |
| **NFR-03** | The ontology shall be modular and extensible. |
| **NFR-04** | The ontology shall support FAIR principles. |
| **NFR-05** | The ontology shall be logically consistent under OWL 2 DL reasoning. |

### b. Functional Requirements

#### Competency Questions

| ID | Competency Question |
| :--- | :--- |
| **CQ-01** | Which material entities compose a given petroleum production plant? |
| **CQ-02** | Which equipment is located at a given functional location? |
| **CQ-03** | Which information artifacts describe a specific asset or location? |
| **CQ-04** | How are functional locations hierarchically organized within a plant? |
| **CQ-05** | How is this material entity classified according to external reference data libraries (e.g., ISO 15926-4, CFIHOS RDL)? |
| **CQ-06** | What are the topological connections (inlet/outlet) between this equipment and other material entities? |
| **CQ-07** | What are the required design properties (e.g., design pressure, design temperature) for a specific functional location? |
| **CQ-08** | Does the installed material entity satisfy the technical requirements of its functional location? |

#### Domain Statements

| ID | Statement |
| :--- | :--- |
| **DS-01** | Every material entity in a petroleum production plant is associated with at least one functional location. |
| **DS-02** | Functional locations may group multiple material entities. |
| **DS-03** | Information artifacts describe material entities, functional locations, or both. |

---

## 7. Pre-Glossary of Terms (optional)

### a. Terms from Competency Questions
* Material entity
* Functional location
* Information artifact

### b. Terms from Answers
* Equipment
* Production unit
* Plant documentation

### c. Objects
* Petroleum production plant
* Asset hierarchy