"""Coverage of the Functional Basis (Hirtz et al. 2002) by copi-core-v2.

hirtz-coverage.csv has one row per term of Table 5 (functions) and Table 3 (flows), plus the declared
extensions of COPI. Columns: tabela, caminho, nivel, status, iri, rotulo, observacao.

status: adotada      the class renders the term as Hirtz gives it
        adaptada     the class renders the term in another BFO category or with another extension (see observacao)
        não adotada  no class; a corpus term that needs it must raise an alert, never fall back to a neighbour
        extensão     not in Hirtz: declared by COPI (no Functional Basis path on the class)

check.py verifies the table against the ontology. resolve() is the entry point for the export: it returns the IRI
of an adopted term and raises NotAdopted otherwise, so that an unadopted flow is never approximated silently.
"""
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
STATUSES = ("adotada", "adaptada", "não adotada", "extensão")

class NotAdopted(LookupError):
    """The Functional Basis term exists in Hirtz but copi-core-v2 has no class for it (or it is unknown)."""

def load(path=None):
    with open(path or os.path.join(HERE, "hirtz-coverage.csv"), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def resolve(caminho, rows=None):
    """IRI (CURIE) of the class that renders the Functional Basis term at `caminho`, e.g. 'Flow/Material/Liquid'."""
    for r in rows or load():
        if r["caminho"] == caminho:
            if r["status"] in ("adotada", "adaptada"):
                return r["iri"]
            raise NotAdopted(f"{caminho}: {r['status']} in copi-core-v2 — create the class (and update hirtz-coverage.csv) "
                             f"before a term uses it; do not approximate to the nearest adopted term")
    raise NotAdopted(f"{caminho}: not a term of the Functional Basis tables (see hirtz-coverage.csv)")
