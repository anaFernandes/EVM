# coding=UTF-8
from Calculo_Porcentagem import Calculo_Porcentagem
from ValidaData import ValidaData
from Projeto import Projeto
from Fase import Fase
from Atividade import Atividade
from Medidas import Medidas
from Medidas_Porcentagem import Medidas_Porcentagem
from LeiaCSV import LeiaCSV
from Calculo import Calculo
from Database import Database
from Responsavel import Responsavel
from Classificacao import Classificacao
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from multiprocessing import Pool
import time
# import logging
# logger = multiprocessing.log_to_stderr()
# logger.setLevel(multiprocessing.SUBDEBUG)

def calculoEVM(arg_list):
    # arg_list.append(['fase', lista_est, lista_id_fase, lista_real])
    i = 0
    somaFaseEstimado = 0
    somaFaseReal = 0
    somaProjetoReal = 0
    somaProjetoEstimado = 0
    acumReal, acumEstimado = list(), list()
    faseAnterior = arg_list[2][0]
    projetoAnterior = arg_list[4][0]
    fase = 'fase'
    projeto = 'projeto'
    for valor in arg_list[1]:
        if (arg_list[2][i] != faseAnterior):
            somaFaseEstimado, somaFaseReal, faseAnterior = 0, 0, 0
        if (arg_list[4][i] != projetoAnterior):
            somaFaseReal, somaFaseEstimado, somaProjetoEstimado, somaProjetoReal = 0, 0, 0, 0
        if (arg_list[0] == fase):
            tip = 'fase'
            somaFaseEstimado += valor
            acumEstimado.append(float(somaFaseEstimado))
            somaFaseReal += arg_list[3][i]
            acumReal.append(float(somaFaseReal))
        elif (arg_list[0] == projeto):
            somaProjetoEstimado += valor
            acumEstimado.append(float(somaProjetoEstimado))
            somaProjetoReal += arg_list[3][i]
            acumReal.append(float(somaProjetoReal))
            tip = 'projeto'
        if i < 10 and arg_list[4][i] == 1:
            print "fase est", somaFaseEstimado
            print "projeto real", somaProjetoReal
            print "fase real", somaFaseReal
            print "projeto est", somaProjetoEstimado

    i=0
    pvAcum, evAcum, acAcum, cpiTrad = list(), list(), list(), list()
    for medida in acumEstimado:
        pvAcum.append(medida * 100)
        evAcum.append(medida * 100)
        acAcum.append(acumReal[i] * 100)
        i+=1

    i = 0
    for medida in evAcum:
        if (acAcum[i] > 0):
            cpi= medida/acAcum[i]
        else:
            cpi = 0
        i+=1
        cpiTrad.append(cpi)
    return [tip, acumEstimado, acumReal, pvAcum, evAcum, acAcum, cpiTrad]

def CalculaAcum(arg_list):
    i = 0
    somaFase = 0
    somaProjeto = 0
    acum = list()
    faseAnterior = arg_list[2][0]
    projetoAnterior = arg_list[3][0]
    estimadoFase = 'estimadoFase'
    estimadoProjeto = 'estimadoProjeto'
    realFase = 'realFase'
    realProjeto = 'realProjeto'
    for valor in arg_list[1]:
        if (arg_list[3][i] != projetoAnterior):
            somaProjeto = 0
            somaFase = 0
            projetoAnterior = arg_list[3][i]
        if (arg_list[0] == estimadoFase):
            tip = 'estimadoFase'
            somaFase += valor
            acum.append(float(somaFase))
            faseAnterior = arg_list[2][i]
        elif (arg_list[0] == realFase):
            tip = 'realFase'
            somaFase += valor
            acum.append(float(somaFase))
            faseAnterior = arg_list[2][i]
        elif (arg_list[0] == estimadoProjeto):
            somaProjeto += valor
            acum.append(float(somaProjeto))
            tip = 'estimadoProjeto'
        elif (arg_list[0] == realProjeto):
            somaProjeto += valor
            acum.append(float(somaProjeto))
            tip = 'realProjeto'
        if (arg_list[2][i] != faseAnterior):
            somaFase = 0
            faseAnterior = arg_list[2][i]
        i += 1

    return [tip, acum]

