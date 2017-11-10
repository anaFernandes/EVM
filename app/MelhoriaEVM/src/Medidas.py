# -*- coding: utf-8 -*-
"""
Created on Wed Aug 03 18:16:09 2016

@author: Ana
"""
import MySQLdb


from Database import Database

class Medidas(object):
    todasMedidas = list()
    
    #Construtor
    def __init__(self, id, esforco_est_acum_fase, esforco_real_acum_fase, pv_acum_fase, ev_acum_fase,
                 cpi_acum_fase, ac_acum_fase, esforco_est_acum_projeto, esforco_real_acum_projeto, ev_acum_projeto,
                 pv_acum_projeto, ac_acum_projeto, cpi_acum_projeto_tec_trad, cpi_acum_projeto_tec_dados_hist,
                 cpi_acum_projeto_outras_tec, eac_tec_trad, eac_dados_hist, eac_outras_tec, 
                 exatidao_tec_trad, exatidao_tec_dados_hist, exatidao_outras_tec, exatidao_acum_tec_trad, exatidao_acum_tec_dados_hist,
                 exatidao_acum_outras_tec, precisao_tec_trad, precisao_tec_dados_hist, precisao_outras_tec, precisao_acum_tec_trad,
                 precisao_acum_tec_dados_hist, precisao_acum_outras_tec, projetos_id_projeto, fases_id_fase, atividades_id_atividade,
                 perfil_responsavel, cpi_acum_projeto_randomT, eac_tec_randomT, precisao_tec_randomT, precisao_acum_tec_randomT,
                 exatidao_tec_randomT, exatidao_acum_tec_randomT) :

        jaExite = False
        for medida in Medidas.todasMedidas:
            if (medida.atividades_id_atividade == atividades_id_atividade):
                if (medida.id == -1):
                    medida.id = id
                jaExite = True


        if (jaExite == False):
            self.id = id
            self.esforco_est_acum_fase = esforco_est_acum_fase
            self.esforco_real_acum_fase = esforco_real_acum_fase
            self.pv_acum_fase = pv_acum_fase
            self.ev_acum_fase = ev_acum_fase
            self.cpi_acum_fase = cpi_acum_fase
            self.ac_acum_fase = ac_acum_fase
            self.esforco_est_acum_projeto = esforco_est_acum_projeto
            self.esforco_real_acum_projeto = esforco_real_acum_projeto
            self.ev_acum_projeto = ev_acum_projeto
            self.pv_acum_projeto = pv_acum_projeto
            self.ac_acum_projeto = ac_acum_projeto
            self.cpi_acum_projeto_tec_trad = cpi_acum_projeto_tec_trad
            self.cpi_acum_projeto_tec_dados_hist = cpi_acum_projeto_tec_dados_hist
            self.cpi_acum_projeto_outras_tec = cpi_acum_projeto_outras_tec
            self.eac_tec_trad = eac_tec_trad
            self.eac_dados_hist = eac_dados_hist
            self.eac_outras_tec = eac_outras_tec
            self.exatidao_tec_trad = exatidao_tec_trad
            self.exatidao_tec_dados_hist = exatidao_tec_dados_hist
            self.exatidao_outras_tec = exatidao_outras_tec
            self.exatidao_acum_tec_trad = exatidao_acum_tec_trad
            self.exatidao_acum_tec_dados_hist = exatidao_acum_tec_dados_hist
            self.exatidao_acum_outras_tec = exatidao_acum_outras_tec
            self.precisao_tec_trad = precisao_tec_trad
            self.precisao_tec_dados_hist = precisao_tec_dados_hist
            self.precisao_outras_tec = precisao_outras_tec
            self.precisao_acum_tec_trad = precisao_acum_tec_trad
            self.precisao_acum_tec_dados_hist = precisao_acum_tec_dados_hist
            self.precisao_acum_outras_tec = precisao_acum_outras_tec
            self.projetos_id_projeto = projetos_id_projeto
            self.fases_id_fase = fases_id_fase
            self.atividades_id_atividade = atividades_id_atividade
            self.perfil_responsavel = perfil_responsavel
            self.cpi_acum_projeto_randomT = cpi_acum_projeto_randomT
            self.eac_tec_randomT = eac_tec_randomT
            self.precisao_tec_randomT = precisao_tec_randomT
            self.precisao_acum_tec_randomT = precisao_acum_tec_randomT
            self.exatidao_tec_randomT = exatidao_tec_randomT
            self.exatidao_acum_tec_randomT = exatidao_acum_tec_randomT
            Medidas.todasMedidas.append(self)
            if (id == -1):
                Medidas.fileToDataBase(self)

    def fileToDataBase(self):
        queryInsert = ("INSERT INTO medidas (esforco_est_acum_fase, esforco_real_acum_fase, pv_acum_fase, ev_acum_fase, cpi_acum_fase, "
                       "ac_acum_fase, esforco_est_acum_projeto, esforco_real_acum_projeto, ev_acum_projeto, pv_acum_projeto, ac_acum_projeto,"
                       "cpi_acum_projeto_tec_trad, eac_tec_trad, exatidao_tec_trad, exatidao_acum_tec_trad, precisao_tec_trad,"
                       "precisao_acum_tec_trad, projetos_id_projeto, fases_id_fase, atividades_id_atividade, perfil_responsavel, "
                       "precisao_outras_tec, exatidao_outras_tec, precisao_acum_outras_tec, exatidao_acum_outras_tec, cpi_acum_projeto_randomT, eac_tec_randomT, precisao_tec_randomT, precisao_acum_tec_randomT, exatidao_tec_randomT, exatidao_acum_tec_randomT) VALUES  "
                       "('"+str(self.esforco_est_acum_fase)+"','"+str(self.esforco_real_acum_fase)+"','"+str(self.pv_acum_fase)+"','"+str(self.ev_acum_fase)+
                       "','"+str(self.cpi_acum_fase)+"','"+str(self.ac_acum_fase)+"','"+str(self.esforco_est_acum_projeto)+"','"+str(self.esforco_real_acum_projeto)+
                       "','"+str(self.ev_acum_projeto)+"','"+str(self.pv_acum_projeto)+"','"+str(self.ac_acum_projeto)+
                       "','"+str(self.cpi_acum_projeto_tec_trad)+"','" +str(self.eac_tec_trad)+"','"+str(self.exatidao_tec_trad)+
                       "','"+str(self.exatidao_acum_tec_trad)+"','"+str(self.precisao_tec_trad)+"','"+str(self.precisao_acum_tec_trad)+
                       "','"+str(self.projetos_id_projeto)+"','"+str(self.fases_id_fase)+"','"+str(self.atividades_id_atividade)+ "','"+str(self.perfil_responsavel)+
                       "','"+str(self.exatidao_outras_tec)+ "','"+str(self.precisao_outras_tec)+ "','"+str(self.precisao_acum_outras_tec)+
                       "','" + str(self.exatidao_acum_outras_tec) + "','" + str(self.cpi_acum_projeto_randomT) + "','" + str(self.eac_tec_randomT) +
                       "','" + str(self.exatidao_tec_randomT) + "','" + str(self.exatidao_acum_tec_randomT) + "','" + str(self.precisao_tec_randomT) +
                       "','"+str(self.precisao_acum_tec_randomT)+"')")
        out = Database.insert(queryInsert)
        Database.con.commit()
        #Alterar id elemento inserido no banco
        Medidas.ChangeElementIdAfterInsert(self)

    def ChangeElementIdAfterInsert(self):
        querySelectSingleElement = "SELECT id_medida FROM medidas WHERE atividades_id_atividade='" + str(self.atividades_id_atividade)+ "'"
        out = Database.get(querySelectSingleElement)
        Medidas(out[0], self.esforco_est_acum_fase, self.esforco_real_acum_fase, self.pv_acum_fase, self.ev_acum_fase, self.cpi_acum_fase, self.ac_acum_fase,
                     self.esforco_est_acum_projeto, self.esforco_real_acum_projeto, self.ev_acum_projeto, self.pv_acum_projeto, self.ac_acum_projeto,
                     self.cpi_acum_projeto_tec_trad, self.cpi_acum_projeto_tec_dados_hist, self.cpi_acum_projeto_outras_tec, self.eac_tec_trad,
                      self.eac_dados_hist, self.eac_outras_tec, self.exatidao_tec_trad,self.exatidao_outras_tec, self.exatidao_tec_dados_hist, self.exatidao_acum_tec_trad,
                      self.exatidao_acum_tec_dados_hist, self.exatidao_acum_outras_tec, self.precisao_tec_trad, self.precisao_tec_dados_hist, self.precisao_acum_outras_tec, self.precisao_acum_tec_trad,
                      self.precisao_acum_tec_dados_hist, self.precisao_acum_outras_tec, self.projetos_id_projeto, self.fases_id_fase, self.atividades_id_atividade, self.perfil_responsavel,
                      self.cpi_acum_projeto_randomT, self.eac_tec_randomT, self.precisao_tec_randomT, self.precisao_acum_tec_randomT, self.exatidao_tec_randomT, self.exatidao_acum_tec_randomT
                )

    @staticmethod
    def MedidasFromDBToApliccation():
        Medidas.todasMedidas = list()
        querySelect = ("SELECT * FROM medidas")
        out = Database.get(querySelect)

        for rowInMedidas in out:
            Medidas(rowInMedidas[0], rowInMedidas[1], rowInMedidas[2], rowInMedidas[3], rowInMedidas[4], rowInMedidas[5],
                    rowInMedidas[6], rowInMedidas[7], rowInMedidas[8], rowInMedidas[9], rowInMedidas[10], rowInMedidas[11],
                    rowInMedidas[12], rowInMedidas[13], rowInMedidas[14], rowInMedidas[15], rowInMedidas[16], rowInMedidas[17],
                    rowInMedidas[18], rowInMedidas[19], rowInMedidas[20], rowInMedidas[21], rowInMedidas[22], rowInMedidas[23],
                    rowInMedidas[24], rowInMedidas[25], rowInMedidas[26], rowInMedidas[27], rowInMedidas[28], rowInMedidas[29],
                    rowInMedidas[30], rowInMedidas[31], rowInMedidas[32], rowInMedidas[33], rowInMedidas[34], rowInMedidas[35],
                    rowInMedidas[36], rowInMedidas[37], rowInMedidas[38], rowInMedidas[39])

    def listIterator(todasMedidas):
        for medidas in todasMedidas:
            return medidas

    @staticmethod
    def UpdateMedidas(cpiHistAcum, precCPIhist, erroCPIHist, precCPIAcumHist, erroCPIAcumHist, eacHist, idAtividade):
        queryUpdate = "UPDATE medidas SET cpi_acum_projeto_tec_dados_hist='" + str(cpiHistAcum) + \
                      "',precisao_tec_dados_hist='" + str(precCPIhist) + "',exatidao_tec_dados_hist='" + str(erroCPIHist) + \
                      "',precisao_acum_tec_dados_hist='" + str(precCPIAcumHist) + "',exatidao_acum_tec_dados_hist='" \
                      + str(erroCPIAcumHist) + "',eac_tec_dados_hist='" + str(eacHist) + \
                      "'WHERE atividades_id_atividade='" + str(idAtividade) + "'"

    # @staticmethod
    # def UpdateMedidasClassificacao(cpi_hist_acum_class, eac_hist_class, idAtividade):
    #     queryUpdate = "UPDATE medidas SET cpi_acum_projeto_outras_tec='" + str(cpi_hist_acum_class) + \
    #                    "',eac_outras_tec='" + str(eac_hist_class) + \
    #                   "'WHERE atividades_id_atividade='" + str(idAtividade) + "'"
    #     out = Database.update(queryUpdate)

    @staticmethod
    def UpdateMedidasClassificacao(cpi_hist_acum_class, prec_cpi_hist_class, erro_cpi_hist_class, prec_cpi_acum_hist_class,
                                      erro_cpi_acum_hist_class, eac_hist_class, idAtividade, cpi_acum_projeto_randomT,
        precisao_tec_randomT, exatidao_tec_randomT, precisao_acum_tec_randomT, exatidao_acum_tec_randomT, eac_tec_randomT):
        queryUpdate = "UPDATE medidas SET cpi_acum_projeto_outras_tec='" + str(cpi_hist_acum_class) + \
                      "',precisao_outras_tec='" + str(prec_cpi_hist_class) + "',exatidao_outras_tec='" + str(erro_cpi_hist_class) + \
                      "',precisao_acum_outras_tec='" + str(prec_cpi_acum_hist_class) + "',exatidao_acum_outras_tec='" \
                      + str(erro_cpi_acum_hist_class) + "',eac_outras_tec='" + str(eac_hist_class) + \
                      "',cpi_acum_projeto_randomT='" + str(cpi_acum_projeto_randomT) + "',precisao_tec_randomT='" + str(precisao_tec_randomT) + \
                      "',exatidao_tec_randomT='" + str(exatidao_tec_randomT) + "',precisao_acum_tec_randomT='" + str(precisao_acum_tec_randomT) + \
                      "',exatidao_acum_tec_randomT='" + str(exatidao_acum_tec_randomT) + "',eac_tec_randomT='" + str(eac_tec_randomT) + \
                      "'WHERE atividades_id_atividade='" + str(idAtividade) + "'"
        out = Database.update(queryUpdate)