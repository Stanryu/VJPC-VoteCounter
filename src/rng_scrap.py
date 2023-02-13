from random_user_agent.params import OperatingSystem
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName
from Cryptodome.Random import random
from bs4 import BeautifulSoup
from mechanize import Browser
from time import sleep


# Total de números para gerar, intervalo dos mesmos e página Web para gerar
total = 10000000
min = pow(10, 11)
max = pow(10, 12) - 1
rng_url = 'https://www.gigacalculator.com/calculators/random-number-generator.php'

# Geração das strings de agente de usuário (para vários SOs e navegadores distintos)
software_names = [SoftwareName.CHROME.value, SoftwareName.FIREFOX.value, SoftwareName.EDGE.value, SoftwareName.OPERA.value, SoftwareName.SAFARI.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value, OperatingSystem.ANDROID.value, OperatingSystem.IOS.value, OperatingSystem.MACOS.value]   
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=500)


def initialize_browser():

    my_browser = Browser()
    my_browser.set_handle_robots(False)

    # Requisita como um User-agent distinto a cada requisição para evitar bloqueios por IP
    my_browser.addheaders = [('User-agent', user_agent_rotator.get_random_user_agent())]
    my_browser.open(rng_url)

    # Seleciona o formulário a ser preenchido
    my_browser.select_form(nr = 1)

    return my_browser


def auto_generation(my_browser):

    # Preenche os valores do intervalo nos campos
    my_browser.form['numbersfrom'] = str(min)
    my_browser.form['numbersto'] = str(max)

    # Quantidade de números a serem gerados definida aleatoriamente a cada requisição
    n = random.randint(800, 1000)
    my_browser.form['number'] = str(n)
    
    # Executa a requisição e recebe o arquivo HTML referente à resposta da mesma
    my_browser.submit()
    response = my_browser.response().read()

    numbers = list()
    soup = BeautifulSoup(response, 'lxml')
    
    # Obtém o texto contendo o(s) número(s) gerados na resposta da requisição (tag HTML <th>)
    r_text = soup.find('th').text
    str_numbers = r_text.split(', ')

    # Converte todos os números da lista para inteiros (str -> int)
    numbers = list(map(int, str_numbers))
    return numbers


def randomness_evaluation():

    print('Inicializando...\n')
    all_numbers = list()
    my_browser = initialize_browser()

    # Enquanto não forem gerados números suficientes
    while len(all_numbers) < total:

        # Preenche os campos da paǵina, obtém os números gerados e adiciona-os na lista
        generated_numbers = auto_generation(my_browser)
        all_numbers += generated_numbers

        del(generated_numbers)
        progress = (len(all_numbers) / total) * 100.0
        print(f'{round(progress, 2)} concluído...')

        # Tempo definido aleatoriamente entre cada requisição para evitar bloqueio por IP
        timing = random.randint(2, 4)
        sleep(timing)

    my_browser.close()

    # Resultado
    print('\nFinalizado!\n')
    size = len(all_numbers)
    uniques = len(set(all_numbers))
    print(f'{size - uniques} repetições em {size} códigos gerados!')
        

if __name__ == '__main__':
    randomness_evaluation()
