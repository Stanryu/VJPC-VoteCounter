from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.py3compat import tobytes
from digitalSignatureEG import keys_generator
from geradorBoletas import adicionaLogo
from geradorBoletas import geraBoleta
from Cryptodome.Hash import SHA256
from Cryptodome.Hash import HMAC
from operator import itemgetter
from Cryptodome.IO import PEM
from flask_cors import CORS
from flask import jsonify
from flask import request
from flask import Flask
from directories import *
from pathlib import Path
import base64
import json
import uuid


app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': 'http://localhost:8080'}})

TEST = [
    {
    'ID': uuid.uuid4().hex,
    'Name': 'Presidential',
    'Description': 'National',
    'Quantity': '3',
    'StartDate': '07/03/2023', 
    'StartTime': '08:00',
    'EndDate': '07/03/2023',
    'EndTime': '17:00',
    'Fingerprint': '1ej829u&a'
    },
    {
    'ID': uuid.uuid4().hex,
    'Name': 'Congress',
    'Description': 'National',
    'Quantity': '594',
    'StartDate': '26/03/2023', 
    'StartTime': '12:00',
    'EndDate': '28/03/2023',
    'EndTime': '12:00',
    'Fingerprint': '(*!XMe21)'
    },
    {
    'ID': uuid.uuid4().hex,
    'Name': 'Academic Center',
    'Description': 'Small',
    'Quantity': '1',
    'StartDate': '14/04/2023',
    'StartTime': '08:00',
    'EndDate': '14/04/2023',
    'EndTime': '09:00',
    'Fingerprint': '@*Ye9*@Uecm)'
    }
]

cipher_name = 'EL GAMAL '
p_type = cipher_name + 'PRIME P'
q_type = cipher_name + 'PRIME Q'
b_type = cipher_name + 'BASE G'
x_type = cipher_name + 'PRIVATE KEY'
y_type = cipher_name + 'PUBLIC KEY'


def exporting(election_id):

    p, q, g, x, y = keys_generator()

    x_b = str(x).encode()
    private_key = tobytes(PEM.encode(x_b, x_type))

    # Mudança de diretório para acessar o dispositivo USB
    os.chdir(str(Path.home()))
    os.chdir('..')
    os.chdir('..')
    if not os.path.isdir(os.getcwd() + 'media/julio/7A2F-BA93/Private Keys/'):
        os.mkdir(os.getcwd() + 'media/julio/7A2F-BA93/Private Keys/')

    # CHANGE PEM DIR TO EXECUTE
    # os.chdir(str(Path.home()))
    # os.chdir('..')
    # os.chdir('..')
    # if not os.path.isdir(os.getcwd() + '/Private Keys/'):
    #     os.mkdir(os.getcwd() + '/Private Keys/')

    # Salva o arquivo contendo a chave privada de assinatura em uma mídia externa no formato PEM
    p_key_file = open(os.getcwd() +  'media/julio/7A2F-BA93/Private Keys/' + election_id + '_privateKey.pem', 'w')
    p_key_file.write(private_key.decode('utf-8'))
    p_key_file.close()

    # Exclui todos os objetos que contenham a chave privada em texto puro, e retorna ao diretório de aplicação
    del(x, x_b, private_key)
    os.chdir(current_dir)

    # Codifica as informações em bytes
    p_b = str(p).encode()
    q_b = str(q).encode()
    g_b = str(g).encode()
    y_b = str(y).encode()

    prime_p = tobytes(PEM.encode(p_b, p_type))
    prime_q = tobytes(PEM.encode(q_b, q_type))
    base_g = tobytes(PEM.encode(g_b, b_type))
    public_key = tobytes(PEM.encode(y_b, y_type))

    key_file = open(os.getcwd() + general_data + stat + keys + election_id + '_publicKey.pem', 'w')

    # Escreve a chave pública, o primo p, o primo q e a base g no arquivo
    key_file.write(public_key.decode('utf-8') + '\n')
    key_file.write(prime_p.decode('utf-8') + '\n')
    key_file.write(prime_q.decode('utf-8') + '\n')
    key_file.write(base_g.decode('utf-8'))
    key_file.close()
    
    return base64.b64encode(p_b), base64.b64encode(q_b), base64.b64encode(g_b), base64.b64encode(y_b)

# Must be 32 bytes or longer
secret = 'Validate'
tag = b'\xdb\xe6\xba\xdb\x91\xc72\xf7M!\xbb\x9ck\x8e/\xaaO\xc2\x8f}"\x1b\xc7*\xfcBO\x15\xac\x96\xf3^'

