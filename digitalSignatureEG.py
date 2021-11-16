from Cryptodome.Random import random
from Cryptodome.Util import number
from datetime import datetime
import qrcode
import os


now = datetime.now()
out_file_name = 'QRCode_DS_EG_' + (str(now.date()) + '_' + str(now.hour) + '_' +
                                   str(now.minute) + '_' + str(now.second) + '.jpg')
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


def EG_Sign(cod, p, q, private_key):

    # Geração da chave efêmera e sua inversa
    ephemeral_key = random.randint(1, q - 1)
    k = number.inverse(ephemeral_key, q)

    # Gera o par da assinatura
    s1 = pow(g, ephemeral_key, p)
    s2 = ((cod - private_key * s1) * k) % (p - 1)

    return s1, s2


def EG_Verify(s1, s2, public_key, p, g, cod):

    r = pow(pow(public_key, s1) * pow(s1, s2), 1, p)

    # Verificação da assinatura
    if pow(g, cod, p) == r:
        return True
    else:
        return False


def EG_Encrypt(g, q, p, public_key, cod):

    ephemeral_key = random.randint(1, q - 1)

    c1 = pow(g, ephemeral_key, p)
    c2 = pow(pow(g, cod) * pow(public_key, ephemeral_key), 1, p)

    # Par de textos cifrados
    return c1, c2


def EG_Decrypt(c1, c2, private_key, p):

    d = pow(pow(c1, -private_key) * c2, 1, p)

    # Mensagem codificada decriptada
    return d


if __name__ == '__main__':

    # Gera os números primos e a base g de ordem q em Fp
    n = 16                          # Mínimo ---> 2048 bits
    p, q = primes_generator(n)
    g = base_g(p, q)

    # Obtém a chave secreta e a chave pública
    private_key, public_key = keys_generator(p, q, g)

    # Codifica a boleta como um número pertencente a Fp escolhido de forma aleatória
    boleta_codificada = codifica_msg(p)

    # Gera a assinatura digital El Gamal da boleta e seu QR Code correspondente
    s1, s2 = EG_Sign(boleta_codificada, p, q, private_key)
    assinatura = (s1, s2)

    # Gera o QR Code da assinatura digital realizada
    img = qrcode.make(assinatura)
    img.save(os.getcwd() + saida + out_file_name)

    # TODO: Verificação da assinatura digital na boleta
    verify = EG_Verify(s1, s2, public_key, p, g, boleta_codificada)
