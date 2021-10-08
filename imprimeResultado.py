#-*-coding:utf-8-*-

candidatos = {'':'Branco',
              '71':'Diego Colombo Dias',
              '92':'Paulo Yagami Elric',
              '33':'Jhonin da Hornet',
              '65':'Josafá Matador',
              '48':'Joaquim Gameplays',
              '21':'Theo Albuquerque Bragança',
              '14141':'Paulo Pinheiro',
              '52539':'Thales Eukalipto',
              '91234':'Ricardo Sucupira'}

def run(votos, categoria):
    ranking = votos.items()
    ranking.sort(key = lambda x: x[1], reverse = True)
    nulos = 0

    print '\n ------------ '+categoria+' -------------'
    for i in range(len(ranking)):
        try:
            print candidatos[ranking[i][0]], '('+ranking[i][0]+')', '\t', ranking[i][1], 'votos'
        except KeyError:
            #print ranking[i][0],'<<<< nulo'
            nulos = nulos + ranking[i][1]
    print 'Nulos : ', nulos
