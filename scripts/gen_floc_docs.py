#!/usr/bin/env python3
"""
gen_floc_docs.py — build docs/copi-floc.html from the copi-floc component.

Renders the functional-location module as a bilingual (EN/PT-BR) term reference
in the same visual language as docs/docs.html (the COPI class reference produced
by COPIeditor/scripts/publish_to_copi.py). Reads only the module file, so the
page cannot drift from the ontology.

Usage:
    python3 scripts/gen_floc_docs.py                     # writes docs/copi-floc.html
    python3 scripts/gen_floc_docs.py --check             # exits 1 if the file is stale

Requires rdflib.
"""
import argparse
import html
import re
import sys
from datetime import date
from pathlib import Path

from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef, BNode, Literal
from rdflib.namespace import DCTERMS, SKOS, XSD

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src/ontology/components/copi-floc.ttl"
OUT = ROOT / "docs/copi-floc.html"

COPI = Namespace("https://www.inf.ufrgs.br/ontologies/copi/")
IOFAV = Namespace("https://spec.industrialontologies.org/ontology/annotation/")
IOF = Namespace("https://spec.industrialontologies.org/ontology/construct/")
OBO = Namespace("http://purl.obolibrary.org/obo/")

# Labels for the imported terms the module refers to. Kept small on purpose: the
# module only ever touches this handful of BFO/IOF terms.
EXTERNAL = {
    OBO.BFO_0000015: ("process", "processo"),
    OBO.BFO_0000023: ("role", "papel"),
    OBO.BFO_0000029: ("site", "sítio"),
    OBO.BFO_0000034: ("function", "função"),
    OBO.BFO_0000040: ("material entity", "entidade material"),
    OBO.BFO_0000057: ("has participant", "tem participante"),
    OBO.BFO_0000066: ("occurs in", "ocorre em"),
    OBO.BFO_0000171: ("located in", "localizado em"),
    OBO.BFO_0000176: ("continuant part of", "parte continuante de"),
    IOF.MaterialArtifact: ("material artifact", "artefato material"),
    IOF.PhysicalLocationIdentifier: ("physical location identifier", "identificador de localização física"),
    IOF.RequirementSpecification: ("requirement specification", "especificação de requisitos"),
    IOF.designates: ("designates", "designa"),
    IOF.isAbout: ("is about", "é sobre"),
    IOF.prescribes: ("prescribes", "prescreve"),
}

SECTIONS = [
    (OWL.Class, "Classes", "Classes"),
    (OWL.ObjectProperty, "Object properties", "Propriedades de objeto"),
    (OWL.DatatypeProperty, "Data properties", "Propriedades de dados"),
]

ANNOTATION_SECTIONS = [
    (IOFAV.explanatoryNote, "Explanatory note", "Nota explicativa", "note"),
    (IOFAV.usageNote, "Usage note", "Nota de uso", "note"),
    (IOFAV.primitiveRationale, "Primitive rationale", "Justificativa de primitividade", "italic"),
]


def esc(text):
    return html.escape(str(text), quote=True)


def by_lang(g, subj, pred):
    """Returns (en_values, pt_values, plain_values) for an annotation."""
    en, pt, plain = [], [], []
    for o in g.objects(subj, pred):
        if not isinstance(o, Literal):
            continue
        lang = (o.language or "").lower()
        if lang.startswith("pt"):
            pt.append(str(o))
        elif lang.startswith("en"):
            en.append(str(o))
        else:
            plain.append(str(o))
    return en, pt, plain


def term_label(g, node, lang="en"):
    if isinstance(node, URIRef):
        if node in EXTERNAL:
            return EXTERNAL[node][0 if lang == "en" else 1]
        en, pt, plain = by_lang(g, node, RDFS.label)
        pool = (en if lang == "en" else pt) or en or pt or plain
        if pool:
            return pool[0]
        return str(node).rsplit("/", 1)[-1].rsplit("#", 1)[-1]
    return "?"


