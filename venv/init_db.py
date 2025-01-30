import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Buat tabel products jika belum ada
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  price REAL NOT NULL)''')

    # Buat tabel orders jika belum ada
    c.execute('''CREATE TABLE IF NOT EXISTS orders
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id TEXT NOT NULL,
                  server_id TEXT NOT NULL,
                  nickname TEXT NOT NULL,
                  email TEXT NOT NULL,
                  whatsapp TEXT NOT NULL,
                  produk TEXT NOT NULL,
                  jumlah_produk INTEGER NOT NULL,
                  total_harga REAL NOT NULL,
                  waktu_checkout DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    # Contoh data awal untuk tabel products
    c.execute("INSERT OR IGNORE INTO products (name, price) VALUES ('Product 1', 19.99)")
    c.execute("INSERT OR IGNORE INTO products (name, price) VALUES ('Product 2', 29.99)")

    conn.commit()
    conn.close()
    
    

if __name__ == "__main__":
    init_db()
