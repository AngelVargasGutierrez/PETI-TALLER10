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


REPO = "https://github.com/AngelVargasGutierrez/PETI-TALLER10"
TALLER_TAG_URL = f"{REPO}/tree/taller-10"
V_TAG_URL = f"{REPO}/tree/v0.10"
PR_URL = f"{REPO}/pull/1"

print("Cargando plantilla...")
doc = Document(TEMPLATE)
print("OK. Parrafos:", len(doc.paragraphs), "Tablas:", len(doc.tables))
TABLE_STYLE = doc.tables[0].style

# ------------------------------------------------------------------
# 1) CARATULA
# ------------------------------------------------------------------
set_paragraph_text(find_paragraph(doc, text_exact='“…………………………………………….”'),
                    '“Modelado de la arquitectura actual y objetivo en Archi”')
set_paragraph_text(find_paragraph(doc, text_exact='“………………………….”'),
                    '“Planeamiento Estratégico de TI”')
set_paragraph_text(find_paragraph(doc, text_startswith='APELLIDOS Y NOMBRES'),
                    'VARGAS GUTIÉRREZ, ANGEL JOSE · 2020066922')
print("Caratula actualizada.")

# ------------------------------------------------------------------
# 2) Elimina la pagina "Como se usa esta plantilla"
# ------------------------------------------------------------------
start = find_paragraph(doc, text_exact='Cómo se usa esta plantilla')
pre_break = start._p.getprevious()
end = find_paragraph(doc, text_exact='Borra esta página antes de entregar.')
body = doc.element.body
to_remove = []
collecting = False
for el in list(body):
    if el is pre_break:
        collecting = True
    if collecting:
        to_remove.append(el)
    if el is end._p:
        break
for el in to_remove:
    body.remove(el)
print(f"Página 'Cómo se usa esta plantilla' eliminada ({len(to_remove)} elementos).")

# Se capturan AMBAS tablas originales (1.5 Recursos y 3. Resultados) y sus
# anclas de insercion ANTES de insertar nada mas: insertar tablas nuevas
# desplaza los indices de doc.tables, asi que cualquier referencia dinamica
# posterior (doc.tables[N]) apuntaria a la tabla equivocada.
orig_recursos_tbl = doc.tables[0]
orig_resultados_tbl = doc.tables[1]
recursos_anchor = docx.text.paragraph.Paragraph(
    orig_recursos_tbl._tbl.getnext(), orig_recursos_tbl._parent)
resultados_anchor = docx.text.paragraph.Paragraph(
    orig_resultados_tbl._tbl.getnext(), orig_resultados_tbl._parent)

# ------------------------------------------------------------------
# 3) SECCION 1 — Informacion sobre el evento practico
# ------------------------------------------------------------------
h11 = find_paragraph(doc, text_exact='1.1 Título del evento práctico')
insert_paragraph_before(
    find_paragraph(doc, text_exact='1.2 Objetivos'),
    'Modelado de la arquitectura empresarial actual y objetivo de la Escuela '
    'Profesional de Ingeniería de Sistemas (EPIS), Universidad Privada de Tacna, '
    'con ArchiMate 3.2: las tres capas de la arquitectura actual, la vista de '
    'cooperación proceso-aplicación, la estructura de la información con sus '
    'fuentes autoritativas y dueños de dato, la arquitectura objetivo derivada de '
    'la visión y la cultura ya diagnosticadas, y el análisis de brechas que '
    'deriva los paquetes de trabajo de la Sección 5 del PETI.'
)

