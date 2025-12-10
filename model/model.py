import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        self.G = nx.Graph()
        self._nodes = None
        self._edges = None

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        self._nodes = DAO.get_rifugi()  #lista di rifugi
        #aggiungo tutti i nodi
        for rifugio in self._nodes:
            self.G.add_node(rifugio)

        for u in self.G:
            for v in self.G:
                if u.id_rifugio < v.id_rifugio:
                    risultato = DAO.esiste_connessione(u,v,year)
                    if len(risultato) > 0:
                        row = risultato[0] #ESSENDO UNA LISTA DI DIZIONARI
                        difficolta = float(self.restituisci_difficolta(row["difficolta"]))
                        distanza = float(row["distanza"])
                        peso = float(distanza * difficolta)
                        self.G.add_edge(u,v, weight=peso)

        for nodo in list(self.G.nodes()):  #RuntimeError: dictionary changed size during iteration "cosa vuol dire sta cosa" : vuol dire che non posso modificare il valore del dizionario e convinee trasformarlo in una lista statica prima di iterarci sopra perchè esso è in continuo movimento e cambiamento
            if self.G.degree(nodo) < 1:
                self.G.remove_node(nodo)

        return self.G

    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        lista = []
        for u, v , d in self.G.edges(data=True):
            lista.append(d["weight"])

        valore_max = max(lista)
        valore_min = min(lista)

        return valore_min, valore_max

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        conto_minori = 0
        conto_maggiori = 0
        for u, v , d in self.G.edges(data=True):
            if d["weight"] < soglia:
                conto_minori += 1
            if d["weight"] > soglia:
                conto_maggiori += 1
        return conto_minori, conto_maggiori


    @staticmethod   #mettere un metodo statico vuol dire associarlo alla classe e non all'oggetto quindi non devo scrivere self o in un altra classe creare un oggetto classe per chiamarlo
    def restituisci_difficolta(difficolta):
        if difficolta == "facile":
            return 1
        if difficolta == "media":
            return 1.5
        if difficolta == "difficile":
            return 2


    """Implementare la parte di ricerca del cammino minimo"""
    # TODo
