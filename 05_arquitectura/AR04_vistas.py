# 05_arquitectura/AR04_vistas.py
"""Genera las 3 vistas minimas en PNG, con la paleta de color habitual de
ArchiMate por capa (negocio=amarillo, aplicacion=celeste, tecnologia=verde).
No requiere Archi instalado: representa el mismo modelo declarado en
AR01/AR02/AR03 para incluir en el informe. El modelo interactivo (.archimate)
se construye en Archi a partir de esta misma especificacion.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D

NEGOCIO = "#FFFFB3"
APLICACION = "#B3D9FF"
TECNOLOGIA = "#B3FFB3"
BORDE = "#4D4D4D"


def box(ax, x, y, w, h, text, color, fontsize=8.5):
    b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.04",
                        linewidth=1.1, edgecolor=BORDE, facecolor=color)
    ax.add_patch(b)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
             fontsize=fontsize, wrap=True)


def arrow(ax, p1, p2, style="-|>", color=BORDE):
    a = FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=10,
                         color=color, linewidth=1.0)
    ax.add_patch(a)


# ------------------------------------------------------------------
# Vista 1 — Arquitectura actual (as-is), tres capas
# ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 8))
ax.set_xlim(0, 13); ax.set_ylim(0, 8); ax.axis("off")
ax.text(0.2, 7.7, "EPIS-UPT · Arquitectura actual (as-is)", fontsize=13, fontweight="bold")

ax.text(0.2, 6.9, "NEGOCIO", fontsize=10, fontweight="bold", color="#7A6A00")
negocio_procesos = ["Admisión", "Matrícula", "Dictado y\nevaluación",
                     "Cobranza de\npensión", "Titulación", "Seguimiento\nal egresado"]
for i, p in enumerate(negocio_procesos):
    box(ax, 0.3 + i * 2.05, 6.0, 1.85, 0.8, p, NEGOCIO)

ax.text(0.2, 4.9, "APLICACIÓN", fontsize=10, fontweight="bold", color="#004C99")
apps = [("Sistema\nAcadémico", 0.3), ("Campus\nVirtual", 2.35), ("Tesorería /\nCaja", 4.4),
        ("Portal de\nGrados y Títulos", 6.45), ("Hoja de cálculo\nseguim. egresado", 8.9),
        ("Hoja de cálculo\ncoord. curricular", 11.1)]
for name, x in apps:
    box(ax, x, 4.0, 1.9, 0.8, name, APLICACION, fontsize=8)

ax.text(0.2, 2.9, "TECNOLOGÍA", fontsize=10, fontweight="bold", color="#0D6B0D")
tecnologia = [("Servidor académico\n(on-premise)", 0.3), ("Nube — hosting\nCampus Virtual", 3.0),
              ("Estaciones de\ntrabajo", 5.7), ("Enlace a\ninternet", 8.4)]
for name, x in tecnologia:
    box(ax, x, 2.0, 2.3, 0.8, name, TECNOLOGIA, fontsize=8)

# relaciones ilustrativas negocio->aplicacion->tecnologia
arrow(ax, (1.2, 6.0), (1.25, 4.8))
arrow(ax, (3.3, 6.0), (3.3, 4.8))
arrow(ax, (5.3, 6.0), (5.35, 4.8))
arrow(ax, (1.25, 4.0), (1.45, 2.8))
arrow(ax, (3.3, 4.0), (4.15, 2.8))
ax.annotate("Integración nocturna\npor archivo plano", (2.6, 3.55), fontsize=7.5,
            color="#B00020", ha="center")
arrow(ax, (3.3, 4.4), (4.4, 4.4), style="-|>", color="#B00020")

plt.tight_layout()
plt.savefig("../graficos/AR_vista_actual.png", dpi=150)
plt.close(fig)

# ------------------------------------------------------------------
# Vista 2 — Cooperacion proceso-aplicacion
# ------------------------------------------------------------------
filas = [
    ("Admisión y matrícula", "Sistema Académico", "Bueno", "#2E7D32"),
    ("Dictado y evaluación", "Sistema Académico + Campus Virtual", "Bueno", "#2E7D32"),
    ("Cobranza de pensión", "Tesorería + hoja de cálculo de convenios", "Parcial", "#B8860B"),
    ("Coordinación curricular (acreditación)", "Hoja de cálculo paralela", "Deficiente", "#B00020"),
    ("Titulación", "Portal de Grados y Títulos", "Bueno", "#2E7D32"),
    ("Seguimiento al egresado", "Hoja de cálculo + encuesta voluntaria", "Deficiente", "#B00020"),
    ("Atención de consultas del estudiante", "Correo / mensajería informal", "Deficiente", "#B00020"),
]
fig, ax = plt.subplots(figsize=(12.5, 5.2))
ax.axis("off")
ax.set_xlim(0, 12.5); ax.set_ylim(0, len(filas) + 1.3)
ax.text(0.1, len(filas) + 0.7, "EPIS-UPT · Vista de cooperación proceso-aplicación",
        fontsize=13, fontweight="bold")
headers = ["Proceso", "Sistema que lo soporta", "Nivel"]
col_x = [0.1, 4.9, 10.3]
for h, x in zip(headers, col_x):
    ax.text(x, len(filas) + 0.15, h, fontsize=10, fontweight="bold")
for i, (proceso, sistema, nivel, color) in enumerate(filas):
    y = len(filas) - i - 0.5
    ax.text(0.1, y, proceso, fontsize=9, va="center", wrap=True)
    ax.text(4.9, y, sistema, fontsize=9, va="center", wrap=True)
    ax.add_patch(FancyBboxPatch((10.3, y - 0.22), 1.9, 0.44,
                 boxstyle="round,pad=0.02,rounding_size=0.08",
                 facecolor=color, edgecolor="none", alpha=0.85))
    ax.text(11.25, y, nivel, fontsize=8.5, va="center", ha="center", color="white", fontweight="bold")
    ax.add_line(Line2D([0, 12.5], [y - 0.5, y - 0.5], color="#DDDDDD", linewidth=0.7))
plt.tight_layout()
plt.savefig("../graficos/AR_cooperacion_proceso_aplicacion.png", dpi=150)
plt.close(fig)

# ------------------------------------------------------------------
# Vista 3 — Arquitectura objetivo (to-be), cambios resaltados
# ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 8))
ax.set_xlim(0, 13); ax.set_ylim(0, 8); ax.axis("off")
ax.text(0.2, 7.7, "EPIS-UPT · Arquitectura objetivo (to-be)", fontsize=13, fontweight="bold")

ax.text(0.2, 6.9, "NEGOCIO", fontsize=10, fontweight="bold", color="#7A6A00")
negocio_obj = ["Admisión", "Matrícula", "Dictado y\nevaluación",
               "Cobranza de\npensión", "Titulación",
               "Seguimiento al\negresado (formal)"]
for i, p in enumerate(negocio_obj):
    nuevo = p.startswith("Seguimiento")
    box(ax, 0.3 + i * 2.05, 6.0, 1.85, 0.8, p + ("\n★ NUEVO" if nuevo else ""), NEGOCIO)

ax.text(0.2, 4.9, "APLICACIÓN", fontsize=10, fontweight="bold", color="#004C99")
apps_obj = [("Sistema\nAcadémico", 0.3), ("Campus\nVirtual", 2.35),
            ("Tesorería /\nCaja", 4.4),
            ("Portal único de\nautoservicio ★ NUEVO", 6.45),
            ("Módulo de gobierno\ndel dato ★ NUEVO", 8.9),
            ("Repositorio de\nacreditación sincronizado", 11.1)]
for name, x in apps_obj:
    box(ax, x, 4.0, 1.9, 0.8, name, APLICACION, fontsize=7.8)

ax.text(0.2, 2.9, "TECNOLOGÍA", fontsize=10, fontweight="bold", color="#0D6B0D")
tec_obj = [("Infraestructura con\nrespaldo verificado ★", 0.3),
           ("Nube — hosting\nCampus Virtual", 3.0),
           ("Capa de integración\npor servicios ★ NUEVO", 5.7),
           ("Plataforma de biblioteca\ncon soporte vigente ★", 8.4)]
for name, x in tec_obj:
    box(ax, x, 2.0, 2.3, 0.8, name, TECNOLOGIA, fontsize=7.8)

arrow(ax, (1.2, 6.0), (1.25, 4.8))
arrow(ax, (3.3, 6.0), (3.3, 4.8))
arrow(ax, (5.3, 6.0), (7.3, 4.8))
arrow(ax, (1.25, 4.0), (1.45, 2.8))
arrow(ax, (3.3, 4.4), (4.4, 4.4), style="-|>", color="#2E7D32")
ax.annotate("Servicios publicados\n(reemplaza archivo plano)", (5.4, 3.55), fontsize=7.5,
            color="#2E7D32", ha="center")
arrow(ax, (3.3, 4.0), (6.3, 2.8), style="-|>", color="#2E7D32")

plt.tight_layout()
plt.savefig("../graficos/AR_vista_objetivo.png", dpi=150)
plt.close(fig)

print("Vistas generadas en graficos/: AR_vista_actual.png, "
      "AR_cooperacion_proceso_aplicacion.png, AR_vista_objetivo.png")