h12_anchor = find_paragraph(doc, text_exact='1.3 Tiempo de duración')
for b in [
    'Declarar los principios de arquitectura que gobernarán las decisiones del plan.',
    'Modelar la arquitectura actual en las tres capas con ArchiMate 3.2.',
    'Construir la vista de cooperación proceso-aplicación y detectar procesos sin soporte.',
    'Construir la estructura de la información con fuentes autoritativas y dueños de dato.',
    'Modelar la arquitectura objetivo derivada de la visión (Sección 2.2) y de la '
    'cultura diagnosticada (Sección 2.4).',
    'Ejecutar el análisis de brechas y derivar los paquetes de trabajo.',
    'Redactar la Sección 5 del PETI.',
]:
    p = insert_paragraph_before(h12_anchor, f"• {b}", size=11, space_after=3)
    p.paragraph_format.left_indent = Cm(0.6)

h13_anchor = find_paragraph(doc, text_exact='1.4 Resultados de aprendizaje')
insert_paragraph_before(
    h13_anchor,
    'Sesión 2 de laboratorio de la Semana 10, según lo programado en el sílabo del curso.'
)

h14_anchor = find_paragraph(doc, text_exact='1.5 Recursos')
insert_paragraph_before(
    h14_anchor,
    'Esta guía no declara un resultado de aprendizaje adicional para esta sesión. '
    'El taller opera sobre los RA ya declarados para el curso —RA1, dirección '
    'estratégica; RA2, análisis FODA—, aplicados ahora a la capa de arquitectura '
    'empresarial que sostiene las decisiones de ambos.'
)

add_table_before(
    recursos_anchor,
    ["Recurso", "Versión", "Para qué se usó"],
    [
        ["Archi", "5.x (modelador ArchiMate libre)",
         "Especificación del modelo actual y objetivo (ver nota sobre el modelo en el README)"],
        ["ArchiMate 3.2 Specification", "The Open Group", "Notación y capas del modelo"],
        ["TOGAF Standard, 10.ª ed.", "The Open Group", "Método ADM que enmarca la fase de arquitectura"],
        ["Python 3.13", "3.13.7", "Scripts de análisis de brechas y de generación de vistas"],
        ["pandas", "librería", "Agrupación de brechas en paquetes y secuencia por dependencias"],
        ["matplotlib", "librería", "Generación de las tres vistas en PNG con paleta ArchiMate"],
        ["Git / GitHub CLI", "2.98.0", "Versionado del modelo, Pull Request y etiquetas taller-10 / v0.10"],
        ["LibreOffice Calc / Excel", "—", "Edición y revisión de AR02_entidades.csv y AR03_brechas.csv"],
    ],
    TABLE_STYLE,
)
orig_recursos_tbl._tbl.getparent().remove(orig_recursos_tbl._tbl)

h16 = find_paragraph(doc, text_exact='1.6 Seguridad')
seg_anchor = find_paragraph(doc, text_exact='2. Procedimiento o metodología')
set_paragraph_text(
    find_paragraph(doc, text_startswith='Reglas de uso del laboratorio'),
    '1. El modelo de arquitectura describe la superficie completa de sistemas, '
    'integraciones y tecnología de la organización analizada. Se trata como '
    'información Restringida: es un mapa útil para un atacante.'
)
insert_paragraph_before(
    seg_anchor,
    '2. No se incluyen en el modelo direcciones IP, credenciales, versiones '
    'exactas de software vulnerable ni rutas internas.'
)
insert_paragraph_before(
    seg_anchor,
    '3. El archivo del modelo y sus especificaciones se almacenan en el '
    'repositorio del taller; las cifras de registros por sistema son '
    'estimaciones ilustrativas, declaradas como tales en el README, y no una '
    'extracción de los sistemas reales de la Escuela.'
)
insert_paragraph_before(
    seg_anchor,
    '4. Las vistas que se incluyen en este informe se generan sin el detalle '
    'técnico sensible: sin IP, sin credenciales, sin versiones de software.'
)

