# coding=UTF-8

import numpy as np

class Classificacao(object):

    def __init__(self, todas_fases):
        self.todas_fases = todas_fases

    def SeparaFases(self, lista_fases):
        #Seleciona os ids dos projetos sem repetir
        projeto_anterior = lista_fases[0][3]
        lista_id_projeto = []
        lista_id_projeto.append(projeto_anterior)

        #Cria uma lista de ids de projetos, sem repetir o id
        for fases in lista_fases:
            if(projeto_anterior != fases[3]):
                lista_id_projeto.append(fases[3])
            projeto_anterior = fases[3]

        implementacao, teste, elaboracao, correcao, copy = [], [], [], [], []

        #Separa cada fase dentro da fase correspondente.
        #Para conseguir fazer o append na fase, primeiro tem q transformar o array em lista
        for id_projeto in lista_id_projeto:
            for fase in lista_fases:
                if (id_projeto == fase[3]):
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

    # def AgrupaPelaData(self, fases_cluster, id_projeto):

    # Juntas as fases em um unico projeto, para a previsão do cpi será necessario a utilização do perfil da equipe, esforco estimado
    # número de atividades e as datas final e inicial do projeto
    def JuntaFases(self, fases_cluster, lista_id_projeto_fase):
        # lista_duracao, lista_nome_fase, lista_cpi_fase, lista_id_projeto_fase, lista_real_acum_fase,
        # lista_est_acum_fase, lista_real_acum_projeto, lista_est_acum_projeto, lista_perfil_equipe_fase,
        # lista_num_atividades, lista_cpi_projeto

        lista_id_projeto, lista_projetos = [], []
        projeto_anterior = fases_cluster[3][0]
        for id_projeto in fases_cluster:
            if (projeto_anterior != id_projeto[3]):
                lista_id_projeto.append(id_projeto[3])
            projeto_anterior = id_projeto[3]

        for id_projeto in lista_id_projeto:
            copy = [ '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
                     '0','0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
            primeiro = 0
            for fases in fases_cluster:
                fase = np.array(fases).tolist()
                if (primeiro == 0):
                    copy[0] = id_projeto
                    copy[33] = fase[10]
                if (id_projeto == fase[3]):
                    if ('implementacao' == fase[1]):
                        copy[1] = fase[0]
                        copy[2] = fase[1]
                        copy[3] = fase[2]
                        copy[4] = fase[4]
                        copy[5] = fase[5]
                        copy[6] = fase[6]
                        copy[7] = fase[7]
                        copy[8] = fase[8]
                        primeiro = 1

                    if ('correcao' == fase[1]):
                        copy[9] = fase[0]
                        copy[10] = fase[1]
                        copy[11] = fase[2]
                        copy[12] = fase[4]
                        copy[13] = fase[5]
                        copy[14] = fase[6]
                        copy[15] = fase[7]
                        copy[16] = fase[8]
                        primeiro = 1

                    if('testes' == fase[1]):
                        copy[17] = fase[0]
                        copy[18] = fase[1]
                        copy[19] = fase[2]
                        copy[20] = fase[4]
                        copy[21] = fase[5]
                        copy[22] = fase[6]
                        copy[23] = fase[7]
                        copy[24] = fase[8]
                        primeiro = 1

                    if ('elaboracao' == fase[1]):
                        copy[25] = fase[0]
                        copy[26] = fase[1]
                        copy[27] = fase[2]
                        copy[28] = fase[4]
                        copy[29] = fase[5]
                        copy[30] = fase[6]
                        copy[31] = fase[7]
                        copy[32] = fase[8]
                        primeiro = 1
            lista_projetos.append(copy)
            test = np.array(lista_projetos)
        return test