def MultiplicaAcumulado(arg_listAcum):
    pvAcumFase = 'pvAcumFase'
    evAcumFase = 'evAcumFase'
    acAcumFase = 'acAcumFase'
    acAcumProjeto = 'acAcumProjeto'
    pvAcumProjeto = 'pvAcumProjeto'
    evAcumProjeto = 'evAcumProjeto'
    if (arg_listAcum[0] == pvAcumFase):
        tip = 'pvAcumFase'
    elif (arg_listAcum[0] == evAcumFase):
        tip = 'evAcumFase'
    elif (arg_listAcum[0] == acAcumFase):
        tip = 'acAcumFase'
    elif (arg_listAcum[0] == acAcumProjeto):
        tip = 'acAcumProjeto'
    elif (arg_listAcum[0] == pvAcumProjeto):
        tip = 'pvAcumProjeto'
    elif (arg_listAcum[0] == evAcumProjeto):
        tip = 'evAcumProjeto'
    # pvAcumF = map(lambda x: x * 100, valores)
    acumuladoMultiplicado = list()
    for medida in arg_listAcum[1]:
        acumuladoMultiplicado.append((medida * 100))
    return [tip, acumuladoMultiplicado]

# Calcula os CPIs tradicionais dos projetos, dividindo o PV acumulado pelo EV acumulado
def CalculaCPITrad (argList):
    argCpiTradFase = 'cpiTradFase'
    if (argList[0] == argCpiTradFase):
        tip = 'cpiTradFase'
    else:
        tip = 'cpiTradProjeto'
    #cpiTrad = map(truediv, pvAcum, evAcum)
    cpiTrad= list()
    i=0
    for medida in argList[1]:
        if (argList[2][i] > 0):
            cpi= medida/argList[2][i]
        else:
            cpi = 0
        i+=1
        cpiTrad.append(cpi)
    return [tip, cpiTrad]

#Pega os dados do Banco
out = Database.get("SELECT * FROM atividades")

def PegarDadosDoBanco():
    Atividade.AtividadesFromDBdaApliccation()
    Fase.FasesFromDBToApliccation()
    Projeto.ProjetosFromDBToApliccation()
    Medidas.MedidasFromDBToApliccation()
    Medidas_Porcentagem.MedidasPorcentagemFromDBToApliccation()

" Insere no Banco a partir do Arquivo "

