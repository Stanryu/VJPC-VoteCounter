class quadrilateral:
    def __init__(self, infos):
        self.x = infos[0]
        self.y = infos[1]
        self.width = infos[2]
        self.height = infos[3]
        self.c = infos[4]

    def __repr__(self):
        # return 'Quadrilátero( x=' + str(self.x) + ', y=' + str(self.y) + ', width=' + str(self.width) + ', height=' + str(self.height) + ' )'
        return '(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.width) + ', ' + str(self.height) + ' )'


if __name__ == '__main__':
    meuQuadrilatero = quadrilateral(
        tuple([2, 3, 10, 20, [1, 2, 2, 3, [3, 4, 5]]]))
    print('teste ' + str(meuQuadrilatero))
