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

    r = pow(pow(public_key, s1, p) * pow(s1, s2, p), 1, p)

    # Verificação da assinatura
    if pow(g, cod, p) == r:
        return True
    else:
        return False


def restore_sign_pair(signature):

    sign_size = len(signature)

    for i in range(sign_size):
        if signature[i] == ',':
            div = i
            break

    p1 = signature[1 : div]
    p2 = signature[div + 2 : sign_size - 1]

    return int(p1), int(p2)


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


def place_QRCode(img, qrc):

    # Redimensiona a imagem
    res = cv.resize(qrc, dsize = (120, 160), interpolation = cv.INTER_CUBIC)
    height, width = res.shape[:2]

    # Cola o QRCode na boleta
    img[10 : 10 + height, 425 : 425 + width] = res

    # Salva as alterações
    cv.imwrite(os.getcwd() + boletas + out_img_name, img)

    return img


def read_QRCode(img):
  
    qr_code = img[5 : 160, 410 : 545]
    info = decode(qr_code)

    for i in info:
        signature = i.data.decode("utf-8")
    
    return signature


if __name__ == '__main__':

    # Gera os números primos e a base g de ordem q em Fp
    n = 256                       # Mínimo ---> 2048 bits
    p, q = primes_generator(n)
    g = base_g(p, q)

    # Obtém a chave secreta e a chave pública
    private_key, public_key = keys_generator(p, q, g)

    # Codifica a boleta como um número pertencente a Fp escolhido de forma aleatória
    boleta = str(codifica_msg(p))

    # Obtém o hash criptográfico da codificação da boleta
    resumo = SHA256.new(bytes(boleta, 'utf-8'))
    boleta_codificada = int(resumo.hexdigest(), 16)

    # Gera a assinatura digital El Gamal da boleta e seu QR Code correspondente
    s1, s2 = sign_elgamal(boleta_codificada, p, q, private_key)
    signed = (s1, s2)
    print('\nPar da assinatura: ', signed)

    # Gera o QR Code da assinatura digital realizada
    qrc = qrcode.make(signed)
    qrc.save(os.getcwd() + saida + out_qr_name)

    # Obtém a boleta e seu QR Code contendo a assinatura correspondente
    qr_code = cv.imread(os.getcwd() + saida + out_qr_name)
    boleta = cv.imread(os.getcwd() + boletas + 'teste4.jpg')
    
    # Insere o QR Code na boleta e realiza sua leitura para obter a assinatura
    boleta_assinada = place_QRCode(boleta, qr_code)
    signature = read_QRCode(boleta_assinada)
    print('\nPar da assinatura lida do QR Code: ', signature)
    
    # Executa o algoritmo de verificação para a assinatura lida do QR Code
    p1, p2 = restore_sign_pair(signature)
    verify = verify_elgamal(p1, p2, public_key, p, g, boleta_codificada)
    print('\nStatus da verificação: ', verify)
