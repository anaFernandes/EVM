# coding=UTF-8

from ValidaData import ValidaData
from Projeto import Projeto
from Fase import Fase
from Atividade import Atividade
from Medidas import Medidas
from LeiaCSV import LeiaCSV
from Calculo import Calculo
from Database import Database
from K_Means import K_Means
from Responsavel import Responsavel
from Classificacao import Classificacao

import numpy as np

#Pega os dados do Banco
out = Database.get("SELECT * FROM atividades")

def PegarDadosDoBanco():
    Atividade.AtividadesFromDBdaApliccation()
    Fase.FasesFromDBToApliccation()
    Projeto.ProjetosFromDBToApliccation()
    Medidas.MedidasFromDBToApliccation()

" Insere no Banco a partir do Arquivo "

def PegarDadosCSVParaBanco():
    " Constroi lista de atividades a partir do CSV "
    #     por enquanto é apenas uma matriz de strings das atividades.
    #     No próximo passo será construída uma lista de objetos "Projetos"
    leitorCsvTmp = LeiaCSV()
    listaAtividadesSemFormatacao = leitorCsvTmp.Leia()

    dataInfo = ValidaData(listaAtividadesSemFormatacao)
    data_inicio, data_fim, duracao= dataInfo.Valida(listaAtividadesSemFormatacao)
    " Cria Objetos e enviar para o banco "
    i=0
    # Lista projetos
    for atividade in listaAtividadesSemFormatacao:
        Projeto(-1, atividade[3], data_inicio[i], data_fim[i], -1, duracao[i], atividade[8], -1)
        i+=1

    # Lista fases
    for atividade in listaAtividadesSemFormatacao:
        Fase(-1, atividade[6], -1,-1, -1, -1, -1, -1, -1, Projeto.getIdByNome(atividade[3]))

    # Lista atividade
    for atividade in listaAtividadesSemFormatacao:
        Atividade(-1, atividade[0], atividade[1], atividade[2], Fase.getIdByNome(atividade[6], atividade[3]),
                  Projeto.getIdByNome(atividade[3]), atividade[7])

