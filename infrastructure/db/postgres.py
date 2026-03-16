import psycopg2

class PostgresClient:
    def _init_(self):
        self.conn= psycopg2.connect(
            host="postgres",
            database="customers",
            user="admin",
            password="admin"
        )

        def get_customer(self, customer_id: int):
            cur= self.conn.cursor()
            cur.execute("""SELECT name, email, last_transaction, risk_score, notes FROM customers WHERE id = %s""", (customer_id,))
            result = cur.fetchone()
            return result 
        
        