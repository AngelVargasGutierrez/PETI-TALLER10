# 05_arquitectura/AR03_brechas.py
"""
Analisis de brechas y derivacion de paquetes de trabajo.
EPIS-UPT (Taller 10, SI-886). No lee ningun archivo: las brechas estan
declaradas aqui, con su capa, tipo, esfuerzo y dependencias. El programa
calcula la agrupacion en paquetes, el esfuerzo total por paquete y la
secuencia obligada por dependencias (orden topologico).
"""
import pandas as pd

BRECHAS = [
    # id,   capa,          descripcion,                                                            tipo,        esfuerzo, depende_de
    ("G01", "Datos",       "Estudiante sin fuente autoritativa ni dueno (3 sistemas, 3 cifras)",     "Gobierno",  5, []),
    ("G02", "Datos",       "Egresado sin fuente autoritativa ni dueno (3 sistemas, 3 cifras)",       "Gobierno",  5, ["G01"]),
    ("G03", "Datos",       "Curso/Silabo sin fuente autoritativa para acreditacion",                 "Gobierno",  3, ["G01"]),
    ("G04", "Datos",       "Sin registro de actividades de tratamiento de datos personales",         "Cumplimiento", 3, ["G01"]),
    ("G05", "Negocio",     "Seguimiento al egresado depende de encuesta voluntaria, sin proceso",     "Proceso",   3, ["G02"]),
    ("G06", "Negocio",     "Atencion de consultas del estudiante sin registro ni trazabilidad",       "Proceso",   4, []),
    ("G07", "Negocio",     "Coordinacion curricular de acreditacion corre en hoja de calculo paralela","Proceso",  3, ["G03"]),
    ("G08", "Aplicacion",  "Integracion Academico-Campus Virtual por proceso nocturno sin confirmacion","Integracion", 4, ["G01"]),
    ("G09", "Aplicacion",  "Integracion Academico-Tesoreria no en tiempo real (deuda desactualizada)", "Integracion", 4, ["G01"]),
    ("G10", "Aplicacion",  "Sin portal unico de autoservicio: el estudiante usa 3 sistemas distintos", "Experiencia", 5, ["G08", "G09"]),
    ("G11", "Aplicacion",  "Repositorio de acreditacion desincronizado del Sistema Academico",         "Integracion", 3, ["G03", "G07"]),
    ("G12", "Tecnologia",  "Sistema Academico sobre infraestructura sin respaldo verificado",          "Continuidad", 4, []),
    ("G13", "Tecnologia",  "Plataforma de biblioteca en fin de soporte del proveedor",                 "Continuidad", 2, []),
]

df = pd.DataFrame(BRECHAS, columns=["id", "capa", "descripcion", "tipo", "esfuerzo", "depende_de"])

PAQUETES = {
    "WP-1 Gobierno del dato":                       ["G01", "G02", "G03", "G04"],
    "WP-2 Integracion academico-financiera":        ["G08", "G09"],
    "WP-3 Portal de autoservicio del estudiante":   ["G10"],
    "WP-4 Formalizacion de procesos informales":    ["G05", "G06", "G07", "G11"],
    "WP-5 Infraestructura y continuidad":           ["G12", "G13"],
}

id_to_wp = {gid: wp for wp, gids in PAQUETES.items() for gid in gids}
df["paquete"] = df["id"].map(id_to_wp)

resumen = (df.groupby("paquete")
             .agg(brechas=("id", "count"), esfuerzo_total=("esfuerzo", "sum"))
             .reindex(PAQUETES.keys()))

# Dependencias entre PAQUETES: un paquete depende de otro si alguna de sus
# brechas depende de una brecha que vive en otro paquete.
wp_deps = {wp: set() for wp in PAQUETES}
for _, row in df.iterrows():
    wp = id_to_wp[row["id"]]
    for dep_id in row["depende_de"]:
        dep_wp = id_to_wp[dep_id]
        if dep_wp != wp:
            wp_deps[wp].add(dep_wp)

# Orden topologico simple (Kahn) para la secuencia obligada.
# Copia profunda: cada paquete necesita su propio set, no el mismo objeto
# que wp_deps, porque el algoritmo vacia los sets a medida que avanza.
pendientes = {wp: set(deps) for wp, deps in wp_deps.items()}
secuencia = []
while pendientes:
    listos = [wp for wp, deps in pendientes.items() if not deps]
    if not listos:
        raise RuntimeError("Ciclo de dependencias entre paquetes de trabajo")
    listos.sort()
    secuencia.extend(listos)
    for wp in listos:
        pendientes.pop(wp)
    for deps in pendientes.values():
        deps.difference_update(listos)

if __name__ == "__main__":
    print("=== Brechas por capa ===")
    print(df["capa"].value_counts().to_string())
    print(f"\nTotal de brechas: {len(df)}  (minimo exigido: 10)")

    print("\n=== Paquetes de trabajo ===")
    print(resumen.to_string())

    print("\n=== Dependencias entre paquetes ===")
    for wp, deps in wp_deps.items():
        print(f"{wp:45s} <- {sorted(deps) if deps else '(sin dependencias)'}")

    print("\n=== Secuencia obligada (orden topologico) ===")
    for i, wp in enumerate(secuencia, 1):
        print(f"{i}. {wp}")

    df_out = df.copy()
    df_out["depende_de"] = df_out["depende_de"].apply(lambda xs: ";".join(xs) if xs else "")
    df_out.to_csv("AR03_brechas.csv", index=False, encoding="utf-8-sig")
    print("\nArchivo generado: AR03_brechas.csv")
