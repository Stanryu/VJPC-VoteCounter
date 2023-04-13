from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.py3compat import tobytes
from digitalSignatureEG import keys_generator
from Cryptodome.Protocol.KDF import scrypt
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
from os import listdir
from os import remove
import base64
import json
import uuid


app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': 'http://localhost:8080'}})

ELECTIONS = list()

cipher_name = 'EL GAMAL '
p_type = cipher_name + 'PRIME P'
q_type = cipher_name + 'PRIME Q'
b_type = cipher_name + 'BASE G'
x_type = cipher_name + 'PRIVATE KEY'
y_type = cipher_name + 'PUBLIC KEY'


def exporting(election_id, password):

    p, q, g, x, y = keys_generator()

    x_b = str(x).encode()
    private_key = tobytes(PEM.encode(x_b, x_type))

    # Mudança de diretório para acessar o dispositivo USB
    chdir(str(Path.home()))
    chdir('..')
    chdir('..')
    if not isdir(getcwd() + 'media/julio/7A2F-BA93/Private Keys/'):
        mkdir(getcwd() + 'media/julio/7A2F-BA93/Private Keys/')

    member_data, board_member, export_member = dict(), dict(), list()
    with open(getcwd() +  'media/julio/7A2F-BA93/Private Keys/' + election_id + '_masterPassword.json', 'w') as file:
        
        salt = get_random_bytes(16)
        password_key = scrypt(private_key, salt, 16, N=2**14, r=8, p=1)

        h = HMAC.new(password_key, digestmod=SHA256)
        tag = h.update(bytes(password, 'utf-8'))

        member_data['Salt'] = str(salt)
        member_data['Tag'] = str(tag.digest())
        export_member.append(member_data)
        board_member['Board Member'] = export_member

        board_json = json.dumps(board_member, indent=4)
        file.write(board_json)

    # CHANGE PEM DIR TO EXECUTE
    # chdir(str(Path.home()))
    # chdir('..')
    # chdir('..')
    # if not isdir(getcwd() + '/Private Keys/'):
    #     mkdir(getcwd() + '/Private Keys/')

    # Salva o arquivo contendo a chave privada de assinatura em uma mídia externa no formato PEM
    p_key_file = open(getcwd() +  'media/julio/7A2F-BA93/Private Keys/' + election_id + '_privateKey.pem', 'w')
    p_key_file.write(private_key.decode('utf-8'))
    p_key_file.close()

    # Exclui todos os objetos que contenham a chave privada em texto puro, e retorna ao diretório de aplicação
    del(x, x_b, private_key)
    chdir(current_dir)

    # Codifica as informações em bytes
    p_b = str(p).encode()
    q_b = str(q).encode()
    g_b = str(g).encode()
    y_b = str(y).encode()

    prime_p = tobytes(PEM.encode(p_b, p_type))
    prime_q = tobytes(PEM.encode(q_b, q_type))
    base_g = tobytes(PEM.encode(g_b, b_type))
    public_key = tobytes(PEM.encode(y_b, y_type))

    key_file = open(f'{current_dir}{general_data}{stat}{keys}{election_id}_publicKey.pem', 'w')

    # Escreve a chave pública, o primo p, o primo q e a base g no arquivo
    key_file.write(public_key.decode('utf-8') + '\n')
    key_file.write(prime_p.decode('utf-8') + '\n')
    key_file.write(prime_q.decode('utf-8') + '\n')
    key_file.write(base_g.decode('utf-8'))
    key_file.close()
    
    return base64.b64encode(p_b), base64.b64encode(q_b), base64.b64encode(g_b), base64.b64encode(y_b)


