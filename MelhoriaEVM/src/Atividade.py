# -*- coding: utf-8 -*-
"""
Created on Wed Aug 03 18:11:28 2016

@author: Ana
"""
from Database import Database
from Fase import Fase
from Projeto import Projeto

class Atividade(object):
    todasAtividades = list()

    #Construtor
    def __init__ (self, id, esforco_est, esforco_real, responsavel, fases_id_fase, projetos_id_projeto, num_requisito):
        jaExite = False
        # Compara o nome da fase e o nome do projeto
        # Caso já exista retorna a variável True
        for atividade in Atividade.todasAtividades:
            if (atividade.num_requisito == num_requisito and atividade.fases_id_fase == fases_id_fase and atividade.projetos_id_projeto == projetos_id_projeto):
                if (atividade.id == -1):
                    atividade.id = id
                jaExite = True

        # Caso contrário e a função que chama a criação do objeto não for um select do banco, é adicionada uma nova fase no banco e na lista de fases
        if (jaExite == False):
            self.id = id
            self.esforco_est = esforco_est
            self.esforco_real = esforco_real
            self.fases_id_fase = fases_id_fase
            self.projetos_id_projeto = projetos_id_projeto
            self.num_requisito = num_requisito
            self.responsavel = responsavel
            Atividade.todasAtividades.append(self)
            if(id == -1) :
                Atividade.fileToDataBase(self)

    #Insere no BD todas as atividades listadas
    def fileToDataBase(self):
        queryInsert = ("INSERT INTO atividades (esforco_est, esforco_real, responsavel, fases_id_fase, projetos_id_projeto, numero_requisito) VALUES ("
                          "'"+str(self.esforco_est)+"', '"+str(self.esforco_real)+"', '"+str(self.responsavel)+"', '"+str(self.fases_id_fase)+"', '"+str(self.projetos_id_projeto)+ "','"+str(self.num_requisito)+"')")
        out = Database.insert(queryInsert)
        Database.con.commit()
        # Alterar id elemento inserido no banco
        Atividade.ChangeElementIdAfterInsert(self)

    @staticmethod
    def getIdByNome(nomeFase, nomeProjeto, num_requisito):
        idProjeto = Projeto.getIdByNome(nomeProjeto)
        idFase = Fase.getIdByNome(nomeFase, nomeProjeto)
        out = Database.get(
            "SELECT * FROM atividades WHERE fases_id_fase='" + str(idFase) + "' AND projetos_id_projeto='" + str(idProjeto) + "'AND numero_requisito = '"+ num_requisito +"'")

        if (len(out) == 0):
            print "ERRO: Nenhuma atividade encontrada com o Requisito: " + num_requisito + " Nome da fase: " + nomeFase + " para o projeto: " + nomeProjeto
            exit()
        return out[0][0]

    # Reinicializando valor da lista todasAtividades.
    @staticmethod
    def AtividadesFromDBdaApliccation():
        Atividade.todasAtividades = list()
        querySelect = ("SELECT * FROM atividades")
        out = Database.get(querySelect)
        for rowInAtividades in out :
            Atividade(rowInAtividades[0], rowInAtividades[1], rowInAtividades[2], rowInAtividades[3], rowInAtividades[4], rowInAtividades[5], rowInAtividades[6])


    def ChangeElementIdAfterInsert(self):
        querySelectSingleElement = "SELECT id_atividade FROM atividades WHERE  fases_id_fase='" + str(self.fases_id_fase) + "'\
                                                              AND projetos_id_projeto='" + str(self.projetos_id_projeto) + "' \
                                                              AND numero_requisito='" + str(self.num_requisito) + "'"

        out = Database.get(querySelectSingleElement)
        Atividade(out[0], self.esforco_est, self.esforco_real, self.responsavel, self.fases_id_fase, self.projetos_id_projeto, self.num_requisito)

    def listIterator (todasAtividades) :
        for atividade in todasAtividades :
            return atividade
