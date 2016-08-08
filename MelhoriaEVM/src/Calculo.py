# coding=UTF-8

from operator import truediv

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
        cpiTrad = map(truediv, pvAcum, evAcum)
        return cpiTrad

    def CalculaCPIHistFase(self, pvAcumF):
        for n in pvAcumF:
            if()



    def CalculaCPIHist(self, nomeFase, pvAcumP, pvAcumF, acAcumP, despHist, despHistNome, cpiTradF):
        valorCPIHist = list()
        pvFase = list()
        cpiTrad = list()
        i = 0
        for m in despHistNome:
            verdadeiro = 0
            for n in nomeFase:
                if (n == m[1]):
                    if (verdadeiro == 0):
                        valorCPIHist.append(m[1])
                        pvFase.append(pvAcumF)
                        cpiTrad.append(cpiTradF)
                        i += 1
                        verdadeiro = 1
        print valorCPIHist

        # # Utlizando os valores obtidos anteiormente, pvTotalFaseAcum e cpiDivHistAcum, para cada valor pvAcumP,
        # i = 0
        # for n in pvAcumP:
        #     pvTotalFaseAcum = 0
        #     cpiDivHistAcum = 0
        #     j = 0
        #
        # "CPI Histórico"
        # # Nesta função para cada pv acumulado da fase onde a fase anterior é diferente da fase atual e a fase
        # cpiPart = list()
        # j = 0
        # pvTotalFase = list()
        # cipHistF = list()
        # idFaseF = list()
        # idProjetoF = list()
        # cpitHistA = list()
        # CPIHistFim = 0
        # i = 1
        # verdadeiro = 0
        # faseAnterior = idFase[0]
        # for n in pvAcumF:
        #     if (i == (len(idFase))) and (verdadeiro == 0):
        #         i -= 1
        #         verdadeiro = 1
        #     if (i <= len(idFase)):
        #         if (i == (len(idFase) - 1)) and (verdadeiro == 1):
        #             pvDivDesHist = n / valorCPIHist[j]
        #             cpiPart.append(pvDivDesHist)
        #             pvTotalFase.append(n)
        #             faseAnterior = idFase[i]
        #             cipHistF.append(cpiTradF[i])
        #             idProjetoF.append(idProjeto[i])
        #             idFaseF.append(idFase[i])
        #             j += 1
        #         elif (idFase[i] != faseAnterior):
        #             pvDivDesHist = n / valorCPIHist[j]
        #             cpiPart.append(pvDivDesHist)
        #             pvTotalFase.append(n)
        #             cipHistF.append(cpiTradF[i - 1])
        #             idProjetoF.append(idProjeto[i - 1])
        #             idFaseF.append(idFase[i - 1])
        #             faseAnterior = idFase[i]
        #             j = +1
        #     i += 1
        #     i = 0
        #     for m in indiceCPIHist:
        #         if (indiceFase[i] < m):
        #             pvTotalFaseAcum = pvTotalFaseAcum + pvTotalFase[j]
        #             cpiDivHistAcum = cpiDivHistAcum + cpiPart[j]
        #         j += 1
        #         CPIHistFim = (n + pvTotalFaseAcum) / (acAcumP[i] + cpiDivHistAcum)
        #     cpitHistA.append(CPIHistFim)
        #     i += 1
        # return cipHistF

    # "Precisão Exatidao e EAC tradicionais"
    # def CalculaExatidaoPrecisaoEAC (self, cpiTradP, acAcumP, pvAcumP):
    #     erroCPITrad = list()
    #     precCPITrad = list()
    #     eacTrad = list()
    #     precAnterior = 0
    #     i=0
    #     #Em cada elemento de cpiTradP
    #     for n in cpiTradP:
    #         #cheque se n for maior que zero.
    #         if n > 0:
    #
    #             # pegue o último elemendo do AC acumulado do projeto e o subtraia por 1, a seguir divida esse
    #             # elemento pelo último valor do pv acumulado do projeto divido pelo CPI Tradicional do projeto
    #             erro = (1 - acAcumP[len(acAcumP) - 1]) / (pvAcumP[len(pvAcumP) - 1] / n)
    #         # caso o CPI tradicional seja igual a 0, a variável erro recebe zero
    #         else:
    #             erro = 0
    #         # adiciona a variavel erro no array
    #         erroCPITrad.append(erro)
    #         i += 1
    #         # Checa que se a a precisao anterior é igual a zero.
    #         if precAnterior == 0:
    #             precisao = 0
    #         # Se for igual a zero a variavel precisao recebe 0, caso contrário precisao recebe a divisão do valor atual CPI
    #         # tradicional acumulado dividido pelo valor anterior do CPI tradicional acumulado
    #         else:
    #             precisao = n / precAnterior
    #         # O array precCPITrad recebe os valores de precisao
    #         precCPITrad.append(precisao)
    #         precAnterior = n
    #         # O eacT recebe o útimo valor do Pv acumulado do projeto dividido pelo CPI atual
    #         eacT = pvAcumP[len(pvAcumP) - 1] / n
    #         # O array eacTrad recebe o eacT
    #         eacTrad.append(eacT)
    #     return erroCPITrad, precCPITrad, eacTrad
    #
    # "EAC Histórico"
    # def CalculaEACHist(self, cpiHistA, pvAcumP):
    #     eacH =0
    #     eacHist = list()
    #     for atividade in cpiHistA:
    #         # O eacT recebe o útimo valor do Pv acumulado do projeto dividido pelo CPI atual
    #         eacH = pvAcumP[len(pvAcumP) - 1] / n
    #         # O array eacTrad recebe o eacT
    #         eacHist.append(eacH)
    #     return eacHist
    #
    # "Precisão Acum Trad"
    # def CalculaPrecisaoAcumTrad(self, precCPITrad):
    #     precCPIAcumTrad = list()
    #     i = 1
    #     precAcumT = 0
    #     for n in precCPITrad:
    #         if (precAcumT + n == 0):
    #             precAcumT = 0
    #         else:
    #             precAcumT = (precAcumT + n) / i
    #         precCPIAcumTrad.append(precAcumT)
    #         i += 1
    #     return precCPIAcumTrad
    #
    # "Precisão Acum Hist"
    # def CalculaPrecisaoAcumHist (self, CPIHistA):
    #     precCPIAcumHist = list()
    #     i = 1
    #     precAcumH = 0
    #     for n in CPIHistA:
    #         if (precAcumH + n == 0):
    #             precAcumH = 0
    #         else:
    #             precAcumH = (precAcumH + n) / i
    #         precCPIAcumHist.append(precAcumH)
    #         i += 1
    #     return precCPIAcumHist
    #
    # "Exatidao Acum Trad"
    # def CalculaExatidaoTrad(self, CPITrad):
    #     erroCPIAcumTrad = list()
    #     i = 1
    #     extidaoAcumT = 0
    #     for n in CPITrad:
    #         if (extidaoAcumT + n == 0):
    #             extidaoAcumT = 0
    #         else:
    #             extidaoAcumT = (extidaoAcumT + n) / i
    #         erroCPIAcumTrad.append(extidaoAcumT)
    #         i += 1
    #     return erroCPIAcumTrad
    #
    # "Exatidao Acum Hist"
    # def CalculaExatidaoAcumHist(self, CPIEstHist):
    #     erroCPIAcumHist = list()
    #     i = 1
    #     extidaoAcumH = 0
    #     for n in CPIEstHist:
    #         if (extidaoAcumH + n == 0):
    #             extidaoAcumH = 0
    #         else:
    #             extidaoAcumH = (extidaoAcumH + n) / i
    #         erroCPIAcumHist.append(extidaoAcumH)
    #         i += 1
    #     return erroCPIAcumHist
    #
    # "BAC"
    # def CalculaBAC(self, pvAcumP):
    #     bac = -1
    #     ONT = pvAcumP[len(pvAcumP) - 1]
    #     bac = ONT
    #     return bac