# ------------------------------------------------------------------
# 4) SECCION 2 — Procedimiento o metodologia
# ------------------------------------------------------------------
set_paragraph_text(
    find_paragraph(doc, text_startswith='Cada paso lleva su título'),
    'Organización analizada: Escuela Profesional de Ingeniería de Sistemas '
    '(EPIS-UPT), continuando el diagnóstico de identidad y cultura del Taller '
    '05. Cada paso nombra el archivo que se crea en el repositorio del taller '
    '— https://github.com/AngelVargasGutierrez/PETI-TALLER10 — y su evidencia.'
)

pasoA = find_paragraph(doc, text_exact='Paso A')
insert_paragraph_before(
    find_paragraph(doc, text_exact='Paso B'),
    'Declaración de seis principios de arquitectura en '
    '05_arquitectura/AR01_principios.md, cada uno con su declaración, razón, '
    'implicancias y trazabilidad: P-01 Dato único con dueño, P-02 Las hojas de '
    'cálculo son arquitectura, P-03 Interoperabilidad por servicios, P-04 '
    'Clasificación antes de integrar, P-05 La arquitectura objetivo se deriva, '
    'P-06 Ninguna brecha se cierra sin dependencias explícitas. Los seis se '
    'derivan del diagnóstico cultural (Jerarquía dominante, Sección 2.4) y del '
    'patrón de datos sin dueño detectado en esta misma sesión.'
)
screenshot_placeholder(find_paragraph(doc, text_exact='Paso B'), '1')

pasoB_anchor = find_paragraph(doc, text_exact='Paso C')
insert_paragraph_before(
    pasoB_anchor,
    'Modelado de la arquitectura actual en Archi, en las tres capas: negocio '
    '(diez procesos de la cadena de valor académico-administrativa, desde '
    'Admisión hasta Seguimiento al egresado), aplicación (Sistema Académico, '
    'Campus Virtual, Tesorería/Caja, Portal de Grados y Títulos, y dos hojas de '
    'cálculo que sostienen procesos críticos) y tecnología (servidor académico '
    'on-premise, hosting en nube del Campus Virtual, estaciones de trabajo y '
    'enlace a internet institucional).'
)
figure_before(pasoB_anchor, 1, "Arquitectura actual de EPIS-UPT, tres capas", G1,
              "Nota. Elaboración propia a partir del modelo especificado en "
              "AR01–AR02 (05_arquitectura/), 2026.")
insert_paragraph_before(
    pasoB_anchor,
    'La estructura de la información se construyó en '
    '05_arquitectura/AR02_entidades.csv: siete entidades con sus sistemas, su '
    'conteo estimado de registros, su clasificación y si contienen datos '
    'personales. Resultado: 4 de 7 entidades sin fuente autoritativa ni dueño '
    '(Estudiante, Docente —parcial—, Curso/Sílabo, Egresado); el caso de '
    'Egresado reproduce dentro de la propia Escuela el mismo patrón '
    'diagnosticado para una organización externa en la dinámica «Rastreo del '
    'dato» de esta misma semana.'
)
insert_paragraph_before(
    pasoB_anchor,
    'La vista de cooperación proceso-aplicación mostró 3 de 7 procesos con '
    'soporte deficiente (coordinación curricular de acreditación, seguimiento '
    'al egresado, atención de consultas del estudiante) y uno parcial '
    '(cobranza de pensión).'
)
figure_before(pasoB_anchor, 2, "Vista de cooperación proceso-aplicación, EPIS-UPT", G2,
              "Nota. Elaboración propia a partir de 05_arquitectura/5_arquitectura_"
              "empresarial.md §5.2.5, 2026.")
screenshot_placeholder(pasoB_anchor, '2')

