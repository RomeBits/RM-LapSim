class Car:
    def __init__(self, file):
        f = open(file)
        self.params = {}
        
        for i in f:
            self.params[i.split()[0]] = i.split()[1]

