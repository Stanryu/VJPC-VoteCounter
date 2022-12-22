from electionConfiguration import getConfigFile
from geradorBoletas import get_ballot_layout
from geradorBoletas import shuffle_metadata
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
    
    try:
        voter_aut = str(input("Informe o CPF: "))

        if len(voter_aut) != 11:
            print('\nCPF no formato incorreto!')
            exit(0)
    except ValueError:
        print('Insira informações válidas!')

    authorized = False
    ghost = True

    try:
        with open(os.getcwd() + general_data + stat + output + name + '_report.json', 'r') as config:
            with open(os.getcwd() + general_data + stat + people + name + '_control.json', 'r') as control:
            
                report_data = json.load(config)
                control_data = json.load(control)

                for voter, enable in zip(report_data['Eleitores'], control_data['Eleitores']):
                    
                    hash_input = voter_aut + voter['Salt']

                    if voter['Authentication'] == SHA256.new(voter_aut.encode()).hexdigest() and\
                    enable['Authentication'] == SHA256.new(hash_input.encode()).hexdigest() and\
                    voter['Salt'] == enable['Salt'] and enable['Vote'] == False:

                        enable['Vote'] = True
                        authorized = True
                        ghost = False

                        # Atualiza o arquivo de configuração, marcando eleitores que já votaram
                        control_data = json.dumps(control_data.copy(), indent=4)
                        with open(os.getcwd() + general_data + stat + people + name + '_control.json', 'w') as file:
                            file.write(control_data)

                        break
                    elif voter['Authentication'] == SHA256.new(voter_aut.encode()).hexdigest() and enable['Vote'] == True:
                        ghost = False
                        break

    except (FileExistsError, FileNotFoundError):
        print('Os arquivos não foram encontrados ou não existem!\n')

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

    # A cada voto inserido, os metadados são manipulados
    shuffle_metadata(name)


if __name__ == '__main__':
    main()
