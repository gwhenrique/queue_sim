
class CongruentialLinearGenerator:

    #Utilizando os parametros do Numerical Recipes como default
    def __init__(self, a=1664525, c=1013904223, max=4294967296, seed=0):
        self.a = a
        self.c = c
        self.seed = seed
        self.max = max
        self.current_value = self.seed



    def set_seed(self, seed):
        self.seed = self.current_value = seed


    def random(self):
        self.current_value = ((self.a * self.current_value) + self.c) % self.max
        return self.current_value

    def uniform(self):
        return (self.random() * 1.) / self.max
