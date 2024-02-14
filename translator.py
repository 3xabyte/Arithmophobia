class Translator:

    def __init__(self):

        self._maps = []
        
        f = open("maps.txt", "r")
        lines = f.readlines()
        f.close()

        for i in range(len(lines)):
            line = lines[i].rstrip("\n").split(',')
            self._maps.append((line[0], line[1]))

        return
    
    
    def key_to_map(self, key):        
        
        output = ""

        for x in self._maps:
            if(x[0] == key):
                output = x[1]

        return output


