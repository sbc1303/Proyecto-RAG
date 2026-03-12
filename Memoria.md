# Memoria del proyecto "Sistema RAG local"

## Descripción general

El objetivo del proyecto es construir un sistema de preguntas y respuestas sobre documentos creados de forma manual, usando exclusivamente herramientas de código abierto que se ejecutan en local, sin depender de ninguna API externa (OpenAi, Cohere o Voyage AI).

El resultado es una aplicación que indexa documentos de texto, los convierte en embeddings semánticos y, a través de una interfaz web, permite hacer preguntas en lenguaje natural sobre el contenido que se ha creado en los documentos de texto.

El sistema muestra tanto la respuesta generada como los fragmentos del corpus que se usaron como contexto para generarla, lo que permite entender cómo funciona el proceso de recuperación de la información de forma interna.

## Decisiones técnicas

**Modelo de lenguaje:** 
Se eligió `llama3.1` por ser una versión reciente de la familia LLaMA, cuenta con buen equilibrio entre rendimiento y requisitos de hardware. Se encuentra disponible directamente a través de Ollama sin necesidad de una configuración adicional.

**Embeddings:** 
Se usó `nomic-embed-text` por ser el modelo de embeddings recomendado para Ollama. Esto lo hace ligero y ofrece buenos resultados para un corpus de tamaño reducido.

**LlamaIndex frente a LangChain:** 
El enunciado proponía ambas opciones. El primer paso fue investigar las dos opciones. Con la información ya en la mano, se optó por LlamaIndex teniendo en cuenta que:

- LlamaIndex está más enfocado a la indexación y recuperación de datos, que es precisamente el núcleo de este proyecto.

- LangChain permite crear aplicaciones de procesamiento de lenguaje natural, lo que es ideal para la construcción de agentes y cadenas de procesamiento más complejas.

**ChromaDB en modo persistente:** Se optó por `PersistentClient` en lugar del modo `memoria` para no tener que reindexar los documentos cada vez que se lanza la aplicación, puesto que los embeddings se guardan en disco en la carpeta `chroma_db/` y se recuperan directamente en cada arranque.

**Interfaz con Streamlit:** Aunque era opcional, se implementó una interfaz web que muestra la respuesta generada, los fragmentos recuperados con una puntuación de similitud con la respuesta ofrecida y un historial de preguntas. Se implementó pensando en que para un usuario final es más fácil e intuitivo que trabajar desde el terminal.

## Problemas encontrados

**ChromaDB persistía embeddings antiguos:** Al modificar los documentos del corpus y reindexar sin borrar la carpeta `chroma_db/`, la base de datos mezclaba embeddings de versiones distintas, produciendo respuestas incorrectas o dando respuestas con los datos antiguos. El problema costó bastante en identificar porque inicialmente se pensaba que el fallo estaba en la ejecución de la interfaz, no en los datos. Una vez localizado el fallo dentro de la capa de indexación, la solución fue sencilla: borrar la carpeta `chroma_db/` antes de cada reindexado.

**Modelo de embeddings no disponible:** Antes de ejecutar `ingest.py` es necesario tener descargado el modelo `nomic-embed-text` en Ollama. Si no está, el script falla pero el mensaje de error no indica claramente que el problema sea ese. Costó bastante identificarlo porque al principio se pensaba que el fallo estaba en el código, hasta que se revisó Ollama y se vio que el modelo simplemente no estaba descargado. La solución fue ejecutar `ollama pull nomic-embed-text` antes de volver a intentarlo.

**Rutas relativas:** `SimpleDirectoryReader("data")` y `chromadb.PersistentClient` buscan las carpetas relativas al directorio desde el que se lanza el script. Si se ejecuta desde dentro de `src/` en lugar de desde la raíz del proyecto, no encuentra los archivos y falla. El problema costó detectarlo porque el error no dejaba claro qué ruta estaba buscando exactamente, y al principio no era obvio que el problema fuera simplemente desde dónde se estaba ejecutando el comando.

**Rendimiento en el primer arranque:** Al principio la interfaz iba muy lenta, cualquier pregunta tardaba demasiado en responder. El problema era que Streamlit recargaba el modelo y reconectaba con ChromaDB cada vez que se interactuaba con la página. La solución fue añadir el decorador `@st.cache_resource` a la función que carga el índice, lo que hace que solo se ejecute una vez por sesión en lugar de en cada interacción.

## Conclusión

La parte más costosa del proyecto no fue la implementación en sí, sino la fase previa: investigar las herramientas disponibles, entender cómo encajan entre sí y decidir la estructura antes de escribir una línea de código. Una vez clara la arquitectura, el desarrollo fue progresivo, aunque la fase final de pruebas y depuración de detalles también llevó tiempo al tener que ajustar comportamientos concretos, que es algo que siempre cuesta más de lo que parece al principio.

El proyecto ha resultado ser una práctica real y directa de conceptos con aplicación inmediata en el ámbito profesional. Construir el sistema desde cero y enfrentarse a los problemas de integración entre componentes ha sido la parte más valiosa del proceso.
