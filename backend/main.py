import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from thefuzz import fuzz, process
from dotenv import load_dotenv

import json

# Cargar variables de entorno
load_dotenv()

app = FastAPI()

# Configurar CORS de forma robusta
cors_origins_raw = os.getenv("CORS_ORIGINS", '["http://localhost:3000"]')
try:
    # Intenta cargarlo como JSON (ej: ["url1", "url2"])
    origins = json.loads(cors_origins_raw)
except json.JSONDecodeError:
    # Si falla, asume que es una lista separada por comas (ej: url1, url2)
    origins = [o.strip() for o in cors_origins_raw.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# Base de conocimiento personalizada de Naycol Linares
KNOWLEDGE_BASE = {
    "saludo": {
        "keywords": ["hola", "buenos dias", "buenas tardes", "hey", "saludos", "que tal"],
        "response": "¡Hola! Un gusto saludarte. Soy el asistente de Naycol Linares. ¿Te interesa saber sobre sus proyectos, servicios o quizás quieres saber cómo puede ayudar a escalar tu equipo técnico?"
    },
    "perfil": {
        "keywords": ["quien eres", "naycol", "experiencia", "director", "perfil", "quien es", "trayectoria", "sobre ti"],
        "response": "Naycol Linares es Director de Desarrollo y experto en React. Se especializa en crear arquitecturas escalables y soluciones digitales de alto impacto. Actualmente lidera equipos técnicos enfocados en la excelencia y el rendimiento."
    },
    "servicios": {
        "keywords": ["servicios", "que haces", "trabajo", "desarrollo", "react", "consultoria", "arquitectura", "web", "programacion"],
        "response": "Naycol se especializa en: 1. Desarrollo Fullstack con MERN (MongoDB, Express, React, Node). 2. Arquitectura de Software escalable. 3. Liderazgo técnico de equipos. 4. Optimización de rendimiento web."
    },
    "contacto": {
        "keywords": ["contacto", "cita", "presupuesto", "contratar", "reunion", "correo", "email", "telefono", "numero", "whatsapp", "celular", "llamar"],
        "response": "Para agendar una cita, solicitar un presupuesto o hablar sobre una colaboración, te recomiendo usar el formulario de contacto al final de esta página. Naycol revisa cada mensaje personalmente para darte la mejor atención."
    },
    "proyectos_especificos": {
        "keywords": ["inventario", "sistema", "negocio", "empresa", "software", "aplicacion", "app", "tienda", "e-commerce", "automatizar"],
        "response": "¡Esa es precisamente la especialidad de Naycol! Desarrollar soluciones a medida como sistemas de inventario, plataformas de e-commerce o automatización de procesos para negocios. Si me das más detalles por el formulario de contacto, él podrá asesorarte mejor."
    },
    "tecnologias": {
        "keywords": ["stack", "tecnologias", "lenguajes", "programacion", "python", "javascript", "mern", "aws", "backend", "frontend"],
        "response": "El stack principal de Naycol es JavaScript (React/Node.js), pero domina Python, bases de datos SQL/NoSQL y despliegues en la nube con AWS y Azure."
    },
    "ayuda": {
        "keywords": ["no se que preguntar", "ayuda", "opciones", "que puedes hacer", "que preguntar"],
        "response": "Puedo contarte sobre la trayectoria de Naycol, detallarte sus servicios técnicos, o explicarte cómo contactarlo para iniciar un proyecto. ¿Por dónde te gustaría empezar?"
    }
}

def get_chatbot_response(user_message: str) -> str:
    user_message = user_message.lower().strip()
    
    best_match = None
    highest_score = 0
    
    # Buscamos la mejor coincidencia usando lógica difusa (fuzzy logic)
    for category, content in KNOWLEDGE_BASE.items():
        # Comparamos el mensaje del usuario con cada palabra clave de la categoría
        match_info = process.extractOne(user_message, content["keywords"], scorer=fuzz.token_set_ratio)
        
        if match_info and match_info[1] > highest_score:
            highest_score = match_info[1]
            best_match = category

    # Si la confianza es mayor al 60%, respondemos con esa categoría
    if highest_score > 60:
        return KNOWLEDGE_BASE[best_match]["response"]
    
    # Respuesta inteligente por defecto
    return "Esa es una buena pregunta. Como asistente de Naycol, trato de ser preciso. Si buscas algo muy técnico o una propuesta comercial, lo ideal es que uses el formulario de contacto para que él mismo te responda con el detalle que mereces. ¿Te gustaría saber algo más sobre su trayectoria?"

@app.post("/chat", response_model=ChatResponse)
async def chat(chat_message: ChatMessage):
    if not chat_message.message:
        raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío")
    
    response_text = get_chatbot_response(chat_message.message)
    return ChatResponse(response=response_text)

@app.get("/")
async def root():
    return {"status": "Chatbot API is running"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
