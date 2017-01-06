import math

class CalculoPorcentagem(object):

    def __init__(self, projetosFromDatabase):
        self.projetosFromDatabase = projetosFromDatabase

    def CalculaMedidasPorcentagem(selfself, erro, lista_pv_acum_p):

        executado_total = lista_pv_acum_p[len(lista_pv_acum_p) - 1]

        contador=0
        true25 = 0
        true50 = 0
        true75 = 0

        for pv_acum_p in lista_pv_acum_p:
            if pv_acum_p == executado_total * 1:
                executado100 = erro[contador]
            elif pv_acum_p <= executado_total * 0.75:
                if (true75 == 0):
                    executado75 = erro[contador]
                    true75 = 1
            elif pv_acum_p <= executado_total * 0.5:
                if (true50 == 0):
                    executado50 = erro[contador]
                    true50 = 1
            elif pv_acum_p <= executado_total * 0.25:
                if (true25 == 0):
                    executado25 = erro[contador]
                    true25 = 1
            contador+=1
