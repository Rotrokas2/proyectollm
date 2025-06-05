import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from ollama import chat

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str

app = FastAPI()

# 1. Endpoint para servir index.html en la raíz "/"
@app.get("/")
async def read_index():
    """
    Devuelve el archivo static/index.html cuando el usuario visite http://127.0.0.1:8000/
    """
    project_root = os.path.dirname(os.path.abspath(__file__))
    return FileResponse(os.path.join(project_root, "static", "index.html"))

# 2. Montamos la carpeta "static" (JS, CSS, imágenes) en "/static"
#    De esta forma, "/static/style.css" servirá static/style.css, etc.
project_root = os.path.dirname(os.path.abspath(__file__))
static_folder = os.path.join(project_root, "static")
app.mount("/static", StaticFiles(directory=static_folder), name="static")

# 3. Endpoint /chat que invoca a Ollama (DeepSeek 7B)
@app.post("/chat", response_model=ChatResponse)
async def get_chat_response(req: ChatRequest):
    """
    Este endpoint recibe un JSON con {"prompt": "<texto del usuario>"}
    y devuelve {"response": "<respuesta de DeepSeek 7B>"}
    """
    mensajes = [
        {"role": "user", "content": req.prompt}
    ]
    respuesta = chat(model="deepseek-r1:7b", messages=mensajes)
    contenido = respuesta.message.content
    return ChatResponse(response=contenido)

