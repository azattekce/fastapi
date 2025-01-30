import sqlite3

conn = sqlite3.connect("tarifler.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tarifler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    baslik TEXT NOT NULL,
    aciklama TEXT NOT NULL,
    malzemeler TEXT NOT NULL,
    hazirlanisi TEXT NOT NULL,
    resim TEXT,
    url TEXT
)
""")

conn.commit()
conn.close()
print("✅ Veritabanı hazır!")
