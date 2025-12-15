

from database.dao import DAO
from model.model import Model


model = Model()
risultato2 = model.build_weighted_graph(2000)

lista = []
"""for u , v , d in risultato2.edges(data=True):
    print(u)
    print(v)
    print(d)
    Rifugio Aurora(Valle Azzurra)
    Rifugio Boreale(Monti Verdi)
    {'weight': 4.5}"""

risultato = model.get_percorso_minimo(4)
print(risultato)



