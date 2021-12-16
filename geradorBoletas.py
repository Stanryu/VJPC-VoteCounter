from datetime import datetime
import electionConfiguration
import cv2 as cv
import sys
import os

fonte = cv.FONT_HERSHEY_DUPLEX
escala, grossura = 1, 2

now = datetime.now()
logos = '/Logotipos/'
templates = '/Templates/'
out_logo_name = 'Boleta_Personalizada_' + (str(now.date()) + '_' + str(now.hour) + '_' +
                                            str(now.minute) + '_' + str(now.second) + '.jpg')
out_cargos_name = 'Boleta_Configurada_' + (str(now.date()) + '_' + str(now.hour) + '_' +
                                            str(now.minute) + '_' + str(now.second) + '.jpg')


def adicionaLogo(boleta):

    logo = cv.imread(os.getcwd() + logos + 'logo_2.jpg')
    
    # Redimensiona o logotipo para acomodar o código de barras e QR Code posteriomente
    res = cv.resize(logo, dsize = (620, 160), interpolation = cv.INTER_CUBIC)
    boleta[175 : 175 + res.shape[0], 80 : 80 + res.shape[1]] = res

    # Salva as alterações
    cv.imwrite(os.getcwd() + logos + out_logo_name, boleta)


def escreveCargos(qtd_cargos, cargos):

    if qtd_cargos == 1:

        boleta = cv.imread(os.getcwd() + templates + 'template_1.jpg')

        # Desenha o texto em branco no centro
        texto_1 = '{} '.format(cargos[0])

        # Pega o tamanho (altura e largura) do texto em pixels
        tamanho, _ = cv.getTextSize(texto_1, fonte, escala, grossura)

        # Insere o texto no centro
        cv.putText(boleta, texto_1, (int(800 / 2 - tamanho[0] / 2), int(1010 / 2 + tamanho[1] / 2)), 
                    fonte, escala, (255, 255, 255), grossura)

    elif qtd_cargos == 2:

        boleta = cv.imread(os.getcwd() + templates + 'template_2.jpg')

        texto_1 = '{} '.format(cargos[0])
        texto_2 = '{} '.format(cargos[1])

        tamanho, _ = cv.getTextSize(texto_1, fonte, escala, grossura)

        cv.putText(boleta, texto_1, (int(800 / 2 - tamanho[0] / 2), int(1010 / 2 + tamanho[1] / 2)), 
                    fonte, escala, (255, 255, 255), grossura)
        cv.putText(boleta, texto_2, (int(810 / 2 - tamanho[0] / 2), int(1430 / 2 + tamanho[1] / 2)),
                    fonte, escala, (255, 255, 255), grossura)

    elif qtd_cargos == 3:

        boleta = cv.imread(os.getcwd() + templates + 'template_3.jpg')

        texto_1 = '{} '.format(cargos[0])
        texto_2 = '{} '.format(cargos[1])
        texto_3 = '{} '.format(cargos[2])

        tamanho, _ = cv.getTextSize(texto_1, fonte, escala, grossura)

        cv.putText(boleta, texto_1, (int( 800 / 2 - tamanho[0] / 2), int(1010 / 2 + tamanho[1] / 2)),
                    fonte, escala, (255, 255, 255), grossura)
        cv.putText(boleta, texto_2, (int(810 / 2 - tamanho[0] / 2), int(1430 / 2 + tamanho[1] / 2)),
                    fonte, escala, (255, 255, 255), grossura)
        cv.putText(boleta, texto_3, (int(810 / 2 - tamanho[0] / 2), int(1855 / 2 + tamanho[1] / 2)),
                    fonte, escala, (255, 255, 255), grossura)

    else:
        print('Quantidade de cargos inválida!')
        sys.exit()

    # Salva as alterações
    cv.imwrite(os.getcwd() + templates + out_cargos_name, boleta)


if __name__ == '__main__':

    # Obtém do usuário a configuração de layout de boleta desejado
    config, qtd_cargos = electionConfiguration.configElection()
    cargos, _, _ = electionConfiguration.readConfigFile(config, qtd_cargos)

    # Insere o nome dos cargos na boleta
    escreveCargos(qtd_cargos, cargos)

    # Adiciona a imagem desejada no cabeçalho
    boleta = cv.imread(os.getcwd() + templates + out_cargos_name)
    adicionaLogo(boleta)
    