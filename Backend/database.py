import psycopg2
import os
from dotenv import load_dotenv

from Backend.API.send_tweet import send_tweet

load_dotenv()


# Connect met de database

class Database():
    def __init__(self):
        self.host = 'localhost'
        self.database = 'NS-Twitterzuil'
        self.user = 'postgres'
        self.password = os.environ.get('DB_PASS')

    def connection(self):
        conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
            # port=5432
        )
        return conn

    def new_user(self, naam, laatstestation):
        conn = self.connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO gebruiker (naam, LaatsteStation) "
                       "VALUES (%s, %s) RETURNING id;", (naam, laatstestation))
        gebruiker_id = cursor.fetchone()[0]

        conn.commit()
        cursor.close()
        conn.close()

        return gebruiker_id

    def new_review(self, gebruiker_id, commentaar, tijd, status=0):
        conn = self.connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO review (tijd, commentaar, gebruiker_id, status)"
                       "VALUES (%s, %s, %s, %s) RETURNING id;",
                       (tijd, commentaar, gebruiker_id, status))
        vendor_id = cursor.fetchone()[0]

        conn.commit()
        cursor.close()
        conn.close()

        return vendor_id

    def get_review(self):
        conn = self.connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, commentaar, tijd, gebruiker_id, status FROM review;")
        newest_review = cursor.fetchone()

        return newest_review

    def moderate_reviews(self, review_id, status, commentaar, tijd, mod_id, gebruiker_id):
        conn = self.connection()
        cursor = conn.cursor()
        tweet_id = None
        if status == 1:
            tweet_id = send_tweet(commentaar)

        cursor.execute("DELETE FROM review WHERE id=%s;", [review_id])
        cursor.execute("INSERT INTO gemodereerde_reviews (status, commentaar, tijd, mod_id, tweet_id, gebruiker_id)"
                       "VALUES (%s, %s, %s, %s, %s, %s)", (status, commentaar, tijd, mod_id, tweet_id, gebruiker_id))


        conn.commit()
        cursor.close()
        conn.close()


    def get_moderated_review(self):
        conn = self.connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gemodereerde_reviews")

        all_reviews = cursor.fetchall()

        for review in all_reviews:
            if int(review[1]) == 1:
                newest_review = review

                cursor.close()
                conn.close()

                return newest_review

        return None

    def get_review_by_tweet(self, id):
        conn = self.connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gemodereerde_reviews WHERE tweet_id = %s", [id])

        review = cursor.fetchone()

        return review

    def get_name_by_id(self, id):
        conn = self.connection()
        cursor = conn.cursor()
        cursor.execute("SELECT naam FROM gebruiker WHERE id = %s", [id])

        name = cursor.fetchone()

        return name

if __name__ == '__main__':
    connection = Database()
    # new_review = connection.get_moderated_review()
    # print(new_review)
    review = connection.moderate_reviews()
