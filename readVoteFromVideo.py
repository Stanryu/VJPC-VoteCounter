# -*- coding:utf-8 -*-
import cv2 as cv
import numpy as np
import sys

FONTE = cv.FONT_HERSHEY_SIMPLEX

def mostrar(titulo, imagem):
    cv.imshow(titulo, imagem)
    cv.waitKey(0)

def run(boleta):
    posicaoQuadrados = list()

    img_o = cv.imread(boleta, 1)
    img_g = cv.imread(boleta, 0)

    blurred = cv.GaussianBlur(img_o, (7, 7), 0)
    blur = cv.GaussianBlur(img_g, (7, 7), 0)

    img_b = cv.cvtColor(blurred, cv.COLOR_BGR2GRAY)
    ret, img_binaria_gray = cv.threshold(blur, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

    img, cont, hier = cv.findContours(img_binaria_gray, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    for c in cont:
        perimetro = cv.arcLength(c, True)
        approx = cv.approxPolyDP(c, 0.04 * perimetro, True)
        cv.drawContours(img_o, [c], -1, (0,255,0), 1)
        x, y, w, h = cv.boundingRect(c)

        if len(approx) == 3:
            forma = "Triangulo"

        elif len(approx) == 4:
            forma = "Quadrado" if (w/h) >= 0.95 and (w/h) <= 1.05 else "Retangulo"

        elif len(approx) == 5:
            forma = "Pentagono"

        else:
            forma = "Circulo"

        if forma == 'Quadrado' or forma == 'Retangulo':
            posicaoQuadrados.append(tuple((x,y,w,h)))
            cv.putText(img_o, str(x)+'-'+str(y)+' - '+forma,(x, y), FONTE, 0.35,(0,255,0),1,cv.LINE_AA)


    posicaoQuadrados.sort(key=lambda x: x[1], reverse = True)
    quadradoFinal = list()
    quadradoFinal.append(posicaoQuadrados.pop(0))
    quadradoFinal.append(posicaoQuadrados.pop(0))

    quadradoFinal.sort(key=lambda x: x[0])

    menor_x = quadradoFinal[0][0]
    maior_x = quadradoFinal[1][0]
    maior_y = quadradoFinal[0][1]
    #print menor_x
    distanciaTotal = maior_x - menor_x
    distanciaUnitaria_x = distanciaTotal / 11
    erro = int(0.2 * distanciaUnitaria_x)


    i = 0
    while(i<len(posicaoQuadrados)):
        if posicaoQuadrados[i][0] > maior_x:
            del(posicaoQuadrados[i])
        else:
            i = i + 1

    ## Identificando os campos de votos
    pos_campo = list()
    colunas = list()

    for i in posicaoQuadrados:
        if len(pos_campo) == 0:
            pos_campo.append(i[1])
        elif(len(pos_campo) != 8):
            if (pos_campo[-1] > i[1] + erro) or (pos_campo[-1] < i[1] - erro):
                pos_campo.append(i[1])
                if len(pos_campo) == 8:
                    colunas.append(i[0])
        else:
            if len(colunas) != 13:
                if ( i[1] == pos_campo[-1] ):
                    colunas.append(i[0])


    menor_y = pos_campo[-1]
    distanciaTotal_y = maior_y - menor_y
    distanciaUnitaria_y = int( distanciaTotal_y / 12)
    erro_y = int(0.2*distanciaUnitaria_y)


    i=0
    while (i<len(posicaoQuadrados)):
        if (posicaoQuadrados[i][0] < (menor_x + erro)) or (posicaoQuadrados[i][1] < menor_y + erro) or (posicaoQuadrados[i][0] > maior_x) : #(50   450)
            del(posicaoQuadrados[i])
        else:
            i = i + 1

    posicaoQuadrados.sort(key=lambda x: x[1])

    votos = []
    for i in posicaoQuadrados:
        votos.append(str(int(round((i[0] - menor_x) / float(distanciaUnitaria_x)))) if ((i[0] - menor_x) / distanciaUnitaria_x != 10) else '0')
    #mostrar('IMG', img_o)

    return ''.join(votos[0:2]), ''.join(votos[2:])

if __name__ == '__main__':
    print run('boletaVoto.jpg')
