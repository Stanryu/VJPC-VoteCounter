from digitalSignatureEG import apply_signature
from directories import *
from readVote import run2
from PIL import Image
import cv2 as cv
import os


# Posição do slot inicial (1º dígito, 1º cargo, 1ª linha, 1ª coluna)
begin = (107, 536)

# Dimensões de cada retângulo vazio para preencher
rect_height = 30
rect_width = 60

# Dimensões de cada retângulo para marcar
mark_height = 15
mark_width = 30

# Distância entre as áreas de votação para cada cargo (eixo y)
role_jump = 60

# Casos especiais
blank_vote = ''
zero_digit = '0'
tol = 13


def marking(election_name, ballot, digits_qtd, vote, campos):

    k = 0
    x = begin[0]
    y = begin[1]

    # Para cada cargo presente no registro
    while digits_qtd:

        j = 0
        digit_counter = 1

        # Ex: vote[k] = '123' ---> list(vote[k]) = ['1', '2', '3']
        if type(vote) is tuple:
            each_choice = list(vote[k])
        else:
            each_choice = list(vote)

        # Enquanto existem dígitos à serem marcados para cada cargo
        while digit_counter <= int(digits_qtd[0]):

            # Votos me branco devem ser ignorados na marcação
            if vote[k] == blank_vote:
                y += rect_height * int(digits_qtd[0])
                break

            # A posição para o dígito 0 deve ser incrementada "manualmente" (rect_width * 0 --> marca o dígito 1)
            elif each_choice[j] == zero_digit:
                temp_x = x + rect_width * 9 + tol

            # Incrementa o eixo x de acordo com a magnitude de cada dígito
            else:
                mag = int(each_choice[j])
                temp_x = x + rect_width * (mag - 1) + mag 

            # Coordenadas no topo superior esquerdo e canto inferior direito do retângulo para preencher
            top_rect = (temp_x, y)
            bottom_rect = (temp_x + mark_width, y + mark_height)

            # Realiza a marcação na boleta
            cv.rectangle(ballot, top_rect, bottom_rect, (0, 0, 0), -1)

            # "Salta" para a próxima linha de voto à ser marcada
            y += rect_height

            # Incrementa o contador de dígitos para aquele cargo
            digit_counter += 1
            j += 1

        # Elimina o cargo cujo voto já foi marcado
        digits_qtd.pop(0)

        # Incrementa o eixo y para preencher o voto para o próximo cargo
        y += role_jump
        k += 1

        cv.imshow('ballot' + str(k), ballot)
        cv.waitKey(0)

    sig = apply_signature(election_name, ballot, campos)

    cv.imshow('ballot', sig)
    cv.waitKey(0)

    # img = Image.open(os.getcwd() + general_data + stat + boletas + election_name + '_qrcode_ballot.png')
    # img_data = list(img.getdata())
    # extract = Image.new(img.mode, img.size)
    # extract.putdata(img_data)
    # extract.save(os.getcwd() + general_data + stat + boletas + election_name + '_qrcode_ballot_nometadata.png')

    # cv.imwrite(os.getcwd() + '/final_2.jpg', ballot)
    return ballot


def main():

    # ballots = os.listdir(os.getcwd() + general_data + stat + logos)
    # ballots.sort()

    ballot = cv.imread(os.getcwd() + general_data + stat + templates + 'template_2.jpg')
    thresholds = [5, 10]
    vote = ('12340', '')

    marked = marking(ballot, [5, 5], vote)

    print(run2(marked, thresholds))


if __name__ == '__main__':
    main()
