import cv2 as cv
import json
import sys
import os

sys.path.append(os.getcwd() + '/src/')
from electionConfiguration import getConfigFile
from readVote import run2 as read_ballot
from imprimeResultado import run as print_result
from directories import *


def video_tally():

    try:
        election_name = str(input("Informe o nome da eleição: "))
    except ValueError:
        print('Insira informações válidas!')

    # Obtém o vídeo de totalização da eleição informada
    try:
        cap = cv.VideoCapture(os.getcwd() + general_data + ver + videos + election_name + '_TallyVideo.avi')
    except FileExistsError:
        print('O vídeo de totalização não existe ou não foi encontrado!')

    # Obtém o arquivo de configuração e os dados necessários para iniciar o processo de totalização
    cargos, _, _, campos = getConfigFile(election_name)
    if not cargos:
        raise FileNotFoundError('Não existe arquivo de configuração para a eleição informada!')
    qtd_cargos = len(cargos)

    # Inicializa mapas de votação
    votos = list()
    for i in range(qtd_cargos):
        votos.append({})
    
    while cap.isOpened():
        ret, img = cap.read()
        
        if ret:
            # cv.imshow('frame',img)
            # cv.waitKey(0)

            # Lê os votos da boleta atual
            tupla_votos = read_ballot(img, campos)

            # Contabiliza os votos da boleta
            for i in range(qtd_cargos):
                key = tupla_votos[i]
                votos[i][key] = votos[i][key] + \
                    1 if key in votos[i] else 1

            # if cv.waitKey(0) & 0xFF == ord('q'):
                #break
        else:
            break

    cap.release()
    cv.destroyAllWindows()

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

    for i in range(qtd_cargos):
        print_result(votos[i], cargos[i], candidates)


if __name__ == '__main__':
    video_tally()
