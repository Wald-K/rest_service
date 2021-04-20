# Rest_Service

Rest_Service is a Python service to search matching tags for given ip address in tags library.
Library is loaded from json file indicated in configuration.

## Technologies

Project is created with:
* python 3.9
* python main packages: Django == 3.2, gunicorn == 20.1.0, ipaddress == 1.0.23

Container tools:
* docker
* docker-compose

HTTP server:
* NGINX - version: 1.19.0-alpine

## Installation

Download project folder from github [repo](https://pip.pypa.io/en/stable/)
Insert into project folder
```bash
cd rest_service
docker-compose build
```

## Configuration
Before service start it should be configured. Following configuration set should be adjusted in django settings.py file to requirements:
* LIBRARY_PATH - path to Library file - relative path in rest_service folder. Default './library_data/library.json'
* LOGGING - json style setting. See Logging section

## Logging
As it was said in previous part project uses django build in logging system, which is described in [django official documentations](https://docs.djangoproject.com/en/3.2/topics/logging/). Default configuration was created.
Two loggers where definded:
* ip_request_logger - logging User request events;
* library_logger - logging library events.

These two loggers write events to console and file (default log file location is './logs/error.log').
Events with INFO log level are sent to console and events with ERROR log level are sent to console and stored in log file.
User can change these rules, by adjusting django setting.py file. 

## Usage
If you are not in project folder enter this directory and run docker-compose
```bash
cd rest_service
docker-compose up
```
After service start in console appears statement 'INFO Library file loaded successfully' and two endpoints will be active:
* http://localhost:8080/ip-tags/{ip}  - for JSON response
* http://localhost:8080/ip-tags-report/{ip} - for HTML response


## Tests
When service starts, user can launch tests using commands

```bash
sudo docker exec -it django-service sh
```
After that all definded tests will be launched.

## License
[MIT](https://choosealicense.com/licenses/mit/)
