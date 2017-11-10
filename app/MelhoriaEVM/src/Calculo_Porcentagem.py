
class Calculo_Porcentagem(object):

    def __init__(self, projetosFromDatabase):
        self.projetosFromDatabase = projetosFromDatabase

    def VerificaNumero(self, lista_esforco_estimado_acum_p, esf_est_acum_porcentagem):
        menorVariacao = 99999
        contador = 0

        for esforco_estimado_acum in lista_esforco_estimado_acum_p:
            variacaoEsforco = esforco_estimado_acum - esf_est_acum_porcentagem
            if (menorVariacao > variacaoEsforco):
                menorVariacao = esforco_estimado_acum
                indice = contador
            contador = contador + 1

        return indice

    def Calcula_Medidas_Porcentagem(self, medida, lista_esforco_estimado_acum_p):
        # print "array: " +str(medida)
        executado_total = lista_esforco_estimado_acum_p[len(lista_esforco_estimado_acum_p) - 1]

        executadoListaEstimado25 = executado_total*0.25
        executadoListaEstimado50 = executado_total*0.50
        executadoListaEstimado75 = executado_total*0.75

        executado100 = medida[len(medida) - 1]
        indice25 = self.VerificaNumero(lista_esforco_estimado_acum_p, executadoListaEstimado25)
        # print "indice: " +str(indice25)
        # print len(medida)
        # print len(lista_esforco_estimado_acum_p)
        if(medida[indice25] != 0):
            executado25 = lista_esforco_estimado_acum_p[indice25]
        else:
            executado25 = lista_esforco_estimado_acum_p[indice25+1]
        indice50 = self.VerificaNumero(lista_esforco_estimado_acum_p, executadoListaEstimado50)
        if (medida[indice50] != 0):
            executado50 = lista_esforco_estimado_acum_p[indice50]
        else:
            executado50 = lista_esforco_estimado_acum_p[indice50+1]
        indice75 = self.VerificaNumero(lista_esforco_estimado_acum_p, executadoListaEstimado75)
        if (medida[indice75] != 0):
            executado75 = lista_esforco_estimado_acum_p[indice75]
        else:
            executado75 = lista_esforco_estimado_acum_p[indice75+1]

        return executado100, executado75, executado50, executado25
