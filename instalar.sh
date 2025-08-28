#!/bin/bash

# Cores para o terminal
GREEN="\033[0;32m"
BLUE="\033[0;34m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
BOLD="\033[1m"
NC="\033[0m" # No Color

print_header() {
    echo -e "\n\033[1m====================================================\033[0m"
    echo -e "\033[1;34m               $1               \033[0m"
    echo -e "\033[1m====================================================\033[0m"
}

print_step() {
    echo -e "\n${BOLD}${GREEN}[$1] $2${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

check_python_version() {
    print_step "1" "Verificando versão do Python..."
    
    if command -v python3 &>/dev/null; then
        python_cmd="python3"
    elif command -v python &>/dev/null; then
        python_cmd="python"
    else
        print_error "Python não encontrado!"
        print_info "Por favor, instale o Python 3.8 ou superior."
        exit 1
    fi
    
    # Verificar versão
    python_version=$($python_cmd -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')")
    python_major=$($python_cmd -c "import sys; print(sys.version_info.major)")
    python_minor=$($python_cmd -c "import sys; print(sys.version_info.minor)")
    
    if [ "$python_major" -lt 3 ] || ([ "$python_major" -eq 3 ] && [ "$python_minor" -lt 8 ]); then
        print_error "Python 3.8 ou superior é necessário! Versão detectada: $python_version"
        print_info "Por favor, instale uma versão mais recente do Python."
        exit 1
    fi
    
    print_success "Python $python_version detectado!"
    return 0
}

install_dependencies() {
    print_step "2" "Instalando dependências..."
    
    if ! $python_cmd -m pip install -r requirements.txt; then
        print_error "Erro ao instalar dependências. Verifique o arquivo requirements.txt"
        return 1
    fi
    
    print_success "Dependências instaladas com sucesso!"
    return 0
}

setup_env_file() {
    print_step "3" "Configurando credenciais..."
    
    if [ -f ".env" ]; then
        read -p "Arquivo .env já existe. Deseja reconfigurá-lo? (s/n): " overwrite
        if [ "$overwrite" != "s" ] && [ "$overwrite" != "S" ]; then
            print_info "Usando arquivo .env existente."
            return 0
        fi
    fi
    
    # Criar arquivo .env a partir do modelo
    if [ ! -f ".env.example" ]; then
        print_error "Arquivo .env.example não encontrado!"
        return 1
    fi
    
    # Ler o modelo
    env_template=$(cat .env.example)
    
    # Solicitar credenciais ao usuário
    print_info "\nVamos configurar suas credenciais para o bot de WhatsApp."
    print_info "Você precisará de uma conta na Twilio e uma chave de API da OpenAI."
    
    # Opção para abrir sites para registro
    read -p "Deseja abrir o site da Twilio para criar uma conta? (s/n): " open_twilio
    if [ "$open_twilio" = "s" ] || [ "$open_twilio" = "S" ]; then
        if command -v xdg-open &>/dev/null; then
            xdg-open "https://www.twilio.com/try-twilio"
        elif command -v open &>/dev/null; then
            open "https://www.twilio.com/try-twilio"
        else
            print_info "URL da Twilio: https://www.twilio.com/try-twilio"
        fi
        print_info "Aguarde até criar sua conta na Twilio..."
        read -p "Pressione Enter quando estiver pronto para continuar..."
    fi
    
    read -p "Deseja abrir o site da OpenAI para obter uma chave de API? (s/n): " open_openai
    if [ "$open_openai" = "s" ] || [ "$open_openai" = "S" ]; then
        if command -v xdg-open &>/dev/null; then
            xdg-open "https://platform.openai.com/account/api-keys"
        elif command -v open &>/dev/null; then
            open "https://platform.openai.com/account/api-keys"
        else
            print_info "URL da OpenAI: https://platform.openai.com/account/api-keys"
        fi
        print_info "Aguarde até obter sua chave de API da OpenAI..."
        read -p "Pressione Enter quando estiver pronto para continuar..."
    fi
    
    # Coletar credenciais
    print_header "Credenciais da Twilio"
    read -p "Account SID: " twilio_account_sid
    read -p "Auth Token: " twilio_auth_token
    read -p "Número de telefone do WhatsApp (formato: whatsapp:+XXXXXXXXXXX): " twilio_phone_number
    
    print_header "Credencial da OpenAI"
    read -p "API Key: " openai_api_key
    
    # Substituir no modelo
    env_content="$env_template"
    env_content="${env_content//your_twilio_account_sid/$twilio_account_sid}"
    env_content="${env_content//your_twilio_auth_token/$twilio_auth_token}"
    env_content="${env_content//whatsapp:+1234567890/$twilio_phone_number}"
    env_content="${env_content//your_openai_api_key/$openai_api_key}"
    
    # Salvar arquivo .env
    echo "$env_content" > .env
    
    print_success "Arquivo .env configurado com sucesso!"
    return 0
}

initialize_database() {
    print_step "4" "Inicializando banco de dados..."
    
    # Criar diretórios necessários
    mkdir -p logs
    mkdir -p database
    
    # Executar script de inicialização do banco de dados
    if ! $python_cmd -c "import sys; sys.path.append('$(pwd)'); from app.database.init_db import init_database; init_database('database/alex_bot.db')"; then
        print_error "Erro ao inicializar banco de dados"
        return 1
    fi
    
    print_success "Banco de dados inicializado com sucesso!"
    return 0
}

setup_webhook() {
    print_step "5" "Configuração do webhook da Twilio..."
    
    print_info "Para que o bot funcione, você precisa configurar um webhook na Twilio."
    print_info "Você tem duas opções:"
    print_info "1. Usar ngrok para expor seu servidor local à internet (para testes)"
    print_info "2. Hospedar o bot em um servidor com IP público (para produção)"
    
    read -p "\nDeseja usar ngrok para testes locais? (s/n): " option
    
    if [ "$option" = "s" ] || [ "$option" = "S" ]; then
        # Verificar se ngrok está instalado
        if ! command -v ngrok &>/dev/null; then
            print_warning "ngrok não encontrado. Você precisará instalá-lo."
            read -p "Deseja abrir o site para baixar o ngrok? (s/n): " install_ngrok
            if [ "$install_ngrok" = "s" ] || [ "$install_ngrok" = "S" ]; then
                if command -v xdg-open &>/dev/null; then
                    xdg-open "https://ngrok.com/download"
                elif command -v open &>/dev/null; then
                    open "https://ngrok.com/download"
                else
                    print_info "URL do ngrok: https://ngrok.com/download"
                fi
                print_info "Siga as instruções de instalação do ngrok..."
                read -p "Pressione Enter quando a instalação estiver concluída..."
            else
                print_warning "Você precisará instalar o ngrok manualmente mais tarde."
            fi
        else
            print_success "ngrok detectado!"
        fi
        
        print_info "\nPara iniciar o servidor com ngrok, siga estes passos:"
        print_info "1. Abra um terminal e execute: $python_cmd run.py"
        print_info "2. Abra outro terminal e execute: ngrok http 8000"
        print_info "3. Copie a URL HTTPS gerada pelo ngrok (ex: https://xxxx-xxxx.ngrok.io)"
        print_info "4. Configure essa URL + '/webhook' como webhook na Twilio"
        
        read -p "\nDeseja abrir o console da Twilio para configurar o webhook? (s/n): " open_twilio_console
        if [ "$open_twilio_console" = "s" ] || [ "$open_twilio_console" = "S" ]; then
            if command -v xdg-open &>/dev/null; then
                xdg-open "https://console.twilio.com/"
            elif command -v open &>/dev/null; then
                open "https://console.twilio.com/"
            else
                print_info "URL do console da Twilio: https://console.twilio.com/"
            fi
        fi
    else
        print_info "\nPara hospedar o bot em um servidor:"
        print_info "1. Faça upload dos arquivos para seu servidor"
        print_info "2. Execute '$python_cmd setup.py' no servidor"
        print_info "3. Execute '$python_cmd run.py' para iniciar o servidor"
        print_info "4. Configure a URL do seu servidor + '/webhook' como webhook na Twilio"
    fi
    
    print_success "Instruções de configuração do webhook fornecidas!"
    return 0
}

start_server() {
    print_step "6" "Iniciar servidor..."
    
    read -p "Deseja iniciar o servidor agora? (s/n): " start
    if [ "$start" = "s" ] || [ "$start" = "S" ]; then
        print_info "Iniciando servidor..."
        print_info "Pressione CTRL+C para encerrar o servidor quando desejar."
        sleep 2
        $python_cmd run.py
        return $?
    else
        print_info "Para iniciar o servidor mais tarde, execute: $python_cmd run.py"
        return 0
    fi
}

main() {
    print_header "INSTALAÇÃO DO BOT DE WHATSAPP PARA ENSINO DE INGLÊS"
    print_info "Este assistente irá guiá-lo através do processo de instalação e configuração."
    
    # Verificar versão do Python
    check_python_version || exit 1
    
    # Instalar dependências
    install_dependencies || exit 1
    
    # Configurar arquivo .env
    setup_env_file || exit 1
    
    # Inicializar banco de dados
    initialize_database || exit 1
    
    # Configurar webhook
    setup_webhook || exit 1
    
    # Iniciar servidor
    start_server || exit 1
    
    print_header "INSTALAÇÃO CONCLUÍDA COM SUCESSO!"
    print_info "Seu bot de WhatsApp para ensino de inglês está pronto para uso."
    print_info "Para iniciar o servidor novamente, execute: $python_cmd run.py"
    
    read -p "\nPressione Enter para sair..."
}

# Tornar o script executável
chmod +x "$0"

# Executar função principal
main