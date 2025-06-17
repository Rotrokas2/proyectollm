import os
import re
from enum import Enum
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from ollama import chat

class Mode(str, Enum):
    consulta = "consulta"
    tutor    = "tutor"

class ChatRequest(BaseModel):
    prompt: str
    mode:    Mode  # 'consulta' o 'tutor'

class ChatResponse(BaseModel):
    response: str

app = FastAPI()

# 1. Servir static/index.html en la raíz "/"
@app.get("/")
async def read_index():
    project_root = os.path.dirname(os.path.abspath(__file__))
    return FileResponse(os.path.join(project_root, "static", "index.html"))

# 2. Montar la carpeta "static" (JS, CSS, imágenes)
project_root = os.path.dirname(os.path.abspath(__file__))
static_folder = os.path.join(project_root, "static")
app.mount("/static", StaticFiles(directory=static_folder), name="static")

# 3. Endpoint /chat con modos 'consulta' y 'tutor'
@app.post("/chat", response_model=ChatResponse)
async def get_chat_response(req: ChatRequest):
    """
    Recibe JSON {"prompt": "<texto>", "mode": "consulta"|"tutor"}
    - Modo consulta: envía prompt directo al LLM.
    - Modo tutor: añade un system prompt que NUNCA revele la respuesta original,
      solo explique el concepto y resuelva un ejercicio ANÁLOGO.
    """
    mensajes = []

    if req.mode == Mode.tutor:
        system_prompt = (
            "Eres un tutor experto. Cuando el usuario plantee un problema "
            "con valores específicos (por ejemplo, “¿Cuánto es 32 × 3?”), "
            "NO debes resolver ese problema ni revelar su resultado. En su lugar:\n"
            "1. Explica el concepto o procedimiento que subyace al problema.\n"
            "2. Plantea y resuelve paso a paso un ejercicio ANÁLOGO con valores diferentes, "
            "mostrando únicamente la respuesta del ejercicio análogo.\n"
            "3. Bajo ninguna circunstancia muestres la solución al problema original."
        )
        mensajes.append({"role": "system", "content": system_prompt})

    mensajes.append({"role": "user", "content": req.prompt})

    # Llamada al modelo
    respuesta = chat(model="deepseek-r1:7b", messages=mensajes)
    content = respuesta.message.content

    # Si estamos en modo tutor, eliminamos bloques de pensamiento interno (<think>...</think>)
    if req.mode == Mode.tutor:
        content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()

    return ChatResponse(response=content)

