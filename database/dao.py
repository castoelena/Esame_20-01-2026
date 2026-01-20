from oauthlib.uri_validate import query

from database.DB_connect import DBConnect
from model.artist import Artist

class DAO:

    @staticmethod
    def get_all_artists():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM artist a
                    
                """
        cursor.execute(query)
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_artists_albums(n_alb):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """ SELECT a.id, a.name, COUNT(*) as num_albums
                    FROM artist a, album b
                    WHERE a.id = b.artist_id 
                    GROUP BY a.id, a.name
                    HAVING num_albums >= %s """

        cursor.execute(query, (n_alb,))
        for row in cursor:
            result.append((row['id'], row['name'], row['num_albums']))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_stesso_genere():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """ SELECT t1.id AS a1, t2.id AS a2, COUNT(t1.genre_id) AS genre
                    FROM (SELECT a.id, t.genre_id
                          FROM artist a, track t , album al
                          WHERE a.id = al.artist_id AND al.id = t.album_id 
                          GROUP BY a.id, t.genre_id) t1,
                          (SELECT a.id, t.genre_id
                           FROM artist a, track t, album al
                           WHERE a.id = al.artist_id AND al.id = t.album_id 
                           GROUP BY a.id, t.genre_id) t2
                    WHERE t1.id <> t2.id AND t1.genre_id = t2.genre_id
                    GROUP BY a1, a2 """
        cursor.execute(query)
        for row in cursor:
            result.append((row['a1'], row['a2'], row['genre']))

        cursor.close()
        conn.close()
        return result