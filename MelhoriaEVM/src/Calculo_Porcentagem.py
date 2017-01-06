import math

class Calculo_Porcentagem(object):

    def __init__(self, projetosFromDatabase):
        self.projetosFromDatabase = projetosFromDatabase

    def Calcula_Medidas_Porcentagem(self, erro, lista_pv_acum_p):

        executado_total = lista_pv_acum_p[len(lista_pv_acum_p) - 1]
        print executado_total
        print lista_pv_acum_p
        print erro
        print len(lista_pv_acum_p)
        print len(erro)
        contador = 0
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

        print executado25
        print executado50
        print executado75
        print executado100
        print "-------_----------"
        return executado100, executado75, executado50, executado25