def render_expr(g, node, lang="en"):
    """Renders a class expression in a Manchester-like reading."""
    if isinstance(node, URIRef):
        return term_label(g, node, lang)
    if isinstance(node, BNode):
        if (node, RDF.type, OWL.Restriction) in g:
            prop = g.value(node, OWL.onProperty)
            pname = term_label(g, prop, lang) if prop is not None else "?"
            some = g.value(node, OWL.someValuesFrom)
            if some is not None:
                word = "some" if lang == "en" else "algum"
                return f"{pname} {word} {render_expr(g, some, lang)}"
            qc = g.value(node, OWL.qualifiedCardinality)
            if qc is not None:
                cls = g.value(node, OWL.onClass)
                word = "exactly" if lang == "en" else "exatamente"
                return f"{pname} {word} {qc} {render_expr(g, cls, lang)}"
            inv = g.value(node, OWL.inverseOf)
            if inv is not None:
                word = "inverse of" if lang == "en" else "inversa de"
                return f"{word} {term_label(g, inv, lang)}"
        inv = g.value(node, OWL.inverseOf)
        if inv is not None:
            word = "inverse of" if lang == "en" else "inversa de"
            return f"{word} {term_label(g, inv, lang)}"
    return "?"


def chain_text(g, subj, lang="en"):
    chain = g.value(subj, OWL.propertyChainAxiom)
    if chain is None:
        return None
    parts = [render_expr(g, item, lang) for item in g.items(chain)]
    return " ∘ ".join(parts)


def bilingual_block(en, pt, style):
    """Two stacked language variants, hidden by the EN/PT toggle."""
    out = []
    css = {
        "note": 'style="font-size:.82rem;color:#374151;"',
        "italic": 'style="font-size:.82rem;color:#374151;font-style:italic;"',
        "example": 'style="font-size:.8rem;color:#475569;font-style:italic;"',
    }[style]
    for text in en:
        out.append(f'<div class="t-en" {css}>{esc(text)}</div>')
    for text in pt:
        out.append(f'<div class="t-pt" {css}>{esc(text)}</div>')
    return "".join(out)


def doc_section(title_en, title_pt, body):
    if not body:
        return ""
    return (
        '<div class="doc-section" style="margin-bottom:.75rem;">'
        f'<div class="doc-section-title"><span class="t-en">{title_en}</span>'
        f'<span class="t-pt">{title_pt}</span></div>{body}</div>'
    )


