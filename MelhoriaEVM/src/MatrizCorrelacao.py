# coding=UTF-8

import pandas as pd
import sns
import numpy as np
import matplotlib.pyplot as plt

#ler os arquivos
#gerar matriz de correlacao
x = pd.read_csv('correcao.csv', delimiter=',')
print(x)
pd.set_option('display.width', 500)
cm = x.corr()
print(cm)
cm = np.array(cm)
sns.heatmap(cm, square= True)
plt.yticks(rotation=0)
plt.xticks(rotation=90)
plt.show()
