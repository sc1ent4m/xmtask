This is part of a test task without:
* performance tests
* random sleeps on all routes (implemented only in POST order route)

### Setup and Environment
Python 3.10.6

Additional libraries can be installed with the following command:
```
pip install -r requirements.txt
```

### How to start server

```
uvicorn app.server:app --reload
```

### How to run tests

```
pytest tests/ --html=report.html
```
For tests rerun server must be restarted

### Run tests using Docker
1) Build images:
```
docker build -f ServerDockerfile -t server_app_image .
docker build -f TestsDockerfile -t pytest_image .
```
2) Start server:
```
docker run  --name appcontainer  -p 8000:8000 server_app_image
```
3) Run tests:
```
docker run --name testcontainer --net=host pytest_image
```

### Comments

This is my very first use of FastAPI, asyncio and WebSockets. I was focused on that.

For performance tests I'd prefer Locust and Allure for reports. 
The other part of the task I can do in PR.