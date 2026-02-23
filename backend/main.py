from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import csv
import sqlite3

app = FastAPI()
#app = FastAPI(docs_url=None, redoc_url=None

origins = [
    "https://freyartt.com",
    "https://www.freyartt.com",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:8800",
    "http://127.0.0.1:8800",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],  # Since your app only "reads" data, only allow GET
    allow_headers=["*"],
)

# 1. SETUP THE DATABASE
# ":memory:" means it lives in RAM—super fast!
conn = sqlite3.connect(":memory:", check_same_thread=False)
conn.row_factory = sqlite3.Row # This allows us to access data like a dictionary
cursor = conn.cursor()

# Create the table structure
cursor.execute('''
    CREATE TABLE venues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        lat REAL,
        lng REAL,
        type TEXT,
        address TEXT,
        description TEXT,
        phone TEXT,
        website TEXT,
        mon INTEGER,
        tue INTEGER,
        wen INTEGER,
        thu INTEGER,
        fri INTEGER,
        sat INTEGER,
        sun INTEGER,
        payment INTEGER,
        price REAL,
        info_website TEXT
    )
''')

# 2. LOAD DATA ON STARTUP
def startup_load():
    with open("venues.csv", mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute('''
                INSERT INTO venues (name, lat, lng, type, address, description, phone, website, mon, tue, wed, thu, fri, sat, sun, payment, price, info_website )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (row['name'], 
                float(row['lat']), 
                float(row['lng']), 
                row['type'],
                row['address'], 
                row['description'], 
                row['phone'], 
                row['website'], 
                int(row['mon']),   # Convert to Integer
                int(row['tue']),   # Convert to Integer
                int(row['wed']),   # Ensure CSV column name is 'wed'
                int(row['thu']),
                int(row['fri']),
                int(row['sat']),
                int(row['sun']),
                int(row['payment']),
                float(row['price']) if row['price'] else 0.0, 
                row['info_website']))
    conn.commit()

# Run the loader once
startup_load()

@app.get("/")
def read_root():
    return {"status": "Pro API with SQLite is running"}

@app.get("/venues")
def get_venues():
    # 3. QUERY THE DATABASE
    cursor.execute("SELECT * FROM venues")
    # Convert SQL rows into a list of dictionaries for JSON
    rows = [dict(row) for row in cursor.fetchall()]
    return rows

# Bonus: High-volume "Search" example
@app.get("/venues/search")
def search_venues(type: str):
    cursor.execute("SELECT * FROM venues WHERE type = ?", (type,))
    return [dict(row) for row in cursor.fetchall()]