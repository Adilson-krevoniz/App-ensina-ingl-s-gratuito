import os
import json
from dotenv import load_dotenv
from app.database.db_manager import DatabaseManager
from app.services.ai_service import AIService
from app.services.whatsapp_service import WhatsAppService
from app.utils.logger import setup_logger

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logger
logger = setup_logger("test_bot")

# Inicializar serviços
db_manager = DatabaseManager(os.getenv("DATABASE_PATH", "database/alex_bot.db"))
ai_service = AIService(os.getenv("OPENAI_API_KEY"))
whatsapp_service = WhatsAppService(db_manager, ai_service)


def test_registration_flow():
    """Testa o fluxo de registro de um novo usuário"""
    logger.info("Testando fluxo de registro...")
    
    # Simular número de telefone
    phone_number = "+5511999999999"
    
    # Processar primeira mensagem (deve iniciar o registro)
    response = whatsapp_service.process_message(phone_number, "Olá")
    logger.info(f"Resposta inicial: {response}")
    
    # Processar nome
    response = whatsapp_service.process_message(phone_number, "João")
    logger.info(f"Resposta após nome: {response}")
    
    # Processar auto-avaliação de nível
    response = whatsapp_service.process_message(phone_number, "iniciante")
    logger.info(f"Resposta após nível: {response}")
    
    # Confirmar início da avaliação
    response = whatsapp_service.process_message(phone_number, "sim")
    logger.info(f"Resposta após confirmar avaliação: {response}")
    
    # Verificar se o usuário foi criado corretamente
    user = db_manager.get_user_by_phone(phone_number)
    logger.info(f"Usuário criado: {json.dumps(user, default=str)}")
    
    return user


def test_assessment_flow(user_id):
    """Testa o fluxo de avaliação de nível"""
    logger.info("Testando fluxo de avaliação...")
    
    # Obter sessão de avaliação atual
    phone_number = "+5511999999999"
    session = db_manager.get_assessment_session(user_id)
    
    if not session:
        logger.error("Sessão de avaliação não encontrada")
        return
    
    logger.info(f"Sessão de avaliação: {json.dumps(session, default=str)}")
    
    # Simular respostas para as perguntas de avaliação
    # Responder a 5 perguntas (ou o número que existir na sessão)
    questions_data = json.loads(session["questions_data"])
    num_questions = len(questions_data)
    
    for i in range(num_questions):
        # Simular uma resposta correta (para fins de teste)
        if questions_data[i]["question_type"] == "multiple_choice":
            # Para múltipla escolha, enviar a letra da resposta correta
            response = whatsapp_service.process_message(phone_number, questions_data[i]["correct_answer"])
        else:
            # Para resposta aberta, enviar a resposta correta
            response = whatsapp_service.process_message(phone_number, questions_data[i]["correct_answer"])
        
        logger.info(f"Resposta após pergunta {i+1}: {response}")
    
    # Verificar se a avaliação foi concluída
    user = db_manager.get_user_by_phone(phone_number)
    logger.info(f"Usuário após avaliação: {json.dumps(user, default=str)}")
    
    return user


def test_commands():
    """Testa os comandos disponíveis"""
    logger.info("Testando comandos...")
    
    phone_number = "+5511999999999"
    
    # Testar comando de ajuda
    response = whatsapp_service.process_message(phone_number, "/ajuda")
    logger.info(f"Resposta para /ajuda: {response}")
    
    # Testar comando de lição
    response = whatsapp_service.process_message(phone_number, "/licao")
    logger.info(f"Resposta para /licao: {response}")
    
    # Testar comando de nível
    response = whatsapp_service.process_message(phone_number, "/nivel")
    logger.info(f"Resposta para /nivel: {response}")
    
    # Testar comando de progresso
    response = whatsapp_service.process_message(phone_number, "/progresso")
    logger.info(f"Resposta para /progresso: {response}")
    
    # Testar comando de prática
    response = whatsapp_service.process_message(phone_number, "/pratica")
    logger.info(f"Resposta para /pratica: {response}")


def test_conversation():
    """Testa uma conversa normal"""
    logger.info("Testando conversa normal...")
    
    phone_number = "+5511999999999"
    
    # Enviar algumas mensagens de conversa
    messages = [
        "Hello, how are you today?",
        "I goed to the park yesterday",
        "What is the weather like?",
        "Can you help me with my English?"
    ]
    
    for msg in messages:
        response = whatsapp_service.process_message(phone_number, msg)
        logger.info(f"Mensagem: {msg}")
        logger.info(f"Resposta: {response}")


def main():
    """Função principal para testar o bot"""
    try:
        # Limpar usuário de teste se existir
        db_manager.execute_query(
            "DELETE FROM users WHERE phone_number = ?", ("+5511999999999",)
        )
        
        # Testar fluxo de registro
        user = test_registration_flow()
        
        if user and user["id"]:
            # Testar fluxo de avaliação
            user = test_assessment_flow(user["id"])
            
            # Testar comandos
            test_commands()
            
            # Testar conversa normal
            test_conversation()
        
        logger.info("Testes concluídos com sucesso!")
        
    except Exception as e:
        logger.error(f"Erro durante os testes: {e}")


if __name__ == "__main__":
    main()