# Paso C ya existe como encabezado en la plantilla; se le agrega contenido.
h3_anchor = find_paragraph(doc, text_exact='3. Resultados')
insert_paragraph_before(
    h3_anchor,
    'Modelado de la arquitectura objetivo, derivada de tres insumos ya '
    'producidos: la visión de TI (Sección 2.2), las implicancias del '
    'diagnóstico cultural (Sección 2.4, CU04_implicancias_peti.md) y los '
    'principios de arquitectura (Paso A). Cada cambio quedó trazado a su '
    'origen en la tabla de 5_arquitectura_empresarial.md §5.3.2: el más '
    'relevante, un maestro único de Estudiante en el Sistema Académico con '
    'dueño designado (Secretaría Académica), que resuelve el hallazgo '
    'principal del Paso B.'
)
figure_before(h3_anchor, 3, "Arquitectura objetivo de EPIS-UPT, cambios marcados ★", G3,
              "Nota. Elaboración propia a partir de 5_arquitectura_empresarial.md "
              "§5.3, 2026.")

# --- Paso D: analisis de brechas y paquetes de trabajo ---
insert_paragraph_before(h3_anchor, 'Paso D', style='Heading 2', size=13, bold=True)
insert_paragraph_before(
    h3_anchor,
    'Ejecución de 05_arquitectura/AR03_brechas.py: trece brechas declaradas en '
    'cuatro capas (4 Datos, 4 Aplicación, 3 Negocio, 2 Tecnología), agrupadas '
    'en cinco paquetes de trabajo y secuenciadas por orden topológico de sus '
    'dependencias.'
)
code_lines = [
    "=== Paquetes de trabajo ===",
    "WP-1 Gobierno del dato                 4 brechas  esfuerzo 16",
    "WP-2 Integracion academico-financiera   2 brechas  esfuerzo 8",
    "WP-3 Portal de autoservicio             1 brecha   esfuerzo 5",
    "WP-4 Formalizacion de procesos          4 brechas  esfuerzo 13",
    "WP-5 Infraestructura y continuidad      2 brechas  esfuerzo 6",
    "",
    "=== Secuencia obligada (orden topologico) ===",
    "1. WP-1 Gobierno del dato",
    "2. WP-5 Infraestructura y continuidad",
    "3. WP-2 Integracion academico-financiera",
    "4. WP-4 Formalizacion de procesos informales",
    "5. WP-3 Portal de autoservicio del estudiante",
]
cb = insert_paragraph_before(h3_anchor, "", space_before=4, space_after=8, indent_cm=0.4)
shd = OxmlElement('w:shd'); shd.set(qn('w:val'), 'clear'); shd.set(qn('w:fill'), 'F2F2F2')
cb._p.get_or_add_pPr().append(shd)
r0 = cb.add_run(code_lines[0]); set_font(r0, "Consolas", 9)
for ln in code_lines[1:]:
    cb.add_run().add_break()
    r = cb.add_run(ln); set_font(r, "Consolas", 9)
insert_paragraph_before(
    h3_anchor,
    'Salida completa en evidencias/S10/salidas/brechas.txt. Ejecutar el '
    'portafolio sin respetar esta secuencia —por ejemplo, WP-3 antes que '
    'WP-1— produciría un portal de autoservicio que muestra las mismas cifras '
    'discrepantes que hoy nadie reconoce como válidas.'
)

# --- Paso E: vistas y redaccion de seccion 5 ---
insert_paragraph_before(h3_anchor, 'Paso E', style='Heading 2', size=13, bold=True)
insert_paragraph_before(
    h3_anchor,
    'Generación de las tres vistas mínimas con 05_arquitectura/AR04_vistas.py '
    '(Figuras 1–3 de este informe) y redacción de la Sección 5 completa del '
    'PETI en 05_arquitectura/5_arquitectura_empresarial.md, con sus cinco '
    'subsecciones (5.1 a 5.4) y los hallazgos numéricos de cada una.'
)

