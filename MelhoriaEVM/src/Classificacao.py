# coding=UTF-8
from Fase import Fase
from Projeto import Projeto
import numpy as np
from datetime import datetime
import pandas as pd

class Classificacao(object):

    def __init__(self, todas_fases, todos_projetos):
        self.todas_fases = todas_fases
        self.todos_projetos = todos_projetos

    #Separa os projetos pela data, projetos com datas parecidas não podem ser usados para fazer a classificação
    #Pois a ideia é prever o CPI
    def Separa_Pela_Data(self, id_projeto):
        lista_id_projetos = []

        #Utiliza o for each para verificar ql o projeto atual
        for projeto in self.todos_projetos :
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

    def Seleciona_Fases(self, lista_id_projetos_selecionados, id_projeto):

        lista_duracao, lista_cpi_projeto, lista_nome_fase, lista_cpi_fase, lista_id_projeto_fase,\
        lista_est_acum_projeto, lista_est_acum_fase, lista_perfil_equipe_fase, lista_num_atividades, \
        = [], [], [], [], [], [], [], [], []

        for fase in self.todas_fases:
            for id in lista_id_projetos_selecionados:
                if (fase.id == id):
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
                    elif (fase[1] == "testes"):
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
    def JuntaFases(self, fases_selecionadas, lista_id_projetos_selecionados):

        """lista_duracao, lista_nome_fase, lista_cpi_fase, lista_id_projeto_fase, lista_est_acum_fase,
        lista_est_acum_projeto, lista_perfil_equipe_fase, lista_num_atividades, lista_cpi_projeto"""

        lista_projetos =[]

        for id_projeto in lista_id_projetos_selecionados:
            copy = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
                    '0', '0', '0', '0', '0', '0']
            primeiro = 0
            for fases in fases_selecionadas:
                fase = np.array(fases).tolist()
                if id_projeto == int(fase[3]):
                    if primeiro == 0:
                        copy[0] = id_projeto
                        copy[1] = fase[7]
                    if 'implementacao' == fase[1]:
                        copy[2] = fase[2]
                        copy[3] = fase[1]
                        copy[4] = fase[4]
                        copy[5] = fase[5]
                        copy[6] = fase[6]
                        copy[7] = fase[8]
                        primeiro = 1
                    if 'correcao' == fase[1]:
                        copy[8] = fase[2]
                        copy[9] = fase[1]
                        copy[10] = fase[4]
                        copy[11] = fase[5]
                        copy[12] = fase[6]
                        copy[13] = fase[8]
                        primeiro = 1
                    if 'testes' == fase[1]:
                        copy[14] = fase[2]
                        copy[15] = fase[1]
                        copy[16] = fase[4]
                        copy[17] = fase[5]
                        copy[18] = fase[6]
                        copy[19] = fase[8]
                        primeiro = 1
                    if 'elaboracao' == fase[1]:
                        copy[20] = fase[2]
                        copy[21] = fase[1]
                        copy[22] = fase[4]
                        copy[23] = fase[5]
                        copy[24] = fase[6]
                        copy[25] = fase[8]
                        primeiro = 1
            lista_projetos.append(copy)
            test = np.array(lista_projetos)
            print test
        return test

    def RandomTree(self, lista_projetos):
        #lista_duracao, lista_cpi_projeto, lista_nome_fase, lista_cpi_fase, lista_id_projeto_fase
        # lista_est_acum_projeto, lista_est_acum_fase, lista_perfil_equipe_fase, lista_num_atividades
        class1, class2, class3, class4, class5, class6, class7 = [], [], [], [], [], [], []
        for projeto in lista_projetos:
            if lista_projetos[5] >= 107.65 : #esforco_estimplementacao_projeto
                if lista_projetos[1] >= 12.5 : #num_atividades
                    projetos = np.array(projeto).tolist()
                    class7.append(projetos)
                else:
                    projetos = np.array(projeto).tolist()
                    class5.append(projetos)
            else:
                if lista_projetos[24] >= 8.85 : #esforco_est_elaboração_fase
                    projetos = np.array(projeto).tolist()
                    class3.append(projetos)
                elif lista_projetos[11] >= 109.85 : #esforco_est_correcao_projeto
                    projetos = np.array(projeto).tolist()
                    class4.append(projetos)
                else:
                    projetos = np.array(projeto).tolist()
                    class2.append(projetos)

                print class2

        return class1, class2, class3, class4, class5, class6, class7