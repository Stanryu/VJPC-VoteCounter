from barcode.writer import ImageWriter
from Cryptodome.Random import random
from Cryptodome.Util import number
from pyzbar.pyzbar import decode
from datetime import datetime
from barcode import EAN13
import cv2 as cv
import qrcode
import os


now = datetime.now()
out_qr_name = 'QRCode_DS_EG_' + (str(now.date()) + '_' + str(now.hour) + '_' +
                                   str(now.minute) + '_' + str(now.second) + '.jpg')
out_bar_name = 'Codigo_Barras_' + (str(now.date()) + '_' + str(now.hour) + '_' +
                                   str(now.minute) + '_' + str(now.second))
out_img_name1 = 'Boleta_Identificada_' + (str(now.date()) + '_' + str(now.hour) + '_' +
                                   str(now.minute) + '_' + str(now.second) + '.jpg')
out_img_name2 = 'Boleta_Assinada_' + (str(now.date()) + '_' + str(now.hour) + '_' +
                                   str(now.minute) + '_' + str(now.second) + '.jpg')
boletas = '/Novas Boletas/'
codes = '/Assinaturas/'
bar = '/Barras/'
if not os.path.isdir(os.getcwd() + codes):
    os.mkdir(os.getcwd() + codes)
if not os.path.isdir(os.getcwd() + bar):
    os.mkdir(os.getcwd() + bar)


def codifica_msg(p):

    # Codifica a mensagem como um número pertencente a Fp escolhido de forma aleatória
    mensagem = random.randint(1, p)
    return mensagem


def primes_generator(n):

    q = number.getPrime(n)
    p = (2 * q) + 1

    # Geração dos números até que p e q sejam primos
    while not number.isPrime(p):
        q = number.getPrime(n)
        p = (2 * q) + 1

    return p, q


def base_g(p, q):

    g = random.randint(2, p - 1)

    # Procura uma base g de ordem q em Fp
    while (pow(g, 2, p) == 1) or (pow(g, q, p) != 1):
        g = random.randint(2, p - 1)

    return g


def keys_generator(p, q, g):

    # Geração da chave secreta e da chave pública
    private_key = random.randint(2, q - 1)
    public_key = pow(g, private_key, p)

    return private_key, public_key


def sign_elgamal(cod, g, p, q, private_key):

    # Geração da chave efêmera e sua inversa
    ephemeral_key = random.randint(1, q - 1)
    k = number.inverse(ephemeral_key, q)

    # Gera o par da assinatura
    s1 = pow(g, ephemeral_key, p)
    s2 = ((cod - private_key * s1) * k) % (p - 1)

    return s1, s2


def verify_elgamal(s1, s2, public_key, p, g, cod):

    r = pow(pow(public_key, s1, p) * pow(s1, s2, p), 1, p)

    # Verificação da assinatura
    if pow(g, cod, p) == r:
        return True
    else:
        return False


def restore_sign_pair(signature):

    check = 0
    for i in range(len(signature)):

        if signature[i] == ',' and not check:
            div1 = i
            check = 1
        elif signature[i] == ',' and check:
            div2 = i
            break

    cod = signature[1 : div1]
    p1 = signature[div1 + 2 : div2]
    p2 = signature[div2 + 2 : len(signature) - 1]

    return int(cod), int(p1), int(p2)


def encrypt_elgamal(g, q, p, public_key, cod):

    ephemeral_key = random.randint(1, q - 1)

    c1 = pow(g, ephemeral_key, p)
    c2 = pow(pow(g, cod) * pow(public_key, ephemeral_key), 1, p)

    # Par de textos cifrados
    return c1, c2


def decrypt_elgamal(c1, c2, private_key, p):

    # Mensagem codificada decriptada
    msg = pow(pow(c1, -private_key) * c2, 1, p)
    return msg


def place_barcode(img, codigo_barra):

    # Redimensiona o código de barras
    res = cv.resize(codigo_barra, dsize = (523, 80), interpolation = cv.INTER_CUBIC)
    height, width = res.shape[:2]

    # Insere o código de barras na boleta
    img[80 : 80 + height, 50 : 50 + width] = res

    # Salva as alterações
    cv.imwrite(os.getcwd() + boletas + out_img_name1, img)

    return img


def read_barcode(img):

    # Destaca o código de barras
    codigo_barra = img[70 : 150, 80 : 550]
    info = decode(codigo_barra)

    # Obtém o número de série
    for i in info:
        n_serie = i.data.decode('utf-8')

    return int(n_serie)


def place_QRCode(img, qrc):

    # Redimensiona o QR Code
    res = cv.resize(qrc, dsize = (120, 160), interpolation = cv.INTER_CUBIC)
    height, width = res.shape[:2]

    # Insere o QRCode na boleta
    img[175 : 175 + height, 760 : 760 + width] = res

    # Salva as alterações
    cv.imwrite(os.getcwd() + boletas + out_img_name2, img)

    return img


def read_QRCode(img):
  
    # Destaca o QR Code da boleta
    qr_code = img[175 : 540, 760 : 880]
    info = decode(qr_code)

    # Obtém o par da assinatura
    for i in info:
        signature = i.data.decode("utf-8")
    
    return signature


if __name__ == '__main__':

    # Gera os números primos e a base g de ordem q em Fp
    n = 256                      # Mínimo ---> 2048 bits
    p, q = primes_generator(n)
    g = base_g(p, q)

    # Obtém a chave secreta e a chave pública
    private_key, public_key = keys_generator(p, q, g)

    # Criação do código de barras de 12 dígitos
    min = pow(10, 11)
    max = pow(10, 12) - 1
    numero = random.randint(min, max)
    c_bar = EAN13(str(numero), writer = ImageWriter())
    c_bar.save(os.getcwd() + bar + out_bar_name)

    # Obtém a boleta e seu código de barras identificador correspondente
    boleta = cv.imread(os.getcwd() + boletas + 'teste1.jpg')
    codigo_barra = cv.imread(os.getcwd() + bar + out_bar_name + '.png')

    # Insere o código de barras na boleta e realiza sua leitura para obter o nº de série
    boleta_id = place_barcode(boleta, codigo_barra)
    n_serie = read_barcode(boleta_id)

    # Gera a assinatura digital El Gamal da boleta
    s1, s2 = sign_elgamal(n_serie, g, p, q, private_key)
    signed = (n_serie, s1, s2)
    print('\nAssinatura: ', signed)

    # Gera o QR Code da assinatura digital realizada
    qrc = qrcode.make(signed)
    qrc.save(os.getcwd() + codes + out_qr_name)

    # Obtém a boleta identificada com o nº de série e seu QR Code contendo a assinatura correspondente
    boleta_barcode = cv.imread(os.getcwd() + boletas + out_img_name1)
    qr_code = cv.imread(os.getcwd() + codes + out_qr_name)
    
    # Insere o QR Code na boleta e realiza sua leitura para obter a assinatura
    boleta_assinada = place_QRCode(boleta_barcode, qr_code)
    signature = read_QRCode(boleta_assinada)
    print('\nAssinatura lida do QR Code: ', signature)
    
    # Executa o algoritmo de verificação para a assinatura lida do QR Code
    cod, p1, p2 = restore_sign_pair(signature)
    verify = verify_elgamal(p1, p2, public_key, p, g, cod)
    print('\nStatus da verificação: ', verify)
