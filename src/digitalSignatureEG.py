from Cryptodome.Random import get_random_bytes
from Cryptodome.PublicKey import ElGamal
from barcode.writer import ImageWriter
from Cryptodome.Random import random
from Cryptodome.Hash import SHA256
from Cryptodome.Util import number
from pyzbar.pyzbar import decode
from barcode import Code128
from readVote import run2
from directories import *
from pathlib import Path
import cv2 as cv
import qrcode
import base64
import os


# Mínimo ---> n = 2048 bits
n = 512

# Criação do código de barras de 12 dígitos
min = pow(10, 38)
max = pow(10, 39) - 1


def keys_generator():

    obj = ElGamal.generate(n, get_random_bytes)

    prime_p = int(obj.__dict__['p'])
    prime_q = int((prime_p - 1) >> 1)
    generator = int(obj.__dict__['g'])
    private_key = int(obj.__dict__['x'])
    public_key = int(obj.__dict__['y'])

    return prime_p, prime_q, generator, private_key, public_key


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


def place_barcode(election_name, img, codigo_barra):

    # Redimensiona o código de barras
    res = cv.resize(codigo_barra, dsize = (500, 100), interpolation = cv.INTER_CUBIC)
    height, width = res.shape[:2]

    # Insere o código de barras na boleta
    img[60 : 60 + height, 150 : 150 + width] = res

    # Salva as alterações
    cv.imwrite(os.getcwd() + general_data + stat + boletas + election_name + '_barcode_ballot.png', img)

    return img


def read_barcode(img):

    # Destaca o código de barras
    codigo_barra = img[50 : 170, 140 : 660]
    info = decode(codigo_barra)

    # Obtém o número de série
    for i in info:
        n_serie = i.data.decode('utf-8')

    return int(n_serie)


def place_QRCode(election_name, img, qrc):

    # Redimensiona o QR Code
    res = cv.resize(qrc, dsize = (120, 160), interpolation = cv.INTER_CUBIC)
    height, width = res.shape[:2]

    # Insere o QRCode na boleta
    img[175 : 175 + height, 760 : 760 + width] = res

    # Salva as alterações
    cv.imwrite(os.getcwd() + general_data + stat + boletas + election_name + '_qrcode_ballot.png', img)

    return img


def read_QRCode(img):
  
    # Destaca o QR Code da boleta
    qr_code = img[175 : 540, 760 : 880]
    info = decode(qr_code)

    # Obtém o par da assinatura
    for i in info:
        signature = i.data.decode("utf-8")
    
    return signature


def parsing_keys_file(election_name):

    try:
        with open(os.getcwd() + general_data + stat + keys + election_name + '_publicKey.pem', 'r') as file:

            each_info = str()
            data = list()
            info = file.readlines()
            info = [x.strip() for x in info]
            
            # Deleta as informações iniciais de cabeçalho
            del info[:1]
            for element in info:

                if '-----END EL GAMAL' in element:
                    data.append(each_info)
                    each_info = ''
                    continue
                
                if '-----BEGIN EL GAMAL' not in element:
                    each_info += element
    
    except (FileNotFoundError, FileExistsError):
        print('O arquivo de chave não foi encontrado!\n')
        exit(0)

    os.chdir(str(Path.home()))
    os.chdir('..')
    os.chdir('..')

    try:
        with open('media/julio/7A2F-BA93/Private Keys/' + election_name + '_privateKey.pem', 'r') as file:
            
            each_info = str()
            pk = list()
            info = file.readlines()
            info = [x.strip() for x in info]
            
            # Deleta as informações iniciais de cabeçalho
            del info[:1]
            for element in info:

                if '-----END EL GAMAL' in element:
                    pk.append(each_info)
                    each_info = ''
                    continue
                
                if '-----BEGIN EL GAMAL' not in element:
                    each_info += element
    
    except (FileNotFoundError, FileExistsError):
        print('O arquivo de chave de derivação não foi encontrado!\n')
        exit(0)

    os.chdir(current_dir)

    x_b = base64.b64decode(pk[0])
    y_b = base64.b64decode(data[0])
    p_b = base64.b64decode(data[1])
    q_b = base64.b64decode(data[2])
    g_b = base64.b64decode(data[3])

    private_key = int(x_b, base=10)
    public_key = int(y_b, base=10)
    prime_p = int(p_b, base=10)
    prime_q = int(q_b, base=10)
    base_g = int(g_b, base=10)

    del(x_b, pk)
    return prime_p, prime_q, base_g, private_key, public_key


def apply_signature(election_name, ballot, campos):

    # Obtém os primos (p, q), o gerador, a chave secreta e a chave pública
    p, q, g, private_key, public_key = parsing_keys_file(election_name)

    numero = random.randint(min, max)
    custom_bar = dict(font_size=6)
    c_bar = Code128(str(numero), writer = ImageWriter())
    c_bar.save(os.getcwd() + general_data + stat + bar + election_name + '_barcode', options=custom_bar)
    
    # Obtém o código de barras identificador correspondente
    codigo_barra = cv.imread(os.getcwd() + general_data + stat + bar + election_name + '_barcode.png')

    # Insere o código de barras na boleta e realiza sua leitura para obter o nº de série
    ballot_id = place_barcode(election_name, ballot, codigo_barra)
    n_serie = read_barcode(ballot_id)

    # Obtém a escolha de voto presente na boleta (tuple -> string -> bytes)
    ballot_vote = bytearray(str(run2(ballot, campos)), encoding='utf-8')

    # A escolha de voto é submetida à uma função Hash, para então ser combinada (somada) ao nº de série (bytes -> int)
    vote_hash = SHA256.new(ballot_vote)
    ballot_content = int.from_bytes(vote_hash.digest(), byteorder='big') + n_serie

    # Gera a assinatura digital El Gamal do conteúdo da boleta
    s1, s2 = sign_elgamal(ballot_content, g, p, q, private_key)
    signed = (ballot_content, s1, s2)
    del(private_key)
    # print('\nAssinatura: ', signed)

    # Gera o QR Code da assinatura digital realizada
    qrc = qrcode.make(signed)
    qrc.save(os.getcwd() + general_data + stat + codes + election_name + '_qrcode.png')

    # Obtém a boleta identificada com o nº de série e seu QR Code contendo a assinatura correspondente
    ballot_barcode = cv.imread(os.getcwd() + general_data + stat + boletas + election_name + '_barcode_ballot.png')
    qr_code = cv.imread(os.getcwd() + general_data + stat + codes + election_name + '_qrcode.png')
    
    # Insere o QR Code na boleta e realiza sua leitura para obter a assinatura
    signed_ballot = place_QRCode(election_name, ballot_barcode, qr_code)
    signature = read_QRCode(signed_ballot)
    # print('\nAssinatura lida do QR Code: ', signature)

    # Executa o algoritmo de verificação para a assinatura lida do QR Code
    cod, p1, p2 = restore_sign_pair(signature)
    verify = verify_elgamal(p1, p2, public_key, p, g, cod)
    # print('\nStatus da verificação: ', verify)

    return signed_ballot, n_serie
