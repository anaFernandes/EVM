# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 17:52:11 2016

@author: Ana
"""
import MySQLdb # importa o banco de dados
import os  # leitura de arquivos
from matplotlib import style
style.use("ggplot")
import pprint  # Quando o resultado é maior que uma linha, o “pretty printer” acrescenta quebras de linha e indentação para revelar as estruturas de maneira mais clara
import csv  # CSV
from operator import truediv  # dividir uma lista pela outra

# Método para abrir o arquivo em CSV
clear = lambda: os.system('cls')
clear()

pp = pprint.PrettyPrinter(indent=4)
with open('gva.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    estAcumP = list()
    estAcumF = list()
    realAcumP = list()
    realAcumF = list()
    pvAcumP = list()
    pvAcumF = list()
    acAcumP = list()
    evAcumP = list()
    evAcumF = list()
    cpiTradF = list()
    cpiTradP = list()
    cpiHist = list()
    CPIEstHist = list()
    cpiPart = list()
    despHist = list()
    cpiOutrasTec = list()
    pvTotalFase = list()
    erroCPITrad = list()
    precCPITrad = list()
    eacTrad = list()
    eacHist = list()
    eacOutrasTec = list()
    erroCPIHist = list()
    erroCPIAcumTrad = list()
    erroCPIAcumHist = list()
    precCPIHist = list()
    precCPIAcumHist = list()
    precCPIAcumTrad = list()


    bac = list()

    nomeProjetoF = list()
    nomeFaseF =list()
    cipHistF = list()

    estSum = 0
    realSum = 0
    estSumFase = 0
    realSumFase = 0
    despHist = [(2.03, 'ELABORACAODCTS'), (1.58, 'IMPLEMENTACAO'),  (2.12, 'TESTE'), (3.17, 'CORRECAO')]

    nomeFase = list()
    ests = list()
    reais = list()
    nomeProjeto = list()
    dataInicio = list()
    dataFim = list()
    dadosCSV = list()

    # le várias linhas de cada coluna
    for row in reader:
        ests.append(float(row['est']))
        reais.append(float(row['real']))
        nomeProjeto.append(row.get('nomeProjeto'))
        dataInicio.append(row.get('dataInicio'))
        dataFim.append(row.get('dataFim'))
        nomeFase.append(row.get('nomeFase'))

    # Adiciona o valor acumulado estimado em cada elemento de Medidas de acordo com a Fase, checando o nome da fase ou do Projeto
    i = 0
    faseAnterior = nomeFase[0]
    for n in ests:
        estSum += n
        estAcumP.append(float(estSum))
        if (nomeFase[i] != faseAnterior):
            estSumFase = 0
        estSumFase += n
        estAcumF.append(float(estSumFase))
        faseAnterior = nomeFase[i]
        i += 1

    # Adiciona o valor acumulado real em cada elemento de Medidas de acordo com a Fase, checando o nome da fase ou do Projeto
    i = 0
    faseAnterior = nomeFase[0]
    for n in reais:
        realSum += n
        realAcumP.append(float(realSum))
        if (nomeFase[i] != faseAnterior):
            realSumFase = 0
        realSumFase += n
        realAcumF.append(float(realSumFase))
        faseAnterior = nomeFase[i]
        i += 1


    # Calcula o pv_acum_fase, multiplicando cada valor estAcumF da lista por 100
    pvAcumF = map(lambda x: x * 100, estAcumF)

    # Calcula o ev_acum_fase, multiplicando cada valor realAcumF da lista por 100

    evAcumF = map(lambda x: x * 100, realAcumF)

    # Calcula o cpiTradF, dividindo o pvAcumF pelo evAcumF
    cpiTradF = map(truediv, pvAcumF, evAcumF)

    # Calcula o pv_acum_projeto, multiplicando cada valor estAcumP da lista por 100
    pvAcumP = map(lambda x: x * 100, estAcumP)

    # Calcula o ac_acum_projeto, multiplicando cada valor realAcumP da lista por 100
    acAcumP = map(lambda x: x * 100, realAcumP)

    # Calcula o ev_acum_projeto, multiplicando cada valor realAcumP da lista por 100
    evAcumP = map(lambda x: x * 100, realAcumP)

    # Calcula o cpiTradP, multiplicando cada valor realAcumP da lista por 100
    cpiTradP = map(truediv, pvAcumP, acAcumP)

    #Obtem-se o indice de cada fase para cada atividade comparando o nome da fase, se o nome da fase for igual ao anterior
    #o indice recebe o mesmo valor da atividade anterior, caso contrário o índice recebe o valor anterior +1
    indiceFase = list()
    faseAnterior = nomeFase[0]
    for n in nomeFase:
        if (n == faseAnterior):
            indiceFase.append(i)
        else:
            i += 1
            indiceFase.append(i)
        faseAnterior = n

    # Obtem-se o indice de cada CPI Historico para cada fase comparando o nome da fase de cada atividade com o nome de
    #de cada fase das atividades, se os nomes forem iguais e verdadeiro for igual a 0, indiceCPIHist recebe i
    indiceCPIHist = list()
    valorCPIHist = list()
    i=0
    for m in despHist:
        verdadeiro = 0
        for n in nomeFase:
            if (n == m[1]) :
                if (verdadeiro == 0):
                    indiceCPIHist.append(i)
                    valorCPIHist.append(m[0])
                    i+=1
                    verdadeiro = 1


    # Utlizando os valores obtidos anteiormente, pvTotalFaseAcum e cpiDivHistAcum, para cada valor pvAcumP,
    i = 0
    for n in pvAcumP:
        pvTotalFaseAcum = 0
        cpiDivHistAcum = 0
        j = 0

    "CPI Histórico Estimado"
    """ Nesta função para cada pv acumulado da fase onde a fase anterior é diferente da fase atual e a fase """
    i = 1
    criatividade = 0
    faseAnterior = nomeFase[0]
    for n in pvAcumF:
        if (i == (len(nomeFase))) and (criatividade == 0):
            i -= 1
            criatividade = 1
        if (i <= len(nomeFase)):
            if (i == (len(nomeFase) - 1)) and (criatividade == 1):
                pvDivDesHist = n / valorCPIHist[j]
                cpiPart.append(pvDivDesHist)
                pvTotalFase.append(n)
                faseAnterior = nomeFase[i]
                cipHistF.append(cpiTradF[i])
                nomeProjetoF.append(nomeProjeto[i])
                nomeFaseF.append(nomeFase[i])
                j+=1
            elif (nomeFase[i] != faseAnterior):
                pvDivDesHist = n / valorCPIHist[j]
                cpiPart.append(pvDivDesHist)
                pvTotalFase.append(n)
                cipHistF.append(cpiTradF[i - 1])
                nomeProjetoF.append(nomeProjeto[i - 1])
                nomeFaseF.append(nomeFase[i - 1])
                faseAnterior = nomeFase[i]
                j=+1
        i += 1
    print nomeFaseF
    i=0
    for m in indiceCPIHist:
        if (indiceFase[i] < m):
            pvTotalFaseAcum = pvTotalFaseAcum + pvTotalFase[j]
            cpiDivHistAcum = cpiDivHistAcum + cpiPart[j]
        j += 1
        CPIHistFim = (n + pvTotalFaseAcum) / (acAcumP[i] + cpiDivHistAcum)
    CPIEstHist.append(CPIHistFim)
    i += 1

    "Exatidão Precisão e EAC tradicionais"
    precAnterior = 0
    # Em cada elemento de cpiTradP
    for n in cpiTradP:
        # cheque se n for maior que zero.
        if n > 0:

            #pegue o último elemendo do AC acumulado do projeto e o subtraia por 1, a seguir divida esse
            #elemento pelo último valor do pv acumulado do projeto divido pelo CPI Tradicional do projeto
            erro = (1 - acAcumP[len(acAcumP) - 1]) / (pvAcumP[len(pvAcumP) - 1] / n)
        # caso o CPI tradicional seja igual a 0, a variável erro recebe zero
        else:
            erro = 0
        # adiciona a variavel erro no array
        erroCPITrad.append(erro)
        i += 1

        # Checa que se a a precisao anterior é igual a zero.
        if precAnterior == 0:
            precisao = 0
        # Se for igual a zero a variavel precisao recebe 0, caso contrário precisao recebe a divisão do valor atual CPI
        # tradicional acumulado dividido pelo valor anterior do CPI tradicional acumulado
        else:
            precisao = n / precAnterior
        # O array precCPITrad recebe os valores de precisao
        precCPITrad.append(precisao)
        precAnterior = n

        # O eacT recebe o útimo valor do Pv acumulado do projeto dividido pelo CPI atual
        eacT = pvAcumP[len(pvAcumP) - 1] / n
        # O array eacTrad recebe o eacT
        eacTrad.append(eacT)


    "Precisão Acum Trad"
    i = 1
    precAcumT = 0
    for n in precCPITrad:
        if (precAcumT + n == 0):
            precAcumT = 0
        else:
            precAcumT = (precAcumT + n) / i
        precCPIAcumTrad.append(precAcumT)
        i += 1

    "Precisão Acum Hist"
    i = 1
    precAcumH = 0
    for n in CPIEstHist:
        if (precAcumH + n == 0):
            precAcumH = 0
        else:
            precAcumH = (precAcumH + n) / i
        precCPIAcumTrad.append(precAcumH)
        i += 1

    "Exatidao Acum Trad"
    i = 1
    extidaoAcumT = 0
    for n in CPIEstHist:
        if (extidaoAcumT + n == 0):
            extidaoAcumT = 0
        else:
            extidaoAcumT = (extidaoAcumT + n) / i
        erroCPIAcumTrad.append(extidaoAcumT)
        i += 1

    "Exatidao Acum Hist"
    i = 1
    extidaoAcumH = 0
    for n in CPIEstHist:
        if (extidaoAcumH + n == 0):
            extidaoAcumH = 0
        else:
            extidaoAcumH = (extidaoAcumH + n) / i
        erroCPIAcumHist.append(extidaoAcumH)
        i += 1

    "BAC"
    ONT = pvAcumP[len(pvAcumP) - 1]
    bac.append(ONT)

con = MySQLdb.connect(host='localhost', user='root', passwd='', db='gva')
c = con.cursor()

sql = "SELECT id_projeto, nome FROM projetos"
c.execute(sql)
print c.fetchall()

projetoT = list()
for row in c:
    projetoT.append(row)

faseT = list()
sql = "SELECT id_fase, nome, projetos_id_projeto FROM fases"
c.execute(sql)
print c.fetchall()

faseT = list()
for row in c:
    faseT.append(row)



projetoNome = list()
projetoNome.append('Midira2')

"Junção das colunas"

projetoTable = zip(projetoNome, bac)

faseTable = zip(cipHistF, nomeFaseF, nomeProjetoF)

atividade = zip(ests, reais, nomeFase, nomeProjeto)

medidasEVM = zip(estAcumF, realAcumF, pvAcumF, evAcumF, cpiTradF,
                 estAcumP, realAcumP, evAcumP, pvAcumP, acAcumP,
                 cpiTradP, cpiHist, cpiOutrasTec, eacTrad, eacHist,
                 eacOutrasTec, erroCPITrad, erroCPIHist, erroCPIAcumTrad,
                 erroCPIAcumHist, precCPITrad, precCPIHist, precCPIAcumTrad,
                 precCPIAcumTrad, nomeFase, nomeProjeto)

"Insersão no Banco"

c.executemany("INSERT INTO projetos (nome, bac) VALUES (%s, %s)", projetoTable)
con.commit()
c.executemany("INSERT INTO fases (cpi_hist, projetos_id_projeto) VALUES (%s, %s)", faseTable)
con.commit()
c.executemany(
    "INSERT INTO atividades (esforco_est, esforco_real, fases_id_fase, projetos_id_projeto) VALUES (%s, %s, %s, %s)",
    atividade)
con.commit()
c.executemany(
    "INSERT INTO medidas (esforco_est_acm_fase, esforco_real_acm_fase, pv_acum_fase, ev_acum_fase, cpi_acum_fase, esforco_est_acm_projeto, esforco_real_acm_projeto, ev_acum_projeto, pv_acum_projeto, ac_acum_projeto, cpi_acum_projeto_tec_trad, cpi_acum_projeto_tec_dados_hist, 	cpi_acum_projeto_outras_tec, eac_tec_trad, eac_tec_dados_hist, eac_outras_tec, exatidao_tec_trad, exatidao_tec_dados_hist, exatidao_acum_tec_trad, exatidao_acum_tec_dados_hist, precisao_tec_trad, precisao_tec_dados_hist, precisao_acm_tec_trad, precisao_acm_tec_dados_hist, projetos_id_projeto, fases_id_fase, atividades_id_atividade),VALUES (%s)",
    medidasEVM)
con.commit()
