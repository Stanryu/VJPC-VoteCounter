import cv2 as cv

# Este é um teste apenas para verificar se o opencv está funcionando.
# Código gera um vídeo a partir de uma lista imagens contido na lista "boletas"
# As imagens devem estar no mesmo diretório deste arquivo.


# Define formato
fourcc = cv.VideoWriter_fourcc('M', 'J', 'P', 'G')

# Lista de imagens para compor o vídeo a ser gerado
boletas = ['boletaBranca.jpg', 'boletaVoto.jpg', 'boletaBranca.jpg']

# Define atributos do vídeo a ser gerado,
# o primeiro parametro diz respeito ao nome do arquivo com a extensão,
# o segundo parametro se refere ao formato do vídeo definido na variável "fourcc"
# o terceiro parametro é o tempo que cada quadro será exibida no vídeo (FPS)
# o quarto parametro é um tupla com a resolução a ser gerada (w, h)
videoWriter = cv.VideoWriter(
    'output_videoGeneratedByExample.avi', fourcc, 1, (922, 873))
for boleta in boletas:

    # A função imread() retorna uma matriz de pixels, onde cada pixel é uma cor RGB
    # example:
    # [
    #   [
    #       [255 255 255]
    #       ...
    #       [224 224 224]
    #   ]
    #   ...
    #   [
    #       [255 255 255]
    #       ...
    #       [165 165 165]
    #   ]
    # ]
    img = cv.imread(boleta)

    # Se a imagem existir e a leitura acontecer com sucesso...
    if(img is not None and img.any()):
        # Para visualizar cada imagem em uma janela, basta decomentar o comando abaixo
        # cv.imshow(boleta, img)

        # O comando abaixo faz com que a aplicação aguarde o fechamento da janela ativa
        #  para continuar a execução. Se não existir janela ativa, o comando é ignorado.
        cv.waitKey(0)

        # Comando abaixo escreve a imagem no vídeo.
        videoWriter.write(img)

# Garante que todas as janelas abertas por esta aplicação sejam fechadas
cv.destroyAllWindows()

# Limpa o gerador do vídeo
videoWriter.release()

print("Finalizado!!!")
