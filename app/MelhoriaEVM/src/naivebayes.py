
# e gordinho?, tem perinha curta?, faz auau?#

porco1 = [1, 1, 0]
porco2 = [1, 1, 0]
porco3 = [1, 1, 0]
dog1 =   [1, 1, 1]
dog2 =   [0, 1, 1]
dog3 =   [0, 1, 1]

dados = [porco1, porco2, porco3, dog1, dog2, dog3]

marcacoes = [1, 1, 1, -1, -1, -1]

misterioso = [1, 1, 1]

from sklearn.naive_bayes import MultinomialNB

modelo = MultinomialNB()
modelo.fit(dados, marcacoes)
modelo.predict(misterioso)