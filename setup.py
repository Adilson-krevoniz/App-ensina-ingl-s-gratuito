import os
import sys
import subprocess
from dotenv import load_dotenv
from app.database.init_db import init_database


def setup_environment():
    """Configura o ambiente de desenvolvimento"""
    print("Configurando ambiente de desenvolvimento para Alex Bot...")
    
    # Verificar se Python 3.8+ está instalado
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("Erro: Python 3.8 ou superior é necessário")
        sys.exit(1)
    
    # Instalar dependências
    print("\nInstalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError:
        print("Erro ao instalar dependências. Verifique o arquivo requirements.txt")
        sys.exit(1)
    
    # Criar arquivo .env se não existir
    if not os.path.exists(".env"):
        print("\nCriando arquivo .env a partir do modelo...")
        if os.path.exists(".env.example"):
            with open(".env.example", "r") as example_file:
                with open(".env", "w") as env_file:
                    env_file.write(example_file.read())
            print("Arquivo .env criado. Por favor, edite-o com suas credenciais.")
        else:
            print("Erro: Arquivo .env.example não encontrado")
            sys.exit(1)
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # Criar diretórios necessários
    print("\nCriando diretórios necessários...")
    os.makedirs("logs", exist_ok=True)
    os.makedirs("database", exist_ok=True)
    
    # Inicializar banco de dados
    print("\nInicializando banco de dados...")
    db_path = os.getenv("DATABASE_PATH", "database/alex_bot.db")
    try:
        init_database(db_path)
    except Exception as e:
        print(f"Erro ao inicializar banco de dados: {e}")
        sys.exit(1)
    
    print("\nConfiguração concluída com sucesso!")
    print("\nPróximos passos:")
    print("1. Edite o arquivo .env com suas credenciais da Twilio e OpenAI")
    print("2. Configure o webhook da Twilio para apontar para sua URL pública")
    print("3. Execute 'python run.py' para iniciar o servidor")


if __name__ == "__main__":
    setup_environment()