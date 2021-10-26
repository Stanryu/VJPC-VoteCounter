# -*- coding: utf-8 -*-
import os
from datetime import datetime
import cv2 as cv
import readVote
import imprimeResultado

# Define dados de seção eleitoral
zona = '256'
secao = "1"
nFrames = 30
now = datetime.now()
out_file_name = 'Totalizacao--Zona_' + zona + '-Secao_' + secao + '-Data' + (str(now.date()) + '_' + str(now.hour)+'-' +
                                                                             str(now.minute)+'-'+str(now.second) + '.avi')
# out_file_name = 'saida1.avi'


# Formato do vídeo (Avi)
fourcc = cv.VideoWriter_fourcc('M', 'J', 'P', 'G')

# Diretórios
urna = '/UrnaFisica/'
saida = '/Output/'

# Lista de nomes dos arquivos (boletas)
boletas = os.listdir(os.getcwd() + urna)

# Identifica tamanhos das imagens
img = cv.imread(os.getcwd() + urna + boletas[0])
height, width, layers = img.shape

# O diretótio '/Output/' é criado caso não exista
if not os.path.isdir(os.getcwd() + saida):
    os.mkdir(os.getcwd() + saida)

# Cria escritor de vídeo com base nas configurações identificadas
out = cv.VideoWriter(os.getcwd() + saida + out_file_name, fourcc, nFrames, (width, height))

# Inicializa mapas de votação
totalVotosPresidente = {}
totalVotosDeputado = {}

# Identifica cada voto e contabiliza no mapa de votação
for boleta in boletas:

    # Adiciona a imagem da boleta em um frame do vídeo
    img = cv.imread(os.getcwd() + urna + boleta)
    out.write(img)

    # Lê os votos da boleta atual
    presidente, deputado = readVote.run2(img)

    # Contabiliza os votos da boleta
    totalVotosPresidente[presidente] = totalVotosPresidente[presidente] + \
        1 if presidente in totalVotosPresidente else 1
    totalVotosDeputado[deputado] = totalVotosDeputado[deputado] + \
        1 if deputado in totalVotosDeputado else 1

# Fecha janelas e finaliza escritor
cv.destroyAllWindows()
out.release()

# Imprime resultado
imprimeResultado.run(totalVotosPresidente, 'Presidente')
imprimeResultado.run(totalVotosDeputado, 'Deputado')

# TODO: Adicionar validação da contagem pelo vídeo com o número de boletas na urna física.
