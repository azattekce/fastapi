from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json

# ✅ DB servis fonksiyonlarını içe aktar
from db_service import (
    add_tarif_to_db, get_all_tarifler_from_db,
    get_tarif_by_id_from_db, delete_tarif_from_db,
    update_tarif_in_db
)

app = FastAPI()

# ✅ CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

# ✅ Tarif modeli
class TarifModel(BaseModel):
    baslik: str
    aciklama: str
    malzemeler: list
    hazirlanisi: str
    resim: str
    url: str

# 1️⃣ Tarif Ekleme
@app.post("/tarifler")
def add_tarif(tarif: TarifModel):
    try:
        add_tarif_to_db(tarif)
        return {"message": "Tarif başarıyla eklendi!", "tarif": tarif.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2️⃣ Tüm Tarifleri Getirme
@app.get("/tarifler")
def get_all_tarifler():
    try:
        tarifler = get_all_tarifler_from_db()
        if not tarifler:
            raise HTTPException(status_code=404, detail="Tarif bulunamadı!")
        
        return {"tarifler": [
            {"id": t["id"], "baslik": t["baslik"], "aciklama": t["aciklama"],
             "malzemeler": json.loads(t["malzemeler"]), "hazirlanisi": t["hazirlanisi"],
             "resim": t["resim"], "url": t["url"]} for t in tarifler]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 3️⃣ Belirli Tarif Getirme
@app.get("/tarifler/{tarif_id}")
def get_tarif_by_id(tarif_id: int):
    try:
        tarif = get_tarif_by_id_from_db(tarif_id)
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

# 4️⃣ Tarif Silme
@app.delete("/tarifler/{tarif_id}")
def delete_tarif(tarif_id: int):
    try:
        tarif = get_tarif_by_id_from_db(tarif_id)
        if not tarif:
            raise HTTPException(status_code=404, detail="Tarif bulunamadı!")

        delete_tarif_from_db(tarif_id)
        return {"message": "Tarif başarıyla silindi!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 5️⃣ Tarif Güncelleme
@app.put("/tarifler/{tarif_id}")
def update_tarif(tarif_id: int, updated_tarif: TarifModel):
    try:
        tarif = get_tarif_by_id_from_db(tarif_id)
        if not tarif:
            raise HTTPException(status_code=404, detail="Tarif bulunamadı!")

        update_tarif_in_db(tarif_id, updated_tarif)
        return {"message": "Tarif başarıyla güncellendi!", "tarif": updated_tarif.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
