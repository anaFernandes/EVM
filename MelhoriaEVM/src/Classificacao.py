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

    def Separa_Pela_Data(self, id_projeto):
        lista_id_projetos = []

        for projeto in self.todos_projetos :
            if (id_projeto == projeto.id):
                ano_projeto_atual, mes_projeto_atual, dia_projeto_atual = str(projeto.dt_inicio).split('-')
        print 'Atual' + str(ano_projeto_atual) + str(mes_projeto_atual) + str(dia_projeto_atual)
        for projeto in self.todos_projetos:
            if (id_projeto > projeto.id):
                ano_projeto_anterior, mes_projeto_anterior, dia_projeto_anterior = str(projeto.dt_fim).split('-')
                if (ano_projeto_atual > ano_projeto_anterior):
                    lista_id_projetos.append(projeto.id)
                elif (ano_projeto_anterior == ano_projeto_atual):
                    if(mes_projeto_atual == mes_projeto_anterior):
                        if(dia_projeto_atual > dia_projeto_anterior):
                            lista_id_projetos.append(projeto.id)
                    if(mes_projeto_atual > mes_projeto_anterior):
                        lista_id_projetos.append(projeto.id)
            if(id_projeto == projeto.id):
                lista_id_projetos.append(projeto.id)
        print lista_id_projetos
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
        print lista_id_projeto_fase
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
        # lista_duracao, lista_cpi_projeto, lista_nome_fase, lista_cpi_fase, lista_id_projeto_fase
        # lista_est_acum_projeto, lista_est_acum_fase, lista_perfil_equipe_fase, lista_num_atividades

        lista_projetos =[]

        for id_projeto in lista_id_projetos_selecionados:
            copy = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
                     '0','0', '0', '0', '0']
            primeiro = 0
            for fases in fases_selecionadas:
                fase = np.array(fases).tolist()
                if (id_projeto == fase[4]):
                    if (primeiro == 0):
                        copy[0] = id_projeto
                        copy[1] = fase[8]

                    if ('implementacao' == fase[1]):
                        copy[2] = fase[2]
                        copy[3] = fase[1]
                        copy[4] = fase[3]
                        copy[5] = fase[5]
                        copy[6] = fase[6]
                        copy[7] = fase[7]
                        primeiro = 1

                    if ('correcao' == fase[1]):
                        copy[8] = fase[2]
                        copy[9] = fase[1]
                        copy[10] = fase[3]
                        copy[11] = fase[5]
                        copy[12] = fase[6]
                        copy[13] = fase[7]
                        primeiro = 1

                    if('testes' == fase[1]):
                        copy[14] = fase[2]
                        copy[15] = fase[1]
                        copy[16] = fase[3]
                        copy[17] = fase[5]
                        copy[18] = fase[6]
                        copy[19] = fase[7]
                        primeiro = 1

                    if ('elaboracao' == fase[1]):
                        copy[20] = fase[2]
                        copy[21] = fase[1]
                        copy[22] = fase[3]
                        copy[23] = fase[5]
                        copy[24] = fase[6]
                        copy[25] = fase[7]
                        primeiro = 1

            lista_projetos.append(copy)
            test = np.array(lista_projetos)
        return test
