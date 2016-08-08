# -*- coding: utf-8 -*-
"""
Created on Wed Aug 03 17:30:25 2016

@author: Ana
"""
from Database import Database

class Projeto(object):
    todosProjetos = [] # todos os projetos (estático)

    # Construtor
    def __init__ (self , id, nome, dtInicio, dtFim, bac ) :
        # Somente adiciona um novo projeto se não existir
        # outro projeto com o mesmo nome
        jaExiste = False
        for projeto in Projeto.todosProjetos:
            if(nome == projeto.nome):
                jaExiste = True

        if(jaExiste==False):
            self.id = id
            self.nome = nome
            self.dtInicio = dtInicio
            self.dtFim = dtFim
            self.bac = bac
            Projeto.todosProjetos.append(self)
            self.fileToDataBase()

    #Insere do arquivo no banco
    def fileToDataBase(self):
        queryInsert = ("INSERT INTO projetos (nome, dt_inicio, dt_fim, bac) VALUES "
                       "('"+self.nome+"','"+self.dtInicio+"','"+self.dtFim+"','"+str(self.bac)+"')" )
        out = Database.insert(queryInsert)
        Database.con.commit()


    #Métodos Estáticos
    @staticmethod
    def getIdByNome(nome):
        out = Database.get("SELECT * FROM projetos WHERE nome='"+nome+"'")
        if (len(out) == 0):
            print "ERRO: Nenhum projeto encontrando com o Nome: "+nome
            exit()

        return out[0][0]

    # @staticmethod
    # def ProjetoFromDBToApliccation():
    #     Projeto.todasProjetos = list()
    #     querySelect = ("SELECT * FROM fases")
    #     out = Database.get(querySelect)
    #     for rowInProjeto in out:
    #         Projeto(rowInProjeto[0], rowInProjeto[1], rowInProjeto[2], rowInProjeto[3], rowInProjeto[4])
