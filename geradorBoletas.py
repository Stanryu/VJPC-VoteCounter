from datetime import datetime
import electionConfiguration
import numpy as np
import cv2 as cv
import os

# Dimensões da altura dos componentes da boleta
campo = 197
foot = 115
header = 488
interval = 17   # Espaço entre os campos de votos
width = 922     # Largura da boleta é fixa

fonte = cv.FONT_HERSHEY_DUPLEX
escala, grossura = 1, 2

now = datetime.now()
logos = '/Logotipos/'
templates = '/Templates/'
componentes = '/Components/'
out_logo_name = 'Boleta_Personalizada_' + (str(now.date()) + '_' + str(now.hour) + '_' +
                                            str(now.minute) + '_' + str(now.second) + '.jpg')
out_cargos_name = 'Boleta_Configurada_' + (str(now.date()) + '_' + str(now.hour) + '_' +
                                            str(now.minute) + '_' + str(now.second) + '.jpg')


def geraBoleta(qtd_cargos, cargos):

    # Calcula quantos px no eixo y os campos de votos ocuparão
    vote_field = qtd_cargos * campo + (qtd_cargos - 1) * interval

    # Obtém a altura total somando a altura em px de todos os componentes da boleta
    height = header + foot + vote_field

    # Cria uma boleta em branco com dimensões que variam de acordo com a configuração da eleição
    boleta = np.zeros((height, width, 3), dtype = np.uint8)
    cv.rectangle(boleta, (0, 0), (width, height), (255, 255, 255), -1)

    # Insere o cabeçalho na boleta
    cabecalho = cv.imread(os.getcwd() + componentes + 'header_488.jpg')
    boleta[0 : 0 + cabecalho.shape[0], 0 : width] = cabecalho

    # Insere o rodapé na boleta
    rodape = cv.imread(os.getcwd() + componentes + 'foot_115.jpg')
    posicaoRodape = height - rodape.shape[0]
    boleta[posicaoRodape : posicaoRodape + rodape.shape[0], 0 : width] = rodape

    # Obtém a posição inicial y logo ao fim do cabeçalho
    y_atual = header

    texto = list()
    voto = cv.imread(os.getcwd() + componentes + 'campo_197.jpg')

    for i in range(qtd_cargos):
        
        # Faz uma nova cópia do campo de voto para inserir o nome do cargo
        escrita = voto.copy()

        # Obtém cada nome de cargo formatado para inserção na boleta
        texto.append('{} '.format(cargos[i]))
        
        # Obtém o tamanho (altura e largura) do texto em pixels
        tamanho, _ = cv.getTextSize(texto[i], fonte, escala, grossura)

        # Insere o texto no centro
        cv.putText(escrita, texto[i], (int(800 / 2 - tamanho[0] / 2), int(40 / 2 + tamanho[1] / 2)),
                    fonte, escala, (255, 255, 255), grossura)

        # Insere o campo de voto na boleta
        boleta[y_atual : y_atual + campo, 0 : width] = escrita

        # Incrementa a posição y para inserção em sequência dos campos de votos
        y_atual += campo + interval

    # cv.imshow('teste', boleta)
    # cv.waitKey(0)
    
    # Salva e retorna a boleta com os campos de votos e nomes de cargos inseridos
    cv.imwrite(os.getcwd() + templates + out_cargos_name, boleta)
    return boleta


def adicionaLogo(boleta):

    logo = cv.imread(os.getcwd() + logos + 'logo_2.jpg')
    
    # Redimensiona o logotipo para acomodar o código de barras e QR Code posteriormente
    res = cv.resize(logo, dsize = (620, 160), interpolation = cv.INTER_CUBIC)
    boleta[175 : 175 + res.shape[0], 80 : 80 + res.shape[1]] = res

    # Salva as alterações
    cv.imwrite(os.getcwd() + logos + out_logo_name, boleta)


if __name__ == '__main__':

    # Obtém do usuário a configuração de layout de boleta desejado
    config, qtd_cargos = electionConfiguration.configElection()
    cargos, _, _ = electionConfiguration.readConfigFile(config, qtd_cargos)

    # Gera a boleta com os cargos desejados e componentes essenciais para leitura
    boleta = geraBoleta(qtd_cargos, cargos)

    # Adiciona um logotipo no cabeçalho (Opcional)
    adicionaLogo(boleta)
