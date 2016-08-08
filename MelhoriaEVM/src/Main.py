# coding=UTF-8
from Projeto import Projeto
from Fase import Fase
from Atividade import Atividade
from Medidas import Medidas
from LeiaCSV import LeiaCSV
from Calculo import Calculo
from Database import Database

#Pega os dados do Banco
out = Database.get("SELECT * FROM atividades")

def PegarDadosDoBanco():
    Atividade.AtividadesFromDBToApliccation()
    Fase.FasesFromDBToApliccation()
    #Projeto.ProjetoFromDBToApliccation()

" Insere no Banco a partir do Arquivo "

def PegarDadosCSVParaBanco():
    " Constroi lista de atividades a partir do CSV "
    #     por enquanto é apenas uma matriz de strings das atividades.
    #     No próximo passo será construída uma lista de objetos "Projetos"
    leitorCsvTmp = LeiaCSV()
    listaAtividadesSemFormatacao = leitorCsvTmp.Leia()

    " Cria Objetos e enviar para o banco "

    # Lista projetos
    for atividade in listaAtividadesSemFormatacao:
        Projeto(-1, atividade[2], atividade[3], atividade[4], -1)

    # Lista fases
    for atividade in listaAtividadesSemFormatacao:
        Fase(-1, atividade[5], -1, Projeto.getIdByNome(atividade[2]))

    # Lista atividade
    for atividade in listaAtividadesSemFormatacao:
        Atividade(-1, atividade[0], atividade[1], Fase.getIdByNome(atividade[5], atividade[2]),
                  Projeto.getIdByNome(atividade[2]))

" Calcula valores EVM "
def CalculaEVM():
    #Pegar os dados do Banco, a seguir separa-los em pacotes de projetos para poder utiliza-los no calculo
    projetosFromDatabase = list()
    mediaCPI = list()
    CPIAcumFase = 0
    i = 0
    contadorCPI = 0
    counterAtividades = 0
    idProjetoAnterior = -1
    faseAnterior =" "

    idProjetoAnterior = -1
    #Agrupa as atividades em
    row = list()
    for atividade in Atividade.todasAtividades :
        if(atividade.projetos_id_projeto != idProjetoAnterior) :
            row.append(atividade)
            idProjetoAnterior = atividade.projetos_id_projeto
            i+=1
            projetosFromDatabase.append(row)
        else :
            projetosFromDatabase[i-1].append(atividade)


    calculoInfo = Calculo(projetosFromDatabase)

    #Para cada projeto dentro de projetosFromDatabase
    for listaProjeto in projetosFromDatabase :
        listaEst = list()
        listaEsfReal = list()
        listaIdFase = list()
        listaIdProjeto = list()
        listaIdAtividades = list()

        #enquanto o contator de atividades for menor que a lista de projetos
        #ele adiciona cada coluna de atividades em uma lista
        while(counterAtividades < len(listaProjeto)) :
            listaEst.append(listaProjeto[counterAtividades].esforcoEst)
            listaEsfReal.append(listaProjeto[counterAtividades].esforcoReal)
            listaIdFase.append(listaProjeto[counterAtividades].fases_id_fase)
            listaIdProjeto.append(listaProjeto[counterAtividades].projetos_id_projeto)
            listaIdAtividades.append(listaProjeto[counterAtividades].id)
            counterAtividades+=1
        counterAtividades=0

        estAcumP, estAcumF = calculoInfo.AcumuladoMedidas(listaEst, listaIdFase)
        realAcumP, realAcumF = calculoInfo.AcumuladoMedidas(listaEsfReal, listaIdFase)
        pvAcumF = calculoInfo.MultiplicaAcumulado(estAcumF)
        evAcumF = calculoInfo.MultiplicaAcumulado(realAcumF)
        cpiTradF = calculoInfo.CalculaCPITrad(pvAcumF, evAcumF)
        pvAcumP = calculoInfo.MultiplicaAcumulado(estAcumP)
        acAcumP = calculoInfo.MultiplicaAcumulado(realAcumP)
        evAcumP = calculoInfo.MultiplicaAcumulado(realAcumP)
        cpiTradP = calculoInfo.CalculaCPITrad(pvAcumP, acAcumP)
        bac = calculoInfo.CalculaBAC(pvAcumP)

        Medidas(-1, estAcumF, realAcumF, pvAcumF, evAcumF, cpiTradF, estAcumF, evAcumF, evAcumP,
                pvAcumP, acAcumP, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                -1, -1, -1, -1, listaProjeto[0].projetos_id_projeto,
                listaIdFase, listaIdAtividades)

        # Pega os dados do banco para calcular o CPI histórico médio de cada fase
        for fase in Fase.todasFases:
            if (fase.nome == faseAnterior):
                CPIAcumFase = CPIAcumFase + fase.cpiHist
                contadorCPI += 1
            else:
                despHist.append(CPIAcumFase)
                despHist.append(fase.nome)
                CPIAcumFase = 0
                contador = 0
                CPIAcumFase = fase.cpiHist


            faseAnterior = fase.nome


            #erroCPIAcumTrad = calculoInfo.CalculaExatidaoTrad(cpiTradP)
        #precCPIAcumTrad = calculoInfo.CalculaPrecisaoAcumTrad(precCPITrad)
        #calculoInfo.CalculaCPIHist(listaIdFase, pvAcumP, pvAcumF, acAcumP, despHist, despHistNome, cpiTradF)
        #precCPITrad, erroCPITrad, eacTrad = calculoInfo.CalculaExatidaoPrecisaoEAC(cpiTradP, acAcumP, pvAcumP)
        #precCPIAcumHist = calculoInfo.CalculaPrecisaoAcumHist(cpiHistA)
        #erroCPIAcumHist = calculoInfo.CalculaExatidaoAcumHist(cpiHistA)
        #eacHist = calculoInfo.CalculaEACHist(cpiHistA, pvAcumP)



def start():
    #PegarDadosCSVParaBanco()
    PegarDadosDoBanco()
    CalculaEVM()
    exit()

start()














