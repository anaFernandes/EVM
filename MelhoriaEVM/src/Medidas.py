# -*- coding: utf-8 -*-
"""
Created on Wed Aug 03 18:16:09 2016

@author: Ana
"""
import MySQLdb


from Database import Database

class Medidas(object):
    
    #Construtor
    def __init__(self, id, esforco_est_acum_fase, esforco_real_acum_fase, 
                 pv_acum_fase, ev_acum_fase, cpi_acum_fase, esforco_est_acum_projeto, 
                 esforco_real_acum_projeto, ev_acum_projeto, pv_acum_projeto,
                 ac_acum_projeto, cpi_acum_projeto_tec_trad, cpi_acum_projeto_tec_dados_hist,
                 cpi_acum_projeto_outras_tec, eac_tec_trad, eac_dados_hist, eac_outras_tec, 
                 exatidao_tec_trad, exatidao_tec_dados_hist, exatidao_acum_tec_trad, exatidao_acum_tec_dados_hist,
                 precisao_tec_trad, precisao_tec_dados_hist,precisao_acum_tec_trad, precisao_acum_tec_dados_hist,
                 projetos_id_projeto,fases_id_fase,atividades_id_atividade):
        
        self.id = id
        self.esforco_est_acum_fase = esforco_est_acum_fase
        self.esforco_real_acum_fase = esforco_real_acum_fase
        self.pv_acum_fase = pv_acum_fase
        self.ev_acum_fase = ev_acum_fase
        self.cpi_acum_fase = cpi_acum_fase
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
        self.exatidao_acum_tec_trad = exatidao_acum_tec_trad
        self.exatidao_acum_tec_dados_hist = exatidao_acum_tec_dados_hist
        self.precisao_tec_trad = precisao_tec_trad
        self.precisao_tec_dados_hist = precisao_tec_dados_hist
        self.precisao_acum_tec_trad = precisao_acum_tec_trad
        self.precisao_acum_tec_dados_hist = precisao_acum_tec_dados_hist
        self.projetos_id_projeto = projetos_id_projeto
        self.atividades_id_atividade = atividades_id_atividade
        self.fases_id_fase = fases_id_fase

        self.fileToDataBase()


    def fileToDataBase(self):
        i=0
        while(i < len(self.esforco_est_acum_fase)) :
            queryInsert = ("INSERT INTO medidas (esforco_est_acm_fase, esforco_real_acm_fase, pv_acum_fase, ev_acum_fase"
                           ",projetos_id_projeto, fases_id_fase, atividades_id_atividade) VALUES "
                           "('" + str(self.esforco_est_acum_fase[i]) + "','" + str(self.esforco_real_acum_fase[i]) + "','" +
                           str(self.pv_acum_fase[i]) + "','" + str(self.ev_acum_fase[i]) + "','" +str(self.projetos_id_projeto)+
                           "','" + str(self.fases_id_fase[i]) + "','" + str(self.atividades_id_atividade[i]) + "')")
            print queryInsert
            out = Database.insert(queryInsert)
            Database.con.commit()
            i+=1


    def add(self):
        MedidasTable = [(self.id, self.esforco_est_acum_fase, self.esforco_real_acum_fase, self.pv_acum_fase, self.ev_acum_fase, self.cpi_acum_fase,
                     self.esforco_est_acum_projeto, self.esforco_real_acum_projeto, self.ev_acum_projeto, self.pv_acum_projeto, self.ac_acum_projeto,
                     self.cpi_acum_projeto_tec_trad, self.cpi_acum_projeto_tec_dados_hist, self.cpi_acum_projeto_outras_tec, self.eac_tec_trad,
                      self.eac_dados_hist, self.eac_outras_tec, self.exatidao_tec_trad, self.exatidao_tec_dados_hist, self.exatidao_acum_tec_trad,
                      self.exatidao_acum_tec_dados_hist, self.precisao_tec_trad, self.precisao_tec_dados_hist, self.precisao_acum_tec_trad,
                      self.precisao_acum_tec_dados_hist)]

        con = MySQLdb.connect(host='localhost', user='root', passwd='', db='gva')
        con = MySQLdb.connect(user='root', db='gva')
        c = con.cursor()
        print MedidasTable

        out = c.executemany("INSERT INTO fases (nome, cpi_hist, projetos_id_projeto) VALUES (%s, %s)", MedidasTable)
        con.commit()



