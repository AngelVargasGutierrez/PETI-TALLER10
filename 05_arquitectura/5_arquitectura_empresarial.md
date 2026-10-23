## 5. Arquitectura empresarial

### 5.1 Principios de arquitectura

Seis principios de arquitectura, desarrollados íntegramente en
[`AR01_principios.md`](AR01_principios.md): **P-01** Dato único con dueño,
**P-02** Las hojas de cálculo son arquitectura, **P-03** Interoperabilidad por
servicios, **P-04** Clasificación antes de integrar, **P-05** La arquitectura
objetivo se deriva, **P-06** Ninguna brecha se cierra sin dependencias
explícitas. Cada uno con su declaración, razón, implicancias y trazabilidad al
diagnóstico cultural (Sección 2.4) y al hallazgo de la dinámica «Rastreo del
dato» de esta misma semana.

### 5.2 Arquitectura actual (as-is)

**5.2.1 Capa de negocio.** La Escuela opera diez procesos de cadena de valor
académico-administrativa: Admisión, Matrícula, Dictado y evaluación, Cobranza
de pensión, Titulación, Seguimiento al egresado, Coordinación curricular para
acreditación, Investigación, Bienestar estudiantil y Atención de consultas del
estudiante. Actores: estudiante, docente, Secretaría Académica, Tesorería,
Bienestar Estudiantil, Biblioteca, Grados y Títulos, Dirección de Escuela.
Véase la vista en
[`graficos/AR_vista_actual.png`](../graficos/AR_vista_actual.png).

**5.2.2 Capa de datos: entidades, fuentes autoritativas y dueños.** La
estructura de la información completa vive en
[`AR02_entidades.csv`](AR02_entidades.csv): siete entidades (Estudiante,
Docente, Curso/Sílabo, Matrícula/Pensión, Egresado, Trabajador administrativo,
Préstamo de biblioteca), cada una con sus sistemas, su conteo estimado de
registros, su clasificación y si contiene datos personales.

**Entidades sin fuente autoritativa: 4 de 7** (Estudiante, Docente —parcial—,
Curso/Sílabo, Egresado). El caso más crítico es **Egresado**: el Sistema
Académico, la hoja de cálculo de seguimiento y el Portal de Grados y Títulos
reportan tres cifras distintas, sin que ningún cargo responda por la cifra
oficial — el mismo patrón diagnosticado para una organización externa en la
dinámica de esta semana, reproducido dentro de la propia Escuela.

**5.2.3 Capa de aplicación: componentes, servicios e integraciones.**
Componentes: Sistema Académico, Campus Virtual, Tesorería/Caja, Portal de
Grados y Títulos, y dos hojas de cálculo que sostienen procesos críticos
(seguimiento al egresado, coordinación curricular). La integración
Académico↔Campus Virtual y Académico↔Tesorería corre por **proceso nocturno
de archivo plano**, no por servicio.

**5.2.4 Capa de tecnología: nodos, servicios y redes.** Servidor académico
on-premise sin respaldo verificado, hosting en nube para el Campus Virtual,
estaciones de trabajo administrativas y enlace a internet institucional. La
plataforma de biblioteca opera en una versión próxima a fin de soporte del
proveedor.

**5.2.5 Vista de cooperación proceso-aplicación.** Véase
[`graficos/AR_cooperacion_proceso_aplicacion.png`](../graficos/AR_cooperacion_proceso_aplicacion.png).

**Procesos sin soporte o con soporte deficiente: 3 de 7** (Coordinación
curricular, Seguimiento al egresado, Atención de consultas del estudiante), más
uno parcial (Cobranza de pensión).

### 5.3 Arquitectura objetivo (to-be)

**5.3.1 Derivación.** Cada cambio de la tabla siguiente se traza a un insumo ya
producido: la visión de TI (Sección 2.2), el diagnóstico cultural y sus
implicancias (Sección 2.4, `CU04_implicancias_peti.md`), o el principio de
arquitectura que lo exige (Sección 5.1). Ningún cambio se incorpora por moda.

**5.3.2 Cambios por capa, con su origen trazado**

| Capa | Elemento actual | Elemento objetivo | Origen del cambio |
|---|---|---|---|
| Negocio | Seguimiento al egresado por encuesta voluntaria sin proceso | Proceso formal de seguimiento al egresado, con responsable designado | Principio P-01; hallazgo 5.2.2 |
| Datos | Estudiante y Egresado sin fuente autoritativa | Maestro único de Estudiante en el Sistema Académico, con dueño designado (Secretaría Académica) | Principio P-01 |
| Datos | Sin registro de tratamiento de datos personales | Registro de actividades de tratamiento, alineado a la Ley 29733 | Principio P-04 |
| Aplicación | Integración Académico↔Tesorería por archivo plano nocturno | Capa de integración por servicios publicados, deuda visible en tiempo real | Principio P-03 |
| Aplicación | Estudiante usa tres sistemas distintos para su gestión | Portal único de autoservicio del estudiante | Visión de TI, Sección 2.2 |
| Aplicación | Coordinación curricular en hoja de cálculo paralela | Repositorio de acreditación sincronizado con el Sistema Académico | Principio P-02; acreditación (ICACIT/SINEACE) |
| Tecnología | Servidor académico sin respaldo verificado | Infraestructura con respaldo verificado y copia inmutable | Continuidad operativa — hallazgo 5.2.4 |
| Tecnología | Plataforma de biblioteca próxima a fin de soporte | Plataforma de biblioteca con soporte vigente | Plazo del proveedor — hallazgo 5.2.4 |

**5.3.3 Vistas objetivo.** Véase
[`graficos/AR_vista_objetivo.png`](../graficos/AR_vista_objetivo.png), con los
elementos nuevos marcados ★.

### 5.4 Análisis de brechas

**5.4.1 Tabla de brechas por capa y tipo.** Trece brechas declaradas y
calculadas en [`AR03_brechas.py`](AR03_brechas.py) / `AR03_brechas.csv`: 4 en
Datos, 4 en Aplicación, 3 en Negocio, 2 en Tecnología. Salida completa en
[`evidencias/S10/salidas/brechas.txt`](../evidencias/S10/salidas/brechas.txt).

**5.4.2 Paquetes de trabajo derivados**

| Paquete | Brechas | Esfuerzo total |
|---|---|---|
| WP-1 Gobierno del dato | G01–G04 | 16 |
| WP-2 Integración académico-financiera | G08, G09 | 8 |
| WP-3 Portal de autoservicio del estudiante | G10 | 5 |
| WP-4 Formalización de procesos informales | G05, G06, G07, G11 | 13 |
| WP-5 Infraestructura y continuidad | G12, G13 | 6 |

**Los paquetes de trabajo son el insumo directo del portafolio (Sección
7.1).**

**5.4.3 Dependencias y secuencia obligada**

WP-2 depende de WP-1; WP-4 depende de WP-1; WP-3 depende de WP-2. WP-1 y WP-5
no tienen dependencias y pueden iniciar en paralelo. Secuencia calculada por
orden topológico: **WP-1 → WP-5 → WP-2 → WP-4 → WP-3.** Ejecutar WP-3 (portal
de autoservicio, el más visible para el estudiante) antes que WP-1 produciría
un portal que muestra las mismas cifras discrepantes que hoy — exactamente el
riesgo que el principio P-06 busca evitar.
