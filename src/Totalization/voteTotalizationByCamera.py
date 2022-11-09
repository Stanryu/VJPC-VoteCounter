# -*- coding: utf-8 -*-
import cv2 as cv
import sys
import os
import time
from datetime import datetime

# Ainda em desenvolvimento inicial

# TODO: Implementação de leitura das imagens pela camera, considerando distorções e votos repetidos.
# Será necessário ajustar dispositivo de segurança que garanta a identificação única da boleta.
# Isso irá evitar que uma boleta seja contabilizada mais de uma vez.

zona = '256'
secao = "1"
camera_port = 0
nFrames = 30.0
emLoop = True

camera = cv.VideoCapture(camera_port)
fourcc = cv.VideoWriter_fourcc('M', 'J', 'P', 'G')
now = datetime.now()
out_file_name = (str(now.date()) + '_' + str(now.hour)+'-'+str(now.minute) +
         '-' + str(now.second) + '_' + zona + '_' + secao + '.avi')

# Diretórios
ver = '/v1.0'
saida = '/Output/'

# O diretótio '/Output/' e '/v1.0/ são criados caso não existam
if not os.path.isdir(os.getcwd() + ver):
    os.mkdir(os.getcwd() + ver)
if not os.path.isdir(os.getcwd() + ver + saida):
    os.mkdir(os.getcwd() + ver + saida)
    
out = cv.VideoWriter(os.getcwd() + ver + saida + out_file_name, fourcc, nFrames, (640, 480))

if not camera.isOpened():
    print('Nao foi possivel abrir a web cam.')
    sys.exit(-1)

while(emLoop):
    retval, img = camera.read()
    if retval == True:
        out.write(img)
        cv.imshow('Foto', img)
        print("."),
    else:
        print('Oops! A captura falhou.')
        break

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

print('Captura encerrada.')

camera.release()
out.release()
cv.destroyAllWindows()
