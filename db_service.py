import sqlite3
import json

# ✅ Veritabanı bağlantı fonksiyonu
def get_db_connection():
    conn = sqlite3.connect("tarifler.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# ✅ Tarif ekleme
def add_tarif_to_db(tarif):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tarifler (baslik, aciklama, malzemeler, hazirlanisi, resim, url) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (tarif.baslik, tarif.aciklama, json.dumps(tarif.malzemeler), 
          tarif.hazirlanisi, tarif.resim, tarif.url))
    conn.commit()
    conn.close()

# ✅ Tüm tarifleri getirme
def get_all_tarifler_from_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tarifler")
    tarifler = cursor.fetchall()
    conn.close()
    return tarifler

# ✅ ID'ye göre tarif getirme
def get_tarif_by_id_from_db(tarif_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tarifler WHERE id = ?", (tarif_id,))
    tarif = cursor.fetchone()
    conn.close()
    return tarif

# ✅ Tarif silme
def delete_tarif_from_db(tarif_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tarifler WHERE id = ?", (tarif_id,))
    conn.commit()
    conn.close()

# ✅ Tarif güncelleme
def update_tarif_in_db(tarif_id, updated_tarif):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tarifler
        SET baslik = ?, aciklama = ?, malzemeler = ?, hazirlanisi = ?, resim = ?, url = ?
        WHERE id = ?
    """, (updated_tarif.baslik, updated_tarif.aciklama, json.dumps(updated_tarif.malzemeler),
          updated_tarif.hazirlanisi, updated_tarif.resim, updated_tarif.url, tarif_id))
    conn.commit()
    conn.close()
    
print("db_service.py loaded successfully!")