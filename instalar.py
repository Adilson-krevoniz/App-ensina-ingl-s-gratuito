import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

# Cores para o terminal
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_colored(text, color):
    """Imprime texto colorido no terminal"""
    print(f"{color}{text}{Colors.END}")

def print_header(text):
    """Imprime um cabeçalho formatado"""
    print("\n" + "=" * 60)
    print_colored(f" {text} ".center(60), Colors.BOLD + Colors.BLUE)
    print("=" * 60)

def print_step(step, description):
    """Imprime um passo numerado"""
    print_colored(f"[{step}] {description}", Colors.BOLD + Colors.GREEN)

def print_info(text):
    """Imprime informação"""
    print_colored(f"ℹ️ {text}", Colors.BLUE)

def print_warning(text):
    """Imprime aviso"""
    print_colored(f"⚠️ {text}", Colors.YELLOW)

def print_error(text):
    """Imprime erro"""
    print_colored(f"❌ {text}", Colors.RED)

def print_success(text):
    """Imprime sucesso"""
    print_colored(f"✅ {text}", Colors.GREEN)

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    print_step(1, "Verificando versão do Python...")
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print_error("Python 3.8 ou superior é necessário!")
        print_info("Por favor, instale uma versão mais recente do Python em https://www.python.org/downloads/")
        webbrowser.open("https://www.python.org/downloads/")
        input("\nPressione Enter para sair...")
        sys.exit(1)
    print_success(f"Python {python_version.major}.{python_version.minor}.{python_version.micro} detectado!")
    return True

