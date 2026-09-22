# Día 18 — Plan de aprendizaje: prompts efectivos con RAG

- **Competencia a desarrollar:** escribir prompts efectivos con RAG (cargar
  documentos propios + dar instrucciones dirigidas) para generar contenido
  personalizado — en este caso, aplicado a mi propio CV y una oferta de
  trabajo real.

- **Prompt de aprendizaje (Modo 1 — Explicador adaptativo):** le pedí a
  Claude que me explicara el patrón de un buen prompt con RAG partiendo de
  lo que ya sabía del Día 14 (RAG con mi código real), y que después me
  hiciera una pregunta de comprobación en vez de solo explicarme la teoría.

- **Ejercicio de comprobación:** se me pidió redactar, con mis propias
  palabras, el prompt que usaría con RAG (CV + oferta) para pedir ayuda con
  mi outreach/CV, aplicando 3 ingredientes: documento correcto, instrucción
  de qué cruzar (no solo qué leer), y criterio de salida explícito.

  **Mi primer intento (real, sin ayuda):**
  > "necesito que a partir de los siguientes archivos que subiré, mi CV y
  > la oferta de empleo, me puedas ayudar a construir y a mejorar mi CV, a
  > destacar y comparar otros postulados, para poder conseguir el empleo y
  > también en orientarme y enseñarme en los requisitos académicos"

  **Feedback recibido:** el documento correcto estaba bien identificado,
  pero el pedido era una lista de deseos generales, no una instrucción
  dirigida (ingrediente 2 faltante), no tenía criterio de salida explícito
  (ingrediente 3 faltante), y contenía un malentendido real sobre RAG:
  pedí "comparar con otros postulantes", pero RAG solo puede trabajar con
  los documentos que yo mismo proporciono — no tiene acceso a los CVs de
  otros candidatos reales de esa vacante.

  **Mi segundo intento (corregido, real):**
  > "necesito de acuerdo a los archivos CV + oferta de empleo que subiré,
  > que me des dónde tengo las 3 mayores fortalezas y las 3 amenazas en
  > cuanto a conocimientos y qué debo estudiar para una buena presentación
  > con respecto a la oferta del empleador, haz que el CV lo pueda generar
  > optimizado a la vanguardia del mercado para poder enviarlo en formato
  > PDF o en algún otro"

- **Qué entendí (avance real):** la diferencia entre pedirle algo vago a
  la IA ("ayúdame a mejorar esto") y darle una instrucción dirigida con
  formato de salida específico (3 fortalezas + 3 amenazas + qué estudiar +
  formato PDF). También entendí un límite real de RAG que no tenía claro
  antes: la IA no "sabe" cosas que no están en los documentos que yo le
  doy — no puede comparar mi CV contra postulantes reales de una vacante,
  porque no tiene acceso a esa información en ningún documento.

- **Qué sigo sin dominar (brecha honesta):** todavía no afiné del todo el
  ingrediente 2 en la parte de "qué debo estudiar" — quedó como una
  instrucción algo abierta, que podría generar una lista larga y genérica
  en vez de algo corto y accionable. Me falta práctica en acotar el
  alcance de una pregunta abierta dentro de un prompt más grande, no solo
  en la instrucción principal.

## Ejercicio de extensión — libro profesional no leído

Pendiente de ejecutar: identificar un libro relevante de ciencia de datos o
ingeniería de software que no haya leído, pedir un resumen estructurado, y
luego pedir 5 preguntas que el libro plantea pero no responde del todo —
para practicar quedarme con las preguntas abiertas en vez de solo consumir
el resumen como si fuera el aprendizaje completo.
