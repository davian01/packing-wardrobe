#!/usr/bin/env python3
"""Regenerate ../index.html by embedding photos (base64) into template.html.

Usage:  python build.py
Requires: pillow  (pip install pillow)

Photos live in ./photos. Items with an empty photo field render a placeholder
emoji in the app. Edit the `have` / `need` tables below, then re-run.
"""
import os, io, json, base64
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PHOTOS = os.path.join(HERE, "photos")
OUT = os.path.join(os.path.dirname(HERE), "index.html")

def dataURI(fname):
    if not fname:
        return None
    path = os.path.join(PHOTOS, fname)
    if not os.path.exists(path):
        return None
    im = Image.open(path).convert("RGB")
    im.thumbnail((560, 560))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=78)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

# (name, brand, category, size, price, sku, url, notes, photo_filename)
have = [
 ("Low-Rise Baggy denim shorts","Hollister","Shorts","W29","","","",
    "Light-wash baggy jorts. Made in Guatemala. Official Hollister image.","hollister_shorts.jpg"),
 ("Linen Blend Easy Shorts — Navy","Uniqlo","Shorts","S","34.90","372-485855 / UPC 2000211187338",
    "https://www.uniqlo.com/us/en/products/E485855-000/00","5\" linen-blend easy shorts. $34.90 CAD.","uniqlo_navy.jpg"),
 ("Linen Blend Easy Shorts — Olive","Uniqlo","Shorts","","","372-485855",
    "https://www.uniqlo.com/us/en/products/E485855-000/00","Same style as navy pair, olive colorway. Size to confirm.","uniqlo_olive.jpg"),
 ("Linen trousers — Cream","Zara / Inditex","Pants","M","","2634/003/250 (180/80A)","",
    "Cream linen trousers. Inditex (Zara group). Official Zara image (relaxed pull-on cut).","zara_linen_trousers.jpg"),
 ("Knit sweater-polo — Ivory/olive stripe","American Eagle","Polo / Knit","M","74.95","44439859","",
    "Clearance (USD 59.95 / CAD 74.95). Waffle-knit button polo.","IMG_2455.jpg"),
 ("Pinstripe crest shirt — Black","Red-OX","Shirt","M","","","",
    "Vintage, bought in-store (source unknown). Embroidered crest, French text.","IMG_2457.jpg"),
 ("Camp-collar shirt — Tan","Forever 21","Shirt","M","","","",
    "Linen-look resort/camp shirt.","IMG_2459.jpg"),
 ("Camp-collar shirt — Olive","Urban Man (Urban Planet)","Shirt","S","","","",
    "Olive/sage camp shirt with chest pocket.","IMG_2460.jpg"),
 ("USA 'Unidad' jersey — White","adidas Originals","Jersey","","","","https://www.ebay.com/itm/115165582451",
    "Originals 'Unidad / Danketsu' jersey, red + blue stars. Official adidas image. Size to confirm.","adidas_unidad.jpg"),
 ("Ribbed tank — Strawberry (Blue)","Old Navy","Tank","M Tall","","884929 / UPC 500148041809","",
    "'Santa Cruz Market - Fruit Growers Assoc.' strawberry graphic. New with tags. Official Old Navy image.","oldnavy_strawberry.jpg"),
 ("Ribbed tank — Summer by the Sea (Coral)","Old Navy","Tank","M","","897561 / UPC 500151603247","",
    "'Summer by the Sea / Cote d'Azur' shell graphic. New with tags. Official Old Navy image.","oldnavy_coral.jpg"),
 ("Ribbed fitted tee — Hotel de la Mer (Navy)","Old Navy","Tee","M","","687771 / UPC 500151806723","",
    "Red 'Hotel de la Mer' text with waves. Official Old Navy product image.","oldnavy_hotel.jpg"),
 ("Ringer tee — Jamaica (Black/Yellow)","","Tee","","","","",
    "Raglan baby/crop ringer tee, Jamaica flag graphic. Brand unknown. Size to confirm.","IMG_2468.jpg"),
 ("Sweat shorts — Grey '404 Not Found'","Urban Heritage","Shorts","L","","","",
    "French-terry drawstring shorts, '404 NOT FOUND' leg print. Made in China.","IMG_2469.jpg"),
 ("Air Jordan 4 Retro 'Metallic Purple'","Jordan","Shoes","","","CT8527-115","",
    "White / Court Purple / Metallic Silver. 2020 'Metallic Pack'. Retail $190.","jordan4_purple.jpg"),
 ("Footbed toe-loop sandals","White Mountain","Shoes","","","","",
    "Women's footbed thong sandal, strap over the big toe (Hayleigh-style toe loop). Brown leather.","white_mountain_sandal.jpg"),
]

# (name, brand, category, size, price, sku, notes, store)  -> shopping list
need = [
 ("Ribbed tank — Black (need XS)","Uniqlo","Tank","XS","","",
    "Exchange: didn't have a small — swapping for XS. Snap a photo to attach.","Uniqlo"),
 ("Ribbed tank — Grey (need XS)","Uniqlo","Tank","XS","","",
    "Exchange: didn't have a small — swapping for XS. Snap a photo to attach.","Uniqlo"),
]

seed = []
n = 1
for (name,brand,cat,size,price,sku,url,notes,pf) in have:
    seed.append({"id":f"seed{n}","status":"have","name":name,"brand":brand,"category":cat,
        "size":size,"price":(float(price) if price else ""),"sku":sku,"url":url,"notes":notes,
        "packed":False,"photo":dataURI(pf)})
    n += 1
for (name,brand,cat,size,price,sku,notes,store) in need:
    seed.append({"id":f"seed{n}","status":"need","name":name,"brand":brand,"category":cat,
        "size":size,"price":(float(price) if price else ""),"sku":sku,"url":"","notes":notes,
        "qty":1,"store":store,"specific":True,"packed":False,"photo":None})
    n += 1

with open(os.path.join(HERE, "template.html"), encoding="utf-8") as f:
    tpl = f.read()
html = tpl.replace("__SEED_JSON__", json.dumps(seed, ensure_ascii=False))
with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
print("Wrote", OUT, "|", len(seed), "items |", round(len(html.encode("utf-8"))/1024/1024, 2), "MB")
