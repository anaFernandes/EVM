# !-*- conding: utf8
import os  # leitura de arquivos
from matplotlib import style
import hashlib
import os.path
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
# 6 - numRequisito

class LeiaCSV(object):

    def Leia(self):
        lista_nome_fase = list()
        lista_est = list()
        lista_real = list()
        lista_responsavel = list()
        lista_nome_projeto = list()
        lista_data_inicio = list()
        lista_data_fim = list()
        lista_numero_requisito = list()
        lista_trimestre = list()

        # Metodo para abrir o arquivo em CSV ..
        clear = lambda: os.system('clear')
        clear()
        oi = 0
        pp = pprint.PrettyPrinter(indent=3)
        with open('projetoRealSimulado.csv') as csvfile:
            reader = csv.DictReader(csvfile)

            # Create hash of cache file
            csvcontent = csvfile.read()
            #como ele ja leu o arquivo, deve se usar a funcao seek para ele voltar e ler o arquivo desde o comeco
            csvfile.seek(0)
            hash_object = hashlib.md5(str(csvcontent))
            hash_file = '/tmp/EVM' + hash_object.hexdigest()
            hash_file_exists = os.path.exists(hash_file)
            open(hash_file, 'w').write(" ")
            dadosCSV = []

            # le varias linhas de cada coluna
            if (not hash_file_exists):
                for row in reader:
                    lista_est.append(float(row['est']))
                    lista_real.append(float(row['real']))
                    lista_responsavel.append(row.get('responsavel'))
                    lista_nome_projeto.append(row.get('nomeProjeto'))
                    lista_data_inicio.append(row.get('dataInicio'))
                    lista_data_fim.append(row.get('dataFim'))
                    lista_nome_fase.append(row.get('nomeFase'))
                    lista_numero_requisito.append(row.get('numeroRequisito'))
                    lista_trimestre.append(row.get('trimestre'))

                dadosCSV = zip(lista_est, lista_real, lista_responsavel, lista_nome_projeto, lista_data_inicio,
                           lista_data_fim, lista_nome_fase, lista_numero_requisito, lista_trimestre)
        return dadosCSV, hash_file_exists