@app.route('/', methods=['GET', 'POST'])
def configElection():

    response_object = {'status': 'success'}

    if request.method == 'POST':
        post_data = request.get_json()

        if len(post_data) == 1:
            message = post_data.get('Password')
        
            h = HMAC.new(bytes(secret, 'utf-8'), digestmod=SHA256)
            h.update(bytes(message, 'utf-8'))

            try:
                h.verify(tag)
                response_object = {'status': 'success'}
                response_object['message'] = 'Authentication Successful!'
            except ValueError:
                response_object = {'status': 'failed'}
                response_object['message'] = 'Authentication Failed!'

        else:
            election_id = uuid.uuid1().hex
            election_name = post_data.get('Name')
            description = post_data.get('Description')
            begin_date = post_data.get('StartDate')
            begin_time = post_data.get('StartTime')
            end_date = post_data.get('EndDate')
            end_time = post_data.get('EndTime')
            candidates_file = f'{post_data.get("CandidatesFile")}.json'
            voters_file = f'{post_data.get("VotersFile")}.json'

            json_config_report, json_config_info = dict(), dict()
            dict_list, voters_list, cargo_generate, digits_generate = list(), list(), list(), list()

            # Arquivos de configuração .json
            report_name = f'{election_id}_report.json'
            info_name = f'{election_id}_fingerprint.json'
            control_name = f'{election_id}_control.json'

            # Arquivos contendo dados sobre os candidatos e eleitores
            with open(f'{os.getcwd()}{general_data}{stat}{people}{candidates_file}', 'r') as file:
                candidates_data = json.load(file)

            with open(f'{os.getcwd()}{general_data}{stat}{people}{voters_file}', 'r') as file:
                voters_data = json.load(file)

            roles_quantity = len(candidates_data['Candidatos'][0])
            candidates_names = list(candidates_data['Candidatos'][0].keys())
            
            for i in range(roles_quantity):

                aux_dict = dict()
                aux_dict['Ordem'] = i + 1
                aux_dict['Digitos'] = len(str(candidates_data['Candidatos'][0][candidates_names[i]][0]['Number']))
                aux_dict['Nome'] = candidates_names[i]

                dict_list.append(aux_dict)

            # A autenticação é o CPF de cada eleitor, armazenado no arquivo de configuração após passar por uma função Hash
            vts_names = dict()
            v_control, vote_checking = dict(), dict()
            control_list = list()
            for vts in voters_data['Eleitores']:

                # Gera a string de sal aleatoriamente e concatena com o cpf
                salt = str(get_random_bytes(32))
                hash_input = vts['CPF'] + salt

                # O aruivo de configuração recebe o hash do cpf e o sal
                vts_names['Authentication'] = SHA256.new(vts['CPF'].encode()).hexdigest()
                vts_names['Salt'] = salt

                # O arquivo de controle de votação recebe o hash do cpf concatenado com o sal, o sal e o booleano de controle
                v_control['Authentication'] = SHA256.new(hash_input.encode()).hexdigest()
                v_control['Salt'] = salt
                v_control['Vote'] = False

                voters_list.append(vts_names.copy())
                control_list.append(v_control.copy())

            # Criação da chave pública da eleição
            prime_p, prime_q, base_g, public_key = exporting(election_id)
            key_dict = dict()
            key_dict['Prime P'] = prime_p.decode('utf-8')
            key_dict['Prime Q'] = prime_q.decode('utf-8')
            key_dict['Base G'] = base_g.decode('utf-8')
            key_dict['Key'] = public_key.decode('utf-8')

            # Informações gerais da eleição
            json_config_report['ID'] = election_id
            json_config_report['Name'] = election_name
            json_config_report['Description'] = description
            json_config_report['Begin Date'] = begin_date
            json_config_report['Begin Time'] = begin_time
            json_config_report['End Date'] = end_date
            json_config_report['End Time'] = end_time
            json_config_report['Public Key'] = key_dict

            # Arquivo JSON da configuração da eleição
            sorted_by_order = sorted(dict_list, key=itemgetter('Ordem'))
            json_config_report['Cargos'] = sorted_by_order
            json_config_report['Eleitores'] = voters_list
            json_object_report = json.dumps(json_config_report, indent=4)

            # Fingerprint da eleição configurada para divulgação
            election_fingerprint = SHA256.new(bytes(json_object_report.encode(encoding='utf-8')))
            json_config_info['Fingerprint'] = election_fingerprint.hexdigest()
            json_object_info = json.dumps(json_config_info, indent=4)

            # Informações sobre os eleitores para controle de votação
            vote_checking['Eleitores'] = control_list
            json_vote_control = json.dumps(vote_checking, indent=4)

            # Exporta o arquivo de configuração JSON da eleição
            with open(os.getcwd() + general_data + stat + output + report_name, 'w') as file:
                file.write(json_object_report)

            # Exporta o arquivo contendo a fingerprint do arquivo de configuração JSON da eleição
            with open(os.getcwd() + general_data + stat + fingerprints + info_name, 'w') as file:
                file.write(json_object_info)

            # Exporta o arquivo para controle de voto dos eleitores
            with open(os.getcwd() + general_data + stat + people + control_name, 'w') as file:
                file.write(json_vote_control)

            for cargo in sorted_by_order:
                cargo_generate.append(cargo['Nome'])
                digits_generate.append(cargo['Digitos'])

            # Gera a boleta com conforme a configuração da eleição especificada pelo usuário
            ballot = geraBoleta(roles_quantity, cargo_generate, digits_generate, election_id)

            # Adiciona um logotipo no cabeçalho (Opcional)
            adicionaLogo(ballot, election_id)

            response_object['message'] = 'Election Created!'
    else:
        response_object['elections'] = TEST

    return jsonify(response_object)
    # return report_name, roles_quantity, election_id


def readConfigFile(file_name):

    i = 0
    cargos, digitos, pos, campos = list(), list(), list(), list()

    with open(os.getcwd() + general_data + stat + output + file_name, 'r') as file:

        data = json.load(file)

        i = 0
        for cargo in data['Cargos']:

            pos.append(cargo['Ordem'])
            digitos.append(cargo['Digitos'])
            cargos.append(cargo['Nome'])

            if i == 0:
                campos.append(int(cargo['Digitos']))
            else:
                campos.append(int(campos[i - 1]) + int(cargo['Digitos']))

            i += 1

    return cargos, pos, digitos, campos


def getConfigFile(name):

    for _, _, files in os.walk(os.getcwd() + general_data + stat + output):
        for file in files:
            
            if name in file:
                cargos, pos, digitos, campos = readConfigFile(file)
                return cargos, digitos, pos, campos

    return False, False, False, False


if __name__ == '__main__':
    app.run(debug=True)
