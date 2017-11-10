# coding=UTF-8

class ValidaData(object):
    def __init__(self, listaAtividadesSemFormatacao):
        self.listaAtividadesSemFormatacao = listaAtividadesSemFormatacao

    def Valida(self, listaAtividadesSemFormatacao):
        data_inicio = list()
        data_fim = list()
        duracao_list = list()
        for atividade in listaAtividadesSemFormatacao:
            dia, mes, ano = atividade[4] .split('/')
            data_inicio.append(ano +"-"+ mes +"-"+ dia)
            dia_fim, mes_fim, ano_fim = atividade[5] .split('/')
            data_fim.append(ano_fim + "-" + mes_fim + "-" + dia_fim)
            dia_inicio = int(dia)
            mes_incio = int(mes)
            dia_f = int(dia_fim)
            mes_f = int(mes_fim)
            duracao = str(dia_f - dia_inicio + (mes_f - mes_incio)*30)
            duracao_list.append(duracao)
        return data_inicio, data_fim, duracao_list
