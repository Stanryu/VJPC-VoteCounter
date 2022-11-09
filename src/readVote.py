# -*- coding:utf-8 -*-
import cv2 as cv
import numpy as np
import os
from quadrilateral import quadrilateral

FONTE = cv.FONT_HERSHEY_SIMPLEX
PROPORCAO_BARRA = 100.0
# PROPORCAO_BARRA = 213.0


def mostrar(titulo, imagem):
    cv.imshow(titulo, imagem)
    cv.waitKey(0)


def recorta(boleta):

    tolerancia = 10
    erro_marcacao = 40

    quadradosBoleta, cabecalho, rodape, marcaçao_atual = list(), list(), list(), list()

    # Dimensões da boleta e tamanho do pincel
    height = boleta.shape[0]
    tam_pincel = int(round(boleta.shape[1] / PROPORCAO_BARRA))
    if tam_pincel % 2 == 0:
        tam_pincel += 1

    # Identificação dos quadrados na boleta completa
    quadradosBoleta, _ = identificaMarcacoes(boleta.copy(), tam_pincel)

    # Obtém as marcações do cabeçalho
    quadradosBoleta.sort(key = lambda q : q.y)
    cabecalho.append(quadradosBoleta.pop(0))
    cabecalho.append(quadradosBoleta.pop(0))
    cabecalho.sort(key = lambda q : q.x)

    # Obtém o marcador de cabeçalho mais a esquerda
    eixo_x = cabecalho[0].x
    marcaçao_atual.append(cabecalho[1])
    
    # Busca pela próxima marcação no mesmo eixo x do cabeçalho (logo abaixo dele)
    while marcaçao_atual[0].x > (eixo_x + tolerancia) or marcaçao_atual[0].x < (eixo_x - tolerancia):     
            marcaçao_atual.pop(0)
            marcaçao_atual.append(quadradosBoleta.pop(0))

    # Obtém as marcações do rodapé
    quadradosBoleta.sort(key = lambda q : q.y, reverse = True)
    rodape.append(quadradosBoleta.pop(0))
    rodape.append(quadradosBoleta.pop(0))
    rodape.sort(key = lambda q : q.x)

    # Obtém as coordenadas x e y para recortar a área de votos
    corte_x = rodape[1].x + erro_marcacao
    corte_y = marcaçao_atual[0].y
    
    return boleta[corte_y : height, 0 : corte_x]


def identificaMarcacoes(img, tam_pincel):

    posicaoQuadrados = list()

    # Imagem em escala cinza
    img_cinza = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Imagem em escala cinza borrada
    img_blur = cv.GaussianBlur(img_cinza, (tam_pincel, tam_pincel), 0)

    # Imagem em escala cinza borrada e binarizada
    _, img_binaria = cv.threshold(img_blur, 0, 255, 
                                    cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

    # Identificação de poligonos com 4 lados
    contornos, _ = cv.findContours(img_binaria, 
                                    cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    for c in contornos:

        perimetro = cv.arcLength(c, True)
        approx = cv.approxPolyDP(c, 0.04 * perimetro, True)
        cv.drawContours(img, [c], -1, (0, 255, 0), 1)
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
            cv.putText(img, str(x) + '-' + str(y), (x, y),
                       FONTE, 0.35, (0, 0, 0), 1, cv.LINE_AA)

    return posicaoQuadrados, img


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

    #print("linhas " + str(linhas))

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

    #print("colunas " + str(colunas))

    result = []
    for q in posicaoQuadrados:
        if q not in toRemove:
            result.append(q)

    return result, linhas, colunas


def run2(boleta, campos):

    mostrar('boleta', boleta)

    # Recorte da área de votação
    boleta = recorta(boleta)

    # print("shape: " + str(boleta.shape))
    posicaoQuadrados = list()

    # Define tamanho do pincel, que precisa ser um valor ímpar.
    tam_pincel = int(round(boleta.shape[1] / PROPORCAO_BARRA))
    if tam_pincel % 2 == 0:
        tam_pincel += 1

    posicaoQuadrados, boleta = identificaMarcacoes(boleta, tam_pincel)

    # mostrar('Boleta', boleta)
    
    posicaoQuadrados.sort(key=lambda q: q.y, reverse=True)

    # Identifica os 2 marcadores do rodapé.
    marcadoresDeRodape = list()
    marcadoresDeRodape.append(posicaoQuadrados.pop(0))
    marcadoresDeRodape.append(posicaoQuadrados.pop(0))
    marcadoresDeRodape.sort(key=lambda m: m.x)

    menor_x = marcadoresDeRodape[0].x
    maior_x = marcadoresDeRodape[1].x

    tamanho_marcador = (marcadoresDeRodape[0].width + marcadoresDeRodape[1].width) / \
        2, (marcadoresDeRodape[0].height +
            marcadoresDeRodape[1].height) / 2

    result, positionLines, positionColumns = removerMarcacoesIniciais(
        posicaoQuadrados, menor_x, maior_x, tamanho_marcador)

    for vote in result:
        cv.drawContours(boleta, vote.c, -1, (0, 0, 255), 2)

    mostrar('Vote', boleta)

    matriz = construct_matrix(result, positionLines, positionColumns)
    votos = imprime_votos(matriz, campos)

    tupla_votos = tuple(votos)    
    return tupla_votos


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


def imprime_votos(matriz, campos):

    # remove linha e coluna de marcação
    matriz = np.delete(matriz, (0), axis=0)
    matriz = np.delete(matriz, (0), axis=1)
    # print(matriz)

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

    i, cargo_atual = 0, 0
    votos = [''] * len(campos)

    # Se foram identificadas 2 ou mais marcações na mesma linha dos campos, o voto é "descartado"
    while i < len(check) and cargo_atual < len(campos):

        # Enquanto estiver nos campos do cargo atual
        if i < campos[cargo_atual] and check[i][0] == 1:
            votos[cargo_atual] += str(int(check[i][1]))

            # Correção para o erro de impressão em certas marcações de votos
            if i == campos[cargo_atual] - 1:
                cargo_atual += 1

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
    
    # Assinada digitalmente com o El Gamal 1024 bits
    # boleta = cv.imread(os.getcwd() + '/election_data/Static/Novas Boletas/Boleta_Assinada_2021-12-03_12_16_30.jpg')
    # campos = [5, 9, 12, 14, 16]

    boleta = cv.imread(os.getcwd() + '/election_data/Static/Novas Boletas/Boleta_Assinada_2022-05-11_23_30_36.jpg')
    campos = [5, 10, 15, 20, 25, 30]

    # boleta = cv.imread(os.getcwd() + '/election_data/Static/Novas Boletas/teste4.jpg')
    # campos = [5, 7]

    # TODO: Mudar print para imprimir resultado
    
    test = run2(boleta, campos)
    print(test)
