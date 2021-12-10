# -*- coding: utf-8 -*-
import os
import readVote
import imprimeResultado
import electionConfiguration
import cv2 as cv

# Executa a configuração da eleição
config, qtd_cargos = electionConfiguration.configElection()
cargos, linhas, campos = electionConfiguration.readConfigFile(config, qtd_cargos)

urna = '/UrnaFisica/'
boletas = os.listdir(os.getcwd() + urna)

# Inicializa mapas de votação
votos = list()
for i in range(qtd_cargos):
    votos.append({})

for boleta in boletas:
    
    img = cv.imread(os.getcwd() + urna + boleta)

    # Lê os votos da boleta atual
    tupla_votos = readVote.run2(img, campos)

    # Contabiliza os votos da boleta
    for i in range(qtd_cargos):
        key = tupla_votos[i]
        votos[i][key] = votos[i][key] + \
            1 if key in votos[i] else 1

    # Imprime resultado
    for i in range(qtd_cargos):
        imprimeResultado.run(votos[i], cargos[i])
