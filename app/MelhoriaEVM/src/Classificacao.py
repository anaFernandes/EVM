# coding=UTF-8
from Fase import Fase
from Projeto import Projeto
import numpy as np
from datetime import datetime
import pandas as pd
from sklearn.naive_bayes import MultinomialNB

class Classificacao(object):

    def __init__(self, todas_fases, todos_projetos):
        self.todas_fases = todas_fases
        self.todos_projetos = todos_projetos

    def SeparaProjetos(self, id_projeto):
        lista_id_projetos = []
        for projeto in self.todos_projetos:
            if(projeto.id <= id_projeto):
                lista_id_projetos.append(projeto.id)

        return lista_id_projetos

    #Separa os projetos pela data, projetos com datas parecidas não podem ser usados para fazer a classificação
    #Pois a ideia é prever o CPI
    def Separa_Pela_Data(self, id_projeto):
        lista_id_projetos = []

        #Utiliza o for each para verificar ql o projeto atual
        for projeto in self.todos_projetos:
            if id_projeto == projeto.id:
                #após encontrar o projeto, a função slipt é utilizada para separa o ano, o mes e o dia do projeto
                ano_projeto_atual, mes_projeto_atual, dia_projeto_atual = str(projeto.dt_inicio).split('-')

        #Percorre toda a lista de projetos, e verifica se o id do projeto é menor que o do projeto atual
        for projeto in self.todos_projetos:
            if id_projeto > projeto.id:
                #a função slipt é utilizada para dividir a data do projeto antigo
                ano_projeto_anterior, mes_projeto_anterior, dia_projeto_anterior = str(projeto.dt_fim).split('-')
                #Verifica se o ano do projeto atual é menor que o ano do projeto antigo
                if (ano_projeto_atual > ano_projeto_anterior):
                    #caso positivo add o projeto em uma nova lista
                    lista_id_projetos.append(projeto.id)
                #se o ano do projeto anterior for igual ao do projeto antigo
                elif (ano_projeto_anterior == ano_projeto_atual):
                    #checa se o mês do projeto anterior é igual ao do projeto antigo
                    if(mes_projeto_atual == mes_projeto_anterior):
                        #Se o dia do inicio do projeto atual for maior que o do projeto antigo
                        if(dia_projeto_atual > dia_projeto_anterior):
                            #add o projeto antigo na lista de projetos
                            lista_id_projetos.append(projeto.id)
                    #Se o mes do projeto atual for maior que o do projeto antigo
                    if(mes_projeto_atual > mes_projeto_anterior):
                        #add o projeto na lista de projetos
                        lista_id_projetos.append(projeto.id)
            #Se o id do projeto for igual ao do projeto atual tb add esse id na lista
            if(id_projeto == projeto.id):
                lista_id_projetos.append(projeto.id)
        return lista_id_projetos

    def Seleciona_Fases(self, lista_id_projetos_selecionados):
        lista_duracao, lista_cpi_projeto, lista_nome_fase, lista_cpi_fase, lista_id_projeto_fase,\
        lista_est_acum_projeto, lista_est_acum_fase, lista_perfil_equipe_fase, lista_num_atividades, \
        = [], [], [], [], [], [], [], [], []
        for fase in self.todas_fases:
            for id in lista_id_projetos_selecionados:
                if (fase.projetos_id_projeto == id):
                    # print fase.projetos_id_projeto
                    # print id
                    for projeto in self.todos_projetos:
                        if (projeto.id == fase.projetos_id_projeto):
                            lista_duracao.append(projeto.duracao)
                            lista_cpi_projeto.append(projeto.cpi_projeto)
                    lista_nome_fase.append(fase.nome)
                    lista_cpi_fase.append(fase.cpi_hist)
                    lista_id_projeto_fase.append(fase.projetos_id_projeto)
                    lista_est_acum_fase.append(fase.esforco_estimado_fase)
                    lista_est_acum_projeto.append(fase.esforco_estimado_projeto)
                    lista_perfil_equipe_fase.append(fase.perfil_equipe)
                    lista_num_atividades.append(fase.num_atividades)
        fases_lista = np.array(zip(lista_duracao, lista_nome_fase, lista_cpi_fase, lista_id_projeto_fase,
                                     lista_est_acum_fase, lista_est_acum_projeto, lista_perfil_equipe_fase,
                                     lista_num_atividades, lista_cpi_projeto))
        return fases_lista


    def SeparaFases(self, lista_fases, lista_id_projetos_selecionados):

        # Seleciona os ids dos projetos sem repetir

        implementacao, teste, elaboracao, correcao, copy = [], [], [], [], []
        #Separa cada fase dentro da fase correspondente.
        #Para conseguir fazer o append na fase, primeiro tem q transformar o array em lista
        for id in lista_id_projetos_selecionados:
            for fase in lista_fases:
                if (id == fase[3]):
                    if (fase[1] == "implementacao"):
                        copy=np.array(fase).tolist()
                        implementacao.append(copy)
                    elif (fase[1] == "elaboracao"):
                        copy = np.array(fase).tolist()
                        elaboracao.append(copy)
                    elif (fase[1] == "teste"):
                        copy = np.array(fase).tolist()
                        teste.append(copy)
                    elif (fase[1] == "correcao"):
                        copy = np.array(fase).tolist()
                        correcao.append(copy)

        imple = np.array(implementacao)
        elab = np.array(elaboracao)
        test = np.array(teste)
        corr = np.array(correcao)
        return imple, test, elab, corr


    # Juntas as fases em um unico projeto, para a previsão do cpi será necessario a utilização do perfil da equipe, esforco estimado
    # número de atividades e as datas final e inicial do projeto
    def JuntaFases(self, fases_selecionadas, lista_id_projetos_selecionados, projeto_atual):

        """lista_duracao, lista_nome_fase, lista_cpi_fase, lista_id_projeto_fase, lista_est_acum_fase,
        lista_est_acum_projeto, lista_perfil_equipe_fase, lista_num_atividades, lista_cpi_projeto"""

        lista_projetos, projeto_atual_selecionado = [], []
        for id_projeto in lista_id_projetos_selecionados:
            copy = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0]
            primeiro = 0
            for fases in fases_selecionadas:
                fase = np.array(fases).tolist()
                if id_projeto == int(fase[3]):
                    if primeiro == 0:
                        copy[0] = id_projeto
                        copy[1] = float(fase[7])
                        copy[23] = float(fase[8])
                    if 'implementacao' == fase[1]:
                        copy[3] = float(fase[2])
                        copy[4] = float(fase[4])
                        copy[5] = float(fase[5])
                        copy[6] = float(fase[6])
                        copy[7] = float(fase[8])
                        primeiro = 1
                    if 'correcao' == fase[1]:
                        copy[8] = float(fase[2])
                        copy[9] = float(fase[4])
                        copy[10] = float(fase[5])
                        copy[11] = float(fase[6])
                        copy[12] = float(fase[8])
                        primeiro = 1
                    if 'teste' == fase[1]:
                        copy[13] = float(fase[2])
                        copy[14] = float(fase[4])
                        copy[15] = float(fase[5])
                        copy[16] = float(fase[6])
                        copy[17] = float(fase[8])
                        primeiro = 1
                    if 'elaboracao' == fase[1]:
                        copy[18] = float(fase[2])
                        copy[19] = float(fase[4])
                        copy[20] = float(fase[5])
                        copy[21] = float(fase[6])
                        copy[22] = float(fase[8])
                        primeiro = 1
            if (id_projeto == projeto_atual):
                projeto_atual_selecionado.append(copy)
                projeto_atual_sel = np.array(projeto_atual_selecionado)
            else:
                lista_projetos.append(copy)
                lista_projetos_selecionados = np.array(lista_projetos)
        return lista_projetos_selecionados, projeto_atual_sel

    def DefineClass(self, lista_projetos):
        class1, class2, class3, class4, class5, class6, class7, classTreinamento = [], [], [], [], [], [], [], []

        for projeto in lista_projetos:
            if(float(projeto[23]) <= 1.0):
                projetos = np.array(projeto).tolist()
                classTreinamento.append(1)
                class1.append(projetos[0])
            elif(float(projeto[23]) <= 1.5):
                projetos = np.array(projeto).tolist()
                classTreinamento.append(2)
                class2.append(projetos[0])
            elif (float(projeto[23]) <= 2):
                projetos = np.array(projeto).tolist()
                classTreinamento.append(3)
                class3.append(projetos[0])
            elif (float(projeto[23]) <= 2.5):
                projetos = np.array(projeto).tolist()
                classTreinamento.append(4)
                class4.append(projetos[0])
            elif (float(projeto[23]) <= 3):
                projetos = np.array(projeto).tolist()
                classTreinamento.append(5)
                class5.append(projetos[0])
            elif (float(projeto[23]) <= 3.5):
                projetos = np.array(projeto).tolist()
                classTreinamento.append(6)
                class6.append(projetos[0])
            else:
                classTreinamento.append(7)
                projetos = np.array(projeto).tolist()
                class7.append(projetos[0])
        return class1, class2, class3, class4, class5, class6, class7, classTreinamento


    def comparaClasse(self, classe, class1, class2, class3, class4, class5, class6, class7):
        if int(classe) == 1:
            lista_id_projetos = class1
        if int(classe) == 2:
            lista_id_projetos = class2
        if int(classe) == 3:
            lista_id_projetos = class3
        if int(classe) == 4:
            lista_id_projetos = class4
        if int(classe) == 5:
            lista_id_projetos = class5
        if int(classe) == 6:
            lista_id_projetos = class6
        if int(classe) == 7:
            lista_id_projetos = class7

        return lista_id_projetos

    def CalculaMediaCPI(self, lista_id_projetos, id_projeto_atual):
        # Pega os dados do banco para calcular o CPI histórico médio de cada fase
        # Reseta os valores inicias do projeto não inserido no banco
        cpi_medio = [0, 0, 0, 0]
        contador_fases = [0, 0, 0, 0]

        i = 0

        # print ("*********************** INTERACAO ******************************* \n\n\n")
        # Percorrer todos os projetos

        for id_projeto in lista_id_projetos:
            # Percorrer projetos com o id menor do que o projeto atual
            if (id_projeto != id_projeto_atual):
                for fase in self.todas_fases:
                    if fase.projetos_id_projeto == long(id_projeto):
                        # Soma os elementos de cada fase
                        if fase.nome != 0 :
                            if fase.nome == "elaboracao":
                                # Soma os valores da fase ao cpiFasesSum.
                                cpi_medio[0] = cpi_medio[0] + Fase.todas_fases[i].cpi_hist
                                contador_fases[0] = contador_fases[0] + 1
                            elif fase.nome == "implementacao":
                                # Soma os valores da fase ao cpiFasesSum.
                                cpi_medio[1] = cpi_medio[1] + Fase.todas_fases[i].cpi_hist
                                contador_fases[1] = contador_fases[1] + 1
                            elif (fase.nome == "teste"):
                                # Soma os valores da fase ao cpiFasesSum.
                                cpi_medio[2] = cpi_medio[2] + Fase.todas_fases[i].cpi_hist
                                contador_fases[2] = contador_fases[2] + 1
                            elif (fase.nome == "correcao"):
                                # # Soma os valores da fase ao cpi_fases_sum.
                                # print ("CPI FASES SUM : " + str(cpi_medio[3]) + " \n FASES CPI HIST : " + str(Fase.todas_fases[i].cpi_hist))
                                # print Fase.todas_fases[i].projetos_id_projeto
                                cpi_medio[3] = cpi_medio[3] + Fase.todas_fases[i].cpi_hist
                                contador_fases[3] = contador_fases[3] + 1
                i += 1
        # Separar Médias
        if (id_projeto_atual != 1):
            if (contador_fases[0] != 0 or contador_fases[1] != 0 or contador_fases[2] != 0 or contador_fases[
                3] != 0):
                cpi_medio = [cpi_medio[0] / contador_fases[0],
                             cpi_medio[1] / contador_fases[1],
                             cpi_medio[2] / contador_fases[2],
                             cpi_medio[3] / contador_fases[3],
                             ]

        return cpi_medio


    def randomTree14(self, lista_projetos):

        # esforco_est_acum_elaboracao < 8.85
        # | esforco_est_testes < 33.65: Class2(2 / 0)
        # | esforco_est_testes >= 33.65: Class4(2 / 0)
        # esforco_est_acum_elaboracao >= 8.85
        # | esforco_est_elaboracao < 12.25: Class3(6 / 0)
        # | esforco_est_elaboracao >= 12.25
        # | | num_atividades < 12.5: Class5(1 / 0)
        # | | num_atividades >= 12.5: Class7(1 / 0)

        projeto = lista_projetos[len(lista_projetos) - 1]

        if(projeto[23] < 8.85):
            if(projeto[16] < 33.65):
                classe = "class2"
            else:
                classe = "class2"
        elif (projeto[22] < 12.25):
            classe = "class2"
        elif(projeto[1] < 12.5):
            classe = "class2"
        else:
            classe = "class2"

        return classe

    def randomTree16(self, lista_projetos):

        # esforco_est_acum_implementacao < 107.65
        # | esforco_est_elaboracao < 8.85
        # | | esforco_est_acum_correcao < 109.95: Class2(2 / 0)
        # | | esforco_est_acum_correcao >= 109.95: Class4(2 / 0)
        # | esforco_est_elaboracao >= 8.85: Class3(6 / 0)
        # esforco_est_acum_implementacao >= 107.65
        # | num_atividades < 12.5: Class5(1 / 0)
        # | num_atividades >= 12.5: Class7(2 / 0)

        projeto = lista_projetos[len(lista_projetos) - 1]

        if (projeto[5] < 107.65):
            if (projeto[22] < 8.85):
                if (projeto[11] < 109.95):
                    classe = 'class2'
                else:
                    classe = "class3"
            else:
                 classe = "class2"
        else:
            if (projeto[1] < 12.5):
                classe = "class2"
            else:
                classe = "class2"

        return classe


    def randomTree19(self, lista_projetos):
        projeto = lista_projetos[len(lista_projetos) - 1]

    # esforco_est_testes < 35.66
    # | esforco_est_testes < 11.35: Class8(1 / 0)
    # | esforco_est_testes >= 11.35
    # | | esforco_est_correcao < 7.4
    # | | | esforco_est_elaboracao < 8.3: Class2(2 / 0)
    # | | | esforco_est_elaboracao >= 8.3: Class3(1 / 0)
    # | | esforco_est_correcao >= 7.4: Class3(7 / 0)
    # esforco_est_testes >= 35.66
    # | num_atividades < 6.5: Class4(2 / 0)
    # | num_atividades >= 6.5
    # | | esforco_est_elaboracao < 14: Class5(1 / 0)
    # | | esforco_est_elaboracao >= 14: Class7(1 / 0)

        if (projeto[17] < 35.66):
            if (projeto[17] < 11.35):
                classe = "class2"
            elif (projeto[11] < 7.4):
                if (projeto[23] < 8.3):
                    classe = "class2"
                else:
                    classe = "class3"
            else:
                classe = "class2"
        elif (projeto[1] < 6.5):
            classe = "class3"
        elif (projeto[23] < 14):
            classe = "class2"
        else:
            classe = "class3"

        return classe


    def NaiveBayes(self, lista_projetos_treinados, class_treinada, projeto_atual):

        modelo = MultinomialNB()
        modelo.fit(lista_projetos_treinados, class_treinada)
        class_prevista = modelo.predict(projeto_atual)

        return class_prevista

