from directories import *
import numpy as np
import cv2 as cv
import os

# Dimensões da altura dos componentes da boleta
campo = 197
foot = 115
header = 488
interval = 17   # Espaço entre os campos de votos
width = 922     # Largura da boleta é fixa
# digit = 30
# base = 40

fonte = cv.FONT_HERSHEY_DUPLEX
escala, grossura = 1, 2


def geraBoleta(qtd_cargos, cargos, digitos, layout_name):
    
    soma_dos_digitos = 0
    
    for elem in digitos:
        if int(elem) == 1:
            soma_dos_digitos = soma_dos_digitos + 70
        elif int(elem) == 2:
            soma_dos_digitos = soma_dos_digitos + 102
        elif int(elem) == 3:
            soma_dos_digitos = soma_dos_digitos + 133
        elif int(elem) == 4:
            soma_dos_digitos = soma_dos_digitos + 165
        elif int(elem) == 5:
            soma_dos_digitos = soma_dos_digitos + 197

    # Calcula quantos px no eixo y os campos de votos ocuparão
    vote_field =  soma_dos_digitos + (qtd_cargos - 1) * interval

    # Obtém a altura total somando a altura em px de todos os componentes da boleta
    height = header + foot + vote_field

    # Cria uma boleta em branco com dimensões que variam de acordo com a configuração da eleição
    boleta = np.zeros((height, width, 3), dtype = np.uint8)
    cv.rectangle(boleta, (0, 0), (width, height), (255, 255, 255), -1)

    # Insere o cabeçalho na boleta
    cabecalho = cv.imread(os.getcwd() + general_data + componentes + 'header_488.jpg')
    boleta[0 : 0 + cabecalho.shape[0], 0 : width] = cabecalho

    # Insere o rodapé na boleta
    rodape = cv.imread(os.getcwd() + general_data + componentes + 'foot_115.jpg')
    posicaoRodape = height - rodape.shape[0]
    boleta[posicaoRodape : posicaoRodape + rodape.shape[0], 0 : width] = rodape

    # Obtém a posição inicial y logo ao fim do cabeçalho
    y_atual = header

    text = list()
    voto1 = cv.imread(os.getcwd() + general_data + componentes + '1.jpg')
    voto2 = cv.imread(os.getcwd() + general_data + componentes + '2.jpg')
    voto3 = cv.imread(os.getcwd() + general_data + componentes + '3.jpg')
    voto4 = cv.imread(os.getcwd() + general_data + componentes + '4.jpg')
    voto5 = cv.imread(os.getcwd() + general_data + componentes + '5.jpg')


    for i in range(qtd_cargos):

        if int(digitos[i]) == 1:
            escrita = voto1.copy()
            aux = 70
        elif int(digitos[i]) == 2:
            escrita = voto2.copy()
            aux = 102
        elif int(digitos[i]) == 3:
            escrita = voto3.copy()
            aux = 133
        elif int(digitos[i]) == 4:
            escrita = voto4.copy()
            aux = 165
        elif int(digitos[i]) == 5:
            escrita = voto5.copy()
            aux = 197

        # Obtém cada nome de cargo formatado para inserção na boleta
        text.append('{} '.format(cargos[i]))

        # Obtém o tamanho (altura e largura) do texto em pixels
        tamanho, _ = cv.getTextSize(text[i], fonte, escala, grossura)

        # Insere o texto no centro
        cv.putText(escrita, text[i], (int(800 / 2 - tamanho[0] / 2), int(40 / 2 + tamanho[1] / 2)), fonte, escala, (255, 255, 255), grossura)

        # Insere o campo de voto na boleta
        boleta[y_atual : y_atual + aux , 0 : width] = escrita

        # Incrementa a posição y para inserção em sequência dos campos de votos
        y_atual += aux + interval

    # Salva e retorna a boleta com os campos de votos e nomes de cargos inseridos
    cv.imwrite(os.getcwd() + general_data + stat + templates + layout_name + '.jpg', boleta)
    return boleta


def adicionaLogo(boleta, layout_name):

    logo = cv.imread(os.getcwd() + general_data + stat + logos + 'logo_2.jpg')

    # Redimensiona o logotipo para acomodar o código de barras e QR Code posteriormente
    res = cv.resize(logo, dsize = (620, 160), interpolation = cv.INTER_CUBIC)
    boleta[175 : 175 + res.shape[0], 80 : 80 + res.shape[1]] = res

    # Salva as alterações
    cv.imwrite(os.getcwd() + general_data + stat + logos + layout_name + '.jpg', boleta)


def get_ballot_layout(name):

    for _, _, arquivo in os.walk(os.getcwd() + general_data + stat + logos):
        for file in arquivo:
            if name in file:
                ballot_layout = cv.imread(os.getcwd() + general_data + stat + logos + file)
                return ballot_layout


def shuffle_metadata(election_name):

    # Obtém a lista com os nomes de todos os arquivos presentes na urna
    try:
        path = current_dir + general_data + ver + election_name + '_Urn/'
        ballots = os.listdir(path)
    except NotADirectoryError:
        print("A urna solicitada não existe ou não foi encontrada!")

    if not ballots:
        print('Não foram encontrados registros na urna!')
        return

    # Para cada registro na urna, leia, remova e reescreva-o
    for img in ballots:

        ballot = cv.imread(path + img)
        os.remove(path + img)
        cv.imwrite(path + img, ballot)
