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


## 5. Has a CI/CD pipeline with GitHub Actions
### Setting Environment Secrets
#### Create Heroku API KEY
You will need the API key to connect GitHub with Heroku. Use this command in the CLI:-
```bash
heroku auth:token
```
#### Add Secrets in GitHub
- In Github, head to `Settings` 
![image](/images/Screenshot2025-09-13at21.33.30.png)
- Then to `Secrets and Variables` and then `Actions`
![image](/images/Screenshot2025-09-13at21.33.53.png)

- Add the secrets:- `HEROKU_API_KEY`, `HEROKU_APP_NAME`, `HEROKU_EMAIL`
- Use the API key that created [above](#Create-Heroku-API-KEY)
![image](/images/Screenshot2025-09-13at21.40.42.png)

### Creating the Deployment Config file
- Create a file `.github/workflows/deploy.yml`
- You can find it here: [.github/workflows/deploy.yml](.github/workflows/deploy.yml)
- You don’t "RUN" a GitHub Actions workflow manually on your laptop. It’s event-driven.
- Workflows are triggered by the events you defined:
```yaml
# deploy.yml
on:
  push:
    branches: [ main ]
```
- So when you push to `main` branch, the GitHub Actions that you configured above will auto-start the pipeline
- You can check this by going to to your GitHub Repo --> `Actions`
![image](/images/Screenshot2025-09-13at21.47.10.png)
- You’ll see the workflow “CI/CD to Heroku” running
![image](/images/Screenshot2025-09-13at22.42.43.png)
- You can also check status in Heroku App
![image](/images/Screenshot2025-09-13at21.55.36.png)
- 
![image](/images/Screenshot2025-09-13at21.57.55.png)

---
## Deployment Notes

### Heroku
When deploying this FastAPI app to Heroku, I ran into a few common issues.  
Here’s a quick summary of the fixes.

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

---
### CI/CD
We set up a GitHub Actions workflow (`deploy.yml`) to automatically deploy a FastAPI app to Heroku whenever code was pushed to main.
The workflow used the `akhileshns/heroku-deploy@v3.12.12`

#### The Issue
When the workflow ran, the deploy step failed with the following error:
![image](/images/Screenshot2025-09-13at21.47.17.png)
![image](/images/Screenshot2025-09-13at21.47.27.png)

#### Root Cause
- The heroku-deploy action expects the Heroku CLI to be available on the GitHub runner.
- GitHub’s ubuntu-latest runners no longer include the Heroku CLI by default.
- As a result, the action couldn’t find the heroku command, leading to a failed deployment.

The Fix
- Explicitly install the Heroku CLI before running the deploy step.