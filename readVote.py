# -*- coding:utf-8 -*-
import cv2 as cv
import numpy as np
import sys
import os
import electionConfiguration
from quadrilateral import quadrilateral

FONTE = cv.FONT_HERSHEY_SIMPLEX
PROPORCAO_BARRA = 100.0
# PROPORCAO_BARRA = 213.0


def recorta(img):
    # TODO:  Implementar lógica para realizar recorte da área de votação
    return img[360:1279, 0:750]


def removerMarcacoesIniciais(posicaoQuadrados, menor_x, maior_x, tamanho_marcador):
    i = 0
    quadradosParaRemoverADireita = []
    quadradosParaRemoverAEsquerda = []
    while(i < len(posicaoQuadrados)):
        # Quadrados que estrapolam o limite a direita da área de votação
        if posicaoQuadrados[i].x > maior_x:
            quadradosParaRemoverADireita.append(posicaoQuadrados[i])
        # Quadrados que estrapolam o limite a esquerda da área de votação
        elif posicaoQuadrados[i].x < menor_x + tamanho_marcador[0]:
            quadradosParaRemoverAEsquerda.append(posicaoQuadrados[i])
        i = i + 1

    quadradosParaRemoverAEsquerda.sort(key=lambda q: q.y)
    linhas = dict()
    for i in range(len(quadradosParaRemoverAEsquerda)):
        linhas[i] = quadradosParaRemoverAEsquerda[i].y

    print("linhas " + str(linhas))

    # Quadrados que estrapolam o limite superior
    menor_y = None
    for i in quadradosParaRemoverAEsquerda:
        if menor_y == None:
            menor_y = i.y
        elif i.y < menor_y:
            menor_y = i.y

    quadradosParaRemoverAcima = []
    i = 0
    while(i < len(posicaoQuadrados)):
        # Quadrados que estrapolam o limite a direita da área de votação
        if posicaoQuadrados[i].y < (menor_y + tamanho_marcador[1]):
            quadradosParaRemoverAcima.append(posicaoQuadrados[i])
        i += 1

    toRemove = quadradosParaRemoverADireita[:] + \
        quadradosParaRemoverAEsquerda+quadradosParaRemoverAcima

    quadradosParaRemoverAcima.sort(key=lambda q: q.x)
    colunas = dict()
    for i in range(len(quadradosParaRemoverAcima)):
        colunas[i] = quadradosParaRemoverAcima[i].x

    print("colunas " + str(colunas))

    result = []
    for q in posicaoQuadrados:
        if q not in toRemove:
            result.append(q)
    return result, linhas, colunas


def mostrar(titulo, imagem):
    cv.imshow(titulo, imagem)
    cv.waitKey(0)


