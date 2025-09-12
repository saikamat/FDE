# It imports FastAPI for building the API and sqlite3 for interacting with a SQLite database.
from fastapi import FastAPI
import sqlite3
from fastapi.responses import FileResponse
import os

# initializes the FastAPI app
app = FastAPI()

@app.get("/")
def root():
    return FileResponse(os.path.join(os.path.dirname(__file__), "..", "index.html"))

# /hello endpoint accepts a query parameter name (default is "World").
@app.get("/hello")


def read_root(name: str = "World"):
    # log and connects to a SQLite database
    conn = sqlite3.connect("hello.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, name TEXT)")

    # inserts the name into a logs table
    c.execute("INSERT INTO logs (name) VALUES (?)", (name,))
    conn.commit()
    conn.close() # commit and close DB connection

    # returns a JSON message containing the entered name
    return {"message": f"Hello, {name}!"}
