from dataclasses import dataclass

@dataclass
class Rifugio:
    id_rifugio: int
    nome : str
    localita : str
    altitudine : str
    capienza : str
    aperto : bool

    def __str__(self):
        return self.nome+"("+self.localita+")"
    #serve per poter usare l'oggetto come nodo del grafo
    def __hash__(self):
        return hash(self.id_rifugio)
    def __eq__(self, other):
        return isinstance(other, Rifugio) and self.id_rifugio == other.id_rifugio


