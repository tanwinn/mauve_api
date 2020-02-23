# Mauve Server 
FastAPI Mauve Server with MongoDB

Deployed: https://mauve-server-2020.herokuapp.com

GitHub: https://github.com/tanwinn/pearlhacks_server

Submission of Pearlhacks2020

## Dev setup

```bash
git clone git@github.com:tanwinn/pearlhacks_server.git
cd pearlhacks_server
pipenv shell  # activate venv
pipenv sync # sync the dependencies packages
```

## Download MongoDB Server Or connect to the MongoDB Cluster Atlas

__.env file__
```bash
MONGO_CONN_STR=mongodb+srv://mauve:<PASSWORD>@cluster0-kz2za.mongodb.net/test?retryWrites=true&w=majority
```
Make sure to reset the pipenv shell to apply the change

## Run the App
```bash
uvicorn mauve_api.main:app --reload  # Run the app
```

### TODO:
Add Pytest as the testing framework
