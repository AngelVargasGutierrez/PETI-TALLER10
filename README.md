# PETI-TALLER10

Repositorio dedicado al **Taller de laboratorio 10** del curso **SI-886 Planeamiento
Estratégico de TI** (Universidad Privada de Tacna): *Modelado de la arquitectura
actual y objetivo en Archi*.

Este taller es parte del PETI que se construye a lo largo del semestre en el repositorio
acumulativo [`peti-si886`](https://github.com/AngelVargasGutierrez/peti-si886), siguiendo
la misma convención de los talleres dedicados
[Taller 04](https://github.com/AngelVargasGutierrez/PETI-TALLER4) y
[Taller 05](https://github.com/AngelVargasGutierrez/PETI-TALLER5).

**Autor** · Vargas Gutierrez, Angel Jose · 2020066922
**Docente** · Dr. Oscar Juan Jimenez Flores

---

## Organización analizada

**Escuela Profesional de Ingeniería de Sistemas (EPIS)** — Facultad de Ingeniería,
Universidad Privada de Tacna. Continúa el análisis de identidad y cultura del
[Taller 05](https://github.com/AngelVargasGutierrez/PETI-TALLER5).

## Hallazgo principal

**4 de 7 entidades de información críticas no tienen fuente autoritativa ni dueño
designado** (Estudiante, Docente —parcial—, Curso/Sílabo, Egresado), y **3 de 7
procesos corren sobre soporte deficiente** (coordinación curricular de
acreditación, seguimiento al egresado, atención de consultas del estudiante),
con un cuarto en estado parcial (cobranza de pensión). El caso de Egresado
reproduce dentro de la propia Escuela el mismo patrón diagnosticado para una
organización externa en la dinámica «Rastreo del dato» de esta misma semana:
tres sistemas, tres cifras, ningún cargo responde por la oficial.

El análisis de brechas derivó **13 brechas** en 4 capas, agrupadas en **5
paquetes de trabajo**, con una secuencia obligada por dependencias:
**Gobierno del dato → Infraestructura → Integración académico-financiera →
Formalización de procesos → Portal de autoservicio del estudiante.** Ejecutar
el portal antes que el gobierno del dato produciría una interfaz nueva
mostrando las mismas cifras que hoy nadie reconoce como válidas.

## Advertencia sobre el origen de los datos

Los conteos de registros por sistema en `AR02_entidades.csv` son **estimaciones
ilustrativas**, no una extracción de los sistemas reales de la Escuela —misma
limitación declarada en el Taller 05 para la encuesta piloto del CVF—. Lo que
sí es observación directa: la existencia de los sistemas, los procesos que
corren sobre hojas de cálculo, y la ausencia de un dueño formal para el dato
de egresados, consistentes con la experiencia del autor como estudiante de la
Escuela.

## Contenido

| Archivo | Qué es |
|---|---|
| `05_arquitectura/AR01_principios.md` | Seis principios de arquitectura, con declaración, razón, implicancias y trazabilidad |
| `05_arquitectura/AR02_entidades.csv` | Estructura de la información: 7 entidades, sistemas, fuente autoritativa y dueño |
| `05_arquitectura/AR03_brechas.py` | Programa del taller: declara las brechas, calcula paquetes de trabajo y la secuencia por dependencias |
| `05_arquitectura/AR03_brechas.csv` | Salida: 13 brechas con capa, tipo, esfuerzo y dependencias |
| `05_arquitectura/AR04_vistas.py` | Genera las tres vistas mínimas en PNG con la paleta de color de ArchiMate por capa |
| `05_arquitectura/5_arquitectura_empresarial.md` | **Sección 5 del PETI** — arquitectura actual, objetivo y análisis de brechas |
| `graficos/AR_vista_actual.png` | Vista de arquitectura actual, tres capas |
| `graficos/AR_cooperacion_proceso_aplicacion.png` | Vista de cooperación proceso-aplicación |
| `graficos/AR_vista_objetivo.png` | Vista de arquitectura objetivo, cambios marcados ★ |
| `evidencias/S10/salidas/brechas.txt` | Salida literal de `AR03_brechas.py` |
| `build_informe.py` | Genera el informe a partir de la plantilla oficial del curso |
| `SI886-S10-TALLER-Grupo1.docx` / `.pdf` | Informe de laboratorio |

## Nota sobre el modelo en Archi

Este repositorio no incluye el archivo `.archimate` nativo: se construye abriendo
**Archi** y modelando los elementos y relaciones exactamente como se
especifican en `AR01_principios.md`, `AR02_entidades.csv` y
`5_arquitectura_empresarial.md`. Las tres vistas PNG de `graficos/` representan
el mismo modelo con la paleta de color estándar de ArchiMate, para que el
contenido del informe sea verificable sin depender de tener Archi instalado.

## Reproducir

```bash
cd 05_arquitectura
python AR03_brechas.py | tee ../evidencias/S10/salidas/brechas.txt
python AR04_vistas.py
cd ..
python build_informe.py
```

El informe se exporta a PDF desde Word, actualizando el índice antes (clic derecho sobre el
índice → Actualizar campos).

Requiere Python 3.11 o superior con `pandas`, `matplotlib` y `python-docx`.
