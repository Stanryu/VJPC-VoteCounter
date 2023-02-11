from Cryptodome.Random import random
from bs4 import BeautifulSoup
from time import sleep
import mechanize
import requests


n = 1000
# total = 10000
total = 1
min = pow(10, 11)
max = pow(10, 12) - 1
rng_url = 'https://www.gigacalculator.com/calculators/random-number-generator.php'


def input_rng():

    browser = mechanize.Browser()

    browser.set_handle_robots(False)
    browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0')]
    browser.open(rng_url)

    browser.select_form(nr = 1)
    browser.form['numbersfrom'] = str(min)
    browser.form['numbersto'] = str(max)
    browser.form['number'] = str(n)

    browser.submit()
    response = browser.response().read()
    browser.close()

    return response


def rng_scrap(raw_html):

    numbers = list()
    soup = BeautifulSoup(raw_html, 'lxml')
    
    r_text = soup.find('th').text
    str_numbers = r_text.split(', ')

    numbers = list(map(int, str_numbers))
    return numbers


def randomness_evaluation():

    all_numbers = list()

    for i in range(total):

        response = input_rng()
        generated_numbers = rng_scrap(response)
        all_numbers += generated_numbers

        del(response, generated_numbers)

        timing = random.randint(2, 5)
        sleep(timing)

    print(len(all_numbers))
    print(len(set(all_numbers)))
        

if __name__ == '__main__':
    pass
    # randomness_evaluation()
