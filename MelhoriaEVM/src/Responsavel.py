
class Responsavel(object):

    def __init__(self, projetosFromDatabase):
        self.projetosFromDatabase = projetosFromDatabase


    def Calcula_Perfil_Responsavel(self, lista_nome_responsavel):
        lista_perfil_responsavel = []
        lista_responsavel = [['Anderson Carvalho', 1], ['Andre Ribeiro Barros', 2], ['Breno Batista Machado', 3],
                             ['Dimas Samid Leme', 1], ['Douglas Barbosa Alexandre', 3],
                             ['Edvane Evangelista', 1], ['Emiliane Silva Soares', 3],
                             ['Fernando Pereira Alves de Araujo', 2],
                             ['Fernando Simeone', 2], ['Glasiana Aparecida Nunes', 1],
                             ['Cristina Alves de Andrade', 1], ['Rodrigo Carvalho Lima', 1],
                             ['Sheila Magalhaes', 2], ['Michelle Cristina Alves de Andrade', 1], ['-', 0]]

        for nome_responsavel in lista_nome_responsavel:
            for responsavel in lista_responsavel:
                if(responsavel[0]== nome_responsavel):
                    lista_perfil_responsavel.append(responsavel[1])
        return lista_perfil_responsavel


    def Calcula_Perfil_Equipe(self, lista_perfil_responsavel, lista_id):
        lista_soma_perfil, lista_contador, lista_id_unico, lista_media_perfil = [], [], [], []
        fase_anterior = ''
        for fase in lista_id:
            if (fase_anterior != fase):
                lista_id_unico.append(fase)
            fase_anterior = fase

        for id_unico in lista_id_unico:
            soma_perfil = 0
            contador = 0
            i=0
            for id in lista_id:
                if(id_unico == id):
                    if (lista_perfil_responsavel[i] !=0):
                        soma_perfil += lista_perfil_responsavel[i]
                        contador += 1
                i+=1
            lista_soma_perfil.append(soma_perfil)
            lista_contador.append(contador)
        i=0
        for soma_perfil in lista_soma_perfil:
            media_perfil = float(soma_perfil)/float(lista_contador[i])
            lista_media_perfil.append(media_perfil)
            i+=1
        return lista_media_perfil