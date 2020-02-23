# Mauve Server 
FastAPI Mauve Server with MongoDB
Deployed: https://mauve-server-2020.herokuapp.com
GitHub: https://github.com/tanwinn/pearlhacks_server

## Dev setup

```bash
pipenv shell  # activate venv
pipenv sync # sync the dependencies packages
uvicorn app.main:app --reload  # Run the app
```

__.env file___
```bash
MONGO_CONN_STR=mongodb+srv://mauve:pearlhacks@cluster0-kz2za.mongodb.net/test?retryWrites=true&w=majority
```

Make sure to reset the pipenv shell to apply the change
