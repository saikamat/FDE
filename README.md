# Hello Worlds of FDE
We’ll build a tiny app that:

1. Has a backend (FastAPI) with one endpoint: /hello.
2. Has a simple frontend (HTML + fetch call) to display the backend response.
3. Stores the requests in a database (SQLite for now).
4. Is deployed on the cloud (Heroku to start, later AWS/GCP).
5. Has a CI/CD pipeline with GitHub Actions.

## Backend (Fast API)
Every time you access `/hello?name=YourName`, it logs the name to the database and returns a greeting.

### Executing
```bash
uvicorn main:app --reload
```

![image](/images/Screenshot2025-09-12at15.58.12.png)

### SQLITE DB Check
You can also verify if the name entered your database using `sqlite3`
```bash
sqlite3 hello.db  # input command
SQLite version 3.43.2 2023-10-10 13:08:14
Enter ".help" for usage hints.
sqlite> SELECT * FROM logs; # input command
1|World
2|venom
4|venom
sqlite> .schema # input command
CREATE TABLE logs (id INTEGER PRIMARY KEY, name TEXT);
sqlite> .exit # input command
```