"""Coverage of the Functional Basis (Hirtz et al. 2002) by copi-core-v2, and the controlled values of the signature.

hirtz-coverage.csv has one row per term of Table 5 (functions) and Table 3 (flows), plus the declared extensions
of COPI. Columns: tabela, caminho, nivel, status, iri, rotulo, observacao.

status: adotada      the class renders the term as Hirtz gives it
        adaptada     the class renders the term in another BFO category or with another extension (see observacao)
        não adotada  no class; a corpus term that needs it must raise an alert, never fall back to a neighbour
        extensão     not in Hirtz: declared by COPI (the class carries no Functional Basis path)

Use from the export:
    resolve("Flow/Material/Liquid")   -> "copi:COPI_0000038"; raises NotAdopted for any term without a class
    flow_values()                     -> the controlled values of the flow fields of a signature
    measured_quantities()             -> the controlled values of the field "measured quantity"

Run as a script (no reasoner needed) to check the table against copi-core-v2.ttl; exit status 1 on any failure:
    python3 -I hirtz_coverage.py
"""
import csv, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
STATUSES = ("adotada", "adaptada", "não adotada", "extensão")
FBTERM = "https://www.inf.ufrgs.br/ontologies/copi/COPI_0001072"
COPI = "https://www.inf.ufrgs.br/ontologies/copi/"

class NotAdopted(LookupError):
    """The Functional Basis term has no class in copi-core-v2, or is not a term of the tables at all."""

def load(path=None):
    with open(path or os.path.join(HERE, "hirtz-coverage.csv"), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def resolve(caminho, rows=None):
    """IRI (CURIE) of the class that renders the term at `caminho`. Never approximates."""
    for r in rows or load():
        if r["caminho"] == caminho:
            if r["status"] in ("adotada", "adaptada", "extensão") and r["iri"]:
                return r["iri"]
            raise NotAdopted(f"{caminho}: '{r['status']}' in copi-core-v2. Create the class and update hirtz-coverage.csv "
                             f"before a term uses it; do not approximate to the nearest adopted term.")
    raise NotAdopted(f"{caminho}: not in hirtz-coverage.csv (neither a term of the Functional Basis nor a declared extension).")

def flow_values(rows=None):
    """{path: iri} of everything a flow field of a signature may hold: adopted Hirtz flows and the COPI extensions."""
    return {r["caminho"]: r["iri"] for r in rows or load()
            if r["iri"] and ((r["caminho"].startswith("Flow/") and r["status"] in ("adotada", "adaptada"))
                             or r["caminho"].startswith("COPI/Flow/"))}

def measured_quantities(rows=None):
    """{path: iri} of the quality classes the field 'measured quantity' may hold."""
    return {r["caminho"]: r["iri"] for r in rows or load() if r["caminho"].startswith("COPI/MeasuredQuantity/")}

def verify(core, rows=None):
    """Checks of the table against the ontology graph `core` (rdflib). Returns [(label, ok)]."""
    from rdflib import URIRef, RDF, Namespace
    SK = Namespace("http://www.w3.org/2004/02/skos/core#")
    rows = rows or load()
    curie = lambda u: "copi:" + str(u)[len(COPI):] if str(u).startswith(COPI) else str(u)
    by_path = {}
    for s, o in core.subject_objects(URIRef(FBTERM)):
        by_path.setdefault(str(o), []).append(curie(s))
    paths = [r["caminho"] for r in rows]
    out = []
    def add(label, bad): out.append((label + (f" — {bad[:5]}" if bad else ""), not bad))
    add("no SKOS concept scheme in copi-core-v2",
        [str(s) for t in (SK.Concept, SK.ConceptScheme) for s in core.subjects(RDF.type, t)])
    add("coverage table: every row has a known status", [r["caminho"] for r in rows if r["status"] not in STATUSES])
    add("coverage table: no path listed twice", sorted({p for p in paths if paths.count(p) > 1}))
    add("one class per Functional Basis path", [p for p, v in by_path.items() if len(v) > 1])
    ours = [r for r in rows if r["status"] in ("adotada", "adaptada") and r["iri"].startswith("copi:")]
    add(f"coverage table: adopted rows match the class carrying the path ({len(ours)} rows)",
        [r["caminho"] for r in ours if by_path.get(r["caminho"]) != [r["iri"]]])
    add("coverage table: unadopted rows and extensions carry no path",
        [r["caminho"] for r in rows if r["status"] in ("não adotada", "extensão") and r["caminho"] in by_path])
    add("coverage table: unadopted rows name no class", [r["caminho"] for r in rows if r["status"] == "não adotada" and r["iri"]])
    add("every class with a Functional Basis path is in the coverage table", [p for p in by_path if p not in paths])
    n = lambda prefix, depth: sum(1 for r in rows if r["caminho"].startswith(prefix) and r["caminho"].count("/") == depth)
    add("coverage table: 8 + 20 + 24 function classes (Hirtz: 8 + 21 + 24 terms; Convert is primary and secondary)", [] if (n("Function/", 1), n("Function/", 2), n("Function/", 3)) == (8, 20, 24) else ["count"])
    add("coverage table: 3 flow classes and 42 flow terms", [] if (n("Flow/", 1), n("Flow/", 2) + n("Flow/", 3)) == (3, 42) else ["count"])
    return out, by_path

if __name__ == "__main__":
    import rdflib
    g = rdflib.Graph(); g.parse(os.path.join(HERE, "copi-core-v2.ttl"), format="turtle")
    res, _ = verify(g)
    for label, ok in res: print(("PASS " if ok else "FAIL ") + label)
    sys.exit(0 if all(ok for _, ok in res) else 1)
