import sqlite3

def update_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Cek apakah kolom waktu_checkout sudah ada
    c.execute("PRAGMA table_info(orders)")
    columns = [col[1] for col in c.fetchall()]
    
    if "waktu_checkout" not in columns:
        c.execute("ALTER TABLE orders ADD COLUMN waktu_checkout DATETIME")
        conn.commit()

    conn.close()

if __name__ == "__main__":
    update_db()
