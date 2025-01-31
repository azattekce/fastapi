import sqlite3
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 📌 CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)
# 📌 Veritabanı bağlantı fonksiyonu
def get_db_connection():
    """ Yeni bir SQLite bağlantısı döndürür. """
    conn = sqlite3.connect("tarifler.db", check_same_thread=False)  # ✅ Thread hatasını önlemek için
    conn.row_factory = sqlite3.Row  # ✅ Verileri sözlük formatında döndürmek için
    return conn

# 📌 Pydantic Modeli (Tarif için giriş doğrulama)
class TarifModel(BaseModel):
    baslik: str
    aciklama: str
    malzemeler: list
    hazirlanisi: str
    resim: str
    url: str

# 📌 📌 1️⃣ Yeni tarif ekleme (POST /tarifler)
@app.post("/tarifler")
def add_tarif(tarif: TarifModel):
    """ Yeni bir tarif ekler. """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO tarifler (baslik, aciklama, malzemeler, hazirlanisi, resim, url) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (tarif.baslik, tarif.aciklama, json.dumps(tarif.malzemeler), tarif.hazirlanisi, tarif.resim, tarif.url))
        
        conn.commit()
        conn.close()

        return {"message": "Tarif başarıyla eklendi!", "tarif": tarif.dict()}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 📌 2️⃣ Tüm tarifleri listeleme (GET /tarifler)
@app.get("/tarifler")
def get_all_tarifler():
    """ Tüm tarifleri getirir. """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tarifler")
        tarifler = cursor.fetchall()
        conn.close()

        if not tarifler:
            raise HTTPException(status_code=404, detail="Tarif bulunamadı!")

        return {"tarifler": [
            {"id": t["id"], "baslik": t["baslik"], "aciklama": t["aciklama"],
             "malzemeler": json.loads(t["malzemeler"]), "hazirlanisi": t["hazirlanisi"],
             "resim": t["resim"], "url": t["url"]} for t in tarifler]}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 📌 3️⃣ ID'ye göre belirli bir tarifi getirme (GET /tarifler/{tarif_id})
@app.get("/tarifler/{tarif_id}")
def get_tarif_by_id(tarif_id: int):
    """ ID'ye göre belirli bir tarifi getirir. """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tarifler WHERE id = ?", (tarif_id,))
        tarif = cursor.fetchone()
        conn.close()

        if not tarif:
            raise HTTPException(status_code=404, detail="Tarif bulunamadı!")

        return {
            "id": tarif["id"],
            "baslik": tarif["baslik"],
            "aciklama": tarif["aciklama"],
            "malzemeler": json.loads(tarif["malzemeler"]),
            "hazirlanisi": tarif["hazirlanisi"],
            "resim": tarif["resim"],
            "url": tarif["url"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
