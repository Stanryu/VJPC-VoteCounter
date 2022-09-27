from electionConfiguration import readConfigFile
from voteMarking import marking
import cv2 as cv
import os


caminho = os.getcwd() + '/Static'
loads = '/Cargas/'
logos = '/Logotipos/'


def getConfigFile(nome):
    for _, _, arquivo in os.walk(caminho + loads):
        for file in arquivo:
            if nome in file:
                cargo, posi, digitos, _ = readConfigFile(file)
                return cargo, digitos, posi


def get_ballot_layout(name):

    for _, _, arquivo in os.walk(caminho + logos):
        for file in arquivo:
            if name in file:
                ballot_layout = cv.imread(caminho + logos + file)
                return ballot_layout


def main():

    name = str(input("Digite o nome da eleição: "))
    cargos, digito, _ = getConfigFile(name)
    ballot_layout = get_ballot_layout(name)
    cont = 0
    votos = list()

    for elem in cargos:
        flag = 0
        
        while flag == 0:
            voto = input(f"Qual seu voto para o cargo {elem} ({digito[cont]} dígitos): ")
            
            if len(voto) == int(digito[cont]):
                votos.append(str(voto))
                cont += 1
                flag = 1
            else:
                print("Número de digitos inválido. Vote novamente!")

    marking(ballot_layout, digito, tuple(votos))


if __name__ == '__main__':
    main()
