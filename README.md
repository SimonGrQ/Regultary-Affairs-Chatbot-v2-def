# MDR-RAG-Bot | Asistente Regulatory Affairs MDR 2017/745 UE

Bot RAG con Gemini 1.5 Flash + ChromaDB especializado en MDR.
No alucina: todas las respuestas se construyen sobre documentación citada.

## Estructura del proyecto

```text
mdr-chatbot/
│
├── app.py                    ← Solo controla el chat
├── rag.py                    ← Recuperación de contexto y configuración del modelo
├── device_state.py           ← Memoria estructurada de la sesión
├── document_generator.py     ← Genera Word/PDF desde texto/Markdown
├── prompts/
│      system_mdr.txt
│      annex2_prompt.txt
│      cer_prompt.txt
│      risk_prompt.txt
│
├── templates/
│      annex2.docx
│      cer.docx
│      risk.docx
│
├── documents/
│
├── mdr_db/
│
└── exportaciones/
```

## Qué hace cada módulo

- `app.py`: controla el flujo de chat, pedidos de usuario y comandos especiales.
- `rag.py`: encapsula la creación del modelo Gemini, carga de Chroma y recuperación de contexto.
- `device_state.py`: guarda el estado de sesión y la última respuesta para exportar.
- `document_generator.py`: genera documentos PDF y Word, con carpeta de exportación.
- `prompts/`: contiene instrucciones de sistema y prompts específicos para Anexo II, certificación y riesgos.
- `templates/`: plantillas `.docx` base para generar documentos formales.

## Funcionalidades nuevas

- Respuestas RAG apoyadas en `mdr_db` y documentación cargada.
- Memoria estructurada simple para guardar la última respuesta.
- Exportación de la última respuesta como PDF con `/pdf`.
- Plantillas Word listas para extender con contenido regulatorio.
- Prompts especializados para:
  - `annex2_prompt.txt`
  - `cer_prompt.txt`
  - `risk_prompt.txt`

## Instalación y uso

```bash
cd "C:/Users/simon/OneDrive/Escritorio/IA projects/mdr-chatbot-RAG-def-main/mdr-chatbot-RAG-def-main"
pip install -r requirements.txt
```

1. Crea o actualiza tu archivo `.env` con la API key:

```text
GEMINI_API_KEY=tu_api_key
```

2. Coloca tus PDFs en `documents/`.

3. Indexa la documentación y crea la base de vectores:

```bash
python build_db.py
```

4. Arranca el chat:

```bash
python app.py
```

## Comandos disponibles

- Pregunta normal: el bot responde usando el contexto RAG.
- `/pdf`: exporta la última respuesta a PDF dentro de `exportaciones/`.
- `salir`, `exit`, `quit`: termina la sesión.

## Requisitos

- Python 3.11+
- Dependencias en `requirements.txt`

## Notas

- Las plantillas `.docx` son placeholders base y pueden ajustarse a tu formato final.
- `mdr_db/` se usa para persistir la base de vectores entre ejecuciones.
- Si no hay `prompts/system_mdr.txt`, `app.py` lanzará un error claro.
