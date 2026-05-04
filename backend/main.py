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

# Configurar CORS de forma muy permisiva para producción y desarrollo
cors_origins_raw = os.getenv("CORS_ORIGINS", "")
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8000",
    "https://desarrollos-wuaicot.vercel.app",
]

if cors_origins_raw:
    try:
        # Intenta cargarlo como JSON (ej: ["url1", "url2"])
        extra_origins = json.loads(cors_origins_raw)
        if isinstance(extra_origins, list):
            origins.extend(extra_origins)
        else:
            origins.append(str(extra_origins))
    except json.JSONDecodeError:
        # Si falla, asume que es una lista separada por comas (ej: url1, url2)
        origins.extend([o.strip() for o in cors_origins_raw.split(",") if o.strip()])

# Eliminar duplicados
origins = list(set(origins))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {
        "status": "online",
        "origins_configured": origins,
        "env_var_present": bool(cors_origins_raw)
    }

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# Base de conocimiento enriquecida de Naycol Linares
KNOWLEDGE_BASE = {
    "saludo": {
        "keywords": ["hola", "buenos dias", "buenas tardes", "buenas noches", "hey", "saludos", "que tal", "como vas", "habla", "que onda"],
        "response": "¡Hola! Un gusto saludarte. Soy el asistente virtual de Naycol Linares. ¿Te gustaría conocer su trayectoria, los servicios que ofrece para escalar negocios o cómo contactarlo directamente?"
    },
    "perfil": {
        "keywords": ["quien eres", "naycol", "linares", "experiencia", "director", "perfil", "quien es", "trayectoria", "sobre ti", "cv", "resumen"],
        "response": "Naycol Linares es Director de Desarrollo y experto en React. Se especializa en crear arquitecturas escalables y soluciones digitales de alto impacto. Ha liderado equipos técnicos internacionales enfocados en la excelencia, el rendimiento y la innovación tecnológica."
    },
    "servicios": {
        "keywords": ["servicios", "que haces", "trabajo", "desarrollo", "react", "consultoria", "arquitectura", "web", "programacion", "apps", "software"],
        "response": "Naycol ofrece servicios de: 1. Desarrollo Fullstack de alto nivel (MERN). 2. Arquitectura de Software escalable. 3. Auditoría de rendimiento web (Core Web Vitals). 4. Mentoría y liderazgo de equipos técnicos. 5. Transformación digital para empresas."
    },
    "contacto": {
        "keywords": ["contacto", "cita", "presupuesto", "contratar", "reunion", "correo", "email", "telefono", "numero", "whatsapp", "celular", "llamar", "agenda", "portafolio", "sitio", "web"],
        "response": "Puedes contactar a Naycol directamente al +56946230876 También te invito a visitar su portafolio detallado en: https://mi-portafolio-full-stack.vercel.app. Para consultas formales, puedes usar el formulario al final de esta página."
    },
    "proyectos_especificos": {
        "keywords": ["proyectos", "portfolio", "trabajos", "inventario", "sistema", "negocio", "empresa", "software", "aplicacion", "app", "tienda", "e-commerce", "automatizar"],
        "response": "Naycol ha desarrollado desde sistemas CRM inmobiliarios hasta plataformas de e-learning y dashboards analíticos complejos. Su especialidad es automatizar procesos de negocio mediante software a medida. Puedes ver ejemplos en la sección de 'Galería' de esta página."
    },
    "tecnologias": {
        "keywords": ["stack", "tecnologias", "lenguajes", "programacion", "python", "javascript", "mern", "aws", "backend", "frontend", "typescript", "node", "fastapi", "sql", "mongodb"],
        "response": "Su stack principal es JavaScript/TypeScript (React, Node.js, Next.js). En el backend domina Python (FastAPI/Django) y tiene amplia experiencia en infraestructuras cloud (AWS/Azure) y bases de datos tanto SQL como NoSQL."
    },
    "agradecimiento": {
        "keywords": ["gracias", "muchas gracias", "agradecido", "perfecto", "buena onda", "vale", "ok", "entendido", "genial", "super"],
        "response": "¡De nada! Es un placer ayudarte. Si tienes más dudas sobre el trabajo de Naycol o quieres iniciar un proyecto, aquí estaré. ¿Hay algo más que te gustaría saber?"
    },
    "despedida": {
        "keywords": ["adios", "chao", "hasta luego", "nos vemos", "bye", "hasta pronto", "me voy"],
        "response": "¡Hasta luego! Gracias por visitar el portafolio de Naycol. ¡Que tengas un excelente día!"
    },
    "estado": {
        "keywords": ["estas", "disponible", "ocupado", "vives", "donde estas", "ubicacion", "chile", "valparaiso", "vina del mar"],
        "response": "¡Aquí estoy! Siempre listo para responder tus dudas. Físicamente, Naycol reside en Viña del Mar, Chile, pero trabaja con clientes y equipos de todo el mundo de forma remota."
    },
    "ayuda": {
        "keywords": ["ayuda", "opciones", "que preguntar", "que sabes hacer", "help", "no se"],
        "response": "Puedo hablarte sobre la experiencia de Naycol, detallar su stack tecnológico, explicarte sus servicios de consultoría o indicarte cómo agendar una reunión con él. ¿Qué te interesa más?"
    }
}

def get_chatbot_response(user_message: str) -> str:
    user_message = user_message.lower().strip()
    
    # Manejo rápido de agradecimientos cortos
    if user_message in ["gracias", "vale", "ok", "listo"]:
        return KNOWLEDGE_BASE["agradecimiento"]["response"]

    # Manejo rápido de saludos cortos
    if user_message in ["hola", "hey", "buenas"]:
        return KNOWLEDGE_BASE["saludo"]["response"]

    best_match = None
    highest_score = 0
    
    # Buscamos la mejor coincidencia usando lógica difusa
    for category, content in KNOWLEDGE_BASE.items():
        # Usamos ratio de conjunto de tokens para manejar frases desordenadas
        match_info = process.extractOne(user_message, content["keywords"], scorer=fuzz.token_set_ratio)
        
        if match_info and match_info[1] > highest_score:
            highest_score = match_info[1]
            best_match = category

    # Si la confianza es alta, respondemos con esa categoría
    if highest_score > 65:
        return KNOWLEDGE_BASE[best_match]["response"]
    
    # Respuesta inteligente por defecto (si no entiende nada)
    return "Entiendo. Esa es una consulta interesante. Como asistente enfocado en el perfil profesional de Naycol, puedo contarte sobre sus servicios en React, su experiencia como Director de Desarrollo o cómo contactarlo. ¿Te gustaría profundizar en alguno de estos temas?"

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