def config_election(election_id, election_name, description,
                    begin_date, begin_time, end_date, end_time,
                    candidates_file, voters_file, password):

    json_config_report, json_config_info = dict(), dict()
    dict_list, voters_list, cargo_generate, digits_generate = list(), list(), list(), list()

    # Arquivos de configuração .json
    report_name = f'{election_id}_report.json'
    info_name = f'{election_id}_fingerprint.json'
    control_name = f'{election_id}_control.json'

    # Arquivos contendo dados sobre os candidatos e eleitores
    with open(f'{current_dir}{general_data}{stat}{people}{candidates_file}', 'r') as file:
        candidates_data = json.load(file)

    with open(f'{current_dir}{general_data}{stat}{people}{voters_file}', 'r') as file:
        voters_data = json.load(file)

    roles_quantity = len(candidates_data['Candidatos'][0])
    candidates_names = list(candidates_data['Candidatos'][0].keys())
    
    for i in range(roles_quantity):

        aux_dict = dict()
        aux_dict['Ordem'] = i + 1
        aux_dict['Digitos'] = len(str(candidates_data['Candidatos'][0][candidates_names[i]][0]['Number'])) # TODO: Refact this!
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
    prime_p, prime_q, base_g, public_key = exporting(election_id, password)
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
    with open(f'{current_dir}{general_data}{stat}{output}{report_name}', 'w') as file:
        file.write(json_object_report)

    # Exporta o arquivo contendo a fingerprint do arquivo de configuração JSON da eleição
    with open(f'{current_dir}{general_data}{stat}{fingerprints}{info_name}', 'w') as file:
        file.write(json_object_info)

    # Exporta o arquivo para controle de voto dos eleitores
    with open(f'{current_dir}{general_data}{stat}{people}{control_name}', 'w') as file:
        file.write(json_vote_control)

    for cargo in sorted_by_order:
        cargo_generate.append(cargo['Nome'])
        digits_generate.append(cargo['Digitos'])

    # Gera a boleta com conforme a configuração da eleição especificada pelo usuário
    ballot = geraBoleta(roles_quantity, cargo_generate, digits_generate, election_id)

    # Adiciona um logotipo no cabeçalho (Opcional)
    adicionaLogo(ballot, election_id)


@app.route('/', methods=['GET', 'POST'])
def all_elections():

    response_object = {'status': 'success'}

    if request.method == 'POST':
        post_data = request.get_json()
        print(f'------{post_data}-------')
        print(post_data)
        if len(post_data) == 2:
            
            election_id = post_data.get('ID')
            message = post_data.get('Password')

            chdir(str(Path.home()))
            chdir('..')
            chdir('..')

            with open(getcwd() +  'media/julio/7A2F-BA93/Private Keys/' + election_id + '_privateKey.pem', 'r') as pk_file:
                with open(getcwd() +  'media/julio/7A2F-BA93/Private Keys/' + election_id + '_masterPassword.json', 'r') as pswd_file:
                    
                    sign_key = pk_file.read().encode()

                    data = json.load(pswd_file)
                    salt = data['Board Member'][0]['Salt']
                    tag = data['Board Member'][0]['Tag']

                    salt = salt.removesuffix("'")
                    salt = salt.removeprefix("b'")
                    salt = salt.encode()
                    tag = tag.removesuffix("'")
                    tag = tag.removeprefix("b'")
                    tag = tag.encode()

                    password_key = scrypt(sign_key, salt.decode('unicode-escape').encode('ISO-8859-1'), 16, N=2**14, r=8, p=1)
                    h = HMAC.new(password_key, digestmod=SHA256)
                    h.update(bytes(message, 'utf-8'))

                    try:
                        h.verify(tag.decode('unicode-escape').encode('ISO-8859-1'))
                        response_object = {'status': 'success'}
                        response_object['message'] = 'Authentication Successful!'
                    except ValueError:
                        response_object = {'status': 'failed'}
                        response_object['message'] = 'Authentication Failed!'

            chdir(current_dir)

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
            password = post_data.get('Password')

            config_election(election_id, election_name, description, 
                            begin_date, begin_time, end_date, end_time, 
                            candidates_file, voters_file, password)

            response_object['message'] = 'Election Created!'
    
    elif request.method == 'GET':

        election_reports = listdir(f'{current_dir}{general_data}{stat}{output}')

        for report in election_reports:

            each_election = dict()
            with open(f'{current_dir}{general_data}{stat}{output}{report}', 'r') as file1:
                election_data = json.load(file1)

                each_election['ID'] = election_data['ID']
                each_election['Name'] = election_data['Name']
                each_election['Description'] = election_data['Description']
                each_election['Quantity'] = len(election_data['Cargos'])
                each_election['StartDate'] = election_data['Begin Date']
                each_election['StartTime'] = election_data['Begin Time']
                each_election['EndDate'] = election_data['End Date']
                each_election['EndTime'] = election_data['End Time']

                with open(f'{current_dir}{general_data}{stat}{fingerprints}{election_data["ID"]}_fingerprint.json', 'r') as file2:
                    finprint = json.load(file2)
                    each_election['Fingerprint'] = finprint['Fingerprint']

            ELECTIONS.append(each_election)

        app_elections = sorted(ELECTIONS.copy(), key=itemgetter('StartDate', 'StartTime'))
        app_elections.reverse()
        response_object['elections'] = app_elections
        ELECTIONS.clear()

    return jsonify(response_object)