" Calcula valores EVM "
def CalculaEVM():
    #Pegar os dados do Banco, a seguir separa-los em pacotes de projetos para poder utiliza-los no calculo
    projetosFromDatabase = list()
    i = 0
    counterAtividades = 0
    id_projeto_anterior = 0

    #Agrupa as atividades dentro de cada projeto
    for atividade in Atividade.todasAtividades :
        row = list()
        if(atividade.projetos_id_projeto != id_projeto_anterior) :
            row.append(atividade)
            id_projeto_anterior = atividade.projetos_id_projeto
            i+=1
            projetosFromDatabase.append(row)
        else :
            projetosFromDatabase[i-1].append(atividade)

    calculoInfo = Calculo(projetosFromDatabase)

    #Para cada projeto dentro de projetosFromDatabase
    for lista_projeto in projetosFromDatabase :

        lista_est, lista_real, lista_id_fase, lista_id_projeto, lista_id_atividades, lista_nome_responsavel = [], [], [], [], [], []

        #enquanto o contator de atividades for menor que a lista de projetos
        #ele adiciona cada coluna de atividades em uma lista
        while(counterAtividades < len(lista_projeto)) :
            lista_est.append(lista_projeto[counterAtividades].esforco_est)
            lista_real.append(lista_projeto[counterAtividades].esforco_real)
            lista_id_fase.append(lista_projeto[counterAtividades].fases_id_fase)
            lista_id_projeto.append(lista_projeto[counterAtividades].projetos_id_projeto)
            lista_id_atividades.append(lista_projeto[counterAtividades].id)
            lista_nome_responsavel.append(lista_projeto[counterAtividades].responsavel)
            counterAtividades+=1
        counterAtividades=0

        """Chamada para os cálculos iniciais"""
        est_acum_p, est_acum_f = calculoInfo.AcumuladoMedidas(lista_est, lista_id_fase)
        real_acum_p, real_acum_f = calculoInfo.AcumuladoMedidas(lista_real, lista_id_fase)
        pv_acum_f = calculoInfo.MultiplicaAcumulado(est_acum_f)
        ev_acum_f = calculoInfo.MultiplicaAcumulado(est_acum_f)
        ac_acum_f = calculoInfo.MultiplicaAcumulado(real_acum_f)
        cpi_trad_f = calculoInfo.CalculaCPITrad(ev_acum_f, ac_acum_f)
        pv_acum_p = calculoInfo.MultiplicaAcumulado(est_acum_p)
        ac_acum_p = calculoInfo.MultiplicaAcumulado(real_acum_p)
        ev_acum_p = calculoInfo.MultiplicaAcumulado(est_acum_p)
        cpi_trad_p = calculoInfo.CalculaCPITrad(ev_acum_p, ac_acum_p)
        id_fases, cpi_hist_f, num_atividades, esforco_est_fase, esforco_real_fase, esforco_real_projeto, esforco_est_projeto = \
            calculoInfo.CalculaCPIHistFase(cpi_trad_f, lista_id_fase, real_acum_f, est_acum_f, est_acum_p, real_acum_p)
        prec_cpi_trad, erro_cpi_trad = calculoInfo.CalculaExatidaoPrecisao(cpi_trad_p, ac_acum_p, pv_acum_p, lista_id_fase)
        prec_cpi_acum_trad = calculoInfo.CalculaPrecisaoAcum(prec_cpi_trad, lista_id_fase)
        erro_cpi_acum_trad = calculoInfo.CalculaExatidaoAcum(erro_cpi_trad)
        eac_trad = calculoInfo.CalculaEAC(cpi_trad_p, pv_acum_p)
        id_projeto, bac, cpi_projeto = calculoInfo.CalculaBAC(pv_acum_p, lista_id_projeto, cpi_trad_p)

        "Chamada para o calculo do perfil de cada responsavel"
        responsavel = Responsavel(projetosFromDatabase)
        lista_perfil_responsavel = responsavel.Calcula_Perfil_Responsavel(lista_nome_responsavel)
        lista_perfil_equipe_fases = responsavel.Calcula_Perfil_Equipe(lista_perfil_responsavel, lista_id_fase)
        lista_perfil_equipe_projeto = responsavel.Calcula_Perfil_Equipe(lista_perfil_responsavel, lista_id_projeto)

        "Update em fase e projeto"
        i=0
        for id_fase in id_fases:
            Fase.UpdateFase(id_fase, cpi_hist_f[i], esforco_real_fase[i], num_atividades[i], lista_perfil_equipe_fases[i],
                            esforco_est_fase[i], esforco_real_projeto[i], esforco_est_projeto[i])
            for fase in Fase.todas_fases:
                if fase.id == id_fase :
                    fase.cpi_hist = cpi_hist_f[i]
                    fase.esforco_real_fase = esforco_real_fase[i]
                    fase.num_atividades = num_atividades[i]
                    fase.esforco_estimado_fase = esforco_est_fase[i]
                    fase.esforco_real_projeto = esforco_real_projeto[i]
                    fase.esforco_estimado_projeto = esforco_est_projeto[i]
                    fase.perfil_equipe = lista_perfil_equipe_fases[i]
            i+=1

        Projeto.UpdateProjeto(id_projeto, bac, cpi_projeto)
        for projeto in Projeto.todos_projetos:
            if(projeto.id == id_projeto):
                projeto.bac = bac
                projeto.cpi_projeto = cpi_projeto

        "Insere em atividades"
        i=0
        for idAtividade in lista_id_atividades:
            if(type(idAtividade) is tuple) :
                Medidas(-1, est_acum_f[i], real_acum_f[i], pv_acum_f[i], ev_acum_f[i], cpi_trad_f[i], ac_acum_f[i], est_acum_p[i], real_acum_p[i], ev_acum_p[i],
                        pv_acum_p[i], ac_acum_p[i], cpi_trad_p[i], -1, -1, eac_trad[i], -1, -1, erro_cpi_trad[i], -1, erro_cpi_acum_trad[i],
                        -1, prec_cpi_trad[i], -1, prec_cpi_acum_trad[i], -1, lista_id_projeto[i], lista_id_fase[i], idAtividade[0], lista_perfil_responsavel[i])
            if(type(idAtividade) is long) :
                Medidas(-1, est_acum_f[i], real_acum_f[i], pv_acum_f[i], ev_acum_f[i], cpi_trad_f[i], ac_acum_f[i], est_acum_p[i], real_acum_p[i],ev_acum_p[i],
                        pv_acum_p[i], ac_acum_p[i], cpi_trad_p[i], -1, -1, eac_trad[i], -1, -1, erro_cpi_trad[i], -1,erro_cpi_acum_trad[i],
                        -1, prec_cpi_trad[i], -1, prec_cpi_acum_trad[i], -1, lista_id_projeto[i], lista_id_fase[i], idAtividade, lista_perfil_responsavel[i])
            i+=1

        #Pega os dados do banco para calcular o CPI histórico médio de cada fase
        # Reseta os valores inicias do projeto não inserido no banco
        contador_fases = [0, 0, 0, 0]
        cpi_fases_soma = [0, 0, 0, 0]

        i = 0
        # print ("*********************** INTERACAO ******************************* \n\n\n")
        #Percorrer todos os projetos
        for projeto in Projeto.todos_projetos :
            #Percorrer projetos com o id menor do que o projeto atual
            while(Fase.todas_fases[i].projetos_id_projeto < id_projeto) :
                #Soma os elementos de cada fase
                if Fase.todas_fases[i].nome !=0 :
                    if Fase.todas_fases[i].nome == "elaboracao" :
                        #Soma os valores da fase ao cpiFasesSum.
                        cpi_fases_soma[0] = cpi_fases_soma[0] + Fase.todas_fases[i].cpi_hist
                        contador_fases[0] = contador_fases[0] + 1
                    elif Fase.todas_fases[i].nome == "implementacao" :
                        # Soma os valores da fase ao cpiFasesSum.
                        cpi_fases_soma[1] = cpi_fases_soma[1] + Fase.todas_fases[i].cpi_hist
                        contador_fases[1] = contador_fases[1] + 1
                    elif (Fase.todas_fases[i].nome == "testes" ) :
                        # Soma os valores da fase ao cpiFasesSum.
                        cpi_fases_soma[2] = cpi_fases_soma[2] + Fase.todas_fases[i].cpi_hist
                        contador_fases[2] = contador_fases[2] + 1
                    elif (Fase.todas_fases[i].nome == "correcao" ):
                        # Soma os valores da fase ao cpiFasesSum.
                        # print ("CPI FASES SUM : " + str(cpiFasesSum[3]) + " \n FASES CPI HIST : " + str(Fase.todas_fases[i].cpi_hist))
                        # print Fase.todas_fases[i].projetos_id_projeto
                        cpi_fases_soma[3] = cpi_fases_soma[3] + Fase.todas_fases[i].cpi_hist
                        contador_fases[3] = contador_fases[3] + 1
                    i += 1

        #Separar Médias
        if (contador_fases[0] !=0):
            cpi_medio = [ cpi_fases_soma[0] / contador_fases[0],
                          cpi_fases_soma[1] / contador_fases[1],
                          cpi_fases_soma[2] / contador_fases[2],
                          cpi_fases_soma[3] / contador_fases[3],
                        ]

        i=0
        if (id_projeto != 1):
            cpi_hist_acum = calculoInfo.CalculaCPI(pv_acum_f, lista_id_fase, cpi_medio, ev_acum_f, ac_acum_p, ac_acum_f, ev_acum_p)
            cpi_hist_est = calculoInfo.CalculaCPIEst(cpi_medio, pv_acum_f, cpi_trad_f, ac_acum_p, pv_acum_p, lista_id_fase)
            prec_cpi_hist, erro_cpi_hist = calculoInfo.CalculaExatidaoPrecisao(cpi_hist_est, ac_acum_p, pv_acum_p, lista_id_fase)
            prec_cpi_acum_hist = calculoInfo.CalculaPrecisaoAcum(prec_cpi_hist, lista_id_fase)
            erro_cpi_acum_hist = calculoInfo.CalculaExatidaoAcum(erro_cpi_hist)
            eac_hist = calculoInfo.CalculaEAC(cpi_hist_est, pv_acum_p)

            i=0
            for idAtividade in lista_id_atividades:
                Medidas.UpdateMedidas(cpi_hist_acum[i], prec_cpi_hist[i], erro_cpi_hist[i], prec_cpi_acum_hist[i], erro_cpi_acum_hist[i], eac_hist[i], idAtividade)
                i+=1

        if(id_projeto > 13):
            i=0
            lista_duracao, lista_cpi_projeto, lista_nome_fase, lista_cpi_fase, lista_id_projeto_fase, lista_real_acum_fase, \
            lista_est_acum_projeto, lista_real_acum_projeto, lista_est_acum_fase, lista_perfil_equipe_fase, lista_num_atividades, \
            lista_data_inicio_projeto, lista_data_fim_projeto = [], [], [], [], [], [], [], [], [], [], [], [], []

            for fase in Fase.todas_fases:
                j = 0
                if (id_projeto > Fase.todas_fases[i].projetos_id_projeto):
                    if (Fase.todas_fases[i].cpi_hist < 6):
                        if (Fase.todas_fases[i].cpi_hist != 0):
                            for projeto in Projeto.todos_projetos:
                                if (projeto.id == Fase.todas_fases[i].projetos_id_projeto):
                                    lista_duracao.append(Projeto.todos_projetos[j].duracao)
                                    lista_cpi_projeto.append(Projeto.todos_projetos[j].cpi_projeto)
                                    lista_data_inicio_projeto.append(Projeto.todos_projetos[j].dt_inicio)
                                    lista_data_fim_projeto.append(Projeto.todos_projetos[j].dt_fim)
                                j += 1
                            lista_nome_fase.append(Fase.todas_fases[i].nome)
                            lista_cpi_fase.append(Fase.todas_fases[i].cpi_hist)
                            lista_id_projeto_fase.append(Fase.todas_fases[i].projetos_id_projeto)
                            lista_real_acum_fase.append(Fase.todas_fases[i].esforco_real_fase)
                            lista_est_acum_fase.append(Fase.todas_fases[i].esforco_estimado_fase)
                            lista_real_acum_projeto.append(Fase.todas_fases[i].esforco_real_projeto)
                            lista_est_acum_projeto.append(Fase.todas_fases[i].esforco_estimado_projeto)
                            lista_perfil_equipe_fase.append(Fase.todas_fases[i].perfil_equipe)
                            lista_num_atividades.append(Fase.todas_fases[i].num_atividades)
                i += 1

            fases_cluster= np.array(zip(lista_duracao, lista_nome_fase, lista_cpi_fase, lista_id_projeto_fase,
                                        lista_real_acum_fase, lista_est_acum_fase, lista_est_acum_projeto, lista_real_acum_projeto,
                                        lista_perfil_equipe_fase, lista_num_atividades, lista_cpi_projeto, lista_data_inicio_projeto,
                                        lista_data_fim_projeto))
            Agrupamento = K_Means(Fase.todas_fases)
            implementacao, teste, elaboracao, correcao = Agrupamento.SeparaFases(fases_cluster)
            dados_projeto = Agrupamento.JuntaFases(fases_cluster, lista_id_projeto_fase)

            Classificacao = Classificacao(Fase.todas_fases)
            implementacao, teste, elaboracao, correcao = Classificacao.SeparaFases(fases_cluster, lista_id_projeto_fase)
            dados_projeto = Classificacao.JuntaFases(fases_cluster, lista_id_projeto_fase)

            # lista_cluster_teste = Agrupamento.Kmeans(teste)
            # lista_cluster_implementacao = Agrupamento.Kmeans(implementacao)
            # lista_cluster_correcao = Agrupamento.Kmeans(correcao)
            # lista_cluster_elaboracao = Agrupamento.Kmeans(elaboracao)
            # lista_cluster_projeto = Agrupamento.Kmeans_projeto(dados_projeto)

            # lista_classificador_projeto = Agrupamento.DecisionTree(dados_projeto)

            # media_clusters_teste_0, media_clusters_teste_1, media_clusters_teste_2, media_clusters_teste_3 = Agrupamento.Media_Clusters(cluster_teste_0, cluster_teste_1, cluster_teste_2, cluster_teste_3)
            # media_clusters_implementacao_0, media_clusters_implementacao_1 = Agrupamento.Media_Clusters(cluster_implementacao_0, cluster_implementacao_1)
            # media_clusters_correcao_0, media_clusters_correcao_1 = Agrupamento.Media_Clusters(cluster_correcao_0, cluster_correcao_1)
            # media_clusters_elaboracao_0, media_clusters_elaboracao_0 = Agrupamento.Media_Clusters(cluster_elaboracao_0, cluster_elaboracao_1)
            # mediana_clusters_teste_0, moda_clusters_teste_0 = Agrupamento.Mediana_Clusters(cluster_teste_0, cluster_teste_1)
            # mediana_clusters_implementacao_0, moda_clusters_implementacao_1 = Agrupamento.Mediana_Clusters(cluster_implementacao_0, cluster_implementacao_1)
            # mediana_clusters_correcao_0, moda_clusters_correcao_1 = Agrupamento.Mediana_Clusters(cluster_correcao_0, cluster_correcao_1)
            # mediana_clusters_elaboracao_0, moda_clusters_elaboracao_0 = Agrupamento.Mediana_Clusters(cluster_elaboracao_0, cluster_elaboracao_1)

def start():
    PegarDadosDoBanco()
    PegarDadosCSVParaBanco()
    CalculaEVM()
    exit()

start()