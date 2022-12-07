# -*-coding:utf-8-*-

def run(votos, categoria, candidatos):

    nulos = 0
    ranking = list(votos.items())
    ranking.sort(key=lambda x: x[1], reverse=True)

    print('\n ------------ ' + categoria + ' -------------')

    for i in range(len(ranking)):
        try:
            print(candidatos[ranking[i][0]], '('+ranking[i]
                  [0]+')', '\t', ranking[i][1], 'votos')
        except KeyError:
            nulos = nulos + ranking[i][1]

    print('Nulos : ', nulos)
