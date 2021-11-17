from Cryptodome.Random import random
from Cryptodome.Hash import SHA256
from Cryptodome.Util import number
from pyzbar.pyzbar import decode
from datetime import datetime
import cv2 as cv
import qrcode
import os


now = datetime.now()
out_qr_name = 'QRCode_DS_EG_' + (str(now.date()) + '_' + str(now.hour) + '_' +
                                   str(now.minute) + '_' + str(now.second) + '.jpg')
out_img_name = 'Boleta_Assinada_' + (str(now.date()) + '_' + str(now.hour) + '_' +
                                   str(now.minute) + '_' + str(now.second) + '.jpg')
boletas = '/Novas Boletas/'
saida = '/Assinaturas/'
if not os.path.isdir(os.getcwd() + saida):
    os.mkdir(os.getcwd() + saida)


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


def sign_elgamal(cod, p, q, private_key):

    # Geração da chave efêmera e sua inversa
    ephemeral_key = random.randint(1, q - 1)
    k = number.inverse(ephemeral_key, q)

    # Gera o par da assinatura
    s1 = pow(g, ephemeral_key, p)
    s2 = ((cod - private_key * s1) * k) % (p - 1)

    return s1, s2


def verify_elgamal(s1, s2, public_key, p, g, cod):

    r = pow(pow(public_key, s1) * pow(s1, s2), 1, p)

    # Verificação da assinatura
    if pow(g, cod, p) == r:
        return True
    else:
        return False


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


def place_QRCode(img, qrc, tipo):

    if tipo:

        # Redimensiona a imagem
        res = cv.resize(qrc, dsize = (100, 140), interpolation = cv.INTER_CUBIC)
        height, width = res.shape[:2]

        # Cola o QRCode na boleta
        img[380 : 380 + height, 760 : 760 + width] = res

        # Salva as alterações
        cv.imwrite(os.getcwd() + boletas + out_img_name, img)

    else: 

        res = cv.resize(qrc, dsize = (100, 140), interpolation = cv.INTER_CUBIC)
        height, width = res.shape[:2]

        img[320 : 320 + height, 760 : 760 + width] = res

        cv.imwrite(os.getcwd() + boletas + out_img_name, img)

    return img



def read_QRCode(img, tipo):
    
    # Recorta o QRCode na boleta
    if tipo:    
        qr_code = img[395 : 505, 770 : 850]
    else:
        qr_code = img[335 : 445, 770 : 850]

    info = decode(qr_code)
    for i in info:
        signature = i.data.decode("utf-8")
    
    return signature


if __name__ == '__main__':

    # Gera os números primos e a base g de ordem q em Fp
    n = 16                          # Mínimo ---> 2048 bits
    p, q = primes_generator(n)
    g = base_g(p, q)

    # Obtém a chave secreta e a chave pública
    private_key, public_key = keys_generator(p, q, g)

    # Codifica a boleta como um número pertencente a Fp escolhido de forma aleatória
    boleta_codificada = codifica_msg(p)
    # resumo = SHA256.new(bytes(boleta_codificada))

    # Gera a assinatura digital El Gamal da boleta e seu QR Code correspondente
    s1, s2 = sign_elgamal(boleta_codificada, p, q, private_key)
    signed = (s1, s2)
    print('Par da assinatura: ', signed)

    # Gera o QR Code da assinatura digital realizada
    qrc = qrcode.make(signed)
    qrc.save(os.getcwd() + saida + out_qr_name)

    # Obtém a boleta e seu QR Code contendo a assinatura correspondente
    qr_code = cv.imread(os.getcwd() + saida + out_qr_name)
    boleta = cv.imread(os.getcwd() + boletas + 'teste1.jpg')
    
    # Insere o QR Code na boleta e realiza sua leitura para obter a assinatura
    boleta_assinada = place_QRCode(boleta, qr_code, tipo = 1)
    signature = read_QRCode(boleta_assinada, tipo = 1)
    print('Par da assinatura lida do QR Code: ', signature)
    
    # TODO: Verificação da assinatura digital na boleta
    # Converter a string em um par de inteiros para realizar a algoritmo de verificação
    verify = verify_elgamal(s1, s2, public_key, p, g, boleta_codificada)
    print('Status da verificação: ', verify)
