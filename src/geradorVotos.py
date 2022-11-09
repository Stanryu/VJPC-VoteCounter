from electionConfiguration import getConfigFile
from geradorBoletas import get_ballot_layout
from voteMarking import marking


def main():

    name = str(input("Digite o nome da eleição: "))
    cargos, digito, _, campos = getConfigFile(name)
    ballot_layout = get_ballot_layout(name)
    cont = 0
    votos = list()

    for elem in cargos:
        flag = 0
        
        while flag == 0:
            voto = input(f"Qual seu voto para o cargo {elem} ({digito[cont]} dígitos): ")
            
            if len(voto) == int(digito[cont]) or len(voto) == 0:
                votos.append(str(voto))
                cont += 1
                flag = 1
            else:
                print("Número de digitos inválido. Vote novamente!")

    marking(name, ballot_layout, digito, tuple(votos), campos)


if __name__ == '__main__':
    main()
