# -*- coding: utf-8 -*-
"""
Created on Wed Aug 03 18:11:28 2016

@author: Ana
"""
from Database import Database

class Atividade(object):
    todasAtividades = list()


    #Construtor
    def __init__ (self, id, esforcoEst, esforcoReal, fases_id_fase, projetos_id_projeto) :
            self.id = id
            self.esforcoEst = esforcoEst
            self.esforcoReal = esforcoReal
            self.fases_id_fase = fases_id_fase
            self.projetos_id_projeto = projetos_id_projeto
            Atividade.todasAtividades.append(self)
            if(id == -1) :
                self.fileToDataBase()

    #Insere no BD todas as atividades listadas
    def fileToDataBase(self):
        queryInsert = ("INSERT INTO atividades (esforco_est, esforco_real, fases_id_fase, projetos_id_projeto) VALUES ("
                          "'"+str(self.esforcoEst)+"', '"+str(self.esforcoReal)+"', '"+str(self.fases_id_fase)+"', '"+str(self.projetos_id_projeto)+"')")
        out = Database.insert(queryInsert)
        Database.con.commit()

    # Reinicializando valor da lista todasAtividades.
    @staticmethod
    def AtividadesFromDBToApliccation():
        Atividade.todasAtividades = list()
        querySelect = ("SELECT * FROM atividades")
        out = Database.get(querySelect)
        for rowInAtividades in out :
            Atividade(rowInAtividades[0], rowInAtividades[1], rowInAtividades[2], rowInAtividades[3], rowInAtividades[4])


