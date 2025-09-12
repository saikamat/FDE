# Hello Worlds of FDE
We’ll build a tiny app that:

1. Has a backend (FastAPI) with one endpoint: /hello.
2. Has a simple frontend (HTML + fetch call) to display the backend response.
3. Stores the requests in a database (SQLite for now).
4. Is deployed on the cloud (Heroku to start, later AWS/GCP).
5. Has a CI/CD pipeline with GitHub Actions.

## 1. Backend (Fast API)
Every time you access `/hello?name=YourName`, it logs the name to the database and returns a greeting.

### Executing
```bash
uvicorn app.main:app --reload
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

## 2. A simple frontend (HTML + fetch call) to display the backend response.
Check [index.html](index.html)

## 3. Is deployed on the cloud (Heroku to start, later AWS/GCP).
- Add a [Procfile](Procfile), which tells Heroku how to start your app.
- Add the [requirements.txt](requirements.txt) file
- Push the code to GitHub
- Create and Deploy Heroku App
```bash
heroku login
heroku create hello-fde-prototype
git push heroku main
```

- If you run into trouble here, check [Heroku Deployment Notes](#Heroku-Deployment-Notes)


- Once deployed, Heroku gives you a URL like:
```bash
https://hello-fde-prototype.herokuapp.com
```

- Since only our `/hello` path is active, visit
```bash
https://hello-fde-prototype.herokuapp.com/hello?name=venom
```

![image](/images/Screenshot2025-09-12at16.57.38.png)


# Heroku Deployment Notes

When deploying this FastAPI app to Heroku, I ran into a few common issues.  
Here’s a quick summary of the fixes.

---

### 1. Requirements
Make sure `requirements.txt` is in the project root:

```bash
pip freeze > requirements.txt
```

### 2. Procfile
Define how Heroku should run the app.

If `main.py` is in the root:
```bash
web: uvicorn main:app --host=0.0.0.0 --port=${PORT}
```

If `main.py` is in the in the `app` folder:
```bash
web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT}
```

### 3. Concurrency Setting (Applicable to Free Tier only)
By default, Heroku runs 2 workers → leads to memory crash (`exit code 137`).
Fix by forcing a single worker:
```bash
heroku config:set WEB_CONCURRENCY=1
```

### 4. Database Notes
- SQLite works for local development.
- On Heroku, SQLite is unreliable (ephemeral filesystem + multiple workers).
- For production, use Heroku Postgres or another external DB.

### 5. Logs
Check live logs when debugging:
```bash
heroku logs --tail
```
