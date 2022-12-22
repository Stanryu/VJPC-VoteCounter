
def run(votos, categoria, candidatos):
    
    nulos = 0
    check = True
    ranking = list(votos.items())
    ranking.sort(key=lambda x: x[1], reverse=True)

    print('\n ------------ ' + categoria + ' -------------')

    for i in range(len(ranking)):
        try:
            print(candidatos[ranking[i][0]], '('+ranking[i]
                  [0]+')', '\t', ranking[i][1], 'votos')

            if ranking[i][0] == '':
                check = False
        except KeyError:
            nulos = nulos + ranking[i][1]

    if check:
        print('Votos em Branco: 0')
    print('Nulos: ', nulos)
