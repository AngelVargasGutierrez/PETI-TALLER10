# 05_arquitectura/AR01_principios.md — Sección 5.1 del PETI

**Organización analizada.** Escuela Profesional de Ingeniería de Sistemas (EPIS),
Facultad de Ingeniería, Universidad Privada de Tacna. Continúa el análisis de
2.3_valores.md y 2.4_cultura.md (PETI-TALLER5).

Seis principios de arquitectura, derivados del diagnóstico cultural (Jerarquía
dominante, brecha −15,5 frente a Clan) y de la fragmentación de datos detectada en
el modelado de esta sesión (Sección 5.2.2).

## P-01 · Dato único con dueño

| Campo | Contenido |
|---|---|
| **Declaración** | Cada entidad de información académica o administrativa tiene una única fuente autoritativa y un dueño de dato designado por cargo. |
| **Razón** | El modelado de la Sección 5.2 encontró entidades críticas (Estudiante, Egresado) replicadas en 3 o más sistemas sin dueño declarado; las decisiones de gestión académica se toman hoy con cifras que no concuerdan entre Secretaría Académica, Tesorería y Bienestar Estudiantil. |
| **Implicancias** | Ningún proyecto puede crear una segunda base de una entidad existente. Todo proyecto que consuma una entidad debe leerla de su fuente autoritativa. El proyecto de gobierno del dato antecede a cualquier proyecto de analítica o de tableros de indicadores de acreditación. |
| **Trazabilidad** | Hallazgo Sección 5.2.2 (entidades sin fuente autoritativa); dinámica «Rastreo del dato», Semana 10. |

## P-02 · Las hojas de cálculo son arquitectura, no un atajo

| Campo | Contenido |
|---|---|
| **Declaración** | Toda hoja de cálculo que sostiene un proceso académico o administrativo crítico se modela, se documenta y se migra con el mismo rigor que un sistema formal. |
| **Razón** | El seguimiento al egresado, la coordinación curricular para la acreditación y parte de la cobranza de pensiones corren hoy sobre hojas de cálculo que nadie reconoce como «sistema», pero de cuyo contenido depende la acreditación y la caja. |
| **Implicancias** | No se automatiza alrededor de una hoja de cálculo sin primero decidir si se reemplaza o se formaliza como fuente autoritativa temporal, con dueño y respaldo. |
| **Trazabilidad** | Sección 5.2.2 — Objetos de datos en hojas de cálculo. |

## P-03 · Interoperabilidad por servicios, no por archivo plano

| Campo | Contenido |
|---|---|
| **Declaración** | Toda integración nueva entre el sistema académico, el campus virtual y el sistema administrativo-financiero se publica como servicio con contrato de interfaz versionado, no como archivo plano o carga manual. |
| **Razón** | La sincronización actual de notas y matrícula hacia el campus virtual y hacia tesorería depende de procesos nocturnos y de reingreso manual, lo que retrasa la visibilidad de la deuda y de la condición de matriculado. |
| **Implicancias** | El inventario de interfaces (Sección 5.2.3) se congela para integraciones nuevas: cualquier archivo plano nuevo requiere excepción justificada ante la Dirección de la Escuela. |
| **Trazabilidad** | Sección 5.2.3 — Interfaces; Sección 5.4 — brechas de capa Aplicación. |

## P-04 · La información personal y académica sensible se clasifica antes de integrarse

| Campo | Contenido |
|---|---|
| **Declaración** | Ninguna entidad que contenga datos personales (estudiante, trabajador, egresado) se integra, se reporta o se usa para analítica sin que su clasificación de confidencialidad esté declarada y su tratamiento, registrado. |
| **Razón** | El modelado encontró entidades «Estudiante» y «Trabajador» con datos personales y, en el caso de Trabajador, datos sensibles de planilla, sin un registro de actividades de tratamiento documentado. |
| **Implicancias** | Todo proyecto de analítica académica pasa primero por el inventario de tratamiento de datos personales (alineado a la Ley 29733 y su reglamento). |
| **Trazabilidad** | Sección 5.2.2 — columna «¿Contiene datos personales?»; marco normativo adoptado en Sección 4.1. |

## P-05 · La arquitectura objetivo se deriva, no se diseña por moda

| Campo | Contenido |
|---|---|
| **Declaración** | Todo cambio propuesto en la arquitectura objetivo se traza a la visión de TI, a una capacidad requerida o a una estrategia ya formulada; no se incorpora tecnología sin ese origen documentado. |
| **Razón** | La Escuela mide su desempeño como «mercado» (captación de postulantes) pero se coordina como «jerarquía» (Sección 2.4); una arquitectura objetivo sin trazabilidad explícita reproduciría esa incongruencia en los sistemas. |
| **Implicancias** | La tabla de la Sección 5.3.2 exige, para cada fila, el origen del cambio. Una fila sin origen se devuelve al equipo. |
| **Trazabilidad** | Sección 5.3.1 — Derivación. |

## P-06 · Ninguna brecha se cierra sin dependencias explícitas

| Campo | Contenido |
|---|---|
| **Declaración** | Todo paquete de trabajo que surge del análisis de brechas declara sus dependencias con otros paquetes antes de entrar a la hoja de ruta del portafolio. |
| **Razón** | Ejecutar un proyecto de analítica o de tablero de indicadores antes que el de gobierno del dato (P-01) produce cifras que la propia Escuela no reconocería como válidas, replicando el síntoma diagnosticado en la dinámica de esta semana. |
| **Implicancias** | La Sección 7.1 (portafolio) no admite un paquete de analítica sin que su dependencia de gobierno del dato esté marcada como completada o en curso. |
| **Trazabilidad** | Sección 5.4.2 y 5.4.3 — paquetes de trabajo y secuencia obligada. |
