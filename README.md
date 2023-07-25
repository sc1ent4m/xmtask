This is part of a test task without:
* containers
* performance tests
* random sleeps on all routes (implemented only in POST order route)

### Setup and Environment
Python 3.10.6

Additional libraries can be installed with the following command:
```
pip install -r requriments.txt
```

### How to start server

```
uvicorn server:app --reload
```

### How to run tests

```
pytest tests/ --html=report.html
```
For tests rerun server must be restarted

### Comments

This is my very first use of FastAPI, asyncio and WebSockets. I was focused on that.

For performance tests I'd prefer Locust and Allure for reports. 
The other part of the task I can do in PR.