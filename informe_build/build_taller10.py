# -*- coding: utf-8 -*-
"""
Construye el informe del Taller de laboratorio 10 (SI-886) a partir de la
plantilla oficial SI886-PLANTILLA-TALLER.docx, preservando su caratula,
encabezado/pie con el logo institucional y sus estilos.

Los espacios reservados para capturas de pantalla se insertan como texto
simple "Captura de pantalla", sin cuadros ni bordes.
"""
import os
import docx
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TEMPLATE = os.path.join(ROOT, "SI886-PLANTILLA-TALLER.docx")
OUT = os.path.join(ROOT, "SI886-S10-TALLER-Grupo1.docx")
G1 = os.path.join(ROOT, "graficos", "AR_vista_actual.png")
G2 = os.path.join(ROOT, "graficos", "AR_cooperacion_proceso_aplicacion.png")
G3 = os.path.join(ROOT, "graficos", "AR_vista_objetivo.png")

BODY_FONT = "Arial"


def set_font(run, name=BODY_FONT, size=11, bold=False, italic=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = color
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:ascii'), name)
    rFonts.set(qn('w:hAnsi'), name)


def find_paragraph(doc, text_exact=None, text_startswith=None, occurrence=1):
    hits = []
    for p in doc.paragraphs:
        t = p.text
        if text_exact is not None and t == text_exact:
            hits.append(p)
        elif text_startswith is not None and t.startswith(text_startswith):
            hits.append(p)
    if not hits:
        raise ValueError(f"No encontrado: {text_exact or text_startswith}")
    return hits[occurrence - 1]


def set_paragraph_text(paragraph, new_text):
    if not paragraph.runs:
        run = paragraph.add_run(new_text)
        set_font(run)
        return
    first = paragraph.runs[0]
    first.text = new_text
    for extra in paragraph.runs[1:]:
        extra.text = ""


def insert_paragraph_before(anchor, text="", style=None, bold=False, italic=False,
                             size=11, align=None, space_before=None, space_after=None,
                             indent_cm=None):
    new_p_el = OxmlElement('w:p')
    anchor._p.addprevious(new_p_el)
    new_p = docx.text.paragraph.Paragraph(new_p_el, anchor._parent)
    if style:
        new_p.style = anchor.part.document.styles[style]
    if align is not None:
        new_p.alignment = align
    if space_before is not None:
        new_p.paragraph_format.space_before = Pt(space_before)
    if space_after is not None:
        new_p.paragraph_format.space_after = Pt(space_after)
    if indent_cm is not None:
        new_p.paragraph_format.left_indent = Cm(indent_cm)
    if text:
        run = new_p.add_run(text)
        set_font(run, BODY_FONT, size, bold=bold, italic=italic)
    return new_p


def screenshot_placeholder(anchor, label=""):
    text = f"Captura de pantalla {label}".strip()
    return insert_paragraph_before(anchor, text, italic=True, size=11,
                                    space_before=6, space_after=10)


def add_table_before(anchor, headers, rows, style_ref):
    doc = anchor.part.document
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = style_ref
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = ""
        run = hdr[i].paragraphs[0].add_run(h)
        set_font(run, BODY_FONT, 10, bold=True)
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            run = cells[i].paragraphs[0].add_run(str(val))
            set_font(run, BODY_FONT, 9)
    anchor._p.addprevious(t._tbl)
    insert_paragraph_before(anchor, "")
    return t


def figure_before(anchor, n, title, image_path, note, width_cm=15.5):
    insert_paragraph_before(anchor, f"Figura {n}", bold=True, size=11, space_before=10)
    insert_paragraph_before(anchor, title, italic=True, size=11, space_after=4)
    p3 = insert_paragraph_before(anchor, "")
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p3.add_run()
    run.add_picture(image_path, width=Cm(width_cm))
    insert_paragraph_before(anchor, note, italic=True, size=9.5, space_after=10)


def reference_before(anchor, text):
    p = insert_paragraph_before(anchor, "", space_after=6)
    p.paragraph_format.left_indent = Cm(1.0)
    p.paragraph_format.first_line_indent = Cm(-1.0)
    run = p.add_run(text)
    set_font(run, BODY_FONT, 10.5)
    return p


print("Cargando plantilla...")
doc = Document(TEMPLATE)
print("OK. Parrafos:", len(doc.paragraphs), "Tablas:", len(doc.tables))
TABLE_STYLE = doc.tables[0].style
