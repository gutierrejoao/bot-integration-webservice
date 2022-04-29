from flask import Flask, request
import jsonify
import urllib3
from random import randint
import os
import io
import requests
import json
import time
urllib3.disable_warnings()

app = Flask(__name__)


@app.route("/citsmart", methods=['POST', 'GET'])
def aprovacao():
    response = request.get_json()
    print(response)
    print("O nome é: " + response['nome'])
    print("O CPF é: " + response['cpf'])
    print("O Telefone é: " + response['numero_de_telefone'])
    print("A Descrição é: " + response['corpo_email'])
    print("O E-mail é: " + response['email'])
    print("A atividade é: " + response['idAtividade'])
    descricao = response['nome'+'corpo_email'+'']
    login = "chatbot"
    codigo = response['idAtividade']
    nome = "MMFDH"
    cidadao = response['nome']
    token = "5146884879:AAF_1KNFttW4lnH6Z3CaRDHTHsoL-9FaMeY"
    chatid = "-1001684649254"
    # Citsmart SessionID
    r = requests.post('https://mmfdh.centralitcloud.com.br/citsmart/services/login', verify=False,
                      data=json.dumps({'userName': 'citsmart.local\\chatbot',
                                      'password': '!@Webservice2@!', 'platform': 'Aiovo'}),
                      headers={'Accept': 'application/json', 'Content-Type': 'application/json'})
    # print(r.text)
    print(r.status_code)
    response = json.loads(r.text)
    sessionID = response['sessionID']
    print("O SessionID é: " + sessionID)
    # Create
    timestamp = int(time.time())
    numberOrigin = str(timestamp) + "." + str(timestamp) + \
        "." + str(login) + "." + str(timestamp)
    print(numberOrigin)
    r1 = requests.post('https://mmfdh.centralitcloud.com.br/citsmart/services/request/create', verify=False,
                       data=json.dumps({"sessionID": sessionID, "synchronize": "false", "sourceRequest": {"numberOrigin": str(numberOrigin), "type": "R", "description": descricao,
                                       "userID": "citsmart.local\\"+login, "contact": {"name": nome, "department": "Atendimento ao Cidadão"}, "contractID": "3", "service": {"code": codigo}}}),
                       headers={'Accept': 'application/json', 'Content-Type': 'application/json'})
    # print(r2.data)
    print(r1.text)
    response1 = json.loads(r1.text)
    numero_solicitacao = response1['request']['number']
    print("O número da solicitação é: " + numero_solicitacao)
    # Telegram
    url1 = f'https://api.telegram.org/bot{token}/sendPhoto'
    data = {'chat_id': chatid, 'photo': "https://s3-sa-east-1.amazonaws.com/prod-jobsite-files.kenoby.com/uploads/centralit-1588710567-logo-site-centralit-linkedinpng.png", 'caption': ''}
    # Ministerio da Mulher!
    data = {'chat_id': chatid,
            'photo': "https://mmfdh.centralitcloud.com.br/citsmart/logoImages/4.jpg", 'caption': ''}
    requests.post(url1, data).json()
    time.sleep(1)
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = {'chat_id': chatid, 'text': '*© Central IT - Citsmart Informa*\n\nCidadão:* ' + cidadao + '\n\n**Descrição:* ' +
            descricao + '\n\n*Ticket:*' + str(numero_solicitacao) + '\n\n*Situação:* Aguardando Conselheiro', 'parse_mode': 'Markdown'}
    requests.post(url, data).json()
    return jsonify({"answer": "</b>" + str(cidadao) + "</b>" + " , sua solicitação foi registrada com sucesso.\n\n<b>Protocolo:</b> " + numero_solicitacao + "\n\nEm até <b>48 horas</b> um conselheiro entrará em contato através do número de <b>telefone:</b> " + telefone + "\n\nO <b>Ministério da Mulher, Família e Diretos Humanos</b> agradece o seu contato.", "answer_clean": "Your order with number 657, was sent to your home", "complements": []})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=False)
