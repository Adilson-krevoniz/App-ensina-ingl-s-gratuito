# Alex - Bot de Ensino de Inglês para WhatsApp

Um sistema de bot para WhatsApp que ensina inglês de forma interativa e personalizada, utilizando inteligência artificial para adaptar o conteúdo ao nível de cada usuário.

## Características

- **Avatar Interativo**: Alex, um professor virtual amigável e paciente
- **Conversação Natural**: Interações fluidas com correções gentis
- **Avaliação de Nível**: Sistema de cadastro e teste para determinar o nível do usuário
- **Ensino Personalizado**: Conteúdo adaptado ao nível do usuário
- **Funcionalidades Adicionais**: Rastreamento de progresso, comandos úteis, suporte a multimídia

## Requisitos

- Python 3.8 ou superior
- Conta na Twilio com acesso à API do WhatsApp
- Chave de API da OpenAI
- Servidor com acesso à internet para hospedar o webhook

## Instalação

### Instalação Simplificada (Recomendada)

1. Faça o download deste repositório e extraia os arquivos

2. **No Windows:**
   - Simplesmente dê um duplo clique no arquivo `instalar.bat`
   - O assistente de instalação irá guiá-lo por todo o processo

3. **No Linux/Mac:**
   - Abra um terminal na pasta do projeto
   - Execute o comando: `bash instalar.sh` ou `./instalar.sh`
   - Siga as instruções na tela

4. Alternativamente, você pode executar o assistente de instalação diretamente:
   ```
   python instalar.py
   ```

### Instalação Manual

1. Clone este repositório:
   ```
   git clone https://github.com/seu-usuario/alex-bot-ingles.git
   cd alex-bot-ingles
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

3. Copie o arquivo de exemplo de variáveis de ambiente e configure suas credenciais:
   ```
   cp .env.example .env
   ```

4. Edite o arquivo `.env` com suas credenciais da Twilio e OpenAI.

## Configuração da Twilio

1. Crie uma conta na [Twilio](https://www.twilio.com/) e acesse o console
2. Ative o sandbox do WhatsApp na seção "Messaging > Try it out > Send a WhatsApp Message"
3. Configure o webhook para apontar para sua URL pública:
   - URL: `https://seu-dominio.com/webhook`
   - Método: `POST`

## Uso

### Após a instalação simplificada

Se você usou o instalador automático, ele já deve ter iniciado o servidor ou fornecido instruções claras para fazê-lo.

1. Para iniciar o servidor manualmente:
   ```
   python run.py
   ```

2. Para expor seu servidor à internet (necessário para testes locais):
   ```
   ngrok http 8000
   ```

3. Configure a URL gerada pelo ngrok como webhook na Twilio:
   - URL: `https://seu-dominio-ngrok.io/webhook`
   - Método: `POST`

4. Envie uma mensagem para o número do WhatsApp fornecido pela Twilio para iniciar a interação

## Comandos Disponíveis

Os usuários podem utilizar os seguintes comandos durante a interação:

- `/ajuda` - Mostra o menu de ajuda
- `/licao` - Inicia uma nova lição
- `/nivel` - Reavalia o nível de inglês
- `/progresso` - Mostra o progresso do usuário
- `/pratica` - Inicia uma sessão de prática livre

## Estrutura do Projeto

```
.
├── app/
│   ├── database/         # Gerenciamento do banco de dados
│   ├── models/           # Modelos de dados
│   ├── services/         # Serviços (IA, WhatsApp)
│   └── utils/            # Utilitários (logging, etc)
├── logs/                 # Arquivos de log
├── database/             # Banco de dados SQLite
├── main.py               # Ponto de entrada da aplicação
├── run.py                # Script para iniciar o servidor
├── instalar.py           # Assistente de instalação interativo
├── instalar.bat          # Inicializador de instalação para Windows
├── instalar.sh           # Inicializador de instalação para Linux/Mac
├── setup.py              # Configuração do ambiente
├── test_bot.py           # Script para testar o bot
├── requirements.txt      # Dependências
├── .env.example          # Exemplo de variáveis de ambiente
└── README.md             # Este arquivo
```

## Personalização

Você pode personalizar o comportamento do bot editando os prompts no arquivo `app/services/ai_service.py`.

## Segurança e Privacidade

O sistema armazena apenas os dados necessários para o funcionamento do bot, como nome do usuário, nível de inglês e histórico de interações para contextualização. Nenhum dado sensível é coletado.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.