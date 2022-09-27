import os
from datetime import datetime

now = datetime.now()
out_file_name = 'Configuracao da Eleicao' + ' - Data ' + (str(now.date()) + ' ' + str(now.hour) + '_' +
                                                          str(now.minute) + '_' + str(now.second) + '.txt')

stat = '/Static'
saida = '/Cargas/'

if not os.path.isdir(os.getcwd() + stat):
    os.mkdir(os.getcwd() + stat)
if not os.path.isdir(os.getcwd() + stat + saida):
    os.mkdir(os.getcwd() + stat + saida)


def configElection():

    cargos = list()

    while True:
        try:
            nome_eleicao = str(input("Digite o nome da eleição: "))
            qtd_cargos = int(input("Digite a quantidade de cargos: "))
            break
        except ValueError:
            print('Insira informações válidas!')

    i = 0
    while i < qtd_cargos:

        aux = list()
        nome = str(input("Digite o nome do cargo: "))

        while True:
            try:
                ordem = int(input('Digite a ordem em que tal cargo deve ser exibido na boleta: '))
                digitos = int(input("Digite a quantidade de digitos do cargo: "))
                break
            except ValueError:
                print('Insira valores inteiros válidos!')

        aux.append(ordem)
        aux.append(nome)
        aux.append(digitos)
        cargos.append(aux)

        aux.clear
        i = i + 1

    cargos.sort()
    nomeEle = nome_eleicao + ' - ' + out_file_name

    # Gera o arquivo de configuração da eleição no diretório destino
    with open(os.getcwd() + stat + saida + nomeEle, 'w') as arquivo:
        for item in cargos:
            arquivo.write(str(item[1]) + ' ' + str(item[0]) + ' ' + str(item[2]) + '\n')

    return nomeEle, qtd_cargos, nome_eleicao


def readConfigFile(file_name):

    i = 0
    cargos, digitos, pos, campos = list(), list(), list(), list()

    with open(os.getcwd() + stat + saida + file_name, 'r') as arquivo:
        
        info = arquivo.readlines()
        info = [x.strip() for x in info]
        
        for elem in info:

            aux = elem.split(' ')
            cargos.append(aux[0])
            pos.append(aux[1])
            digitos.append(aux[2])

            if i == 0:
                campos.append(digitos[i])
            else:
                campos.append(str(int(digitos[i - 1]) + int(digitos[i])))

            i += 1


    return cargos, pos, digitos, campos


if __name__ == '__main__':

    file, qtd, _ = configElection()
    cargos, pos, digits, campos = readConfigFile(file)
