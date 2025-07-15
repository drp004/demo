import os
from fastapi import FastAPI
from pymongo import MongoClient
from fuzzywuzzy import process
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

app = FastAPI()

try:
    conn = MongoClient(MONGO_URI)
    db = conn["be_ws"]

except Exception as e:
    print(f"Error while connecting DB: {e}")

@app.get("/stovekraft/getModels")
async def get_models(brand: str, product: str):
    brand = brand.lower().strip()
    product = product.lower().strip()

    if not brand or not product:
        return {"message": "brand name and product name required"}

    try:
        models_collection = db["stovekraft_products"]   # collection where brand name, product name and model names are stored

        # fetch models name from db
        models_cursor = models_collection.find({"brand": brand, "product": product}, {"_id": 0, "model name": 1})
        models = list(list(models_cursor)[0]["model name"])

        return {"models": models}

    except Exception as e:
        print("Incorrect brand name or product name")
        print(f"\nError: {e}")
        return {"models": [], "message": "Incorrect brand name or product name"}


@app.get("/stovekraft/getDefects")
async def get_defects(product: str, symptom: str):
    product = product.lower().strip()
    symptom = symptom.lower().strip()

    if not product or not symptom:
        return {"message": "product name and symptom required"}

    try:
        defects_collection = db["stovekraft_product_issues"]    # collection where issues are stored

        # availble product with symptom list
        products = {'cooker', 'wonder cast cookware', 'induction cooktop', 'microwave oven', 'egg cooker', 'air fryer', 'toaster', 'strolley', 'non stick cookware', 'tiffin box', 'juicer mixer', 'slow juicer', 'kessel', 'chair', 'water purifier', 'hard anodised cookware', 'mixer grinder', 'food steamer', 'water bottle', 'stainless steel glass cook top', 'infrared thermometer', 'hob', 'popcorn maker', 'gilma led tv ', 'food processor', 'wet grinder', 'sandwich maker', 'salad maker', 'built in oven', 'flask', 'electrical chopper', 'ceramic heater', 'modular kitchen', 'blender', 'electric rice cooker', 'roti maker', 'emergency lamp', 'led', 'mop', 'air cooler', 'oven toaster grill (otg)', 'chimney', 'kettle', 'water heater', 'dry iron', 'vacuum cleaner', 'oxi meter', 'personal care', 'glass cook top', 'hand mixer', 'citrus juicer', 'electronic safe', 'coffee maker', 'garment steamer', 'room heaters', 'steam iron', 'juice extractor', 'furniture', 'chopper', 'kitchen tool set', 'stakbox', 'oil radiator', 'fan'}
        
        # if product is not in products list return empty list and mark issues as other
        if product not in products:
            return {"problem": [], "defects": []}

        # get all symptoms of product
        product_cursor = defects_collection.find({"product": product}, {"_id": 0, "symptom": 1, "defects": 1})
        symptoms = list(product_cursor) 

        symptom_list = [symp["symptom"] for symp in symptoms]

        correct_symptom = process.extractOne(symptom, symptom_list)

        threshold = 50

        if correct_symptom[1] < threshold:
            return {"problem": symptom, "defects": []}

        # return models, issues and defects
        defects_cursor = defects_collection.find_one({"product": product, "symptom": correct_symptom[0]}, {"_id": 0, "defects": 1})
        
        if defects_cursor:
            defects = defects_cursor["defects"]
            return {"problem": correct_symptom[0], "defects": defects}
        else:
            return {"message": f"no defects found for symptom: {symptom}"}

    except Exception as e:
        return {"problem": [], "defects": [], "message": f"Error: {e}"}
    

@app.get("/stovekraft/getServiceDetails")
async def get_service__details(brand: str, product: str):
    brand = brand.lower().strip()
    product = product.lower().strip()

    if not brand or not product:
        return {"message": "brand name and product name required."}
    
    try:
        collection = db["stovekraft_products"]

        service_cursor = collection.find_one({"brand": brand, "product": product}, {"_id": 0, "service_available_at": 1})

        if service_cursor:
            service_detail = service_cursor["service_available_at"]
            print(service_detail)

            return {"service_available_at": service_detail[0]}
        else:
            return {"message": f"no data found for mentioned brad: {brand} and product: {product}"}

    except Exception as e:
        print(f"Error: {e}")
        return {"error": f"an error occured during getting service details;"}