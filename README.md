## Cómo ejecutar localmente

1. Clonar repo  
2. `pip install -r requirements.txt`  
3. `uvicorn main:app --reload --host 0.0.0.0 --port 8000`  
4. Abrir en el navegador `http://localhost:8000`


## Descripción del Proyecto

Este es un pequeño servicio web de chat offline que utiliza FastAPI y Ollama (DeepSeek-7B) para responder tus preguntas. La aplicación consta de dos componentes:

1. **Backend (FastAPI)**  
   - Sirve una página estática (`index.html`) y los recursos (CSS, JS) desde la carpeta `static/`.  
   - Expone un endpoint `POST /chat` que recibe un JSON con tu pregunta y el modo de uso, lo envía al modelo LLM y devuelve la respuesta.

2. **Frontend (HTML + JavaScript)**  
   - Al cargar la página, te pide elegir entre **Modo Consulta** y **Modo Tutor**.  
   - En **Modo Consulta**, el modelo responde de forma directa.  
   - En **Modo Tutor**, primero explica el concepto y luego resuelve un ejemplo análogo sin revelar la solución del problema original; además, oculta cualquier “pensamiento interno” del modelo.  
   - Usa MathJax para renderizar expresiones matemáticas en LaTeX y muestra un indicador “Pensando…” mientras el modelo genera la respuesta.

El flujo de uso es muy sencillo:  
1. Abres `http://localhost:8000` en tu navegador.  
2. Eliges el modo de interacción.  
3. Escribes tu pregunta en el campo de texto y presionas “Enviar”.  
4. Obtienes la respuesta directamente en la misma ventana de chat.
