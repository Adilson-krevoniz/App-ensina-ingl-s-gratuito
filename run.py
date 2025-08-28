import os
import uvicorn
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Obter configurações do servidor
HOST = os.getenv("SERVER_HOST", "0.0.0.0")
PORT = int(os.getenv("SERVER_PORT", "8000"))

if __name__ == "__main__":
    print(f"Iniciando servidor Alex Bot em {HOST}:{PORT}...")
    print("Pressione CTRL+C para encerrar")
    
    # Iniciar servidor Uvicorn
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=True,
        log_level="info"
    )