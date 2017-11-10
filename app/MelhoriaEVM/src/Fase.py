# -*- coding: utf-8 -*-
"""
Created on Wed Aug 03 18:06:54 2016

@author: Ana
"""
from Projeto import Projeto
from Database import Database

class Fase():
    todas_fases = list()

    #Construtor
    def __init__(self, id, nome, cpi_hist, num_atividades, esforco_real_fase, esforco_estimado_fase,
                 esforco_real_projeto, esforco_estimado_projeto, perfil_equipe, projetos_id_projeto):
        jaExite = False
        #Compara o nome da fase e o nome do projeto
        #Caso já exista retorna a variável True
        for fase in Fase.todas_fases:
            if(fase.nome == nome and fase.projetos_id_projeto == projetos_id_projeto):
                if(fase.id == -1) :
                    fase.id = id
                jaExite = True

        #Caso contrário e a função que chama a criação do objeto não for um select do banco, é adicionada uma nova fase no banco e na lista de fases
        if (jaExite==False):
            self.id = id
            self.nome = nome
            self.cpi_hist = cpi_hist
            self.num_atividades = num_atividades
            self.esforco_real_fase = esforco_real_fase
            self.esforco_estimado_fase = esforco_estimado_fase
            self.esforco_real_projeto = esforco_real_projeto
            self.esforco_estimado_projeto = esforco_estimado_projeto
            self.perfil_equipe = perfil_equipe
            self.projetos_id_projeto = projetos_id_projeto
            Fase.todas_fases.append(self)
            if(id == -1) :
                Fase.fileToDatabase(self)

    #Insere o arquivo na
    def fileToDatabase(self):
        queryInsert = ("INSERT INTO fases (nome, cpi_hist, num_atividades, perfil_equipe, esforco_real_fase, esforco_estimado_fase,"
                       "esforco_real_projeto, esforco_estimado_projeto, projetos_id_projeto) VALUES "
                       "('" +self.nome+"','"+str(self.cpi_hist)+"','"+str(self.num_atividades)+"','"+str(self.perfil_equipe)+
                       "','"+str(self.esforco_real_fase)+"','"+str(self.esforco_estimado_fase)+"','"+str(self.esforco_real_projeto)+
                       "','"+str(self.esforco_estimado_projeto)+"','"+str(self.projetos_id_projeto)+"')")
        out = Database.insert(queryInsert)
        Database.con.commit()
        #Alterar id elemento inserido no banco
        Fase.ChangeElementIdAfterInsert(self)


    def ChangeElementIdAfterInsert(self):
        querySelectSingleElement = "SELECT id_fase FROM fases WHERE nome='" + str(self.nome) + "' \
                                                              AND projetos_id_projeto='" + str(self.projetos_id_projeto) + "'"
        out = Database.get(querySelectSingleElement)
        Fase(out[0], self.nome, self.cpi_hist, self.num_atividades, self.perfil_equipe, self.esforco_real_fase, self.esforco_estimado_fase,
             self.esforco_real_projeto, self.esforco_estimado_projeto, self.projetos_id_projeto)

    #Métodos Estáticos
    @staticmethod
    def getIdByNome(nome_fase, nome_projeto):
        id_projeto = Projeto.getIdByNome(nome_projeto)
        out = Database.get(
            "SELECT * FROM fases WHERE nome='" + nome_fase + "' AND projetos_id_projeto='" + str(id_projeto) + "'")
        if (len(out) == 0):
            print "ERRO: Nenhuma fase encontrando com o Nome " + nome_fase + " para o projeto " + nome_projeto
            exit()
        return out[0][0]

    #Reinicializando valor da lista todas_fases, para ela ser utilizada no cálculo do CPI Histórico médio
    @staticmethod
    def FasesFromDBToApliccation():
        querySelect = ("SELECT * FROM fases")
        out = Database.get(querySelect)
        for rowInFases in out:
            Fase(rowInFases[0], rowInFases[1], rowInFases[2], rowInFases[3], rowInFases[4], rowInFases[5], rowInFases[6],
                 rowInFases[7], rowInFases[8], rowInFases[9])

    @staticmethod
    def UpdateFase(id_fase, cpi_hist, esforco_real_fase, num_atividades, perfil_equipe, esforco_estimado_fase, esforco_real_projeto, esforco_estimado_projeto):
        queryUpdate = "UPDATE fases SET cpi_hist= '"+str(cpi_hist)+"',esforco_real_fase='"+str(esforco_real_fase)+ \
                      "',num_atividades='"+str(num_atividades)+"',perfil_equipe='"+str(perfil_equipe)+"',esforco_estimado_fase='"+str(esforco_estimado_fase)+ \
                      "',esforco_real_projeto='" + str(esforco_real_projeto) + "',esforco_estimado_projeto='" \
                      + str(esforco_estimado_projeto) + "' WHERE id_fase='"+str(id_fase)+"'"
        out = Database.update(queryUpdate)

    def listIterator (todas_fases) :
        for fase in todas_fases :
            return fase