def run2(boleta):

    # Recorte da área de votação
    boleta = recorta(boleta)

    # print("shape: " + str(boleta.shape))
    posicaoQuadrados = list()

    # Define tamanho do pincel, que precisa ser um valor ímpar.
    tam_pincel = int(round(boleta.shape[1] / PROPORCAO_BARRA))
    if tam_pincel % 2 == 0:
        tam_pincel += 1

    # Boleta em escala cinza
    boleta_cinza = cv.cvtColor(boleta, cv.COLOR_BGR2GRAY)

    # Boleta em escala cinza borrada
    boleta_blur = cv.GaussianBlur(boleta_cinza, (tam_pincel, tam_pincel), 0)
    # mostrar("Borrado", boleta_blur)

    # Boleta em escala cinza borrada e binarizada
    ret, boleta_binaria = cv.threshold(
        boleta_blur, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
    # mostrar("Binario", boleta_binaria)

    # Identificação de poligonos com 4 lados
    cont, hier = cv.findContours(
        boleta_binaria, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    for c in cont:

        perimetro = cv.arcLength(c, True)
        approx = cv.approxPolyDP(c, 0.04 * perimetro, True)
        cv.drawContours(boleta, [c], -1, (0, 255, 0), 1)
        x, y, w, h = cv.boundingRect(c)

        if len(approx) == 3:
            forma = "Triangulo"

        elif len(approx) == 4:
            forma = "Quadrado" if (
                w/h) >= 0.95 and (w/h) <= 1.05 else "Retangulo"

        elif len(approx) == 5:
            forma = "Pentagono"

        else:
            forma = "Circulo"

        if forma == 'Quadrado' or forma == 'Retangulo':
            posicaoQuadrados.append(quadrilateral((x, y, w, h, c)))
            cv.putText(boleta, str(x) + '-' + str(y), (x, y),
                       FONTE, 0.35, (0, 0, 0), 1, cv.LINE_AA)

    # cv.imshow('Boleta', boleta)
    # cv.waitKey(0)

    posicaoQuadrados.sort(key=lambda q: q.y, reverse=True)

    # Identifica os 2 marcadores do rodapé.
    marcadoresDeRodape = list()
    marcadoresDeRodape.append(posicaoQuadrados.pop(0))
    marcadoresDeRodape.append(posicaoQuadrados.pop(0))
    marcadoresDeRodape.sort(key=lambda m: m.x)

    menor_x = marcadoresDeRodape[0].x
    maior_x = marcadoresDeRodape[1].x
    maior_y = marcadoresDeRodape[0].y
    tamanho_marcador = (marcadoresDeRodape[0].width + marcadoresDeRodape[1].width) / \
        2, (marcadoresDeRodape[0].height +
            marcadoresDeRodape[1].height) / 2

    result, positionLines, positionColumns = removerMarcacoesIniciais(
        posicaoQuadrados, menor_x, maior_x, tamanho_marcador)

    for vote in result:
        cv.drawContours(boleta, vote.c, -1, (0, 0, 255), 2)

    # mostrar('Vote', boleta)

    # Teste - Boleta Presidencial
    campos = [5, 9, 12, 14, 16]
    cargos = ['Deputado Estadual', 'Deputado Federal',
              'Senador', 'Governador', 'Presidente da República']
    linhas = 16

    # Configuração da Eleição
    # file, qtd = electionConfiguration.configElection()
    # cargos, linhas, campos = electionConfiguration.readConfigFile(file, qtd)

    matriz = construct_matrix(result, positionLines, positionColumns)
    # print(matriz)

    votos = imprime_votos2(matriz, campos, cargos)
    print(votos)

    mostrar('Vote', boleta)


def construct_matrix(votes, positionLines, positionColumns):

    matrix = np.zeros((len(positionLines), 11))
    folga_x = 12  # pixels de folga no eixo x
    folga_y = 12  # pixels de folga no eixo y

    for vote in votes:
        for l in positionLines.keys():
            if vote.y > (positionLines[l] - folga_y) and vote.y < (positionLines[l] + folga_y):
                for c in positionColumns.keys():
                    if vote.x > (positionColumns[c] - folga_x) and vote.x < (positionColumns[c] + folga_x):
                        # print(str(vote) + ' - linha: ' +
                        #       str(l) + ' - coluna: ' + str(c))
                        matrix[l][c] = 1
                        break
                break

    return matrix


def imprime_votos1(m):

    # Matriz de teste
    # m = [[0,0,1,0,0,0,0,0,0,0],
    #     [0,0,0,0,1,0,0,0,0,0,],
    #     [0,0,0,0,0,0,0,0,0,0],
    #     [0,0,0,0,0,0,0,0,0,0],
    #     [0,0,0,0,0,0,0,0,0,0],
    #     [1,0,0,0,0,0,0,0,0,0],
    #     [0,1,0,0,0,0,0,0,0,0]]

    presidente = ""
    deputado = ""
    cont = 0
    flag = 0

    while cont < 2 and flag == 0:
        invalido = 0
        con = 0
        while con < 10:
            if m[cont][con] == 0:
                con = con + 1
                continue
            if m[cont][con] == 1:
                invalido = invalido + 1
                if con == 9:
                    presidente = presidente + str(0)
                else:
                    presidente = presidente + str(con + 1)
                    con = con + 1
        if invalido != 1:
            presidente = 'Voto invalido'
        cont = cont + 1
    flag = 0

    while cont < 7 and flag == 0:
        invalido = 0
        con = 0
        while con < 10:
            if m[cont][con] == 0:
                con = con + 1
                continue
            if m[cont][con] == 1:
                invalido = invalido + 1
                if con == 9:
                    deputado = deputado + str(0)
                    con = con + 1
                else:
                    deputado = deputado + str(con + 1)
                    con = con + 1
        if invalido != 1:
            deputado = " Voto invalido"
            flag = 1

        cont = cont + 1

    print(f"Presidente: {presidente}\n Deputado:{deputado}")


def imprime_votos2(matriz, campos, cargos):

    # matriz = np.zeros((linhas, 10))
    # matriz[0][0] = 1
    # matriz[0][3] = 1
    # matriz[0][6] = 1
    # matriz[1][4] = 1
    # matriz[2][1] = 1
    # matriz[3][7] = 1
    # matriz[4][5] = 1

    # remove linha e coluna de marcação
    matriz = np.delete(matriz, (0), axis=0)
    matriz = np.delete(matriz, (0), axis=1)
    print(matriz)

    # Matriz para checagem da ocorrência de dígitos por linha
    check = np.zeros((len(matriz), 2))

    i, cargo_atual = 0, 0
    while i < (len(matriz)) and cargo_atual < len(campos):
        for j in range(len(matriz[0])):

            if matriz[i][j]:

                # Acumula a ocorrência de retângulos na linha atual da matriz
                check[i][0] += 1

                # Caso em que existam dois ou mais retângulos na mesma linha
                if i < campos[cargo_atual] and check[i][0] > 1:
                    i = campos[cargo_atual] - 1
                    cargo_atual += 1
                    break

                # Armazena os dígitos do voto
                if j != len(matriz[0]) - 1:
                    check[i][1] = j + 1
                else:
                    check[i][1] = 0

            # Caso em que exista(m) linha(s) em branco nos campos da boleta
            if i < campos[cargo_atual] and j == len(matriz[0]) - 1 and check[i][0] == 0:
                i = campos[cargo_atual] - 1
                cargo_atual += 1
                break

        i += 1

    # print(check)
    # Layout da boleta ---> [('2', 'Governador'), ('2', 'Presidente'), ('5', 'Deputado')]
    # Cargos ---> ['Governador', 'Presidente', 'Deputado']
    # Linhas ---> 9
    # Campos ---> [2, 4, 9]

    i, cargo_atual = 0, 0
    votos = [''] * len(cargos)

    # Se foram identificadas 2 ou mais marcações na mesma linha dos campos, o voto é "descartado"
    while i < len(check) and cargo_atual < len(cargos):

        # Enquanto estiver nos campos do cargo atual
        if i < campos[cargo_atual] and check[i][0] == 1:
            votos[cargo_atual] += str(int(check[i][1]))

        elif i < campos[cargo_atual] and check[i][0] != 1:
            votos[cargo_atual] = ''

            # Passagem para o próximo cargo
            i = campos[cargo_atual]
            cargo_atual += 1
            continue

        i += 1

    return votos


if __name__ == '__main__':
    # TODO: Adicionar verificação de existencia de arquivo
    #boleta = cv.imread(os.getcwd() + '/Examples/GenerateVideo/boletaVoto.jpg')
    boleta = cv.imread(os.getcwd() + '/Novas Boletas/teste.jpg')

    # TODO: Mudar print para imprimir resultado
    run2(boleta)