def install_dependencies():
    """Instala as dependências necessárias"""
    print_step(2, "Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print_success("Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError:
        print_error("Erro ao instalar dependências. Verifique o arquivo requirements.txt")
        return False

def setup_env_file():
    """Configura o arquivo .env com as credenciais do usuário"""
    print_step(3, "Configurando credenciais...")
    
    if os.path.exists(".env"):
        overwrite = input("Arquivo .env já existe. Deseja reconfigurá-lo? (s/n): ").lower() == 's'
        if not overwrite:
            print_info("Usando arquivo .env existente.")
            return True
    
    # Criar arquivo .env a partir do modelo
    if not os.path.exists(".env.example"):
        print_error("Arquivo .env.example não encontrado!")
        return False
    
    # Ler o modelo
    with open(".env.example", "r") as example_file:
        env_template = example_file.read()
    
    # Solicitar credenciais ao usuário
    print_info("\nVamos configurar suas credenciais para o bot de WhatsApp.")
    print_info("Você precisará de uma conta na Twilio e uma chave de API da OpenAI.")
    
    # Opção para abrir sites para registro
    open_twilio = input("Deseja abrir o site da Twilio para criar uma conta? (s/n): ").lower() == 's'
    if open_twilio:
        webbrowser.open("https://www.twilio.com/try-twilio")
        print_info("Aguarde até criar sua conta na Twilio...")
        input("Pressione Enter quando estiver pronto para continuar...")
    
    open_openai = input("Deseja abrir o site da OpenAI para obter uma chave de API? (s/n): ").lower() == 's'
    if open_openai:
        webbrowser.open("https://platform.openai.com/account/api-keys")
        print_info("Aguarde até obter sua chave de API da OpenAI...")
        input("Pressione Enter quando estiver pronto para continuar...")
    
    # Coletar credenciais
    print_header("Credenciais da Twilio")
    twilio_account_sid = input("Account SID: ").strip()
    twilio_auth_token = input("Auth Token: ").strip()
    twilio_phone_number = input("Número de telefone do WhatsApp (formato: whatsapp:+XXXXXXXXXXX): ").strip()
    
    print_header("Credencial da OpenAI")
    openai_api_key = input("API Key: ").strip()
    
    # Substituir no modelo
    env_content = env_template
    env_content = env_content.replace("your_twilio_account_sid", twilio_account_sid)
    env_content = env_content.replace("your_twilio_auth_token", twilio_auth_token)
    env_content = env_content.replace("whatsapp:+1234567890", twilio_phone_number)
    env_content = env_content.replace("your_openai_api_key", openai_api_key)
    
    # Salvar arquivo .env
    with open(".env", "w") as env_file:
        env_file.write(env_content)
    
    print_success("Arquivo .env configurado com sucesso!")
    return True

def initialize_database():
    """Inicializa o banco de dados"""
    print_step(4, "Inicializando banco de dados...")
    try:
        # Criar diretórios necessários
        os.makedirs("logs", exist_ok=True)
        os.makedirs("database", exist_ok=True)
        
        # Importar e executar a função de inicialização do banco de dados
        sys.path.append(os.getcwd())
        from app.database.init_db import init_database
        
        db_path = os.path.join("database", "alex_bot.db")
        init_database(db_path)
        
        print_success("Banco de dados inicializado com sucesso!")
        return True
    except Exception as e:
        print_error(f"Erro ao inicializar banco de dados: {e}")
        return False

def setup_webhook():
    """Ajuda o usuário a configurar o webhook da Twilio"""
    print_step(5, "Configuração do webhook da Twilio...")
    
    print_info("Para que o bot funcione, você precisa configurar um webhook na Twilio.")
    print_info("Você tem duas opções:")
    print_info("1. Usar ngrok para expor seu servidor local à internet (para testes)")
    print_info("2. Hospedar o bot em um servidor com IP público (para produção)")
    
    option = input("\nDeseja usar ngrok para testes locais? (s/n): ").lower() == 's'
    
    if option:
        # Verificar se ngrok está instalado
        try:
            subprocess.check_call(["ngrok", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print_success("ngrok detectado!")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print_warning("ngrok não encontrado. Vamos instalar...")
            install_ngrok = input("Deseja abrir o site para baixar o ngrok? (s/n): ").lower() == 's'
            if install_ngrok:
                webbrowser.open("https://ngrok.com/download")
                print_info("Siga as instruções de instalação do ngrok...")
                input("Pressione Enter quando a instalação estiver concluída...")
            else:
                print_warning("Você precisará instalar o ngrok manualmente mais tarde.")
                return False
        
        print_info("\nPara iniciar o servidor com ngrok, siga estes passos:")
        print_info("1. Abra um terminal e execute: python run.py")
        print_info("2. Abra outro terminal e execute: ngrok http 8000")
        print_info("3. Copie a URL HTTPS gerada pelo ngrok (ex: https://xxxx-xxxx.ngrok.io)")
        print_info("4. Configure essa URL + '/webhook' como webhook na Twilio")
        
        open_twilio_console = input("\nDeseja abrir o console da Twilio para configurar o webhook? (s/n): ").lower() == 's'
        if open_twilio_console:
            webbrowser.open("https://console.twilio.com/")
    else:
        print_info("\nPara hospedar o bot em um servidor:")
        print_info("1. Faça upload dos arquivos para seu servidor")
        print_info("2. Execute 'python setup.py' no servidor")
        print_info("3. Execute 'python run.py' para iniciar o servidor")
        print_info("4. Configure a URL do seu servidor + '/webhook' como webhook na Twilio")
    
    print_success("Instruções de configuração do webhook fornecidas!")
    return True

def start_server():
    """Pergunta ao usuário se deseja iniciar o servidor"""
    print_step(6, "Iniciar servidor...")
    
    start = input("Deseja iniciar o servidor agora? (s/n): ").lower() == 's'
    if start:
        print_info("Iniciando servidor...")
        print_info("Pressione CTRL+C para encerrar o servidor quando desejar.")
        time.sleep(2)
        try:
            subprocess.call([sys.executable, "run.py"])
            return True
        except KeyboardInterrupt:
            print_info("\nServidor encerrado pelo usuário.")
            return True
        except Exception as e:
            print_error(f"Erro ao iniciar o servidor: {e}")
            return False
    else:
        print_info("Para iniciar o servidor mais tarde, execute: python run.py")
        return True

def main():
    """Função principal de instalação"""
    print_header("INSTALAÇÃO DO BOT DE WHATSAPP PARA ENSINO DE INGLÊS")
    print_info("Este assistente irá guiá-lo através do processo de instalação e configuração.")
    
    # Verificar versão do Python
    if not check_python_version():
        return
    
    # Instalar dependências
    if not install_dependencies():
        return
    
    # Configurar arquivo .env
    if not setup_env_file():
        return
    
    # Inicializar banco de dados
    if not initialize_database():
        return
    
    # Configurar webhook
    if not setup_webhook():
        return
    
    # Iniciar servidor
    if not start_server():
        return
    
    print_header("INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
    print_info("Seu bot de WhatsApp para ensino de inglês está pronto para uso.")
    print_info("Para iniciar o servidor novamente, execute: python run.py")
    
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_info("\nInstalação interrompida pelo usuário.")
    except Exception as e:
        print_error(f"Erro durante a instalação: {e}")
        input("\nPressione Enter para sair...")