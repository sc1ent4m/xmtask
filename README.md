This is part of a test task without:
* random sleeps on all routes (implemented only in POST order route)

### Setup and Environment
Python 3.10.6

Additional libraries can be installed with the following command:
```commandline
pip install -r requirements.txt
```

### How to start server

```commandline
uvicorn app.server:app --reload
```

### How to run tests

```commandline
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
```commandline
docker run  --name appcontainer  -p 8000:8000 server_app_image
```
3) Run tests:
```commandline
docker run --name testcontainer --net=host pytest_image
```
### Run performance tests
Simply run following command:
```commandline
LOCUST_PLAYWRIGHT=1 locust -f tests/perftest.py --headless -u 100 -r 100  -i 100 -t 20 --host http://127.0.0.1:8000/
```
After execution standard deviation and average order execution will appear in the console:
Here is stdout example:
```
Response time percentiles (approximated)
Type     Name                                                                                  50%    66%    75%    80%    90%    95%    98%    99%  99.9% 99.99%   100% # reqs
--------|--------------------------------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
WSR      EXECUTED msg received                                                                 790    870    920    960   1000   1100   1100   1100   1100   1100   1100    100
--------|--------------------------------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
         Aggregated                                                                            790    870    920    960   1000   1100   1100   1100   1100   1100   1100    100
Standard deviation is - 242ms
Average order execution is - 721ms
```
