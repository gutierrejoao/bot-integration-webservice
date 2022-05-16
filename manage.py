from imports import *

urllib3.disable_warnings()

app = Flask(__name__)


@app.route("/citsmart", methods=['POST', 'GET'])
def cria_ticket():

    # Server response:
    response = request.get_json()
    print(response)

    # Citizen Data
    cidadao = response['nome']
    cpf = response['cpf']
    telefone = response['numero_de_telefone']
    email = response['email']
    descricao = response['corpo_email']
    localidade = response['idLocalidade']
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
    print("A localidade é: " + localidade)
    print("A cidade é: " + cidade)
    print("O município é: " + municipio)

    # Create ticket

    url = 'https://mmfdh-hom.centralitcloud.com.br/citsmart/services/login'
    usr = 'citsmart.local\\chatbot'
    psswd = '!@Webservice2@!'
    verify = False
    platform = 'Aivo'

    authenticatorInstance = Authenticator()
    authenticator = authenticatorInstance.authentication(url,usr,psswd,verify,platform)
    request_dump = authenticator.return_request_dump()
    status_code = authenticator.return_status_code()
    session_id = authenticator.return_status_code(request_dump)
    print(request_dump)
    print(status_code)
    print(session_id)

    # Set numberOrigin (timestamp + timestamp + login name + timestamo)
    timestamp = int(time.time())
    numberOrigin = str(timestamp) + "." + str(timestamp) + \
        "." + str(login) + "." + str(timestamp)
    print(numberOrigin)

    r1 = requests.post('https://mmfdh-hom.centralitcloud.com.br/citsmart/services/request/create',
                       verify=False,
                       data=json.dumps({"sessionID": session_id,
                                        "synchronize": "false",
                                        "sourceRequest": {
                                            "numberOrigin": str(numberOrigin),
                                            "type": "R",
                                            "description": "<strong>Nome: </strong>" + cidadao + "<br> <strong>Telefone: </strong>" + str(telefone) + "<br> <strong>CPF: </strong>" + str(
                                                cpf) + "<br> <strong>E-mail: </strong>" + email + "<br> <strong> Localidade: </strong>" + localidade + "<br><br> <strong>Descrição: </strong>" + descricao,
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


@app.route("/citsmart", methods=['POST', 'GET'])
def consulta_ticket():
    # Server response:
    response = request.get_json()
    # Agent Data
    login = "chatbot"
    ticket = response['number']
    auth_res = requests.post('https://mmfdh.centralitcloud.com.br/citsmart/services/login',
                             verify=False,
                             data=json.dumps({
                                 'userName': 'citsmart.local\\chatbot',
                                 'password': '!@Webservice2@!',
                                 'platform': 'Aiovo'
                             }),
                             headers={
                                 'Accept': 'application/json',
                                 'Content-Type': 'application/json'
                             })

    timestamp = int(time.time())
    numberOrigin = str(timestamp) + "." + str(timestamp) + \
        "." + str(login) + "." + str(timestamp)
    ticket_status = requests.get('https://mmfdh.centralitcloud.com.br/citsmart/services/request/getById',
                                 verify=False,
                                 data=json.dumps({
                                     "number": ticket,
                                     "numberOrigin": numberOrigin
                                 }))

    return jsonify({
        "answer": "O status da solicitação é: " + ticket_status.text + "",
        "answer_clean": "O status da solicitação é: " + ticket_status.text + "",
        "complements": []
    })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=False)
