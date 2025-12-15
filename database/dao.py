from database.DB_connect import DBConnect
from model.rifugio import Rifugio


class DAO:

    @staticmethod
    def get_rifugi():
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * FROM rifugio"""

        cursor.execute(query)

        for row in cursor:
            rifugio = Rifugio(row["id"], row["nome"], row["localita"], row["altitudine"], row["capienza"],row["aperto"])
            result.append(rifugio)

        cursor.close()
        conn.close()
        return result

    #si occupa solo di verificare la connessione tra due rifugi e poi eventualmente se esiste la connessione viene creato un arco
    @staticmethod
    def esiste_connessione(u: Rifugio, v: Rifugio, anno):
        conn = DBConnect.get_connection()
        result = []
        query = """SELECT * 
                   FROM connessione c 
                   WHERE (c.id_rifugio1 = %s AND c.id_rifugio2 = %s) OR (c.id_rifugio1 = %s AND c.id_rifugio2 = %s) 
                   GROUP BY c.id_rifugio1 , c.id_rifugio2 
                   HAVING c.anno <= %s"""
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (u.id_rifugio,v.id_rifugio,v.id_rifugio,u.id_rifugio, anno))

        for row in cursor:
            result.append(row)
            print(row)

        cursor.close()
        conn.close()
        return result