# --- Paso F: validar y corregir ---
insert_paragraph_before(h3_anchor, 'Paso F', style='Heading 2', size=13, bold=True)
for chk in [
    '1. Se revisó que cada elemento del modelo esté en la capa que le '
    'corresponde (negocio, aplicación o tecnología). Corregido: «Hojas de '
    'cálculo» se había dejado fuera del modelo en un primer borrador; se '
    'incorporó como componente de aplicación por el Principio P-02.',
    '2. Se verificó que toda aplicación del modelo actual exista de verdad en '
    'la Escuela: Sistema Académico, Campus Virtual, Tesorería/Caja y Portal de '
    'Grados y Títulos son sistemas reales y de uso cotidiano del autor como '
    'estudiante de la Escuela.',
    '3. Se comprobó que cada brecha de AR03_brechas.csv se puede señalar en '
    'los dos modelos (actual y objetivo): las trece brechas tienen su elemento '
    'correspondiente marcado en al menos una de las vistas.',
]:
    insert_paragraph_before(h3_anchor, chk, space_after=4)

# --- Paso G: evidencia y cierre ---
insert_paragraph_before(h3_anchor, 'Paso G', style='Heading 2', size=13, bold=True)
insert_paragraph_before(
    h3_anchor,
    f'Se versionó el trabajo en la rama taller-10, se abrió el Pull Request '
    f'#1 ({PR_URL}) hacia main, se fusionó, y se crearon las etiquetas '
    f'taller-10 ({TALLER_TAG_URL}) y v0.10 ({V_TAG_URL}) sobre el commit '
    f'entregado.'
)
screenshot_placeholder(h3_anchor, '3')
insert_paragraph_before(
    h3_anchor,
    'Pregunta de transferencia — qué riesgo correría una organización real si '
    'esto se hiciera mal: respondida en la Sección 5 (Cuestionario) de este '
    'informe.'
)

# ------------------------------------------------------------------
# 5) SECCION 3 — Resultados (checklist 3.2, con evidencia en GitHub)
# ------------------------------------------------------------------
BASE = f"{REPO}/blob/taller-10"
TREE = f"{REPO}/tree/taller-10"
resultados = [
    ["1", "Seis principios de arquitectura con sus cinco campos y trazabilidad",
     "Sí", f"{BASE}/05_arquitectura/AR01_principios.md"],
    ["2", "Modelo con las tres capas de la arquitectura actual",
     "Parcial — especificado en AR01/AR02 y en las vistas; el .archimate "
     "nativo se construye en Archi a partir de esa especificación (ver README)",
     f"{TREE}/graficos"],
    ["3", "Las hojas de cálculo modeladas como componentes de aplicación",
     "Sí", f"{BASE}/05_arquitectura/AR01_principios.md"],
    ["4", "Vista de cooperación proceso-aplicación, procesos sin soporte identificados",
     "Sí", f"{BASE}/graficos/AR_cooperacion_proceso_aplicacion.png"],
    ["5", "Estructura de la información con ≥ 6 entidades, sistemas y registros",
     "Sí — 7 entidades", f"{BASE}/05_arquitectura/AR02_entidades.csv"],
    ["6", "Entidades sin fuente autoritativa y sin dueño identificadas y contadas",
     "Sí — 4 de 7", f"{BASE}/05_arquitectura/AR02_entidades.csv"],
    ["7", "Entidades con datos personales marcadas, con su clasificación",
     "Sí", f"{BASE}/05_arquitectura/AR02_entidades.csv"],
    ["8", "Arquitectura objetivo modelada, cada cambio trazado a su origen",
     "Sí", f"{BASE}/05_arquitectura/5_arquitectura_empresarial.md"],
    ["9", "Análisis de brechas con ≥ 10 brechas, tipo, esfuerzo y dependencias",
     "Sí — 13 brechas", f"{BASE}/05_arquitectura/AR03_brechas.csv"],
    ["10", "Paquetes de trabajo derivados de las brechas",
     "Sí — 5 paquetes", f"{BASE}/evidencias/S10/salidas/brechas.txt"],
    ["11", "Secuencia obligada por dependencias determinada",
     "Sí", f"{BASE}/evidencias/S10/salidas/brechas.txt"],
    ["12", "Tres vistas exportadas en PNG, sin detalle técnico sensible",
     "Sí", f"{TREE}/graficos"],
    ["13", "Sección 5 redactada · etiqueta v0.10",
     "Sí", V_TAG_URL],
]
add_table_before(resultados_anchor, ["#", "Resultado esperado", "¿Se logró?", "Evidencia (GitHub)"],
                  resultados, TABLE_STYLE)
