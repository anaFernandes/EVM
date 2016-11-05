# -*- coding: utf-8 -*-
"""
Created on Wed Aug 03 17:30:25 2016

@author: Ana
"""
from Database import Database

class Projeto(object):
    todos_projetos = [] # todos os projetos (estático)

    # Construtor
    def __init__ (self , id, nome, dt_inicio, dt_fim, bac, duracao, semestre, cpi_projeto) :
        # Somente adiciona um novo projeto se não existir
        # outro projeto com o mesmo nome
        jaExiste = False
        for projeto in Projeto.todos_projetos:
            if(nome == projeto.nome):
                if (projeto.id == -1):
                    projeto.id = id
                jaExiste = True

        if(jaExiste==False):
            self.id = id
            self.nome = nome
            self.dt_inicio = dt_inicio
            self.dt_fim = dt_fim
            self.bac = bac
            self.duracao = duracao
            self.semestre = semestre
            self.cpi_projeto = cpi_projeto
            Projeto.todos_projetos.append(self)
            if (id == -1):
                Projeto.fileToDatabase(self)

    #Insere do arquivo no banco
    def fileToDatabase(self):
        queryInsert = ("INSERT INTO projetos (nome, dt_inicio, dt_fim, bac, duracao, semestre, cpi_projeto) VALUES "
                       "('"+self.nome+"','"+self.dt_inicio+"','"+self.dt_fim+"','"+str(self.bac)+ "','"+str(self.duracao)+
                       "','"+str(self.semestre)+ "','"+str(self.cpi_projeto)+"')" )
        out = Database.insert(queryInsert)
        Database.con.commit()
        # Alterar id elemento inserido no banco
        Projeto.ChangeElementIdAfterInsert(self)


    def ChangeElementIdAfterInsert(self):
        querySelectSingleElement = "SELECT id_projeto FROM projetos WHERE nome='" + str(self.nome) + "'"
        out = Database.get(querySelectSingleElement)
        Projeto(out[0], self.nome, self.dt_inicio, self.dt_fim, self.bac, self.duracao, self.semestre, self.cpi_projeto)

    #Métodos Estáticos
    @staticmethod
    def getIdByNome(nome):
        out = Database.get("SELECT * FROM projetos WHERE nome='"+nome+"'")
        if (len(out) == 0):
            print "ERRO: Nenhum projeto encontrando com o Nome: "+nome
            exit()
        return out[0][0]

    @staticmethod
    def UpdateProjeto(id_projeto, bac, cpi_projeto):
            queryUpdate = "UPDATE projetos SET bac = '"+str(bac)+ "', cpi_projeto = '"+ str(cpi_projeto)+ \
                          "' WHERE id_projeto = '"+str(id_projeto)+"'"

            out = Database.update(queryUpdate)


    @staticmethod
    def ProjetosFromDBToApliccation():
        Projeto.todasProjetos = list()
        querySelect = ("SELECT * FROM projetos")
        out = Database.get(querySelect)
        for rowInProjeto in out:
            Projeto(rowInProjeto[0], rowInProjeto[1], rowInProjeto[2], rowInProjeto[3], rowInProjeto[4], rowInProjeto[5],
                    rowInProjeto[6], rowInProjeto[7])

    def listIterator (todos_projetos) :
        for projeto in todos_projetos :
            return projeto
