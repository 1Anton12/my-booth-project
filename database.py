import aiosqlite
import datetime
import json

DB_PATH = "booth_bot.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        # Таблица пользователей
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                language TEXT DEFAULT 'EN',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Таблица заказов
        await db.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                length REAL,
                width REAL,
                construction_type TEXT,
                materials TEXT,
                equipment TEXT,
                total_price REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)
        await db.commit()

async def add_user(user_id, username, full_name, language):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO users (user_id, username, full_name, language) VALUES (?, ?, ?, ?)",
            (user_id, username, full_name, language)
        )
        await db.commit()

async def save_order(user_id, length, width, construction_type, materials, equipment, total_price):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO orders (user_id, length, width, construction_type, materials, equipment, total_price) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, length, width, construction_type, json.dumps(materials), json.dumps(equipment), total_price)
        )
        await db.commit()

async def get_user_orders(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC", (user_id,)) as cursor:
            return await cursor.fetchall()
