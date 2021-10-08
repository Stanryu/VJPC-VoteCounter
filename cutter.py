# -*- coding:utf-8 -*-
import cv2 as cv
import numpy as np
import sys

FONTE = cv.FONT_HERSHEY_SIMPLEX
posicaoQuadrados = list()

def mostrar(titulo, imagem):
    cv.imshow(titulo, imagem)
    cv.waitKey(0)

img_o = cv.imread('boletaNn.png', 1)
img_g = cv.imread('boletaNn.png', 0)

blurred = cv.GaussianBlur(img_o, (7, 7), 0)
blur = cv.GaussianBlur(img_g, (7, 7), 0)

img_b = cv.cvtColor(blurred, cv.COLOR_BGR2GRAY)
ret, img_binaria_gray = cv.threshold(blur, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
mostrar('img_binaria_gray', img_binaria_gray)


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
        #if x <= 701 and x >=600 and y == 417:
        # cv.putText(img_o, forma,(x, y), FONTE, 0.5,(0,255,0),1,cv.LINE_AA)
        cv.putText(img_o, str(x)+'-'+str(y),(x, y), FONTE, 0.35,(0,255,0),1,cv.LINE_AA)
        posicaoQuadrados.append(tuple((x,y,w,h)))



# for quadrado in posicaoQuadrados:
#     print quadrado
# print len(posicaoQuadrados)
#
# print
posicaoQuadrados.sort(key=lambda x: x[1], reverse = True)
# print posicaoQuadrados
quadradoFinal = list()
quadradoFinal.append(posicaoQuadrados.pop(0))
quadradoFinal.append(posicaoQuadrados.pop(0))

# print
# print posicaoQuadrados
quadradoFinal.sort(key=lambda x: x[0])
# print quadradoFinal

menor_x = quadradoFinal[0][0]
maior_x = quadradoFinal[1][0]
maior_y = quadradoFinal[0][1]
distanciaTotal = maior_x - menor_x
distanciaUnitaria_x = distanciaTotal / 11
erro = int(0.2 * distanciaUnitaria_x)

# print "maior x = ", maior_x

##Excluido todos os objetos a direita do maior_x (Como somente adicionei quadrados e retangulos, não espere remover outros objetos detectados)
# print 'antes ',len(posicaoQuadrados)


# for i in posicaoQuadrados:
#     if i[0] > maior_x:
#         posicaoQuadrados.remove(i)
# print 'depois ',len(posicaoQuadrados)

i = 0
while(i<len(posicaoQuadrados)):
    if posicaoQuadrados[i][0] > maior_x:
        del(posicaoQuadrados[i])
    else:
        i = i + 1


##Agora preciso identificar e remover os objetos acima da marcacao principal

## Identificando os campos de votos
pos_campo = list()
colunas = list()
# print '<<<',posicaoQuadrados
for i in posicaoQuadrados:
    #print i
    if len(pos_campo) == 0:
        pos_campo.append(i[1])
    elif(len(pos_campo) != 8):
        if (pos_campo[-1] > i[1] + erro) or (pos_campo[-1] < i[1] - erro):
            pos_campo.append(i[1])
            if len(pos_campo) == 8:
                # print '1111 - ', i
                colunas.append(i[0])
    else:
        # print '>>> ', i
        if len(colunas) != 13:
            if ( i[1] == pos_campo[-1] ):
                colunas.append(i[0])
        #else:
            #posicaoQuadrados.remove(i)

# print pos_campo

menor_y = pos_campo[-1]
print 'menor y = ',menor_y
distanciaTotal_y = maior_y - menor_y
distanciaUnitaria_y = int( distanciaTotal_y / 12)
erro_y = int(0.2*distanciaUnitaria_y)


print '' , len(posicaoQuadrados)
print 'numero de campos' , len(pos_campo)
print 'numero de colunas' , len(colunas)
print ' campos' , (pos_campo)
print ' colunas' ,(colunas)
print '' , len(posicaoQuadrados)

# Nao funciona percorrer com for e remover ao mesmo tempo
# for i in posicaoQuadrados:
#     if i[0] < 50 or i[1] < 450 :
#         posicaoQuadrados.remove(i)

i=0
while (i<len(posicaoQuadrados)):
    if (posicaoQuadrados[i][0] < (menor_x + erro)) or (posicaoQuadrados[i][1] < menor_y + erro): #(50   450)
        del(posicaoQuadrados[i])
    else:
        i = i + 1

print '' , len(posicaoQuadrados)
print posicaoQuadrados

# print 'distancia unitaria_x',distanciaUnitaria_x
# print 'erro x ',erro
# print 'distancia unitaria_y',distanciaUnitaria_y
# print 'erro y ',erro_y

posicaoQuadrados.sort(key=lambda x: x[1])

for i in posicaoQuadrados:
    print i,' - ', int(round((i[0] - menor_x) / float(distanciaUnitaria_x)) )

#img_croped = img_e[cut_height : cut_height + img_o.shape[1], 0 : cut_width]

#ret, img_b = cv.threshold(blur, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

#mostrar('IMG', img_g)
#mostrar('IMG', img_b)
#mostrar('IMG', img_binaria_gray)
mostrar('IMG', img_o)

## TODO: Nao add obj reconhecidos fora da area de interesse
#       considerar inclinacao do papel
