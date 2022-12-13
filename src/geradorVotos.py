from electionConfiguration import getConfigFile
from geradorBoletas import get_ballot_layout
from Cryptodome.Hash import SHA256
from voteMarking import marking
from directories import *
import json
import os


def main():

    name = str(input("Digite o nome da eleição: "))
    cargos, digito, _, campos = getConfigFile(name)
    ballot_layout = get_ballot_layout(name)
    cont = 0
    votos = list()

    # Obtém o nome do arquivo de configuração
    check = False
    for _, _, files in os.walk(os.getcwd() + general_data + stat + output):
        for file in files:
            
            if name in file:
                file_election = file
                check = True
                break
        
        if check:
            break

    if not check:
        print('\nO arquivo desejado não existe ou não foi encontrado!')
        exit(0)
    
    try:
        voter_aut = str(input("Informe o CPF: "))

        if len(voter_aut) != 11:
            print('\nCPF no formato incorreto!')
            exit(0)
    except ValueError:
        print('Insira informações válidas!')

    authorized = False
    ghost = True
    with open(os.getcwd() + general_data + stat + output + file_election, 'r') as file:
        
        data = json.load(file)

        for voter in data['Eleitores']:

            if voter['Password'] == SHA256.new(voter_aut.encode()).hexdigest() and voter['Vote'] == False:
                voter['Vote'] = True
                authorized = True
                ghost = False

                # Atualiza o arquivo de configuração, marcando eleitores que já votaram
                data = json.dumps(data.copy(), indent=4)
                with open(os.getcwd() + general_data + stat + output + file_election, 'w') as file:
                    file.write(data)

                break
            elif voter['Password'] == SHA256.new(voter_aut.encode()).hexdigest() and voter['Vote'] == True:
                ghost = False
                break

    if authorized:

        for elem in cargos:
            flag = 0
            
            while flag == 0:
                voto = input(f"Qual seu voto para o cargo {elem} ({digito[cont]} dígitos): ")
                
                if len(voto) == int(digito[cont]) or len(voto) == 0:
                    votos.append(str(voto))
                    cont += 1
                    flag = 1
                else:
                    print("\nNúmero de digitos inválido. Vote novamente!\n")

        marking(name, ballot_layout, digito, tuple(votos), campos)

    elif ghost:
        print('\nNão existe eleitor na base de dados com o CPF informado!')

    elif not authorized:
        print('\nO eleitor já votou!')



if __name__ == '__main__':
    main()
