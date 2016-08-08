# -*- coding: utf-8 -*-
"""
Created on Wed Aug 03 18:06:54 2016

@author: Ana
"""
from Projeto import Projeto
from Database import Database

class Fase():
    todasFases = list()

    #Construtor
    def __init__(self, id, nome, cpiHist, projetos_id_projeto):
        jaExite = False

        #Compara o nome da fase e o nome do projeto
        #Caso já exista retorna a variável True
        for fase in Fase.todasFases:
            if(fase.nome == nome and fase.projetos_id_projeto == projetos_id_projeto):
                jaExite = True

        #Caso contrário, é adicionada uma nova fase no banco e na lista de fases
        if (jaExite==False):
            self.id = id
            self.nome = nome
            self.cpiHist = cpiHist
            self.projetos_id_projeto = projetos_id_projeto
            Fase.todasFases.append(self)
            self.fileToDatabase()

    #Insere o arquivo na
    def fileToDatabase(self):
        queryInsert = ("INSERT INTO fases (nome, cpi_hist, projetos_id_projeto) VALUES ('"
                       ""+self.nome+"', '"+str(self.cpiHist)+"', '"+str(self.projetos_id_projeto)+"')")
        out = Database.insert(queryInsert)
        Database.con.commit()


    #Métodos Estáticos
    @staticmethod
    def getIdByNome(nomeFase, nomeProjeto):
        idProjeto = Projeto.getIdByNome(nomeProjeto)

        out = Database.get(
            "SELECT * FROM fases WHERE nome='" + nomeFase + "' AND projetos_id_projeto='" + str(idProjeto) + "'")
        if (len(out) == 0):
            print "ERRO: Nenhuma fase encontrando com o Nome " + nomeFase + " para o projeto " + nomeProjeto
            exit()

        return out[0][0]

    #Reinicializando valor da lista todasFases, para ela ser utilizada no cálculo do CPI Histórico médio
    @staticmethod
    def FasesFromDBToApliccation():
        Fase.todasFases = list()
        querySelect = ("SELECT * FROM fases")
        out = Database.get(querySelect)
        for rowInFases in out:
            Fase(rowInFases[0], rowInFases[1], rowInFases[2], rowInFases[3])

