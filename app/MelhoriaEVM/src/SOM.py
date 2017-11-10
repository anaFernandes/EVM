# -*- coding: utf-8 -*-
"""
Created on Tue May 24 10:44:02 2016

@author: Ana
"""

import Orange
import numpy as np
import pprint
import csv

pp = pprint.PrettyPrinter(indent = 16)
with open('fases_evm.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    x = list()
    y = list()
    z = list()
    w = list()
    a = list()
    for row in reader:
        idfase = int(row['idFase'])
        nomeFase = str(row['nomeFase'])
        numAtividades = int(row['numAtividades'])
        esforcoReal = float(row['esforcoReal'])
        cpi = float(row['cpi'])
        idProjeto = int(row['idProjeto'])
        if (nomeFase == 'elaboracao'):
            x.append(idfase)
            y.append(numAtividades)
            z.append(esforcoReal)
            w.append(cpi)
            a.append(idProjeto)

X = np.array(zip(x, y, w, z, a))
X = np.array(list(zip(x, y, w, z, a)))

import random
random.seed(0)

som = Orange.projection.som.SOMLearner(map_shape=(1, 2),
                initialize=Orange.projection.som.InitializeRandom)
map = som(X)

print "Node    Instances"
print "\n".join(["%s  %d" % (str(n.pos), len(n.instances)) for n in map])

i, j = 0, 1
print
print "Data instances in cell (%d, %d):" % (i, j)
for e in map[i, j].instances:
    print e