@app.route('/<election_id>', methods=['PUT', 'DELETE'])
def single_election(election_id):

    response_object = {'status': 'success'}

    if request.method == 'PUT':
        put_data = request.get_json()
        remove_election(election_id)

        election_id = uuid.uuid1().hex
        election_name = put_data.get('Name')
        description = put_data.get('Description')
        begin_date = put_data.get('StartDate')
        begin_time = put_data.get('StartTime')
        end_date = put_data.get('EndDate')
        end_time = put_data.get('EndTime')
        candidates_file = f'{put_data.get("CandidatesFile")}.json'
        voters_file = f'{put_data.get("VotersFile")}.json'
        password = put_data.get('Password')

        config_election(election_id, election_name, description, 
                        begin_date, begin_time, end_date, end_time, 
                        candidates_file, voters_file, password)

        response_object['message'] = 'Election Updated!'

    elif request.method == 'DELETE':
        print(election_id)
        remove_election(election_id)
        response_object['message'] = 'Election Removed!'

    return jsonify(response_object)


def remove_election(election_id):

    remove(f'{getcwd()}{general_data}{stat}{output}{election_id}_report.json')
    remove(f'{getcwd()}{general_data}{stat}{fingerprints}{election_id}_fingerprint.json')
    remove(f'{getcwd()}{general_data}{stat}{people}{election_id}_control.json')
    remove(f'{getcwd()}{general_data}{stat}{keys}{election_id}_publicKey.pem')
    remove(f'{getcwd()}{general_data}{stat}{logos}{election_id}.jpg')
    remove(f'{getcwd()}{general_data}{stat}{templates}{election_id}.jpg')

    chdir(str(Path.home()))
    chdir('..')
    chdir('..')

    remove(f'{getcwd()}media/julio/7A2F-BA93/Private Keys/{election_id}_privateKey.pem')
    remove(f'{getcwd()}media/julio/7A2F-BA93/Private Keys/{election_id}_masterPassword.json')
    
    chdir(current_dir)


@app.route('/voting', methods=['GET', 'POST'])
def show_elections():

    response_object = {'status': 'success'}
    
    if request.method == 'POST':

        post_data = request.get_json()
        voter_id = post_data.get('ID')
        message = post_data.get('Password')
        
        # chdir(str(Path.home()))
        # chdir('..')
        # chdir('..')

        # with open(getcwd() +  'media/julio/7A2F-BA93/Private Keys/' + election_id + '_privateKey.pem', 'r') as pk_file:
        #     with open(getcwd() +  'media/julio/7A2F-BA93/Private Keys/' + election_id + '_masterPassword.json', 'r') as pswd_file:
                
        #         sign_key = pk_file.read().encode()

        #         data = json.load(pswd_file)
        #         salt = data['Board Member'][0]['Salt']
        #         tag = data['Board Member'][0]['Tag']

        #         salt = salt.removesuffix("'")
        #         salt = salt.removeprefix("b'")
        #         salt = salt.encode()
        #         tag = tag.removesuffix("'")
        #         tag = tag.removeprefix("b'")
        #         tag = tag.encode()

        #         password_key = scrypt(sign_key, salt.decode('unicode-escape').encode('ISO-8859-1'), 16, N=2**14, r=8, p=1)
        #         h = HMAC.new(password_key, digestmod=SHA256)
        #         h.update(bytes(message, 'utf-8'))

        #         try:
        #             h.verify(tag.decode('unicode-escape').encode('ISO-8859-1'))
        #             response_object = {'status': 'success'}
        #             response_object['message'] = 'Authentication Successful!'
        #         except ValueError:
        #             response_object = {'status': 'failed'}
        #             response_object['message'] = 'Authentication Failed!'

        # chdir(current_dir)
    
    elif request.method == 'GET':
        
        election_reports = listdir(f'{current_dir}{general_data}{stat}{output}')

        for report in election_reports:

            each_election = dict()
            with open(f'{current_dir}{general_data}{stat}{output}{report}', 'r') as file1:
                election_data = json.load(file1)

                each_election['ID'] = election_data['ID']
                each_election['Name'] = election_data['Name']
                each_election['Description'] = election_data['Description']
                each_election['Quantity'] = len(election_data['Cargos'])
                each_election['StartDate'] = election_data['Begin Date']
                each_election['StartTime'] = election_data['Begin Time']
                each_election['EndDate'] = election_data['End Date']
                each_election['EndTime'] = election_data['End Time']

                with open(f'{current_dir}{general_data}{stat}{fingerprints}{election_data["ID"]}_fingerprint.json', 'r') as file2:
                    finprint = json.load(file2)
                    each_election['Fingerprint'] = finprint['Fingerprint']

            ELECTIONS.append(each_election)

        app_elections = sorted(ELECTIONS.copy(), key=itemgetter('StartDate', 'StartTime'))
        app_elections.reverse()
        response_object['elections'] = app_elections
        ELECTIONS.clear()

    return jsonify(response_object)


if __name__ == '__main__':
    chdir(f'{getcwd()}/src')
    app.run(debug=True)
