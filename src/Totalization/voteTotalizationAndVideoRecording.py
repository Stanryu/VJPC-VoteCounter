import cv2 as cv
import json
import sys
import os

sys.path.append(os.getcwd() + '/src/')
from electionConfiguration import getConfigFile
from readVote import run2 as read_ballot
from imprimeResultado import run as print_result
from directories import *


def generate_video():

    try:
        election_name = str(input("Informe o nome da eleição: "))
    except ValueError:
        print('Insira informações válidas!')

    # Formato do vídeo (Avi)
    fourcc = cv.VideoWriter_fourcc('M', 'J', 'P', 'G')
    nFrames = 30

    # Diretório da urna
    urna = '/' + election_name + '_Urn/'
    if not os.path.isdir(current_dir + general_data + ver + urna):
        raise NotADirectoryError('O diretório não existe! Cheque o nome da eleição e se existem registros para gerar o vídeo.')

    # Lista de nomes dos arquivos (boletas)
    boletas = os.listdir(current_dir + general_data + ver + urna)

    # Identifica tamanhos das imagens
    img = cv.imread(os.getcwd() + general_data + ver + urna + boletas[0])
    height, width, _ = img.shape

    # Cria escritor de vídeo com base nas configurações identificadas
    out = cv.VideoWriter(os.getcwd() + general_data + ver + videos + election_name + '_TallyVideo.avi', fourcc, nFrames, (width, height))

    # Identifica cada voto e contabiliza no mapa de votação
    for boleta in boletas:

        # Adiciona a imagem da boleta em um frame do vídeo
        img = cv.imread(os.getcwd() + general_data + ver + urna + boleta)
        out.write(img)

    # Fecha janelas e finaliza escritor
    cv.destroyAllWindows()
    out.release()


def tallying():

    try:
        election_name = str(input("Informe o nome da eleição: "))
    except ValueError:
        print('Insira informações válidas!')

    # Diretório da urna
    urna = '/' + election_name + '_Urn/'
    if not os.path.isdir(current_dir + general_data + ver + urna):
        raise NotADirectoryError('O diretório não existe! Cheque o nome da eleição e se existem registros para totalizar.')

    # Lista de nomes dos arquivos (boletas)
    boletas = os.listdir(current_dir + general_data + ver + urna)

    # Obtém o arquivo de configuração e os dados necessários para iniciar o processo de totalização
    cargos, _, _, campos = getConfigFile(election_name)
    if not cargos:
        raise FileNotFoundError('Não existe arquivo de configuração para a eleição informada!')
    qtd_cargos = len(cargos)

    # Inicializa mapas de votação
    votos = list()
    for i in range(qtd_cargos):
        votos.append(dict())

    # Identifica cada voto e contabiliza no mapa de votação
    for boleta in boletas:

        # Adiciona a imagem da boleta em um frame do vídeo
        img = cv.imread(os.getcwd() + general_data + ver + urna + boleta)

        # Lê os votos da boleta atual
        tupla_votos = read_ballot(img, campos)
        
        # Contabiliza os votos da boleta
        for i in range(qtd_cargos):
            key = tupla_votos[i]
            votos[i][key] = votos[i][key] + \
                1 if key in votos[i] else 1
    
    # Obtém o nome do arquivo de configuração
    check = False
    for _, _, files in os.walk(os.getcwd() + general_data + stat + output):
        for file in files:
            
            if election_name in file:
                file_election = file
                check = True
                break
        
        if check:
            break
    
    # Monta o dicionário de candidatos {número de voto : nome do candidato}
    candidates = dict()
    with open(os.getcwd() + general_data + stat + output + file_election, 'r') as file:

        data = json.load(file)

        for cargo in data['Cargos']:
            for value in cargo['Candidatos']:
                candidates[value] = cargo['Candidatos'][value]

    candidates[''] = 'Votos em Branco'

    # Imprime resultado
    for i in range(qtd_cargos):
        print_result(votos[i], cargos[i], candidates)

    # TODO: Adicionar validação da contagem pelo vídeo com o número de boletas na urna física.


if __name__ == '__main__':

    print('1 - Gerar Vídeo\n2 - Totalizar\n')
    try:
        option = int(input("Informe a operação: "))
    except ValueError:
        print('Insira valores inteiros!')
    
    if option == 1:
        generate_video()
    elif option == 2:
        tallying()
    else:
        print('Opção Inválida!')
