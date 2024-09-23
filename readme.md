# Documentação do Script Flask

## **Descrição Geral**

Este script é uma aplicação Flask que integra com um scrapper do WhatsApp. Ele permite iniciar e
parar processos, obter mensagens, verificar a conexão com o WhatsApp e gerar QR codes para
login.

## **Rotas e Funcionalidades**

- `/`: Página inicial que verifica se o backend está online.
- `/startprocess`: Inicia o processo de scrapping do WhatsApp.
- `/stopprocess`: Para o processo de scrapping.
- `/getqrcode`: Gera um QR code para autenticação no WhatsApp.
- `/getmessages`: Retorna as mensagens capturadas pelo scrapper.
- `/verifyconnected`: Verifica se o WhatsApp está conectado.

## **Como Funciona o Script**

O script utiliza o Flask para criar uma API que se comunica com o scrapper do WhatsApp. O
scrapper é controlado pelas rotas definidas, permitindo que o usuário interaja com o WhatsApp
através dos endpoints da API.

# Documentação para Executar o Script Localmente

## **Requisitos:**

1. Python 3.9 ou superior instalado.
2. Biblioteca `python-dotenv` instalada para carregar as variáveis de ambiente.
3. Arquivo `.env` configurado com as credenciais necessárias.

## **Passos para Configuração e Execução:**

### 1. Clone o repositório:

Clone o repositório do projeto para o seu ambiente local usando o Git.

```bash
git clone 
cd 
```

### 2. Crie e ative um ambiente virtual:

Recomenda-se o uso de um ambiente virtual para evitar conflitos de dependências.

```bash
python -m venv venv
source venv/bin/activate # No Windows, use: venv\Scriptsctivate
```

### 3. Instale as dependências:

Instale todas as bibliotecas necessárias listadas no `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 4. Configure o arquivo `.env`:

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
OPEN_AI_KEY=your_open_ai_key_here
```

Certifique-se de substituir `your_open_ai_key_here` pela sua chave da OpenAI.

### 5. Configurar a variável `FLASK_APP`:

Configure a variável de ambiente `FLASK_APP` para apontar para o arquivo do seu aplicativo
Flask. Substitua `` pelo nome do seu arquivo Python (sem a extensão `.py`).

```bash
export FLASK_APP= # No Windows, use: set FLASK_APP=
```

### 6. Executar a aplicação com Flask:

Inicie o servidor Flask localmente usando o comando:

```bash
flask run --host=0.0.0.0 --port=5000
```

Isso iniciará o servidor Flask no endereço `http://0.0.0.0:5000`.

### 7. Testar a API:

- **Página Inicial:** Acesse `http://0.0.0.0:5000/` para verificar se o backend está online.
- **Iniciar Processo:** Use o endpoint `/startprocess` para iniciar o processo do WhatsApp
  Scrapper.
- **Parar Processo:** Use o endpoint `/stopprocess` para parar o processo do WhatsApp Scrapper.
- **Obter QR Code:** Use o endpoint `/getqrcode` para gerar o QR code para login no WhatsApp.
- **Obter Mensagens:** Acesse `/getmessages` para obter as mensagens capturadas.
- **Verificar Conexão:** Utilize `/verifyconnected` para verificar se o WhatsApp está conectado.

### 8. Encerrar o Servidor:

Para encerrar o servidor, pressione `Ctrl + C` no terminal onde o Flask está rodando.

## **Observações:**

- Certifique-se de que o arquivo `.env` está devidamente configurado, pois o script depende da
  variável `OPEN_AI_KEY`.
- Caso encontre erros de permissão, execute o comando com permissões elevadas (por exemplo,
  `sudo` no Linux).

## **Pronto!**

Agora você pode executar e testar o script localmente usando o comando `flask run`.
