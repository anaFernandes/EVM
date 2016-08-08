#!-*- conding: utf8
import os  # leitura de arquivos
from matplotlib import style
style.use("ggplot")
import pprint  # Quando o resultado e maior que uma linha, o pretty printer acrescenta quebras de linha e
                # indentacao para revelar as estruturas de maneira mais clara
import csv  # CSV


# 0 - ests
# 1 - real
# 2 - nomeProjeto
# 3 - dataInicio
# 4 - dataFim
# 5 - nomeFase

class LeiaCSV(object):

    def Leia(self):
        nomeFase = list()
        ests = list()
        reais = list()
        nomeProjeto = list()
        dataInicio = list()
        dataFim = list()

        # Metodo para abrir o arquivo em CSV
        clear = lambda: os.system('cls')
        clear()

        pp = pprint.PrettyPrinter(indent=3)
        with open('gva.csv') as csvfile:
            reader = csv.DictReader(csvfile)

            # le varias linhas de cada coluna
            for row in reader:
                ests.append(float(row['est']))
                reais.append(float(row['real']))
                nomeProjeto.append(row.get('nomeProjeto'))
                dataInicio.append(row.get('dataInicio'))
                dataFim.append(row.get('dataFim'))
                nomeFase.append(row.get('nomeFase'))
            dadosCSV = zip(ests, reais, nomeProjeto, dataInicio, dataFim, nomeFase)

        #return dadosCSV, ests, reais, nomeProjeto, dataInicio, dataFim, nomeFase
        return dadosCSV
