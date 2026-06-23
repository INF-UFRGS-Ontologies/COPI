# scripts/fol_extract.py
"""Extract per-class OWL data from copi-full.ttl using rdflib."""
import rdflib
from rdflib.collection import Collection
from fol_gen import label_to_pred

COPI_NS = 'https://www.inf.ufrgs.br/ontologies/copi/COPI_'
IOF_CORE = rdflib.Namespace('https://spec.industrialontologies.org/ontology/construct/')
IOF_AV = rdflib.Namespace('https://spec.industrialontologies.org/ontology/annotation/')
BFO = rdflib.Namespace('http://purl.obolibrary.org/obo/')
OWL = rdflib.OWL
RDFS = rdflib.RDFS
RDF = rdflib.RDF

# Map property IRI → FOL predicate name
_PROP_MAP = {
    str(IOF_CORE.hasFunction): 'hasFunction',
    str(IOF_CORE.describes): 'describes',
    str(IOF_CORE.hasComponentPartAtAllTimes): 'hasComponentPartAtAllTimes',
    str(BFO.BFO_0000054): 'realizedIn',   # has realization
}


def _get_label(g, node, lang='en'):
    """Return the label of a node for a given language tag (exact match only)."""
    for lbl in g.objects(node, RDFS.label):
        if hasattr(lbl, 'language') and lbl.language == lang:
            return str(lbl)
    return None


def _get_label_or_local(g, node):
    lbl = _get_label(g, node)
    if lbl:
        return lbl
    s = str(node)
    return s.split('/')[-1].split('#')[-1]


def _parse_bnode_restriction(g, bnode):
    """Return (prop_name, filler_label, mode) or None."""
    prop = g.value(bnode, OWL.onProperty)
    if prop is None:
        return None
    prop_name = _PROP_MAP.get(str(prop))
    if prop_name is None:
        return None
    svf = g.value(bnode, OWL.someValuesFrom)
    avf = g.value(bnode, OWL.allValuesFrom)
    filler = svf or avf
    if filler is None:
        return None
    # For blank-node fillers (intersections), try to extract the named class
    if isinstance(filler, rdflib.BNode):
        # intersection of (NamedClass, restriction): find the named class
        members_node = g.value(filler, OWL.intersectionOf)
        if members_node:
            members = list(Collection(g, members_node))
            for m in members:
                if isinstance(m, rdflib.URIRef):
                    filler = m
                    break
    if isinstance(filler, rdflib.URIRef):
        filler_label = _get_label(g, filler)
    else:
        return None
    if filler_label is None:
        return None
    mode = 'some' if svf else 'all'
    return (prop_name, filler_label.lower(), mode)


def extract_class_data(ttl_path: str) -> dict:
    g = rdflib.Graph()
    g.parse(ttl_path, format='turtle')

    result = {}
    for cls in g.subjects(RDF.type, OWL.Class):
        iri = str(cls)
        if not iri.startswith(COPI_NS):
            continue

        label_en = _get_label(g, cls, 'en')
        if label_en is None:
            continue
        label_pt = _get_label(g, cls, 'pt-br') or ''

        # FOL annotations
        fol_axiom = None
        for a in g.objects(cls, IOF_AV.firstOrderLogicAxiom):
            if hasattr(a, 'language') and a.language == 'en':
                fol_axiom = str(a)
                break
            elif fol_axiom is None:
                fol_axiom = str(a)
        fol_def = None
        for d in g.objects(cls, IOF_AV.firstOrderLogicDefinition):
            if hasattr(d, 'language') and d.language == 'en':
                fol_def = str(d)
                break
            elif fol_def is None:
                fol_def = str(d)

        # Named parents
        parents = []
        some_restr = []
        all_restr = []
        for sc in g.objects(cls, RDFS.subClassOf):
            if isinstance(sc, rdflib.URIRef):
                p_en_label = _get_label(g, sc, 'en')
                if p_en_label:
                    # COPI / IOF classes with @en label → lowercase
                    parents.append(p_en_label.lower())
                else:
                    # No @en label → use IRI local name (CamelCase, as-is)
                    local = str(sc).split('/')[-1].split('#')[-1]
                    if local:
                        parents.append(local)
            elif isinstance(sc, rdflib.BNode):
                parsed = _parse_bnode_restriction(g, sc)
                if parsed:
                    prop, filler, mode = parsed
                    if mode == 'some':
                        some_restr.append((prop, filler))
                    else:
                        all_restr.append((prop, filler))

        # Equivalents (→ is_definition)
        has_equiv = bool(list(g.objects(cls, OWL.equivalentClass)))

        # Disjoint
        disjoint_with = []
        for d in g.objects(cls, OWL.disjointWith):
            d_label = _get_label(g, d)
            if d_label:
                disjoint_with.append(d_label.lower())

        cid = iri.split('COPI_')[1]
        result[label_en.lower()] = {
            'id': f'COPI_{cid}',
            'label_en': label_en,
            'label_pt': label_pt,
            'pred': label_to_pred(label_en),
            'fol_axiom': fol_axiom,
            'fol_def': fol_def,
            'parents': parents,
            'some_restrictions': some_restr,
            'all_restrictions': all_restr,
            'disjoint_with': disjoint_with,
            'has_equiv': has_equiv,
            'is_definition': has_equiv or (fol_def is not None),
        }

    return result