def PegarDadosCSVParaBanco():
    " Constroi lista de atividades a partir do CSV "
    #     por enquanto é apenas uma matriz de strings das atividades.
    #     No próximo passo será construída uma lista de objetos "Projetos"
    leitorCsvTmp = LeiaCSV()
    listaAtividadesSemFormatacao, hash_file_exists = leitorCsvTmp.Leia()

    # dataInfo = ValidaData(listaAtividadesSemFormatacao)
    # data_inicio, data_fim, duracao= dataInfo.Valida(listaAtividadesSemFormatacao)

    " Cria Objetos e enviar para o banco "
    if(not hash_file_exists):
        i=0
        # Lista projetos
        for atividade in listaAtividadesSemFormatacao:
            Projeto(-1, atividade[3], 1, 1, -1, 1, atividade[8], -1)
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
    #Pegar os dados do Banco,
    projetosFromDatabase = list()
    i = 0
    counterAtividades = 0
    id_projeto_anterior = 0

    esforco_est, esforco_real, fases_id_fase, projetos_id_projeto = list(), list(), list(), list()

    for atividade in Atividade.todasAtividades:
        esforco_est.append(atividade.esforco_est)
        esforco_real.append(atividade.esforco_real)
        fases_id_fase.append(atividade.projetos_id_projeto)
        projetos_id_projeto.append(atividade.projetos_id_projeto)

    """1 Thread"""
    ini = time.time()
    # p = Pool(processes=2)
    # arg_list = []
    # arg_list.append(['fase', esforco_est, fases_id_fase, esforco_real, projetos_id_projeto])
    # arg_list.append(['projeto', esforco_est, fases_id_fase, esforco_real, projetos_id_projeto])
    # result = p.map(calculoEVM, arg_list)

    # tip, acumEstimado, acumReal, pvAcum, evAcum, acAcum, cpiTrad
    # est_acum_fase = result[0][1]
    # real_acum_fase = result[0][2]
    # pv_acum_fase = result[0][3]
    # ev_acum_fase = result[0][4]
    # ac_acum_fase = result[0][5]
    # cpi_trad_fase = result[0][6]
    # est_acum_projeto = result[1][1]
    # real_acum_projeto = result[1][2]
    # pv_acum_projeto = result[1][3]
    # ev_acum_projeto = result[1][4]
    # ac_acum_projeto = result[1][5]
    # cpi_trad_projeto = result[1][6]

    # for est in est_acum_projeto:
    #     print "projeto", est
    #     print "fase", est_acum_fase[i]


    fim = time.time()
    print fim - ini

    # "2 Threads"
    # ini = time.time()
    # p = Pool()
    # arg_list_fase = []
    # arg_list_fase.append(['fase', esforco_est, fases_id_fase, esforco_real, projetos_id_projeto])
    # result = p.map(calculoEVM, arg_list_fase)
    # # tip, acumEstimado, acumReal, pvAcum, evAcum, acAcum, cpiTrad
    # est_acum_fase = result[0][1]
    # real_acum_fase = result[0][2]
    # pv_acum_fase = result[0][3]
    # ev_acum_fase = result[0][4]
    # ac_acum_fase = result[0][5]
    # cpi_trad_fase = result[0][6]
    #
    # p = Pool()
    # arg_list_projeto = []
    # arg_list_projeto.append(['projeto', esforco_est, fases_id_fase, esforco_real,projetos_id_projeto])
    # result = p.map(calculoEVM, arg_list_projeto)
    # # tip, acumEstimado, acumReal, pvAcum, evAcum, acAcum, cpiTrad
    # est_acum_projeto = result[0][1]
    # real_acum_projeto = result[0][2]
    # pv_acum_projeto = result[0][3]
    # ev_acum_projeto = result[0][4]
    # ac_acum_projeto = result[0][5]
    # cpi_trad_projeto = result[0][6]
    # fim = time.time()
    # print "2 threads", fim - ini

    # "4 Threads"
    ini = time.time()
    p = Pool(processes=4)
    arg_list_acum = []
    arg_list_acum.append(['estimadoProjeto', esforco_est, fases_id_fase, projetos_id_projeto])
    arg_list_acum.append(['realProjeto', esforco_real, fases_id_fase, projetos_id_projeto])
    arg_list_acum.append(['estimadoFase', esforco_est, fases_id_fase, projetos_id_projeto])
    arg_list_acum.append(['realFase', esforco_est, fases_id_fase, projetos_id_projeto])
    result = p.map(CalculaAcum, arg_list_acum)

    est_acum_projeto = result[0][1]
    real_acum_projeto = result[1][1]
    est_acum_fase = result[2][1]
    real_acum_fase = result[3][1]

    processoEVPVAV = Pool(processes=6)
    arg_listEVPVAC = []
    arg_listEVPVAC.append(['evAcumFase', est_acum_fase])
    arg_listEVPVAC.append(['evAcumProjeto', est_acum_projeto])
    arg_listEVPVAC.append(['acAcumFase', real_acum_fase])
    arg_listEVPVAC.append(['acAcumProjeto', real_acum_projeto])
    arg_listEVPVAC.append(['pvAcumFase', est_acum_fase])
    arg_listEVPVAC.append(['pvAcumProjeto', est_acum_projeto])
    resultEV_PV_AC = processoEVPVAV.map(MultiplicaAcumulado, arg_listEVPVAC)

    ev_acum_fase = resultEV_PV_AC[0][1]
    ev_acum_projeto = resultEV_PV_AC[1][1]
    pv_acum_fase = resultEV_PV_AC[2][1]
    pv_acum_projeto = resultEV_PV_AC[3][1]
    ac_acum_fase = resultEV_PV_AC[4][1]
    ac_acum_projeto = resultEV_PV_AC[5][1]

    processoCalculaCPITrad = Pool(processes=2)
    arg_listFase = []
    arg_listFase.append(['CPIFase', ev_acum_fase, ac_acum_fase])
    arg_listFase.append(['CPIProjeto', ev_acum_projeto, ac_acum_projeto])
    resultCalculaCPITrad = processoCalculaCPITrad.map(CalculaCPITrad, arg_listFase)

    cpi_trad_fase = resultCalculaCPITrad[0][1]
    cpi_trad_projeto = resultCalculaCPITrad[1][1]
    fim = time.time()
    print "tempo 4 threads", fim - ini
    # exit(1)

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
        est_acum_f, est_acum_p, real_acum_f, real_acum_p, pv_acum_p, pv_acum_f, ev_acum_p, ev_acum_f, \
        ac_acum_p, ac_acum_f, cpi_trad_p, cpi_trad_f = [], [], [], [], [], [], [], [], [], [], [], []
        #enquanto o contator de atividades for menor que a lista de projetos
        #ele adiciona cada coluna de atividades em uma lista
        while(counterAtividades < len(lista_projeto)) :
            lista_est.append(lista_projeto[counterAtividades].esforco_est)
            lista_real.append(lista_projeto[counterAtividades].esforco_real)
            lista_id_fase.append(lista_projeto[counterAtividades].fases_id_fase)
            lista_id_projeto.append(lista_projeto[counterAtividades].projetos_id_projeto)
            lista_id_atividades.append(lista_projeto[counterAtividades].id)
            lista_nome_responsavel.append(lista_projeto[counterAtividades].responsavel)

            "Add Threads"
            est_acum_f.append(est_acum_fase[counterAtividades])
            est_acum_p.append(est_acum_projeto[counterAtividades])
            real_acum_f.append(real_acum_fase[counterAtividades])
            real_acum_p.append(real_acum_projeto[counterAtividades])
            pv_acum_p.append(pv_acum_projeto[counterAtividades])
            ev_acum_p.append(ev_acum_projeto[counterAtividades])
            ac_acum_p.append(ac_acum_projeto[counterAtividades])
            pv_acum_f.append(pv_acum_fase[counterAtividades])
            ev_acum_f.append(ev_acum_fase[counterAtividades])
            ac_acum_f.append(ac_acum_fase[counterAtividades])
            cpi_trad_f.append(cpi_trad_fase[counterAtividades])
            cpi_trad_p.append(cpi_trad_projeto[counterAtividades])

            counterAtividades+=1
        counterAtividades=0

    #     """Chamada para os cálculos iniciais"""
    #     ini = time.time()
    #     est_acum_p, est_acum_f = calculoInfo.AcumuladoMedidas(lista_est, lista_id_fase)
    #     real_acum_p, real_acum_f = calculoInfo.AcumuladoMedidas(lista_real, lista_id_fase)
    #     pv_acum_f = calculoInfo.MultiplicaAcumulado(est_acum_f)
    #     ev_acum_f = calculoInfo.MultiplicaAcumulado(est_acum_f)
    #     ac_acum_f = calculoInfo.MultiplicaAcumulado(real_acum_f)
    #     pv_acum_p = calculoInfo.MultiplicaAcumulado(est_acum_p)
    #     ac_acum_p = calculoInfo.MultiplicaAcumulado(real_acum_p)
    #     ev_acum_p = calculoInfo.MultiplicaAcumulado(est_acum_p)
    #     cpi_trad_f = calculoInfo.CalculaCPITrad(ev_acum_f, ac_acum_f)
    #     cpi_trad_p = calculoInfo.CalculaCPITrad(ev_acum_p, ac_acum_p)
    #     fim = time.time()
    #     print " calculos ", ini - fim
    #
        id_fases, cpi_hist_f, num_atividades, esforco_est_fase, esforco_real_fase, esforco_real_projeto, esforco_est_projeto = \
            calculoInfo.CalculaCPIHistFase(cpi_trad_f, lista_id_fase, real_acum_f, est_acum_f, est_acum_p, real_acum_p)
        prec_cpi_trad, erro_cpi_trad = calculoInfo.CalculaExatidaoPrecisao(cpi_trad_p, ac_acum_p, pv_acum_p, lista_id_fase)
        prec_cpi_acum_trad = calculoInfo.CalculaPrecisaoAcum(prec_cpi_trad, lista_id_fase)
        erro_cpi_acum_trad = calculoInfo.CalculaExatidaoAcum(erro_cpi_trad)
        eac_trad = calculoInfo.CalculaEAC(cpi_trad_p, pv_acum_p)
        id_projeto, bac, cpi_projeto = calculoInfo.CalculaBAC(pv_acum_p, lista_id_projeto, cpi_trad_p)

        "Chamada para o calculo do perfil de cada responsavel"
        # responsavel = Responsavel(projetosFromDatabase)
        # lista_perfil_responsavel = responsavel.Calcula_Perfil_Responsavel(lista_nome_responsavel)
        # lista_perfil_equipe_fases = responsavel.Calcula_Perfil_Equipe(lista_perfil_responsavel, lista_id_fase)
        # lista_perfil_equipe_projeto = responsavel.Calcula_Perfil_Equipe(lista_perfil_responsavel, lista_id_projeto)

        "Update em fase e projeto"
        i=0
        for id_fase in id_fases:
            Fase.UpdateFase(id_fase, cpi_hist_f[i], esforco_real_fase[i], num_atividades[i], 1,
                            esforco_est_fase[i], esforco_real_projeto[i], esforco_est_projeto[i])
            for fase in Fase.todas_fases:
                if fase.id == id_fase :
                    fase.cpi_hist = cpi_hist_f[i]
                    fase.esforco_real_fase = esforco_real_fase[i]
                    fase.num_atividades = num_atividades[i]
                    fase.esforco_estimado_fase = esforco_est_fase[i]
                    fase.esforco_real_projeto = esforco_real_projeto[i]
                    fase.esforco_estimado_projeto = esforco_est_projeto[i]
                    fase.perfil_equipe = 1
            i+=1

        for projeto in Projeto.todos_projetos:
            if(projeto.id == id_projeto):
                projeto.bac = Projeto.UpdateProjeto(id_projeto, bac, cpi_projeto)
                projeto.cpi_projeto = cpi_projeto

        "Insere em medidas"
        i=0

        for idAtividade in lista_id_atividades:
            # if(type(idAtividade) is tuple) :
            Medidas(-1, est_acum_f[i], real_acum_f[i], pv_acum_f[i], ev_acum_f[i], cpi_trad_f[i], ac_acum_f[i], est_acum_p[i],
                    real_acum_p[i], ev_acum_p[i], pv_acum_p[i], ac_acum_p[i], cpi_trad_p[i], -1, -1, eac_trad[i], -1, -1, erro_cpi_trad[i], -1,
                    -1, erro_cpi_acum_trad[i], -1, -1, prec_cpi_trad[i], -1, -1, prec_cpi_acum_trad[i], -1, -1, lista_id_projeto[i], lista_id_fase[i],
                    idAtividade, 1, -1, -1, -1, -1, -1, -1)
            if(type(idAtividade) is long) :
                Medidas(-1, est_acum_f[i], real_acum_f[i], pv_acum_f[i], ev_acum_f[i], cpi_trad_f[i], ac_acum_f[i], est_acum_p[i],
                        real_acum_p[i], ev_acum_p[i], pv_acum_p[i], ac_acum_p[i], cpi_trad_p[i], -1, -1, eac_trad[i], -1, -1, erro_cpi_trad[i], -1,
                        -1, erro_cpi_acum_trad[i], -1, -1, prec_cpi_trad[i], -1, -1, prec_cpi_acum_trad[i], -1, -1, lista_id_projeto[i], lista_id_fase[i],
                        idAtividade, 1, -1, -1, -1, -1, -1, -1)
            i+=1

        #Pega os dados do banco para calcular o CPI histórico médio de cada fase
        # Reseta os valores inicias do projeto não inserido no banco
        cpi_medio = [0, 0, 0, 0]
        contador_fases = [0, 0, 0, 0]

        i = 0
        # print ("*********************** INTERACAO ******************************* \n\n\n")
        #Percorrer todos os projetos
        for projeto in Projeto.todos_projetos :
            #Percorrer projetos com o id menor do que o projeto atual
            while(Fase.todas_fases[i].projetos_id_projeto < id_projeto) :
                #Soma os elementos de cada fase
                if Fase.todas_fases[i].nome !=0 :
                    if(fase.todas_fases[i].cpi_hist !=-1):
                        # if(fase.todas_fases[i].cpi_hist < 5):
                        if Fase.todas_fases[i].nome == "elaboracao" :
                            #Soma os valores da fase ao cpiFasesSum.
                            cpi_medio[0] = cpi_medio[0] + Fase.todas_fases[i].cpi_hist
                            contador_fases[0] = contador_fases[0] + 1
                        elif Fase.todas_fases[i].nome == "implementacao" :
                            # Soma os valores da fase ao cpiFasesSum.
                            cpi_medio[1] = cpi_medio[1] + Fase.todas_fases[i].cpi_hist
                            contador_fases[1] = contador_fases[1] + 1
                        elif Fase.todas_fases[i].nome == "teste" :
                            # Soma os valores da fase ao cpiFasesSum.
                            cpi_medio[2] = cpi_medio[2] + Fase.todas_fases[i].cpi_hist
                            contador_fases[2] = contador_fases[2] + 1
                        elif Fase.todas_fases[i].nome == "correcao" :
                            # Soma os valores da fase ao cpi_fases_sum.
                            # print ("CPI FASES SUM : " + str(cpi_medio[3]) + " \n FASES CPI HIST : " + str(Fase.todas_fases[i].cpi_hist))
                            # print Fase.todas_fases[i].projetos_id_projeto
                            cpi_medio[3] = cpi_medio[3] + Fase.todas_fases[i].cpi_hist
                            contador_fases[3] = contador_fases[3] + 1
                i += 1

        #Separar Médias
        if(id_projeto != 1):
            if (contador_fases[0] != 0 or contador_fases[1] != 0 or contador_fases[2] != 0 or contador_fases[3] != 0):
                cpi_medio = [ cpi_medio[0] / contador_fases[0],
                              cpi_medio[1] / contador_fases[1],
                              cpi_medio[2] / contador_fases[2],
                              cpi_medio[3] / contador_fases[3],
                            ]
                # print "cpi_medio" + str(cpi_medio)
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


        if(id_projeto > 7):
            Classification = Classificacao(Fase.todas_fases, Projeto.todos_projetos)

            # lista_id_projetos_selecionados = Classification.Separa_Pela_Data(id_projeto)

            lista_id_projetos_selecionados = Classification.SeparaProjetos(id_projeto)
            fases_selecionadas = Classification.Seleciona_Fases(lista_id_projetos_selecionados)

            implementacao, teste, elaboracao, correcao = Classification.SeparaFases(fases_selecionadas, lista_id_projetos_selecionados)
            lista_projetos_treinados, projeto_atual = Classification.JuntaFases(fases_selecionadas, lista_id_projetos_selecionados, id_projeto)
            class1, class2, class3, class4, class5, class6, class7, class_treinada = Classification.DefineClass(lista_projetos_treinados)
            # print class_treinada

            modelo = MultinomialNB()

            modelo.fit(lista_projetos_treinados, class_treinada)
            class_prevista = modelo.predict(projeto_atual)

            clf = svm.SVR()
            clf.fit(lista_projetos_treinados, class_treinada)
            class_prevista_svm = clf.predict(projeto_atual)
            # print class_prevista
            # print class_prevista_svm

            lista_id_projetos_CPI = Classification.comparaClasse(class_prevista,class1, class2, class3, class4, class5, class6, class7)
            cpi_medio_classificado = Classification.CalculaMediaCPI(lista_id_projetos_CPI, id_projeto)
            cpi_hist_acum_class = calculoInfo.CalculaCPI(pv_acum_f, lista_id_fase, cpi_medio_classificado, ev_acum_f, ac_acum_p, ac_acum_f, ev_acum_p)
            cpi_hist_est_class = calculoInfo.CalculaCPIEst(cpi_medio_classificado, pv_acum_f, cpi_trad_f, ac_acum_p, pv_acum_p, lista_id_fase)
            prec_cpi_hist_class, erro_cpi_hist_class = calculoInfo.CalculaExatidaoPrecisao(cpi_hist_est_class, ac_acum_p, pv_acum_p, lista_id_fase)
            prec_cpi_acum_hist_class = calculoInfo.CalculaPrecisaoAcum(prec_cpi_hist_class, lista_id_fase)
            erro_cpi_acum_hist_class = calculoInfo.CalculaExatidaoAcum(erro_cpi_hist_class)
            eac_hist_class = calculoInfo.CalculaEAC(cpi_hist_est_class, pv_acum_p)

            lista_id_projetos_CPI_svm = Classification.comparaClasse(class_prevista_svm, class1, class2, class3, class4, class5, class6, class7)
            cpi_medio_classificado_svm = Classification.CalculaMediaCPI(lista_id_projetos_CPI_svm, id_projeto)
            cpi_hist_acum_class_svm = calculoInfo.CalculaCPI(pv_acum_f, lista_id_fase, cpi_medio_classificado_svm, ev_acum_f, ac_acum_p, ac_acum_f, ev_acum_p)
            cpi_hist_est_class_svm = calculoInfo.CalculaCPIEst(cpi_medio_classificado_svm, pv_acum_f, cpi_trad_f, ac_acum_p, pv_acum_p, lista_id_fase)
            prec_cpi_hist_class_svm, erro_cpi_hist_class_svm = calculoInfo.CalculaExatidaoPrecisao(cpi_hist_est_class_svm, ac_acum_p, pv_acum_p, lista_id_fase)
            prec_cpi_acum_hist_class_svm = calculoInfo.CalculaPrecisaoAcum(prec_cpi_hist_class_svm, lista_id_fase)
            erro_cpi_acum_hist_class_svm = calculoInfo.CalculaExatidaoAcum(erro_cpi_hist_class)
            eac_hist_class_svm = calculoInfo.CalculaEAC(cpi_hist_est_class_svm, pv_acum_p)

            i = 0
            for idAtividade in lista_id_atividades:
                Medidas.UpdateMedidasClassificacao(cpi_hist_acum_class[i], prec_cpi_hist_class[i], erro_cpi_hist_class[i],
                                                   prec_cpi_acum_hist_class[i], erro_cpi_acum_hist_class[i], eac_hist_class[i], idAtividade,
                                                   cpi_hist_acum_class_svm[i], prec_cpi_hist_class_svm[i], erro_cpi_hist_class_svm[i],
                                                   prec_cpi_acum_hist_class_svm[i], erro_cpi_acum_hist_class_svm[i], eac_hist_class_svm[i]                                                   )
                i += 1

            Calculo_info_porcentagem = Calculo_Porcentagem(projetosFromDatabase)

            # executado_precisao_trad_25, executado_precisao_trad_50, executado_precisao_trad_75, executado_precisao_trad_100 = Calculo_info_porcentagem.Calcula_Medidas_Porcentagem(prec_cpi_acum_trad, est_acum_p)
            # executado_exatidao_trad_25, executado_exatidao_trad_50, executado_exatidao_trad_75, executado_exatidao_trad_100 = Calculo_info_porcentagem.Calcula_Medidas_Porcentagem(erro_cpi_acum_trad, est_acum_p)
            # executado_precisao_hist_25, executado_precisao_hist_50, executado_precisao_hist_75, executado_precisao_hist_100 = Calculo_info_porcentagem.Calcula_Medidas_Porcentagem(prec_cpi_acum_hist, est_acum_p)
            # executado_exatidao_hist_25, executado_exatidao_hist_50, executado_exatidao_hist_75, executado_exatidao_hist_100 = Calculo_info_porcentagem.Calcula_Medidas_Porcentagem(erro_cpi_acum_hist, est_acum_p)
            # executado_precisao_class_25, executado_precisao_class_50, executado_precisao_class_75, executado_precisao_class_100 = Calculo_info_porcentagem.Calcula_Medidas_Porcentagem(prec_cpi_acum_hist_class, est_acum_p)
            # executado_exatidao_class_25, executado_exatidao_class_50, executado_exatidao_class_75, executado_exatidao_class_100 = Calculo_info_porcentagem.Calcula_Medidas_Porcentagem(erro_cpi_acum_hist_class, est_acum_p)

            # print "Erro Trad: " + str(erro_cpi_trad[len(erro_cpi_trad) - 1]) + "Projeto: " + str(id_projeto)
            # print "Erro Hist: " + str(erro_cpi_hist_class[len(erro_cpi_hist_class) - 1])


            # Medidas_Porcentagem(-1, executado_precisao_trad_25, executado_precisao_trad_50, executado_precisao_trad_75, executado_precisao_trad_100,
            #      executado_exatidao_trad_25, executado_exatidao_trad_50, executado_exatidao_trad_75, executado_exatidao_trad_100,
            #      executado_precisao_hist_25, executado_precisao_hist_50, executado_precisao_hist_75, executado_precisao_hist_100,
            #      executado_exatidao_hist_25, executado_exatidao_hist_50, executado_exatidao_hist_75, executado_exatidao_hist_100,
            #      executado_precisao_class_25, executado_precisao_class_50, executado_precisao_class_75, executado_precisao_class_100,
            #      executado_exatidao_class_25, executado_exatidao_class_50, executado_exatidao_class_75, executado_exatidao_class_100,
            #      id_projeto)
            #
            # i = 0
            # for idAtividade in lista_id_atividades:
            #     Medidas.UpdateMedidas(cpi_hist_acum_class[i], prec_cpi_hist_class[i], erro_cpi_hist_class[i], prec_cpi_acum_hist_class[i],
            #                           erro_cpi_acum_hist_class[i], eac_hist_class[i], idAtividade)
            #     i += 1

            # fases_cluster= np.array(zip(lista_duracao, lista_nome_fase, lista_cpi_fase, lista_id_projeto_fase,
            #                              lista_real_acum_fase, lista_est_acum_fase, lista_est_acum_projeto, lista_real_acum_projeto,
            #                             lista_perfil_equipe_fase, lista_num_atividades, lista_cpi_projeto, lista_data_inicio_projeto,
            #                             lista_data_fim_projeto))
            # Agrupamento = K_Means(Fase.todas_fases)
            # implementacao, teste, elaboracao, correcao = Agrupamento.SeparaFases(fases_cluster)
            # dados_projeto = Agrupamento.JuntaFases(fases_cluster, lista_id_projeto_fase)
            #
            # lista_cluster_teste = Agrupamento.Kmeans(teste)
            # lista_cluster_implementacao = Agrupamento.Kmeans(implementacao)
            # lista_cluster_correcao = Agrupamento.Kmeans(correcao)
            # lista_cluster_elaboracao = Agrupamento.Kmeans(elaboracao)
            # lista_cluster_projeto = Agrupamento.Kmeans_projeto(dados_projeto)
            #
            # lista_classificador_projeto = Agrupamento.DecisionTree(dados_projeto)
            #
            # media_clusters_teste_0, media_clusters_teste_1, media_clusters_teste_2, media_clusters_teste_3 = Agrupamento.Media_Clusters(cluster_teste_0, cluster_teste_1, cluster_teste_2, cluster_teste_3)
            # media_clusters_implementacao_0, media_clusters_implementacao_1 = Agrupamento.Media_Clusters(cluster_implementacao_0, cluster_implementacao_1)
            # media_clusters_correcao_0, media_clusters_correcao_1 = Agrupamento.Media_Clusters(cluster_correcao_0, cluster_correcao_1)
            # media_clusters_elaboracao_0, media_clusters_elaboracao_0 = Agrupamento.Media_Clusters(cluster_elaboracao_0, cluster_elaboracao_1)
            # mediana_clusters_teste_0, moda_clusters_teste_0 = Agrupamento.Mediana_Clusters(cluster_teste_0, cluster_teste_1)
            # mediana_clusters_implementacao_0, moda_clusters_implementacao_1 = Agrupamento.Mediana_Clusters(cluster_implementacao_0, cluster_implementacao_1)
            # mediana_clusters_correcao_0, moda_clusters_correcao_1 = Agrupamento.Mediana_Clusters(cluster_correcao_0, cluster_correcao_1)
            # mediana_clusters_elaboracao_0, moda_clusters_elaboracao_0 = Agrupamento.Mediana_Clusters(cluster_elaboracao_0, cluster_elaboracao_1)

#
def start():
    ini = time.time()
    PegarDadosDoBanco()
    fim = time.time()
    print "Função DadosdoBando: ", fim - ini
    ini = time.time()
    PegarDadosCSVParaBanco()
    fim = time.time()
    print "Função CSV: ", fim - ini
    ini = time.time()
    CalculaEVM()
    fim = time.time()
    print "Função CalculaEVM: ", fim - ini
    exit()

start()