orig_resultados_tbl._tbl.getparent().remove(orig_resultados_tbl._tbl)

set_paragraph_text(
    find_paragraph(doc, text_startswith='Si algo no se logró'),
    'El único resultado no logrado al 100 % es el ítem 2: no se produjo el '
    'archivo nativo .archimate porque Archi no está disponible como '
    'herramienta de línea de comandos en el entorno donde se generó este '
    'informe. El modelo está completamente especificado (elementos, capas y '
    'relaciones) en AR01_principios.md y AR02_entidades.csv, y representado en '
    'las tres vistas PNG; construirlo en Archi a partir de esa especificación '
    'es el paso manual pendiente, documentado en el README del repositorio.'
)

# ------------------------------------------------------------------
# 6) SECCION 4 — Conclusiones
# ------------------------------------------------------------------
set_paragraph_text(
    find_paragraph(doc, text_startswith='Mínimo tres. Una conclusión'),
    'La capa de datos es la que más valor aporta al diagnóstico y la que menos '
    'existe documentada. Preguntar quién es el dueño de Estudiante o de '
    'Egresado en EPIS-UPT reveló exactamente el mismo síntoma que la dinámica '
    '«Rastreo del dato» diagnosticó para una organización externa: varias '
    'áreas mantienen su propia versión del dato y ninguna responde por la '
    'cifra oficial.'
)
c4_anchor = find_paragraph(doc, text_exact='5. Cuestionario')
insert_paragraph_before(
    c4_anchor,
    'La arquitectura objetivo no se inventa. Se derivó de la visión de TI '
    '(Sección 2.2) y de las implicancias del diagnóstico cultural (Sección '
    '2.4): la Escuela se coordina como Jerarquía pero se mide como Mercado '
    '(incongruencia detectada en el Taller 05), y esa misma incongruencia es '
    'la que explica por qué hoy nadie es dueño del dato de Egresado —se mide '
    'la captación de postulantes, no se gestiona el ciclo de vida completo del '
    'estudiante.'
)
insert_paragraph_before(
    c4_anchor,
    'Las dependencias entre paquetes de trabajo imponen una secuencia que la '
    'hoja de ruta debe respetar: el análisis de brechas obligó a WP-1 '
    '(gobierno del dato) antes que WP-3 (portal de autoservicio del '
    'estudiante), porque un portal nuevo sobre datos sin dueño solo cambiaría '
    'la interfaz en la que la Escuela sigue sin poder responder cuántos '
    'egresados activos tiene.'
)
insert_paragraph_before(
    c4_anchor,
    'Modelar con el mismo rigor una hoja de cálculo y un sistema formal '
    '—Principio P-02— cambió el diagnóstico: sin esa decisión, el seguimiento '
    'al egresado y la coordinación curricular de acreditación habrían '
    'quedado fuera del modelo por no ser «sistemas», cuando en la práctica '
    'sostienen procesos de los que depende la acreditación de la Escuela.'
)

# ------------------------------------------------------------------
# 7) SECCION 5 — Cuestionario (pregunta de transferencia del Paso G)
# ------------------------------------------------------------------
set_paragraph_text(
    find_paragraph(doc, text_startswith='Copia cada pregunta'),
    'Pregunta de transferencia (Paso G). Si una organización real modelara su '
    'arquitectura actual sin incluir las hojas de cálculo que sostienen '
    'procesos críticos —como se hizo aquí con el seguimiento al egresado y la '
    'coordinación curricular—, el diagnóstico de brechas quedaría incompleto '
    'y el portafolio de proyectos no incluiría el gobierno de esos datos. '
    'El riesgo concreto es repetir, en cualquier área de la organización, el '
    'mismo hallazgo de la dinámica «Rastreo del dato»: una cifra que gerencia '
    'pide y que nadie puede sostener con una sola fuente.'
)

