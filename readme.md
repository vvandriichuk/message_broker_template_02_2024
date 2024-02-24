1. For running check of the code, run:

```
ruff check app
```

2. For running the formatting of the code, run:

```
ruff format app
```

3. To run the project manualy, run:

```
poetry shell
python test_request_to_flask_api.py
```

4. Before running the project in docker create docker network:

```
docker network create test-fastapi-sql-network
```
5. Run the project in docker:

```
docker-compose up
```