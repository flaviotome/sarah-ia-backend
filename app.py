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