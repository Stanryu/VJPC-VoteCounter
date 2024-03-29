from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.py3compat import tobytes
from digitalSignatureEG import keys_generator
from geradorBoletas import adicionaLogo
from geradorBoletas import geraBoleta
from Cryptodome.Hash import SHA256
from operator import itemgetter
from Cryptodome.IO import PEM
from datetime import datetime
from directories import *
from pathlib import Path
import base64
import json


cipher_name = 'EL GAMAL '
p_type = cipher_name + 'PRIME P'
q_type = cipher_name + 'PRIME Q'
b_type = cipher_name + 'BASE G'
x_type = cipher_name + 'PRIVATE KEY'
y_type = cipher_name + 'PUBLIC KEY'


def exporting(election_name):

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
    p_key_file = open(os.getcwd() +  'media/julio/7A2F-BA93/Private Keys/' + election_name + '_privateKey.pem', 'w')
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

    key_file = open(os.getcwd() + general_data + stat + keys + election_name + '_publicKey.pem', 'w')

    # Escreve a chave pública, o primo p, o primo q e a base g no arquivo
    key_file.write(public_key.decode('utf-8') + '\n')
    key_file.write(prime_p.decode('utf-8') + '\n')
    key_file.write(prime_q.decode('utf-8') + '\n')
    key_file.write(base_g.decode('utf-8'))
    key_file.close()
    
    return base64.b64encode(p_b), base64.b64encode(q_b), base64.b64encode(g_b), base64.b64encode(y_b)


def configElection():

    check = False
    candidates_file, voters_file = None, None
    json_config_report, json_config_info = dict(), dict()
    dict_list, cargo_generate, digits_generate = list(), list(), list()
    voters_list, each_number = list(), list()

    while True:
        try:
            election_name = str(input("Informe o nome da eleição: "))
            description = str(input("Informe uma descrição para a eleição: "))
            qtd_cargos = int(input("Digite a quantidade de cargos: "))
            break
        except ValueError:
            print('Insira informações válidas!')

    # Arquivos de configuração .json
    report_name = election_name + '_report.json'
    info_name = election_name + '_fingerprint.json'
    control_name = election_name + '_control.json'

    while True:
        try:
            begin_date = str(input("Informe a data de início da votação (dd/mm/yyyy): "))
            begin_time = str(input("Informe o horário de início da votação (hh:mm): "))
            end_date = str(input("Informe a data de término da votação (dd/mm/yyyy): "))
            end_time = str(input("Informe o horário de término da votação (hh:mm): "))
            
            begin_day, begin_month, begin_year = begin_date.split('/')
            begin_hour, begin_minute = begin_time.split(':')
            begin = datetime(int(begin_year), int(begin_month), int(begin_day), int(begin_hour), int(begin_minute), 0)

            end_day, end_month, end_year = end_date.split('/')
            end_hour, end_minute = end_time.split(':')
            end = datetime(int(end_year), int(end_month), int(end_day), int(end_hour), int(end_minute), 0)

            if (begin < end and begin > datetime.now()):
                break
            else:
                print('As datas estão inconsistentes!')

        except ValueError:
            print('Insira informações válidas no formato especificado!')

    for i in range(qtd_cargos):

        aux_dict = dict()
        nome = str(input("Digite o nome do cargo: "))

        while True:
            try:
                ordem = int(input('Digite a ordem em que tal cargo deve ser exibido na boleta: '))
                digitos = int(input("Digite a quantidade de digitos do cargo: "))
                break
            except ValueError:
                print('Insira valores inteiros válidos!')

        aux_dict['Ordem'] = ordem
        aux_dict['Digitos'] = digitos
        aux_dict['Nome'] = nome

        dict_list.append(aux_dict)

    while True:
        try:
            candidates = str(input("Informe o nome do arquivo contendo as informações dos candidatos: "))
            voters = str(input("Informe o nome do arquivo contendo as informações dos eleitores: "))

            for _, _, files in os.walk(os.getcwd() + general_data + stat + people):
                for file in files:
                    
                    if candidates in file:
                        candidates_file = file
                    if voters in file:
                        voters_file = file

            if not candidates_file or not voters_file:
                raise FileNotFoundError('Arquivo não encontrado. A eleição necessita de candidaturas e eleitores para ser configurada!')
            else:
                break

        except ValueError:
            print('Inconsistência encontrada!')

    # Arquivos contendo dados sobre os candidatos e eleitores
    with open(os.getcwd() + general_data + stat + people + candidates_file, 'r') as file:
        candidates_data = json.load(file)

    with open(os.getcwd() + general_data + stat + people + voters_file, 'r') as file:
        voters_data = json.load(file)

    # Para cada cargo listado
    candidates_list = list()
    for cdts in candidates_data['Candidatos']:
        for cdt in cdts:

            # Percorre as candidaturas relacionando o cargo correspondente e o número de dígitos
            for i in range(len(dict_list)):
                for j in range(len(cdts[cdt])):

                    number_ = str(cdts[cdt][j]['Number'])
                    if dict_list[i]['Nome'] == str(cdt) and dict_list[i]['Digitos'] == len(number_):
                        
                        # (nome do cargo, número, nome)
                        candidates_list.append((cdt, number_, cdts[cdt][j]['Name']))

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

        # O aruivo de controle de votação recebe o hash do cpf concatenado com o sal, o sal e o booleano de controle
        v_control['Authentication'] = SHA256.new(hash_input.encode()).hexdigest()
        v_control['Salt'] = salt
        v_control['Vote'] = False

        voters_list.append(vts_names.copy())
        control_list.append(v_control.copy())
        
    for i in range(len(dict_list)):
        
        # Gera um dicionário contendo as candidaturas para cada cargo
        each_number = dict()
        for j in range(len(candidates_list)):
            
            # Checa se o nome do cargo corresponde
            if candidates_list[j][0] == dict_list[i]['Nome']:
                
                # (key = número, value = nome)
                each_number[str(candidates_list[j][1])] = candidates_list[j][2]
                check = True
        
        # A eleição só deve conter candidatos cujo cargo concorrido e número de dígitos se enquadrem na eleição
        dict_list[i]['Candidatos'] = each_number.copy()

    # Eleição sem candidatos não deve ocorrer
    if not check:
        print('Não existem candidatos aptos para eleição no arquivo informado!')
        exit(0)

    # Criação da chave pública da eleição
    prime_p, prime_q, base_g, public_key = exporting(election_name)
    key_dict = dict()
    key_dict['Prime P'] = prime_p.decode('utf-8')
    key_dict['Prime Q'] = prime_q.decode('utf-8')
    key_dict['Base G'] = base_g.decode('utf-8')
    key_dict['Key'] = public_key.decode('utf-8')

    # Informações gerais da eleição
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
    ballot = geraBoleta(qtd_cargos, cargo_generate, digits_generate, election_name)

    # Adiciona um logotipo no cabeçalho (Opcional)
    adicionaLogo(ballot, election_name)

    return report_name, qtd_cargos, election_name


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

    file, qtd, _ = configElection()
    cargos, pos, digits, campos = readConfigFile(file)
