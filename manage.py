from Authenticator import Authenticator
from imports import *

urllib3.disable_warnings()

app = Flask(__name__)


@app.route("/citsmart", methods=['POST', 'GET'])
def startApp():

   # Server response:
    response = request.get_json()
    print(response)

    # Citizen Data
    cidadao = response['nome']
    cpf = response['cpf']
    telefone = response['numero_de_telefone']
    email = response['email']
    descricao = response['corpo_email']
    estado = response['estado']
    municipio = response['municipio']
    cidade = response['cidade']

    # Agent Data
    login = "chatbot"
    codigo = response['idAtividade']
    nome = "MMFDH"
    token = "5146884879:AAF_1KNFttW4lnH6Z3CaRDHTHsoL-9FaMeY"
    chatid = "-1001684649254"

    # Show Citizen Data inserted dump
    print("O nome é: " + cidadao)
    print("O CPF é: " + cpf)
    print("O Telefone é: " + telefone)
    print("A Descrição é: " + descricao)
    print("O E-mail é: " + email)
    print("A atividade é: " + codigo)
    print("O estado é: " + estado)
    print("O município é: " + municipio)
    print("A cidade é: " + cidade)

    # Citsmart SessionID
    # r = requests.post('https://mmfdh.centralitcloud.com.br/citsmart/services/login',
    #                   verify=False,
    #                   data=json.dumps({
    #                       'userName': 'citsmart.local\\chatbot',
    #                       'password': '!@Webservice2@!',
    #                       'platform': 'Aiovo'
    #                   }),
    #                   headers={
    #                       'Accept': 'application/json',
    #                       'Content-Type': 'application/json'
    #                   })
    # print(r.text)
    # print(r.status_code)
    # response = json.loads(r.text)
    # sessionID = response['sessionID']
    # print("O SessionID é: " + sessionID)
    
    url = 'https://mmfdh.centralitcloud.com.br/citsmart/services/login'
    usr = 'citsmart.local\\chatbot'
    psswd = '!@Webservice2@!'
    verify = False
    platform = 'Aivo'

    authenticator = Authenticator(url, usr, psswd, verify, platform)

    # Create

    # Set date
    timestamp = int(time.time())
    numberOrigin = str(timestamp) + "." + str(timestamp) + \
        "." + str(login) + "." + str(timestamp)
    print(numberOrigin)

    r1 = requests.post('https://mmfdh.centralitcloud.com.br/citsmart/services/request/create',
                       verify=False,
                       data=json.dumps({
                           "sessionID": sessionID,
                           "synchronize": "false",
                           "sourceRequest": {
                               "numberOrigin": str(numberOrigin),
                               "type": "R",
                               "description": "Nome: " + cidadao + "<br> Telefone: " + str(telefone) + "<br> CPF: " + str(cpf) + "<br> E-mail: " + email + "<br><br> Descrição: " + descricao,
                               "userID": "citsmart.local\\"+login,
                               "contact": {
                                   "name": nome,
                                   "department": "Atendimento ao Cidadão"
                               },
                               "contractID": "3",
                               "service": {
                                   "code": codigo
                               }
                           }
                       }),
                       headers={
                           'Accept': 'application/json',
                           'Content-Type': 'application/json'
                       })
    # print(r2.data)
    print(r1.text)
    response1 = json.loads(r1.text)
    numero_solicitacao = response1['request']['number']
    print("O número da solicitação é: " + numero_solicitacao)

    # Telegram
    url1 = f'https://api.telegram.org/bot{token}/sendPhoto'
    data = {
        'chat_id': chatid,
        'photo': "https://s3-sa-east-1.amazonaws.com/prod-jobsite-files.kenoby.com/uploads/centralit-1588710567-logo-site-centralit-linkedinpng.png",
        'caption': ''
    }

    # Ministerio da Mulher!
    data = {
        'chat_id': chatid,
        'photo': "https://mmfdh.centralitcloud.com.br/citsmart/logoImages/4.jpg",
        'caption': ''
    }
    requests.post(url1, data).json()
    time.sleep(1)
    url = f'https://api.telegram.org/bot{token}/sendMessage'

    data = {
        'chat_id': chatid,
        'text': '*© Central IT - Citsmart Informa*\n\nCidadão:* ' + cidadao + '\n\n**Descrição:* ' + descricao + '\n\n*Ticket:*' + str(numero_solicitacao) + '\n\n*Situação:* Aguardando Conselheiro',
        'parse_mode': 'Markdown'
    }
    requests.post(url, data).json()
    return jsonify({
        "answer": "</b>" + str(cidadao) + "</b>" + " , sua solicitação foi registrada com sucesso.\n\n<b>Protocolo:</b> " + numero_solicitacao + "\n\nEm até <b>48 horas</b> um conselheiro entrará em contato através do número de <b>telefone:</b> " + telefone + "\n\nO <b>Ministério da Mulher, Família e Diretos Humanos</b> agradece o seu contato.",
        "answer_clean": "Your order with number 657, was sent to your home",
        "complements": []
    })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=False)