def render_term(g, subj, kind):
    lab_en, lab_pt, lab_plain = by_lang(g, subj, RDFS.label)
    name_en = (lab_en or lab_plain or ["?"])[0]
    name_pt = (lab_pt or lab_en or lab_plain or ["?"])[0]
    local = str(subj).rsplit("/", 1)[-1]

    pills = []
    prim = g.value(subj, IOFAV.isPrimitive)
    if prim is not None:
        text = "primitive" if str(prim).lower() in ("true", "1") else "defined"
        bg = "#f1f5f9" if text == "primitive" else "#ecfdf5"
        fg = "#475569" if text == "primitive" else "#047857"
        pills.append(
            f'<span style="font-size:.62rem;font-family:system-ui,sans-serif;font-weight:600;'
            f'padding:.1rem .45rem;border-radius:4px;background:{bg};color:{fg};">{text}</span>'
        )
    for char, text in ((OWL.FunctionalProperty, "functional"), (OWL.TransitiveProperty, "transitive")):
        if (subj, RDF.type, char) in g:
            pills.append(
                '<span style="font-size:.62rem;font-family:system-ui,sans-serif;font-weight:600;'
                'padding:.1rem .45rem;border-radius:4px;background:#eff6ff;color:#1d4ed8;">'
                f'{text}</span>'
            )

    body = []

    # natural-language definition, the headline of every card
    d_en, d_pt, _ = by_lang(g, subj, IOFAV.naturalLanguageDefinition)
    if not d_en and not d_pt:
        d_en, d_pt, _ = by_lang(g, subj, RDFS.comment)
    for text in d_en:
        body.append(f'<div class="nl-def t-en"><div class="lang-tag">en</div>{esc(text)}</div>')
    for text in d_pt:
        body.append(
            '<div class="nl-def t-pt" style="border-left-color:#059669;">'
            f'<div class="lang-tag">pt-br</div>{esc(text)}</div>'
        )

    # the OWL shape, read back in words
    rows = []
    supers = [s for s in g.objects(subj, RDFS.subClassOf)]
    if supers:
        rows.append(("Subclass of", "Subclasse de", supers))
    parents = [s for s in g.objects(subj, RDFS.subPropertyOf)]
    if parents:
        rows.append(("Subproperty of", "Subpropriedade de", parents))
    axiom_lines = []
    for title_en, title_pt, nodes in rows:
        rendered_en = "<br>".join(esc(render_expr(g, n, "en")) for n in nodes)
        rendered_pt = "<br>".join(esc(render_expr(g, n, "pt")) for n in nodes)
        axiom_lines.append(
            f'<tr><td><span class="t-en">{title_en}</span><span class="t-pt">{title_pt}</span></td>'
            f'<td><span class="t-en">{rendered_en}</span><span class="t-pt">{rendered_pt}</span></td></tr>'
        )
    for pred, title_en, title_pt in (
        (RDFS.domain, "Domain", "Domínio"),
        (RDFS.range, "Range", "Imagem"),
        (OWL.inverseOf, "Inverse of", "Inversa de"),
        (OWL.disjointWith, "Disjoint with", "Disjunta de"),
    ):
        vals = list(g.objects(subj, pred))
        if vals:
            r_en = ", ".join(esc(render_expr(g, v, "en")) for v in vals)
            r_pt = ", ".join(esc(render_expr(g, v, "pt")) for v in vals)
            axiom_lines.append(
                f'<tr><td><span class="t-en">{title_en}</span><span class="t-pt">{title_pt}</span></td>'
                f'<td><span class="t-en">{r_en}</span><span class="t-pt">{r_pt}</span></td></tr>'
            )
    chain_en = chain_text(g, subj, "en")
    if chain_en:
        axiom_lines.append(
            '<tr><td><span class="t-en">Property chain</span><span class="t-pt">Cadeia</span></td>'
            f'<td><span class="t-en">{esc(chain_en)}</span>'
            f'<span class="t-pt">{esc(chain_text(g, subj, "pt"))}</span></td></tr>'
        )
    if axiom_lines:
        body.append(
            doc_section(
                "OWL axioms", "Axiomas OWL",
                '<table class="meta-table">' + "".join(axiom_lines) + "</table>",
            )
        )

    # FOL, in the same dark block the class reference uses
    for pred, title_en, title_pt in (
        (IOFAV.firstOrderLogicDefinition, "FOL Definition (↔)", "LPO Definition (↔)"),
        (IOFAV.firstOrderLogicAxiom, "FOL Axiom (→)", "LPO Axiom (→)"),
    ):
        for o in g.objects(subj, pred):
            body.append(
                doc_section(
                    title_en, title_pt,
                    '<div class="owl-block" style="font-size:.76rem;padding:.55rem .8rem;">'
                    f"{esc(o)}</div>",
                )
            )
    for pred, title_en, title_pt in (
        (IOFAV.semiFormalNaturalLanguageDefinition, "Semi-formal definition", "Definição semiformal"),
        (IOFAV.semiFormalNaturalLanguageAxiom, "Semi-formal axiom", "Axioma semiformal"),
    ):
        en, pt, plain = by_lang(g, subj, pred)
        inner = ""
        for text in en + plain:
            inner += (
                '<div class="t-en" style="font-family:monospace;font-size:.82rem;background:#f8f9fa;'
                f'border-radius:4px;padding:.35rem .6rem;margin-bottom:.3rem;">{esc(text)}</div>'
            )
        for text in pt:
            inner += (
                '<div class="t-pt" style="font-family:monospace;font-size:.82rem;background:#f0faf4;'
                f'border-radius:4px;padding:.35rem .6rem;">{esc(text)}</div>'
            )
        body.append(doc_section(title_en, title_pt, inner))

    for pred, title_en, title_pt, style in ANNOTATION_SECTIONS:
        en, pt, plain = by_lang(g, subj, pred)
        body.append(doc_section(title_en, title_pt, bilingual_block(en + plain, pt, style)))

    en, pt, plain = by_lang(g, subj, SKOS.example)
    body.append(doc_section("Examples", "Exemplos", bilingual_block(en + plain, pt, "example")))

    # provenance footer of the card
    meta = []
    alt_en, alt_pt, _ = by_lang(g, subj, SKOS.altLabel)
    if alt_en or alt_pt:
        meta.append(
            '<tr><td><span class="t-en">Also known as</span><span class="t-pt">Também chamado</span></td>'
            f'<td><span class="t-en">{esc(", ".join(alt_en))}</span>'
            f'<span class="t-pt">{esc(", ".join(alt_pt))}</span></td></tr>'
        )
    for o in g.objects(subj, DCTERMS.source):
        meta.append(
            '<tr><td><span class="t-en">Source</span><span class="t-pt">Fonte</span></td>'
            f'<td style="font-family:monospace;font-size:.78rem;">{esc(o)}</td></tr>'
        )
    for o in g.objects(subj, IOFAV.adaptedFrom):
        meta.append(
            '<tr><td><span class="t-en">Adapted from</span><span class="t-pt">Adaptado de</span></td>'
            f'<td style="font-size:.8rem;">{esc(o)}</td></tr>'
        )
    if meta:
        body.append(
            '<div class="doc-section" style="margin-bottom:.5rem;">'
            '<table class="meta-table">' + "".join(meta) + "</table></div>"
        )

    return f"""<div class="class-card" id="{esc(local)}">
  <div class="class-card-header">
    <div style="min-width:0;">
      <div class="class-card-name"><span class="t-en">{esc(name_en)}</span><span class="t-pt">{esc(name_pt)}</span></div>
      <div class="class-iri">{esc(subj)}</div>
    </div>
    <div class="d-flex gap-2 align-items-center flex-shrink-0">{''.join(pills)}</div>
  </div>
  <div class="class-card-body"><div style="flex:1;min-width:0;">{''.join(body)}</div></div>
</div>"""


