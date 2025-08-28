import os
import uvicorn
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

# Importações dos módulos internos
from app.database.db_manager import DatabaseManager
from app.services.whatsapp_service import WhatsAppService
from app.services.ai_service import AIService
from app.models.user import User
from app.utils.logger import setup_logger

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logger
logger = setup_logger()

# Inicializar aplicação FastAPI
app = FastAPI(title="Alex - Bot de Ensino de Inglês")

# Inicializar serviços
db_manager = DatabaseManager(os.getenv("DATABASE_PATH"))
ai_service = AIService(os.getenv("OPENAI_API_KEY"))
whatsapp_service = WhatsAppService(
    account_sid=os.getenv("TWILIO_ACCOUNT_SID"),
    auth_token=os.getenv("TWILIO_AUTH_TOKEN"),
    phone_number=os.getenv("TWILIO_PHONE_NUMBER"),
    ai_service=ai_service,
    db_manager=db_manager
)


@app.on_event("startup")
async def startup_event():
    """Executado quando a aplicação inicia"""
    # Criar tabelas no banco de dados se não existirem
    db_manager.create_tables()
    logger.info("Aplicação iniciada com sucesso")


@app.post("/webhook")
async def webhook(request: Request):
    """Endpoint para receber mensagens do WhatsApp via Twilio"""
    try:
        form_data = await request.form()
        
        # Extrair dados da mensagem recebida
        sender = form_data.get("From", "")
        body = form_data.get("Body", "")
        media_url = form_data.get("MediaUrl0", None)
        
        # Processar a mensagem recebida
        response = await whatsapp_service.process_message(sender, body, media_url)
        
        # Criar resposta TwiML
        twiml_response = MessagingResponse()
        twiml_response.message(response)
        
        return JSONResponse(content={"success": True, "message": str(twiml_response)})
    
    except Exception as e:
        logger.error(f"Erro ao processar webhook: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Erro interno do servidor"}
        )


@app.get("/health")
async def health_check():
    """Endpoint para verificar se a aplicação está funcionando"""
    return {"status": "ok"}


if __name__ == "__main__":
    # Iniciar servidor
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run("main:app", host=host, port=port, reload=True)