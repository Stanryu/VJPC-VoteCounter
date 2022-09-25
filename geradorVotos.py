import os
from electionConfiguration import readConfigFile

caminho = os.getcwd() + '/Static/Cargas/'


def getConfigFile(nome):
    for _, _, arquivo in os.walk(caminho):
        for file in arquivo:
            if nome in file:
                cargo, posi, digitos = readConfigFile(file)
                return cargo, digitos, posi


if __name__ == '__main__':
    name = str(input("Digite o nome da eleição:"))
    cargos, digito, pos = getConfigFile(name)
    cont = 0
    votos = {}
    for elem in cargos:
        flag = 0
        while flag == 0:
            voto = input(f"Qual seu voto para o cargo {elem} ({digito[cont]} digitos): ")
            if len(voto) == int(digito[cont]):
                votos[elem] = voto
                cont += 1
                flag = 1
            else:
                print("Número de digitos invalido. Vote novamente")

    print(votos)
