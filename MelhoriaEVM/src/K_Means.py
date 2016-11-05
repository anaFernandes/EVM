import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import MeanShift
from sklearn.cluster import KMeans
from IPython.display import Image
from sklearn import tree
import pydotplus
import os

class K_Means(object):

    def __init__(self, todas_fases):
       self.todas_fases = todas_fases

    def SeparaFases(self, cluster_fases):
        #Seleciona os ids dos projetos sem repetir
        projeto_anterior = cluster_fases[0][3]
        lista_id_projeto = []
        lista_id_projeto.append(projeto_anterior)

        for id_projeto in cluster_fases:
            if(projeto_anterior != id_projeto[3]):
                lista_id_projeto.append(id_projeto[3])
            projeto_anterior = id_projeto[3]

        implementacao, teste, elaboracao, correcao, copy = [], [], [], [], []

        for id_projeto in lista_id_projeto:
            for fase in cluster_fases:
                if (id_projeto == fase[3]):
                    if (fase[1] == "implementacao"):
                        copy=np.array(fase).tolist()
                        implementacao.append(copy)
                    elif (fase[1] == "elaboracao"):
                        copy = np.array(fase).tolist()
                        elaboracao.append(copy)
                    elif (fase[1] == "testes"):
                        copy = np.array(fase).tolist()
                        teste.append(copy)
                    elif (fase[1] == "correcao"):
                        copy = np.array(fase).tolist()
                        correcao.append(copy)

        imple = np.array(implementacao)
        elab = np.array(elaboracao)
        test = np.array(teste)
        corr = np.array(correcao)
        return imple, test, elab, corr

    def Kmeans(self, fase):
        # lista_duracao, lista_nome_fase, lista_cpi_fase, lista_id_projeto_fase, lista_real_acum_fase,
        # lista_est_acum_fase, lista_real_acum_projeto, lista_est_acum_projeto, lista_perfil_equipe_fase,
        # lista_num_atividades, lista_cpi_projeto
        cluster = np.array(zip(fase[:,4], fase[:,5], fase[:, 8], fase[:, 9], fase[:]))

        ap = KMeans(n_clusters= 5, init = 'k-means++')
        ap.fit_predict(cluster)

        clusters_centers_indices = ap.cluster_centers_
        labels = ap.labels_
        n_clusters_ = len(clusters_centers_indices)

        # print(clusters_centers_indices)
        # print(labels)

        # print "Projeto"
        # agrupamento = list()
        # for j in range(0, n_clusters_):
        #     i = 0
        #     for label in labels:
        #         if(j == label):
        #            print str(cluster[i]) + " id " + str(fase[i][3]) + " label " + str (labels[i])+ " cpi " + str(fase[i][2])
        #         i+=1
        cluster_0, cluster_1, cluster_2, cluster_3, cluster_4 = [], [], [], [], []
        lista_1, lista_2, lista_3, lista_4, lista_5  = [], [], [], [], []
        cpi_1, cpi_2, cpi_3, cpi_4, cpi_5 = [], [], [], [], []
        i=0
        for i in range(len(cluster)):
            if (labels[i] == 0):
                cluster_0.append(cluster)
                lista_1.append(fase[i][3])
                cpi_1.append(fase[i][2])
            elif (labels[i]== 1):
                cluster_1.append(cluster)
                lista_2.append(fase[i][3])
                cpi_2.append(fase[i][2])
            elif (labels[i]== 2):
                cluster_2.append(cluster)
                lista_3.append(fase[i][3])
                cpi_3.append(fase[i][2])
            elif (labels[i]== 3):
                cluster_3.append(cluster)
                lista_4.append(fase[i][3])
                cpi_4.append(fase[i][2])
            elif (labels[i]== 4):
                cluster_4.append(cluster)
                lista_5.append(fase[i][3])
                cpi_5.append(fase[i][2])
        # print "cluster 1"+str(lista_1)+ "cluster 2" +str(lista_2)+ "cluster 3" +str(lista_3)+ "cluster 4" +str(lista_4)+ "cluster 5" +str(lista_5)
        # print "cluster 1" + str(cpi_1) + "cluster 2" + str(cpi_2) + "cluster 3" + str(cpi_3) + "cluster 4" + str(cpi_4) + "cluster 5" + str(cpi_5)

        cluster_fase = np.array(list(zip(cluster_0, cluster_1, cluster_2, cluster_3, cluster_4)))
        return cluster_fase


    def JuntaFases(self, fases_cluster, id_projeto):
        # lista_duracao, lista_nome_fase, lista_cpi_fase, lista_id_projeto_fase, lista_real_acum_fase,
        # lista_est_acum_fase, lista_real_acum_projeto, lista_est_acum_projeto, lista_perfil_equipe_fase,
        # lista_num_atividades, lista_cpi_projeto, lista_data_inicio_projeto, lista_data_fim_projeto
        lista_id_projeto, lista_projetos = [], []
        projeto_anterior = fases_cluster[3][0]
        for id_projeto in fases_cluster:
            if (projeto_anterior != id_projeto[3]):
                lista_id_projeto.append(id_projeto[3])
            projeto_anterior = id_projeto[3]

        for id_projeto in lista_id_projeto:
            copy = [ '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
                     '0','0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
            primeiro = 0
            for fases in fases_cluster:
                fase = np.array(fases).tolist()
                if (primeiro == 0):
                    copy[0] = id_projeto
                    copy[33] = fase[10]
                if (id_projeto == fase[3]):
                    if ('implementacao' == fase[1]):
                        copy[1] = fase[0]
                        copy[2] = fase[1]
                        copy[3] = fase[2]
                        copy[4] = fase[4]
                        copy[5] = fase[5]
                        copy[6] = fase[6]
                        copy[7] = fase[7]
                        copy[8] = fase[8]
                        primeiro = 1

                    if ('correcao' == fase[1]):
                        copy[9] = fase[0]
                        copy[10] = fase[1]
                        copy[11] = fase[2]
                        copy[12] = fase[4]
                        copy[13] = fase[5]
                        copy[14] = fase[6]
                        copy[15] = fase[7]
                        copy[16] = fase[8]
                        primeiro = 1

                    if('testes' == fase[1]):
                        copy[17] = fase[0]
                        copy[18] = fase[1]
                        copy[19] = fase[2]
                        copy[20] = fase[4]
                        copy[21] = fase[5]
                        copy[22] = fase[6]
                        copy[23] = fase[7]
                        copy[24] = fase[8]
                        primeiro = 1

                    if ('elaboracao' == fase[1]):
                        copy[25] = fase[0]
                        copy[26] = fase[1]
                        copy[27] = fase[2]
                        copy[28] = fase[4]
                        copy[29] = fase[5]
                        copy[30] = fase[6]
                        copy[31] = fase[7]
                        copy[32] = fase[8]
                        primeiro = 1
            lista_projetos.append(copy)
            test = np.array(lista_projetos)
        return test

    def Kmeans_projeto(self, dados):

        cluster = np.array(zip(dados[:, 4], dados[:, 5], dados[:, 11], dados[:, 12], dados[:, 19], dados[:, 20],
                           dados[:, 28], dados[:, 29], dados[:, 8] , dados[:, 16], dados[:, 24], dados[:, 32]))

        # print cluster

        ap = KMeans(n_clusters=5, init='k-means++')
        ap.fit_predict(cluster)
        clusters_centers_indices = ap.cluster_centers_
        labels = ap.labels_
        n_clusters_ = len(clusters_centers_indices)
        # print(clusters_centers_indices)
        # print(labels)

        # print "Projeto"
        # agrupamento = list()
        # for j in range(0, n_clusters_):
        #     i = 0
        #     for label in labels:
        #         if(j == label):
        #            print str(cluster[i]) + " id " +str(dados[i][0])+ " label " +str(labels[i])+ " cpi imple " +str(dados[i][3])+ \
        #                  " cpi cor " +str(dados[i][11])+ " cpi teste " +str(dados[i][19])+ " cpi elab "+str(dados[i][27])
        #         i+=1


        cluster_0, cluster_1, cluster_2, cluster_3, cluster_4 = [], [], [], [], []
        lista_0, lista_1, lista_2, lista_3, lista_4 = [], [], [], [], []
        cpi_0, cpi_1, cpi_2, cpi_3, cpi_4 = [], [], [], [], []
        i = 0
        for i in range(len(cluster)):
            if (labels[i] == 0):
                cluster_0.append(cluster)
                lista_0.append(dados[i][0])
                cpi_0.append(dados[i][3])
                cpi_0.append(dados[i][11])
                cpi_0.append(dados[i][19])
                cpi_0.append(dados[i][27])
                cpi_0.append("/")
            elif (labels[i]== 1):
                cluster_1.append(cluster)
                lista_1.append(dados[i][0])
                cpi_1.append(dados[i][3])
                cpi_1.append(dados[i][11])
                cpi_1.append(dados[i][19])
                cpi_1.append(dados[i][27])
                cpi_1.append("/")
            elif (labels[i]== 2):
                cluster_2.append(cluster)
                lista_2.append(dados[i][0])
                cpi_2.append(dados[i][3])
                cpi_2.append(dados[i][11])
                cpi_2.append(dados[i][19])
                cpi_2.append(dados[i][27])
                cpi_2.append("/")
            elif (labels[i]== 3):
                cluster_3.append(cluster)
                lista_3.append(dados[i][0])
                cpi_3.append(dados[i][3])
                cpi_3.append(dados[i][11])
                cpi_3.append(dados[i][19])
                cpi_3.append(dados[i][27])
                cpi_1.append("/")
            elif (labels[i]== 4):
                cluster_4.append(cluster)
                lista_4.append(dados[i][0])
                cpi_4.append(dados[i][3])
                cpi_4.append(dados[i][11])
                cpi_4.append(dados[i][19])
                cpi_4.append(dados[i][27])
                cpi_1.append("/")
        # print "cluster 1"+str(lista_0)+ "cluster 2" +str(lista_1)+ "cluster 3" +str(lista_2)+ "cluster 4" +str(lista_3)+ "cluster 5" +str(lista_4)
        # print "cluster 1" + str(cpi_0) + "cluster 2" + str(cpi_1) + "cluster 3" + str(cpi_2) + "cluster 4" + str(cpi_3) + "cluster 5" + str(cpi_4)

        cluster_projeto = np.array(list(zip(cluster_0, cluster_1, cluster_2, cluster_3, cluster_4)))

        return cluster_projeto


    def DecisionTree(self, dados):

        database = np.array(zip(dados[:, 4], dados[:, 5], dados[:, 11], dados[:, 12], dados[:, 19], dados[:, 20],
                               dados[:, 28], dados[:, 29], dados[:, 8], dados[:, 16], dados[:, 24], dados[:, 32]))
        class_names = ('implementacao_estimado','implementacao_real','correcao_est','correcao_real','teste_est',
                 'teste_real','elaboracao_estimado', 'elaboracao_real','perfil_imple','perfil_cor','perfil_teste',
                 'perfil_elab')
        kind = []
        for dado in dados[:, 33]:
            if(float(dado) <= 1.5):
                kind.append('class1')
            elif (float(dado) <= 2.0):
                kind.append('class2')
            elif (float(dado) <= 2.5):
                kind.append('class3')
            elif (float(dado) <= 3.0):
                kind.append('class4')
            elif (float(dado) <= 3.5):
                kind.append('class5')
            elif (float(dado) <= 4.0):
                kind.append('class6')
            elif (float(dado) <= 4.5):
                kind.append('class7')
            else:
                kind.append('class8')

        target = np.array(kind)

        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(database, target)

        with open("projetos.dot", 'w') as f:
            f = tree.export_graphviz(clf, out_file=f)

        os.unlink('projetos.dot')

        dot_data = tree.export_graphviz(clf, out_file=None)
        graph = pydotplus.graph_from_dot_data(dot_data)
        graph.write_pdf('projetos.pdf')

        dot_data = tree.export_graphviz(clf, out_file=None,
                                             feature_names=class_names,
                                             class_names=target,
                                             filled=True, rounded=True,
                                             special_characters=True)
        graph = pydotplus.graph_from_dot_data(dot_data)
        Image(graph.create_png())


    def Media_Clusters(self, cluster_0, cluster_1, cluster_2, cluster_3):
        media_0 = 0
        for cluster in cluster_0:
            media_0 = cluster + media_0
        media_cluster_0 = media_0/len(cluster_0)

        media_1 = 0
        for cluster in cluster_1:
            media_1 = cluster + media_1
            media_cluster_1 = media_1 / len(cluster_1)

        media_2 = 0
        for cluster in cluster_1:
            media_2 = cluster + media_2
            media_cluster_2 = media_2 / len(cluster_2)

        media_3 = 0
        for cluster in cluster_3:
            media_3 = cluster + media_3
            media_cluster_3 = media_3 / len(cluster_3)
        print " ______Media______"
        print media_cluster_0
        print media_cluster_1
        print media_cluster_2
        print media_cluster_3
        return media_cluster_0, media_cluster_1, media_cluster_2, media_cluster_3

    def Mediana_Clusters(self, cluster_0, cluster_1, cluster_2, cluster_3):
        cluster_0.sort()
        cluster_1.sort()
        cluster_2.sort()
        cluster_3.sort()

        if(len(cluster_0)%2 == 0):
            posicao = len(cluster_0)/2
            mediana_cluster_0 = (cluster_0[posicao] + cluster_0[posicao - 1])/2
        else:
            posicao = int(len(cluster_0)/2)
            mediana_cluster_0 = cluster_0[posicao]

        if (len(cluster_1) % 2 == 0):
            posicao = len(cluster_1)/2
            mediana_cluster_1 = (cluster_1[posicao] + cluster_1[posicao - 1]) / 2
        else:
            posicao = int(len(cluster_1) / 2)
            mediana_cluster_1 = cluster_1[posicao]

        if (len(cluster_2) % 2 == 0):
            posicao = len(cluster_2)/2
            mediana_cluster_2 = (cluster_2[posicao] + cluster_2[posicao - 1]) / 2
        else:
            posicao = int(len(cluster_2) / 2)
            mediana_cluster_2 = cluster_2[posicao]

        if (len(cluster_3) % 2 == 0):
            posicao = len(cluster_3)/2
            mediana_cluster_3 = (cluster_3[posicao] + cluster_3[posicao - 1]) / 2
        else:
            posicao = int(len(cluster_3) / 2)
            mediana_cluster_3 = cluster_3[posicao]
        # print " ______----______"
        # print mediana_cluster_0
        # print mediana_cluster_1
        # print mediana_cluster_2
        # print mediana_cluster_3
        return mediana_cluster_0, mediana_cluster_1, mediana_cluster_2, mediana_cluster_3









        # clear = lambda: os.system('cls')
    # clear()
    #
    # pp = pprint.PrettyPrinter(indent = 16)
    # with open('fases_evm.csv') as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     z = list()
    #     w = list()
    #     a = list()
    #     y = list()
    #     x = list()
    #     for row in reader:
    #         idfase = int(row['idFase'])
    #         nomeFase = str(row['nomeFase'])
    #         numAtividades = int(row['numAtividades'])
    #         esforcoReal = float(row['esforcoReal'])
    #         cpi = float(row['cpi'])
    #         idProjeto = int(row['idProjeto'])
    #         if (nomeFase == 'elaboracao'):
    #             x.append(idfase)
    #             y.append(numAtividades)
    #             z.append(esforcoReal)
    #             w.append(cpi)
    #             a.append(idProjeto)