def pending_items(text):
    """Pulls the PENDING block out of the module's header comment."""
    block = re.search(r"# PENDING \(.*?\n(.*?)#=====", text, re.S)
    if not block:
        return []
    items, current = [], None
    for line in block.group(1).splitlines():
        line = line.lstrip("#").strip()
        if re.match(r"^\d+\.", line):
            if current:
                items.append(current)
            current = line
        elif line and current:
            current += " " + line
    if current:
        items.append(current)
    return items


PAGE = """<!DOCTYPE html>
<html lang="en" id="copi-root">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>COPI-FLOC · Functional Location Module</title>
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='14 8 80 92'><polygon points='54,8 93.8,31 93.8,77 54,100 14.2,77 14.2,31' fill='%230a1628'/><polygon points='54,8 93.8,31 93.8,77 54,100 14.2,77 14.2,31' fill='none' stroke='%232563eb' stroke-width='3'/><circle cx='54' cy='54' r='11' fill='%2307101e' stroke='%232563eb' stroke-width='2'/><path d='M54,44 C61,47.5 61,52 61,53.5 A7,7 0,0,1 47,53.5 C47,52 47,47.5 54,44Z' fill='%23f59e0b'/></svg>">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
<style>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Serif:ital,wght@0,400;0,600;1,400&display=swap');
  :root{{
    --accent:#1e3a5f;--accent2:#2563eb;--border:#dee2e6;--muted:#6c757d;--light:#f8fafc;
    --layer-floc:#7c3aed;   /* copi-floc: violet — the position layer */
  }}
  body{{font-family:'IBM Plex Serif','Georgia',serif;background:#fff;color:#1a1a1a;font-size:15px;}}
  a{{color:var(--accent2);}}
  .doc-nav{{background:var(--accent);color:white;padding:.6rem 0;
           font-family:system-ui,sans-serif;font-size:.85rem;}}
  .doc-nav a{{color:rgba(255,255,255,.75);text-decoration:none;}}
  .doc-nav a:hover{{color:white;}}
  .doc-hero{{background:linear-gradient(160deg,#0a1628 0%,#140f2f 55%,#0a1628 100%);
            color:white;padding:2rem 2rem 1.75rem;border-radius:4px;margin-bottom:2rem;
            border-top:3px solid var(--layer-floc);}}
  .onto-eyebrow{{font-family:'IBM Plex Mono','Courier New',monospace;font-size:.68rem;
                font-weight:600;letter-spacing:.18em;text-transform:uppercase;
                color:rgba(255,255,255,.4);margin-bottom:.5rem;}}
  .onto-title{{font-family:system-ui,sans-serif;font-size:2.8rem;font-weight:800;letter-spacing:-.04em;
              line-height:1;}}
  .onto-subtitle{{font-size:1rem;color:rgba(255,255,255,.55);font-weight:300;margin-top:.3rem;}}
  .onto-iri{{font-family:'IBM Plex Mono','Courier New',monospace;font-size:.88rem;
            color:rgba(255,255,255,.75);margin-top:1rem;letter-spacing:.01em;
            padding:.4rem .7rem;background:rgba(255,255,255,.07);border-radius:4px;
            display:inline-block;border-left:3px solid var(--layer-floc);}}
  .hero-meta-strip{{display:flex;flex-wrap:wrap;gap:.5rem 1.5rem;margin-top:1rem;
                   font-family:'IBM Plex Mono','Courier New',monospace;
                   font-size:.72rem;color:rgba(255,255,255,.45);}}
  .hero-meta-strip strong{{color:rgba(255,255,255,.75);font-weight:600;}}
  .lang-toggle{{display:flex;align-items:center;gap:2px;background:rgba(255,255,255,.1);
               border-radius:5px;padding:2px;}}
  .lang-seg{{background:transparent;border:none;color:rgba(255,255,255,.5);
            padding:.15rem .55rem;font-family:system-ui,sans-serif;font-size:.72rem;
            font-weight:700;letter-spacing:.06em;border-radius:3px;cursor:pointer;}}
  .lang-seg.active{{background:rgba(255,255,255,.2);color:white;}}
  .lang-toggle-label{{font-family:system-ui,sans-serif;font-size:.65rem;font-weight:600;
                     text-transform:uppercase;letter-spacing:.1em;color:rgba(255,255,255,.35);
                     margin-right:.4rem;}}
  .section-header{{font-family:system-ui,sans-serif;font-size:1.35rem;font-weight:700;
                  color:var(--accent);border-bottom:2px solid var(--layer-floc);
                  padding-bottom:.35rem;margin:2.5rem 0 1.25rem;}}
  .class-card{{border:1px solid var(--border);border-radius:8px;margin-bottom:1.5rem;overflow:hidden;
              border-left:3px solid var(--layer-floc);}}
  .class-card-header{{padding:.85rem 1.1rem .7rem;background:var(--light);border-bottom:1px solid var(--border);
                     display:flex;align-items:flex-start;justify-content:space-between;gap:1rem;}}
  .class-card-name{{font-family:system-ui,sans-serif;font-size:1.1rem;font-weight:700;color:var(--accent);}}
  .class-iri{{font-family:monospace;font-size:.72rem;color:var(--muted);}}
  .class-card-body{{padding:.85rem 1.1rem;display:flex;gap:1.5rem;align-items:flex-start;}}
  .doc-section-title{{font-family:system-ui,sans-serif;font-size:.72rem;font-weight:700;text-transform:uppercase;
                     letter-spacing:.1em;color:var(--muted);border-bottom:1px solid var(--border);
                     padding-bottom:.4rem;margin-bottom:1rem;}}
  .nl-def{{font-size:1.08rem;font-style:italic;color:#1a1a1a;border-left:4px solid var(--accent2);
          padding:.6rem 1rem;margin-bottom:.75rem;background:#f8faff;}}
  .nl-def .lang-tag{{font-size:.7rem;font-family:monospace;font-style:normal;color:var(--muted);margin-bottom:.2rem;}}
  .owl-block{{background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1rem 1.2rem;
             font-family:'JetBrains Mono','Fira Code','Courier New',monospace;font-size:.78rem;
             line-height:1.7;overflow-x:auto;white-space:pre-wrap;}}
  .meta-table{{font-size:.8rem;font-family:system-ui,sans-serif;}}
  .meta-table td:first-child{{color:var(--muted);padding-right:1rem;white-space:nowrap;}}
  .meta-table td{{padding:.2rem 0;vertical-align:top;}}
  .prose{{font-size:.95rem;line-height:1.65;color:#374151;}}
  .callout{{border:1px solid var(--border);border-left:3px solid #b45309;border-radius:6px;
           background:#fffbeb;padding:.85rem 1.1rem;margin-bottom:1rem;font-size:.88rem;color:#374151;}}
  .toc-grid{{display:flex;flex-wrap:wrap;gap:.4rem;margin-bottom:1.5rem;}}
  .toc-grid a{{font-family:'IBM Plex Mono','Courier New',monospace;font-size:.75rem;
              text-decoration:none;border:1px solid var(--border);border-radius:4px;
              padding:.2rem .5rem;color:var(--accent);background:var(--light);}}
  .toc-grid a:hover{{border-color:var(--layer-floc);color:var(--layer-floc);}}
  footer{{margin:3rem 0 2rem;padding-top:1rem;border-top:1px solid var(--border);
         font-family:system-ui,sans-serif;font-size:.8rem;color:var(--muted);}}
  html.lang-pt .t-en{{display:none!important;}}
  html:not(.lang-pt) .t-pt{{display:none!important;}}
  @media print{{.doc-nav,.no-print{{display:none!important;}}body{{font-size:13px;}}}}
</style>
</head>
<body>
<nav class="doc-nav">
  <div class="container-fluid px-4 d-flex align-items-center gap-3">
    <a href="docs.html" style="display:flex;align-items:center;text-decoration:none;color:rgba(255,255,255,.85);"><strong>COPI</strong></a>
    <span style="opacity:.3">·</span>
    <a href="docs.html"><span class="t-en">Class Reference</span><span class="t-pt">Referência de Classes</span></a>
    <span style="opacity:.3">·</span>
    <a href="copi-floc.html" style="color:white;"><span class="t-en">FLOC Module</span><span class="t-pt">Módulo FLOC</span></a>
    <span style="opacity:.3">·</span>
    <a href="https://github.com/INF-UFRGS-Ontologies/copi" target="_blank" rel="noopener"
       style="color:rgba(255,255,255,.55);font-size:.8rem;">GitHub ↗</a>
    <div style="margin-left:auto;display:flex;align-items:center;gap:.5rem;">
      <span class="lang-toggle-label">Lang</span>
      <div class="lang-toggle" title="Switch language / Mudar idioma">
        <button class="lang-seg active" id="lang-btn-en">EN</button>
        <button class="lang-seg" id="lang-btn-pt">PT</button>
      </div>
    </div>
  </div>
</nav>
<div class="container-fluid px-4 py-4" style="max-width:1200px;">

<div class="doc-hero">
  <div class="onto-eyebrow"><span class="t-en">OWL 2 DL Module · Term Reference</span><span class="t-pt">Módulo OWL 2 DL · Referência de Termos</span></div>
  <div class="onto-title">COPI-FLOC</div>
  <div class="onto-subtitle"><span class="t-en">Functional locations: positions, identifiers and installation history</span><span class="t-pt">Locais de instalação: posições, identificadores e histórico de instalação</span></div>
  <div class="onto-iri">https://www.inf.ufrgs.br/ontologies/copi/copi-floc</div>
  <div class="hero-meta-strip">
    <span><strong>{n_classes}</strong> <span class="t-en">classes</span><span class="t-pt">classes</span></span>
    <span><strong>{n_obj}</strong> <span class="t-en">object properties</span><span class="t-pt">propriedades de objeto</span></span>
    <span><strong>{n_data}</strong> <span class="t-en">data properties</span><span class="t-pt">propriedades de dados</span></span>
    <span><strong>{n_axioms}</strong> <span class="t-en">triples</span><span class="t-pt">triplas</span></span>
    <span>BFO 2020</span>
    <span>IOF-Core 202603</span>
    <span>CC BY 4.0</span>
    <span>{version}</span>
  </div>
  <div style="margin-top:1.1rem;padding:.65rem .9rem;background:rgba(255,255,255,.06);
              border-left:2px solid rgba(255,255,255,.25);border-radius:0 4px 4px 0;">
    <div style="font-family:'IBM Plex Mono','Courier New',monospace;font-size:.65rem;
                font-weight:600;letter-spacing:.12em;text-transform:uppercase;
                color:rgba(255,255,255,.35);margin-bottom:.35rem;">
      <span class="t-en">Published at · FOIS 2026</span><span class="t-pt">Publicado em · FOIS 2026</span>
    </div>
    <div style="font-family:'IBM Plex Serif','Georgia',serif;font-size:.82rem;
                color:rgba(255,255,255,.75);line-height:1.45;font-style:italic;">
      An Ontology Design Pattern for Functional Locations in Industrial Asset Management
    </div>
    <div style="font-family:system-ui,sans-serif;font-size:.75rem;color:rgba(255,255,255,.4);margin-top:.25rem;">
      Santos, Rojas, Antunes, Rodrigues, Romeu, Petry, Abel &amp; Netto · UFRGS ·
      <span class="t-en">to appear, September 2026</span><span class="t-pt">a aparecer, setembro 2026</span>
    </div>
  </div>
</div>

<div class="prose">
  <div class="t-en">
    <p><strong>copi-floc</strong> models a functional location as a persistent <em>site</em> whose boundaries are
    fixed by delimiting material entities, not by the equipment that occupies it. Four concerns stay apart: the
    site and its hierarchy; the two identifiers that designate it (the location code, <em>where</em> in the
    breakdown, and the equipment tag, <em>what kind</em> of item is expected); the specification stating what the
    position requires; and the installation periods through which artifacts occupy the site over time.</p>
    <p>The module imports <strong>BFO 2020</strong> and <strong>IOF-Core 202603</strong> only. It carries no
    equipment classes, no observation vocabulary and no maintenance records, so it can be imported on its own by
    ontologies outside oil and gas. Equipment types come from <code>copi-core</code>; observations and maintenance
    are left to separate bridge modules.</p>
  </div>
  <div class="t-pt">
    <p>O <strong>copi-floc</strong> modela um local de instalação como um <em>sítio</em> persistente cujos limites
    são fixados por entidades materiais delimitadoras, e não pelo equipamento que o ocupa. Quatro preocupações
    ficam separadas: o sítio e sua hierarquia; os dois identificadores que o designam (o código do local,
    <em>onde</em> na estrutura, e a tag de equipamento, <em>que tipo</em> de item é esperado); a especificação que
    declara o que a posição requer; e os períodos de instalação pelos quais artefatos ocupam o sítio ao longo do
    tempo.</p>
    <p>O módulo importa apenas <strong>BFO 2020</strong> e <strong>IOF-Core 202603</strong>. Não carrega classes de
    equipamento, vocabulário de observação nem registros de manutenção, e por isso pode ser importado isoladamente
    por ontologias fora de óleo e gás. Os tipos de equipamento vêm do <code>copi-core</code>; observações e
    manutenção ficam em módulos-ponte separados.</p>
  </div>
</div>

<div class="section-header"><span class="t-en">Provenance</span><span class="t-pt">Proveniência</span></div>
<div class="prose">
  <div class="t-en">
    <p>Migrated from the FOIS 2026 design pattern
    (<a href="https://www.inf.ufrgs.br/ontologies/odp/functional-location">odp/functional-location</a>, v0.8;
    <a href="https://doi.org/10.5281/zenodo.21072929">Zenodo</a>), which remains the citable pattern. The migration
    changed five things:</p>
    <ul>
      <li><strong>IAO replaced by IOF-Core.</strong> Importing IAO alongside IOF-Core would have created two
      unaligned information-entity hierarchies. Identifiers are now <code>iof:PhysicalLocationIdentifier</code> and
      the identifier relations specialise <code>iof:designates</code>.</li>
      <li><strong>Part-of corrected.</strong> v0.8 used <code>BFO_0000050</code>, which BFO 2020 core does not
      declare; the module uses <code>continuant part of</code> (<code>BFO_0000176</code>).</li>
      <li><strong>Installation history added.</strong> v0.8 made <code>installedAt</code> functional and put the
      dates on the artifact, which allowed one installation per artifact for its whole life — a rotable spare
      reinstalled at a second position made the ontology inconsistent. Installation periods replace that.</li>
      <li><strong>Requirement slots removed.</strong> v0.8 required an instance of <code>bfo:Function</code>, which
      forced a function with no bearer whenever the position was empty. The expected item class, which does exist
      in source systems, is carried on the position instead.</li>
      <li><strong>Domain classes and examples dropped.</strong> Equipment and function classes belong to
      <code>copi-core</code>; the pattern's illustrative individuals are not part of COPI.</li>
    </ul>
    <p>Term-by-term correspondence with the published pattern is recorded in
    <code>src/ontology/copi-floc-odp-map.sssom.tsv</code>.</p>
  </div>
  <div class="t-pt">
    <p>Migrado do padrão de projeto do FOIS 2026
    (<a href="https://www.inf.ufrgs.br/ontologies/odp/functional-location">odp/functional-location</a>, v0.8;
    <a href="https://doi.org/10.5281/zenodo.21072929">Zenodo</a>), que continua sendo o padrão citável. A migração
    mudou cinco coisas:</p>
    <ul>
      <li><strong>IAO substituído pelo IOF-Core.</strong> Importar o IAO junto com o IOF-Core criaria duas
      hierarquias de entidade informacional desalinhadas. Os identificadores agora são
      <code>iof:PhysicalLocationIdentifier</code> e as relações de identificação especializam
      <code>iof:designates</code>.</li>
      <li><strong>Relação de parte corrigida.</strong> A v0.8 usava <code>BFO_0000050</code>, que o BFO 2020 core
      não declara; o módulo usa <code>parte continuante de</code> (<code>BFO_0000176</code>).</li>
      <li><strong>Histórico de instalação incluído.</strong> A v0.8 fazia <code>installedAt</code> funcional e punha
      as datas no artefato, o que permitia uma única instalação por artefato em toda a vida — um sobressalente
      rotativo reinstalado numa segunda posição tornava a ontologia inconsistente. Os períodos de instalação
      substituem isso.</li>
      <li><strong>Slots de requisito removidos.</strong> A v0.8 exigia uma instância de <code>bfo:Function</code>, o
      que forçava uma função sem portador sempre que a posição estivesse vazia. A classe esperada de item, que de
      fato existe nos sistemas de origem, passou a ficar na posição.</li>
      <li><strong>Classes de domínio e exemplos removidos.</strong> Equipamentos e funções pertencem ao
      <code>copi-core</code>; os indivíduos ilustrativos do padrão não fazem parte da COPI.</li>
    </ul>
    <p>A correspondência termo a termo com o padrão publicado está em
    <code>src/ontology/copi-floc-odp-map.sssom.tsv</code>.</p>
  </div>
</div>

{pending_block}

<div class="section-header"><span class="t-en">Term index</span><span class="t-pt">Índice de termos</span></div>
<div class="toc-grid">{toc}</div>

{sections}

<footer>
  <div><span class="t-en">Generated from</span><span class="t-pt">Gerado a partir de</span>
  <code>src/ontology/components/copi-floc.ttl</code> ·
  <code>scripts/gen_floc_docs.py</code> · {version}</div>
  <div style="margin-top:.3rem;">© 2026 UFRGS · CC BY 4.0 ·
  <a href="https://github.com/INF-UFRGS-Ontologies/copi">github.com/INF-UFRGS-Ontologies/copi</a></div>
</footer>
</div>
<script>
(function(){{
  var root=document.getElementById('copi-root');
  var btnEn=document.getElementById('lang-btn-en');
  var btnPt=document.getElementById('lang-btn-pt');
  if(!btnEn||!btnPt)return;
  var titleEn="COPI-FLOC \\u00b7 Functional Location Module";
  var titlePt="COPI-FLOC \\u00b7 M\\u00f3dulo de Local de Instala\\u00e7\\u00e3o";
  function applyLang(pt){{
    if(pt){{root.classList.add('lang-pt');root.lang='pt-BR';document.title=titlePt;
      btnPt.classList.add('active');btnEn.classList.remove('active');}}
    else{{root.classList.remove('lang-pt');root.lang='en';document.title=titleEn;
      btnEn.classList.add('active');btnPt.classList.remove('active');}}
  }}
  try{{applyLang(localStorage.getItem('copi-lang')==='pt');}}catch(e){{}}
  btnEn.addEventListener('click',function(){{applyLang(false);try{{localStorage.setItem('copi-lang','en');}}catch(e){{}}}});
  btnPt.addEventListener('click',function(){{applyLang(true);try{{localStorage.setItem('copi-lang','pt');}}catch(e){{}}}});
}})();
</script>
</body>
</html>
"""


