# -*- coding: utf-8 -*-
from Projeto import Projeto
from Database import Database

class Medidas_Porcentagem():
    todas_medidas_porcentagem = list()

    #Construtor
    def __init__(self, id, executado_precisao_trad_25, executado_precisao_trad_50, executado_precisao_trad_75, executado_precisao_trad_100,
                 executado_exatidao_trad_25, executado_exatidao_trad_50, executado_exatidao_trad_75, executado_exatidao_trad_100,
                 executado_precisao_hist_25, executado_precisao_hist_50, executado_precisao_hist_75, executado_precisao_hist_100,
                 executado_exatidao_hist_25, executado_exatidao_hist_50, executado_exatidao_hist_75, executado_exatidao_hist_100,
                 executado_precisao_class_25, executado_precisao_class_50, executado_precisao_class_75, executado_precisao_class_100,
                 executado_exatidao_class_25, executado_exatidao_class_50, executado_exatidao_class_75, executado_exatidao_class_100,
                 projetos_id_projeto):
        jaExite = False
        #Compara o nome da fase e o nome do projeto
        #Caso já exista retorna a variável True
        for medidas_porcentagem in Medidas_Porcentagem.todas_medidas_porcentagem:
            if(medidas_porcentagem.projetos_id_projeto == projetos_id_projeto):
                if(medidas_porcentagem.id == -1) :
                    medidas_porcentagem.id = id
                jaExite = True

        #Caso contrário e a função que chama a criação do objeto não for um select do banco, é adicionada uma nova fase no banco e na lista de fases
        if (jaExite==False):
            self.id = id
            self.executado_precisao_trad_25 = executado_precisao_trad_25
            self.executado_precisao_trad_50 = executado_precisao_trad_50
            self.executado_precisao_trad_75 = executado_precisao_trad_75
            self.executado_precisao_trad_100 = executado_precisao_trad_100
            self.executado_exatidao_trad_25 = executado_exatidao_trad_25
            self.executado_exatidao_trad_50 = executado_exatidao_trad_50
            self.executado_exatidao_trad_75 = executado_exatidao_trad_75
            self.executado_exatidao_trad_100 = executado_exatidao_trad_100
            self.executado_precisao_hist_25 = executado_precisao_hist_25
            self.executado_precisao_hist_50 = executado_precisao_hist_50
            self.executado_precisao_hist_75 = executado_precisao_hist_75
            self.executado_precisao_hist_100 = executado_precisao_hist_100
            self.executado_exatidao_hist_25 = executado_exatidao_hist_25
            self.executado_exatidao_hist_50 = executado_exatidao_hist_50
            self.executado_exatidao_hist_75 = executado_exatidao_hist_75
            self.executado_exatidao_hist_100 = executado_exatidao_hist_100
            self.executado_precisao_class_25 = executado_precisao_class_25
            self.executado_precisao_class_50 = executado_precisao_class_50
            self.executado_precisao_class_75 = executado_precisao_class_75
            self.executado_precisao_class_100 = executado_precisao_class_100
            self.executado_exatidao_class_25 = executado_exatidao_class_25
            self.executado_exatidao_class_50 = executado_exatidao_class_50
            self.executado_exatidao_class_75 = executado_exatidao_class_75
            self.executado_exatidao_class_100 = executado_exatidao_class_100
            self.projetos_id_projeto = projetos_id_projeto
            Medidas_Porcentagem.todas_medidas_porcentagem.append(self)
            if(id == -1) :
                Medidas_Porcentagem.fileToDatabase(self)

    #Insere o arquivo na
    def fileToDatabase(self):
        queryInsert = ("INSERT INTO medidas_porcentagem (executado_precisao_trad_25, executado_precisao_trad_50, executado_precisao_trad_75, executado_precisao_trad_100,"
                       "executado_exatidao_trad_25, executado_exatidao_trad_50, executado_exatidao_trad_75, executado_exatidao_trad_100,"
                       "executado_precisao_hist_25, executado_precisao_hist_50, executado_precisao_hist_75, executado_precisao_hist_100,"
                        "executado_exatidao_hist_25, executado_exatidao_hist_50, executado_exatidao_hist_75, executado_exatidao_hist_100,"
                        "executado_precisao_class_25, executado_precisao_class_50, executado_precisao_class_75, executado_precisao_class_100,"
                        "executado_exatidao_class_25, executado_exatidao_class_50, executado_exatidao_class_75, executado_exatidao_class_100, projetos_id_projeto) VALUES "
                       "('"+str(self.executado_precisao_trad_25)+"','"+str(self.executado_precisao_trad_50)+"','"+str(self.executado_precisao_trad_75)+"','"+str(self.executado_precisao_trad_100)+
                       "','"+str(self.executado_exatidao_trad_25)+"','"+str(self.executado_exatidao_trad_50)+ "','"+str(self.executado_exatidao_trad_75)+"','"+str(self.executado_exatidao_trad_100)+
                       "','"+str(self.executado_precisao_hist_25)+"','"+str(self.executado_precisao_hist_50)+"','"+str(self.executado_precisao_hist_75)+"','"+str(self.executado_precisao_hist_100)+
                       "','"+str(self.executado_exatidao_hist_25)+"','"+str(self.executado_exatidao_hist_50)+"','"+str(self.executado_exatidao_hist_75)+"','"+str(self.executado_exatidao_hist_100)+
                       "','"+str(self.executado_precisao_class_25)+"','"+str(self.executado_precisao_class_50)+"','"+str(self.executado_precisao_class_75)+"','"+str(self.executado_precisao_class_100) +
                       "','"+str(self.executado_exatidao_class_25)+"','"+str(self.executado_exatidao_class_50)+"','"+str(self.executado_exatidao_class_75)+"','"+str(self.executado_exatidao_class_100)+
                       "','"+str(self.projetos_id_projeto)+"')")
        out = Database.insert(queryInsert)
        Database.con.commit()
        #Alterar id elemento inserido no banco
        Medidas_Porcentagem.ChangeElementIdAfterInsert(self)


    def ChangeElementIdAfterInsert(self):
        querySelectSingleElement = "SELECT id_medidas_porcentagem FROM medidas_porcentagem WHERE projetos_id_projeto='" + str(self.projetos_id_projeto) + "'"
        out = Database.get(querySelectSingleElement)
        Medidas_Porcentagem(out[0], self.executado_precisao_trad_25, self.executado_precisao_trad_50, self.executado_precisao_trad_75, self.executado_precisao_trad_100,
                 self.executado_exatidao_trad_25, self.executado_exatidao_trad_50, self.executado_exatidao_trad_75, self.executado_exatidao_trad_100,
                 self.executado_precisao_hist_25, self.executado_precisao_hist_50, self.executado_precisao_hist_75, self.executado_precisao_hist_100,
                 self.executado_exatidao_hist_25, self.executado_exatidao_hist_50, self.executado_exatidao_hist_75, self.executado_exatidao_hist_100,
                 self.executado_precisao_class_25, self.executado_precisao_class_50, self.executado_precisao_class_75, self.executado_precisao_class_100,
                 self.executado_exatidao_class_25, self.executado_exatidao_class_50, self.executado_exatidao_class_75, self.executado_exatidao_class_100, self.projetos_id_projeto)


    #Reinicializando valor da lista todas_fases, para ela ser utilizada no cálculo do CPI Histórico médio
    @staticmethod
    def MedidasPorcentagemFromDBToApliccation():
        querySelect = ("SELECT * FROM medidas_porcentagem")
        out = Database.get(querySelect)
        for rowInMedidasPorcentagen in out:
            Medidas_Porcentagem(rowInMedidasPorcentagen[0], rowInMedidasPorcentagen[1], rowInMedidasPorcentagen[2],
                                rowInMedidasPorcentagen[3], rowInMedidasPorcentagen[4], rowInMedidasPorcentagen[5],
                                rowInMedidasPorcentagen[6], rowInMedidasPorcentagen[7], rowInMedidasPorcentagen[8],
                                rowInMedidasPorcentagen[9], rowInMedidasPorcentagen[10], rowInMedidasPorcentagen[11],
                                rowInMedidasPorcentagen[12], rowInMedidasPorcentagen[13], rowInMedidasPorcentagen[14],
                                rowInMedidasPorcentagen[15], rowInMedidasPorcentagen[16], rowInMedidasPorcentagen[17],
                                rowInMedidasPorcentagen[18], rowInMedidasPorcentagen[19], rowInMedidasPorcentagen[20],
                                rowInMedidasPorcentagen[21], rowInMedidasPorcentagen[22], rowInMedidasPorcentagen[23],
                                rowInMedidasPorcentagen[24], rowInMedidasPorcentagen[25]
            )


    def listIterator (todas_medidas_porcentagem) :
        for medida_porcentagem in todas_medidas_porcentagem :
            return medida_porcentagem
