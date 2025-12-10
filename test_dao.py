

from database.dao import DAO
from model.model import Model


model = Model()
risultato2 = model.build_weighted_graph(1960)

lista = []
for u , v , d in risultato2.edges(data=True):
    lista.append(d["weight"])

print(lista)

valore_max = max(lista)
valore_min = min(lista)

print(valore_max, valore_min)