def build():
    text = SRC.read_text(encoding="utf-8")
    g = Graph().parse(SRC, format="turtle")

    counts, toc, sections = {}, [], []
    for rdf_type, title_en, title_pt in SECTIONS:
        subjects = sorted(
            (s for s in g.subjects(RDF.type, rdf_type) if str(s).startswith(str(COPI))),
            key=str,
        )
        counts[rdf_type] = len(subjects)
        if not subjects:
            continue
        sections.append(
            f'<div class="section-header"><span class="t-en">{title_en} ({len(subjects)})</span>'
            f'<span class="t-pt">{title_pt} ({len(subjects)})</span></div>'
        )
        for s in subjects:
            local = str(s).rsplit("/", 1)[-1]
            name_en = term_label(g, s, "en")
            name_pt = term_label(g, s, "pt")
            toc.append(
                f'<a href="#{esc(local)}"><span class="t-en">{esc(name_en)}</span>'
                f'<span class="t-pt">{esc(name_pt)}</span></a>'
            )
            sections.append(render_term(g, s, rdf_type))

    items = pending_items(text)
    pending_block = ""
    if items:
        lis = "".join(f"<li>{esc(i)}</li>" for i in items)
        pending_block = (
            '<div class="section-header"><span class="t-en">Known gaps</span>'
            '<span class="t-pt">Lacunas conhecidas</span></div>'
            '<div class="callout"><div class="t-en"><strong>This module is provisional.</strong> '
            "The following are recorded in the source file and are not resolved:</div>"
            '<div class="t-pt"><strong>Este módulo é provisório.</strong> '
            "Os pontos abaixo estão registrados no arquivo-fonte e não estão resolvidos:</div>"
            f'<ul style="margin:.5rem 0 0 0;padding-left:1.1rem;">{lis}</ul></div>'
        )

    onto = COPI["copi-floc"]
    version = str(g.value(onto, DCTERMS.modified) or date.today().isoformat())
    return PAGE.format(
        n_classes=counts.get(OWL.Class, 0),
        n_obj=counts.get(OWL.ObjectProperty, 0),
        n_data=counts.get(OWL.DatatypeProperty, 0),
        n_axioms=len(g),
        version=esc(version),
        pending_block=pending_block,
        toc="".join(toc),
        sections="\n".join(sections),
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="fail if docs/copi-floc.html is stale")
    args = ap.parse_args()
    page = build()
    if args.check:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != page:
            print("STALE: docs/copi-floc.html does not match copi-floc.ttl", file=sys.stderr)
            return 1
        print("OK: docs/copi-floc.html is up to date")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(page):,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
