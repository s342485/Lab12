import networkx as nx
from database.dao import DAO
from pprint import pprint

class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        self.G = nx.Graph()
        self._nodes = None
        self._edges = None
        self._lista_rifugi =[]
        self._dizionario_rifugi = {}

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
    def get_percorso_minimo(self, soglia):
        distanza_minima = float("inf") #lo mette a infinito
        percorso_minimo = []
        G_filtrato = nx.Graph()

        #creo un sottografo con soli archi peso > soglia
        for u,v,d in self.G.edges(data=True):
            if d["weight"] > soglia:
                G_filtrato.add_edge(u,v, weight=d["weight"])

        #se non ha archi ritorna una lista vuota
        if G_filtrato.number_of_edges() == 0:
            return []

        #per ogni nodo come sorgente
        for sorgente in G_filtrato.nodes():
            distanze, percorsi = nx.single_source_dijkstra(G_filtrato,sorgente, weight="weight")
            #percorsi = nodoX : lista di nodi per raggiungere nodoX
            for destinazione in distanze: #per ogni nodo del grafo destinazione = nodo

                #scarta se stesso
                if destinazione == sorgente:
                    continue

                percorso = percorsi[destinazione] #lista di nodi di destinazione

                #scarto quelli che hanno meno di tre nodi
                if len(percorso) < 3:
                    continue

                distanza = distanze[destinazione] #recupera il peso

                if distanza < distanza_minima:
                    distanza_minima = distanza
                    percorso_minimo = percorso


        return percorso_minimo

        #output = [
        #
        #          Rifugio(id_rifugio=11, nome='Rifugio Kappa', localita='Monte K', altitudine=1900, capienza=35, aperto=1),
        #          Rifugio(id_rifugio=20, nome='Rifugio Tiglio', localita='Valle dei Tigli', altitudine=1500, capienza=25, aperto=1),
        #          Rifugio(id_rifugio=24, nome='Rifugio Alpestre', localita='Monti Alpestri', altitudine=1800, capienza=35, aperto=1)
        #
        #          ]   cammino minimo composto da 3 rifugi

    def get_percorso_minimo_ricorsivo(self, soglia):

        # costruisco il grafo filtrato, stessa cosa di prima
        self.G_filtrato = nx.Graph()
        for u, v, d in self.G.edges(data=True):
            if d["weight"] > soglia:
                self.G_filtrato.add_edge(u, v, weight=d["weight"])

        if self.G_filtrato.number_of_edges() == 0:
            return []

        # variabili globali della ricerca
        self.min_corrente = float("inf")
        self.risultato = []

        # provo ogni nodo come partenza
        for nodo in self.G_filtrato.nodes():
            self.ricorsione([nodo], 0)
        return self.risultato

    def ricorsione (self,cammino,peso):

        #cammino = lista dei nodi visitati finora, al primo giro è il nodo di partenza, il primo che c'è nella lista nodi
        #peso = somma dei pesi degli archi percorsi fino ad adesso, al primo giro è 0 ovviamente
        """
        Sono in un certo nodo (l’ultimo del cammino).
        Provo ad andare in tutti i nodi vicini che non ho ancora visitato.
        Ogni volta aggiorno il peso e verifico se ho trovato un cammino migliore.
        """

        if len(cammino)>=3: #almeno tre nodi

            if peso < self.min_corrente:
                self.min_corrente = peso # variabile che memorizza il minor peso trovato fino ad ora
                self.risultato = cammino.copy()  # .copy crea una nuova lista con gli stessi elementi ma indipendente dalla lista originale


        ultimo = cammino[-1]
        for vicino in self.G_filtrato.neighbors(ultimo):
            if vicino not in cammino:
                w = self.G_filtrato[ultimo][vicino]['weight']

                if peso + w >= self.min_corrente:
                    continue  #Se anche aggiungendo questo arco il costo diventa già maggiore (o uguale) del miglior cammino che ho trovato finora, allora NON ha senso continuare su questo ramo

                cammino.append(vicino)
                self.ricorsione(cammino, peso + w)
                cammino.pop() #backtracking = rimuove l'ultimo elemento della lista cammino



