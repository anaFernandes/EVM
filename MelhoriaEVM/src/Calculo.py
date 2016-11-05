# coding=UTF-8

#from operator import truediv
import math

class Calculo(object):

    def __init__(self, projetosFromDatabase):
        self.projetosFromDatabase = projetosFromDatabase

    # Adiciona o valor acumulado em cada elemento de Medidas de acordo com a fase ou o projeto.
    #Para calcular acumulado de cada atividade do projeto, o valor anterior é somado ao atual,
    #Para calcular o valor acum de cada atividade da fase, o id da fase é comparada caso o id seja seja diferente o
    # valor acumulado recebe zero e a soma começa novamente.
    def AcumuladoMedidas(self, valores, idFase):
        i = 0
        somaProjeto =0
        SomaFase=0
        AcumProjeto = list()
        AcumFase = list()
        faseAnterior = idFase
        for valor in valores:
            somaProjeto += valor
            AcumProjeto.append(float(somaProjeto))
            if (idFase[i] != faseAnterior):
                estSumFase = 0
            estSumFase += valor
            AcumFase.append(float(estSumFase))
            faseAnterior = idFase[i]
            i += 1
        return AcumProjeto, AcumFase

    # Multiplica os valores acumulados de cada atividade por 100
    def MultiplicaAcumulado (self, valores):
        #pvAcumF = map(lambda x: x * 100, valores)
        acumuladoMultiplicado = list()
        for medida in valores:
            acumuladoMultiplicado.append((medida*100))
        return acumuladoMultiplicado

    # Calcula os CPIs tradicionais dos projetos, dividindo o PV acumulado pelo EV acumulado
    def CalculaCPITrad (self, pvAcum, evAcum ):
        #cpiTrad = map(truediv, pvAcum, evAcum)
        cpiTrad= list()
        i=0
        for medida in pvAcum:
            if (evAcum[i] > 0):
                cpi= medida/evAcum[i]
            else:
                cpi = 0
            i+=1
            cpiTrad.append(cpi)
        return cpiTrad

    def CalculaCPIHistFase(self, lista_cpi_acum_f, lista_id_fase, real_acum_fase, est_acum_fase, est_acum_projeto, real_acum_projeto):

        fase_anterior = lista_id_fase[0]
        lista_cpi_hist_fase, lista_id_fase_unica, lista_real_acum_fase, num_atividade, lista_est_acum_fase= [], [], [], [], []
        lista_real_acum_projeto, lista_est_acum_projeto = [], []
        i = 0

        for cpi_acum_f in lista_cpi_acum_f:
            if(lista_id_fase[i] != fase_anterior):
                lista_cpi_hist_fase.append(lista_cpi_acum_f[i-1])
                lista_id_fase_unica.append(lista_id_fase[i-1])
                lista_real_acum_fase.append(real_acum_fase[i-1])
                lista_est_acum_fase.append(est_acum_fase[i-1])
                lista_real_acum_projeto.append(real_acum_projeto[i-1])
                lista_est_acum_projeto.append(est_acum_projeto[i-1])
            fase_anterior = lista_id_fase[i]
            i += 1
        lista_id_fase_unica.append(lista_id_fase[len(lista_id_fase)-1])
        lista_cpi_hist_fase.append(lista_cpi_acum_f[len(lista_cpi_acum_f)-1])
        lista_real_acum_fase.append(real_acum_fase[len(real_acum_fase)-1])
        lista_est_acum_fase.append(est_acum_fase[len(est_acum_fase)-1])
        lista_real_acum_projeto.append(real_acum_projeto[len(real_acum_fase)-1])
        lista_est_acum_projeto.append(est_acum_projeto[len(est_acum_projeto)-1])

        for id_fase_unica in lista_id_fase_unica:
            contadorfase = 0
            for id_fase in lista_id_fase:
                if id_fase == id_fase_unica:
                    contadorfase += 1
            num_atividade.append(contadorfase)

        return lista_id_fase_unica, lista_cpi_hist_fase, num_atividade, lista_est_acum_fase, lista_real_acum_fase, \
               lista_real_acum_projeto, lista_est_acum_projeto


        # print ("\n ***************************************** \n ")
        # print ("CPI HISTÓRICO FASE > " + str(cpiHistF))
        # print ("\n PV ACUMULADO FASE > " + str(pvAcumF))
        # print ("\n CPI TRADICIONAL FASE > " + str(cpiTradF))
        # print ("\n AC ACUMULADO DO PROJETO > " + str(acAcumP))
        # print ("\n ID LISTA FASE > " + str(listaIdFase))
        # print ("\n ***************************************** \n ")

    "CPI Histórico"
    # Nesta função para cada pv acumulado da fase onde a fase anterior é diferente da fase atual e a fase
    def CalculaCPIEst(self, lista_cpi_hist_fase, lista_pv_acum_fase, lista_cpi_trad_fase, lista_ac_acum_projeto,
                      lista_pv_acum_projeto, lista_id_fase):

        lista_fase_unica, lista_cpi_part, lista_pv_total_fase, lista_cip_hist_unico, lista_cpi_est_hist  = [], [], [], [], []
        j, i=0, 0
        fase_anterior = lista_id_fase[0]
        for id_fase in lista_id_fase:
            if (fase_anterior != id_fase):
                pv_div_des_hist = lista_pv_acum_fase[j] / lista_cpi_hist_fase[i]
                lista_cpi_part.append(pv_div_des_hist)
                lista_pv_total_fase.append(lista_pv_acum_fase[j])
                lista_cip_hist_unico.append(lista_cpi_trad_fase[j])
                lista_fase_unica.append(id_fase)
                i+=1
            fase_anterior = id_fase
            j += 1

        lista_pv_total_fase.append(lista_pv_acum_fase[len(lista_pv_acum_fase)-1])
        pv_div_des_hist = lista_pv_acum_fase[len(lista_pv_acum_fase)-1] / lista_cpi_hist_fase[len(lista_cpi_hist_fase) - 1]
        lista_cpi_part.append(pv_div_des_hist)
        lista_cip_hist_unico.append(lista_cpi_trad_fase[len(lista_cpi_trad_fase)-1])
        lista_fase_unica.append(lista_id_fase[len(lista_id_fase) -1])

        i = 0
        for id_fase in lista_id_fase:
            j = 0
            pv_total_fase_acum = 0
            cpi_div_hist_acum = 0
            for indice_cpi_medio in lista_fase_unica:
                if (id_fase < indice_cpi_medio):
                    pv_total_fase_acum = pv_total_fase_acum + lista_pv_total_fase[j]
                    cpi_div_hist_acum = cpi_div_hist_acum + lista_cpi_part[j]
                j += 1
            cpi_est_hist = (pv_total_fase_acum + lista_pv_acum_projeto[i]) / (lista_ac_acum_projeto[i] + cpi_div_hist_acum)
            print cpi_div_hist_acum
            lista_cpi_est_hist.append(cpi_est_hist)
            i +=1
        exit
        return lista_cpi_est_hist


    "Precisão Exatidao e tradicionais"
    def CalculaExatidaoPrecisao (self, lista_cpi_projeto, ac_acum_projeto, pv_acum_projeto, lista_id_fase):
        erro_CPI, precisao_CPI = [], []
        cpi_anterior = 0
        i=0
        j=0
        #Em cada elemento de cpiTradP
        for cpi in lista_cpi_projeto:
            #cheque se n for maior que zero.
            if cpi > 0:

                # pegue o último elemendo do AC acumulado do projeto e o subtraia por 1, a seguir divida esse
                # elemento pelo último valor do pv acumulado do projeto divido pelo CPI Tradicional do projeto
                erro = 100*(1 - (ac_acum_projeto[len(ac_acum_projeto) - 1] / (pv_acum_projeto[len(pv_acum_projeto) - 1] / cpi)))
            # caso o CPI tradicional seja igual a 0, a variável erro recebe zero
            else:
                erro = 0
            # adiciona a variavel erro no array
            erro_CPI.append(math.fabs(erro))
            i += 1
            # Checa que se a a precisao anterior é igual a zero.
            if(lista_id_fase[j] == lista_id_fase[j-1]):
                if cpi_anterior == 0:
                    precisao = 0
                # Se for igual a zero a variavel precisao recebe 0, caso contrário precisao recebe a divisão do valor atual CPI
                # tradicional acumulado dividido pelo valor anterior do CPI tradicional acumulado
                else:
                    precisao = 100*(1-(cpi_anterior/cpi))
                # O array precCPITrad recebe os valores de precisao
            else:
                precisao = 0
            precisao_CPI.append(math.fabs(precisao))
            cpi_anterior = cpi
            j+=1

        return precisao_CPI, erro_CPI

    "EAC"
    def CalculaEAC(self, listaCpi, pvAcumP):
        eacList = list()
        for cpi in listaCpi:
            # O eacT recebe o útimo valor do Pv acumulado do projeto dividido pelo CPI atual
            if (cpi != 0):
                eac = pvAcumP[len(pvAcumP) - 1] / cpi
            else:
                eac = 0
            # O array eacTrad recebe o eacT
            eacList.append(eac)
        return eacList

    "Precisão Acum"
    def CalculaPrecisaoAcum(self, precCPI, listaIdFase):
        precCPIAcum = list()
        i = 1
        precAcum = 0
        for n in precCPI:
            if(listaIdFase[i-1] == listaIdFase[i-2] ):
                if (precAcum + n == 0):
                    precAcum = 0
                else:
                    precAcum = (precAcum + n) / i
            else:
                precAcum=0
            precCPIAcum.append(precAcum)
            i += 1
        return precCPIAcum

    "Exatidao Acum"
    def CalculaExatidaoAcum(self, erro):
        erroCPIAcum = list()
        i = 1
        extidaoAcum = 0
        for n in erro:
            if (extidaoAcum + n == 0):
                extidaoAcum = 0
            else:
                extidaoAcum = (extidaoAcum + n) / i
            erroCPIAcum.append(extidaoAcum)
            i += 1
        return erroCPIAcum

    "BAC"
    def CalculaBAC(self, lista_pv_acum_p,lista_id_projeto, lista_cpi_projeto ):
        bac = lista_pv_acum_p[len(lista_pv_acum_p) - 1]
        cpi_projeto_final = lista_cpi_projeto[len(lista_cpi_projeto) -1]
        id_projeto = (lista_id_projeto[len(lista_id_projeto)-1])
        return id_projeto, bac, cpi_projeto_final

    "CPI Histórico"
    def CalculaCPI (self, pvAcumF, listaIdFase, cpiHistF, evAcumF, acAcumP, acAcumF, evAcumP):
        cpiPart = list()
        pvTotalFase = list()
        listaCRPrev = list()
        listaFaseF = list()
        DiferencaACCPI = list()
        evTotalFase = list()
        i=1
        faseAnterior = listaIdFase[0]
        verdadeiro = 0
        j = 0
        for n in pvAcumF:
            if (i == (len(listaIdFase))) and (verdadeiro == 0):
                i -= 1
                verdadeiro = 1
            if (i <= len(listaIdFase)):
                if (i == (len(listaIdFase) - 1)) and (verdadeiro == 1):
                    DiferencaPVeEVDaFase = n - evAcumF[i]
                    cpiPart.append(DiferencaPVeEVDaFase)
                    pvTotalFase.append(n)
                    evTotalFase.append(evAcumF[i])
                    faseAnterior = listaIdFase[j]
                    CRPrevisto = pvAcumF[i]/cpiHistF[j]
                    listaCRPrev.append(CRPrevisto)
                    DiferencaACeCPIMedio = CRPrevisto - acAcumF[i]
                    DiferencaACCPI.append(DiferencaACeCPIMedio)
                    listaFaseF.append(listaIdFase[i])
                    j+=1
                elif (listaIdFase[i] != faseAnterior):
                    DiferencaPVeEVDaFase = n - evAcumF[i-1]
                    cpiPart.append(DiferencaPVeEVDaFase)
                    pvTotalFase.append(n)
                    evTotalFase.append(evAcumF[i-1])
                    faseAnterior = listaIdFase[i]
                    CRPrevisto = pvAcumF[i-1]/cpiHistF[j]
                    listaCRPrev.append(CRPrevisto)
                    DiferencaEveCPIMedio = CRPrevisto - acAcumF[i-1]
                    DiferencaACCPI.append(DiferencaEveCPIMedio)
                    listaFaseF.append(listaIdFase[i-1])
                    j+=1
            i+=1
        i=0
        "--------------------------------------"
        # print DiferencaACCPI
        cpiHist = list()
        for indiceIdProjeto in listaIdFase:
            pvTotalFaseAtual = 0
            CRPrev = 0
            EACFase = 0
            pvAcumTotalFase = 0
            j = 0
            EACFasesNaoExecutadas = 0
            for indiceCPIMedio in listaFaseF:
                if (indiceIdProjeto == indiceCPIMedio):
                    pvTotalFaseAtual = pvTotalFase[j]
                    EACFase = listaCRPrev[j]
                if(indiceIdProjeto < indiceCPIMedio):
                    EACFasesNaoExecutadas = listaCRPrev[j] + EACFasesNaoExecutadas
                    pvAcumTotalFase = pvTotalFase[j] + pvAcumTotalFase
                j+=1
            CPIHistFim = (evAcumP[i] + (pvTotalFaseAtual - evAcumF[i]) + pvAcumTotalFase) / (acAcumP[i] + (EACFase - acAcumF[i]) + EACFasesNaoExecutadas)
            cpiHist.append(CPIHistFim)
            i += 1

        return cpiHist
