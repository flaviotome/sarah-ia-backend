from flask import Flask, request, jsonify
import whatsapp_scrapper

# Criação da aplicação Flask
app = Flask(__name__)


if __name__ == "__main__":    
    app.run(host='0.0.0.0', port=5000)

# Rota para a página inicial
@app.route('/')
def home():
    return jsonify(result = 'Sarah backend online!')


@app.route('/startprocess', methods=['GET'])
def startprocess():
    whatsapp_scrapper.STOP = False
    whatsapp_scrapper.startprocess()
    return jsonify(result = 'Processo iniciado!')

@app.route('/stopprocess', methods=['GET'])
def stopprocess():
    whatsapp_scrapper.stopprocess()
    return jsonify(result = 'Processo parado!')
    
@app.route('/getqrcode', methods=['GET'])
def getqrcode():
    result = whatsapp_scrapper.getqrcode()
    if result != 500:
        return jsonify(result = result)
    else:
        return jsonify(result = 'Erro ao gerar qr code!')

@app.route('/getmessages', methods=['GET'])
def getmessages():
    
    return whatsapp_scrapper.getmessagesdf()

@app.route('/verifyconnected', methods=['GET'])
def verifyconnected():
                
        return jsonify(result= whatsapp_scrapper.verifica_conectado())

@app.route('/resetmessages', methods=['GET'])
def resetmessages():
                
        return jsonify(result= whatsapp_scrapper.resetmessages())

@app.route('/sendmessage', methods=['POST'])
def sendmessage():
    # Obtém os dados do JSON enviado pelo frontend
    data = request.get_json()
    
    # Extrai os parâmetros 'nome_contato' e 'mensagem' do JSON
    nome_contato = data.get('nome_contato')
    mensagem = data.get('mensagem')
    
    # Verifica se ambos os parâmetros foram fornecidos
    if not nome_contato or not mensagem:
        return jsonify({"status": 400, "message": "Parâmetros 'nome_contato' e 'mensagem' são obrigatórios"}), 400

    # Chama a função para enviar a mensagem
    status_code = whatsapp_scrapper.send_message_from_frontend(nome_contato, mensagem)
    
    # Retorna o status com base no resultado da função
    if status_code == 200:
        return jsonify({"status": 200, "message": "Mensagem enviada com sucesso"}), 200
    else:
        return jsonify({"status": 500, "message": "Erro ao enviar a mensagem"}), 500


@app.route('/insertmessagedataframe', methods=['POST'])
def insertmessagedataframe():
        # Obtém os dados do JSON enviado pelo frontend
        data = request.get_json()
    
        # Extrai os parâmetros 'nome_contato' e 'mensagem' do JSON
        nome_contato = data.get('nome_contato')
        mensagem = data.get('mensagem')
        
        whatsapp_scrapper.insert_message_dataframe(nome_contato, mensagem)        
        return whatsapp_scrapper.getmessagesdf()
        
