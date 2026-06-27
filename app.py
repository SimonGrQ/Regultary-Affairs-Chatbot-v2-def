import os
from dotenv import load_dotenv
from rag import configure_gemini, load_vector_db, retrieve_context, build_rag_prompt
from document_generator import generate_pdf_from_markdown, create_export_filename
from device_state import DeviceState

# Cargar variables de entorno
load_dotenv()

SYSTEM_PROMPT_PATH = "prompts/system_mdr.txt"
if not os.path.exists(SYSTEM_PROMPT_PATH):
    raise FileNotFoundError(f"No se encontró el archivo de prompt del sistema: {SYSTEM_PROMPT_PATH}")

with open(SYSTEM_PROMPT_PATH, "r", encoding="utf8") as f:
    SYSTEM_PROMPT = f.read()

model = configure_gemini(system_instruction=SYSTEM_PROMPT)
chat = model.start_chat()

# Cargar la base de vectores
db = load_vector_db(persist_directory="mdr_db")

# Estado estructurado de la sesión
state = DeviceState(session_id="mdr_chat_session")

print("MDR Bot listo. Escribe '/pdf' después de una respuesta para descargarla en documento oficial.")
print("Usa 'salir', 'exit' o 'quit' para terminar.")

while True:
    try:
        question = input("
Tú: ")
        if question.lower() in ["salir", "exit", "quit"]:
            print("¡Hasta luego!")
            break

        if not question.strip():
            continue

        if question.strip().lower() == "/pdf":
            ultima_respuesta = state.get("last_response")
            if not ultima_respuesta:
                print("
MDR Bot: Todavía no hay ninguna respuesta previa que pueda exportar.")
                continue

            print("
Generando PDF...")
            filename = create_export_filename("mdr_document")
            archivo_creado = generate_pdf_from_markdown(ultima_respuesta, filename)
            print(f"¡Éxito! PDF guardado en: {archivo_creado}")
            continue

        context = retrieve_context(db, question, k=5)
        prompt = build_rag_prompt(context, question)

        response = chat.send_message(prompt)
        respuesta_texto = getattr(response, "text", None) or str(response)

        state.update("last_response", respuesta_texto)
        print(f"
MDR Bot:
{respuesta_texto}")

    except KeyboardInterrupt:
        print("
Chat finalizado.")
        break
    except Exception as e:
        print(f"
Ocurrió un error inesperado: {e}")