# ------------------------------------------------------------------
# 8) SECCION 6 — Referencias bibliograficas
# ------------------------------------------------------------------
refs = [
    'The Open Group. (2022). TOGAF Standard, 10th Edition. '
    'https://www.opengroup.org/togaf',
    'The Open Group. (2022). ArchiMate 3.2 Specification. '
    'https://pubs.opengroup.org/architecture/archimate3-doc/',
    'Archi. Archi — Open Source ArchiMate Modelling. '
    'https://www.archimatetool.com/',
    'ISACA. (2018). COBIT 2019, objetivo APO03 Managed Enterprise Architecture. '
    'https://www.isaca.org/resources/cobit',
    'Ross, J. W., Weill, P., y Robertson, D. C. (2006). Enterprise Architecture '
    'as Strategy. Harvard Business School Press.',
    'Lankhorst, M. (2017). Enterprise Architecture at Work: Modelling, '
    'Communication and Analysis (4.ª ed.). Springer.',
    'Rodríguez Bermúdez, J. R. (2015). Planificación y dirección estratégica de '
    'sistemas de información. Editorial UOC. '
    'https://elibro.net/es/lc/bibliotecaupt/titulos/57875',
    'MINTIC Colombia. Marco de Referencia de Arquitectura Empresarial para la '
    'gestión de TI. https://www.mintic.gov.co/arquitecturati/630/w3-channel.html',
    'Decreto Supremo 029-2021-PCM — arquitectura digital del Estado peruano. '
    'https://www.gob.pe/13326-reglamento-de-la-ley-de-gobierno-digital',
]
ref6_anchor = find_paragraph(doc, text_exact='7. Anexos')
set_paragraph_text(
    find_paragraph(doc, text_startswith='Normas técnicas, marcos profesionales'),
    refs[0]
)
for r in refs[1:]:
    reference_before(ref6_anchor, r)

# ------------------------------------------------------------------
# 9) SECCION 7 — Anexos
# ------------------------------------------------------------------
anexos = [
    f'Anexo A — AR01_principios.md (seis principios de arquitectura). {BASE}/05_arquitectura/AR01_principios.md',
    f'Anexo B — AR02_entidades.csv (estructura de la información). {BASE}/05_arquitectura/AR02_entidades.csv',
    f'Anexo C — Vistas PNG de la arquitectura actual, cooperación proceso-aplicación y objetivo. {TREE}/graficos',
    f'Anexo D — AR03_brechas.csv y salida de AR03_brechas.py (brechas y paquetes de trabajo). {BASE}/evidencias/S10/salidas/brechas.txt',
    f'Anexo E — 5_arquitectura_empresarial.md (Sección 5 completa del PETI). {BASE}/05_arquitectura/5_arquitectura_empresarial.md',
    f'Anexo F — Pull Request #1 fusionado y etiquetas taller-10 / v0.10. {PR_URL}',
]
anexo_anchor_text = 'Capturas completas, archivos de configuración'
a7 = find_paragraph(doc, text_startswith=anexo_anchor_text)
set_paragraph_text(a7, anexos[0])
last = a7
for a in anexos[1:]:
    new_p_el = OxmlElement('w:p')
    last._p.addnext(new_p_el)
    np = docx.text.paragraph.Paragraph(new_p_el, last._parent)
    run = np.add_run(a)
    set_font(run, BODY_FONT, 11)
    last = np

print("Contenido insertado.")
os.makedirs(os.path.dirname(OUT), exist_ok=True) if os.path.dirname(OUT) else None
doc.save(OUT)
print("Guardado en:", OUT)

