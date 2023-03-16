# Engie Test

I've tried to make this test as lean as possible while making sure the different components are clearly defined and separated, to make sure that the project complies with the SOLID principles.

## Structure

The source code of the project is contained in the src directory. In the same folder there is a tests folder with the tests of the project. 

I've provided a makefile to the project to make easier working with the project in *NIX platforms as have been shown in the later parts of this readme. 
I have also provided some requests files in common formats that I believe can make easier the testing of the project.

As the project have been fully developed in a Mac OS computer the windows instruction can fail by unexpected steps. 

## Running the server

To run the server you can choose between two options. Both should work just fine. In case you're using a *NIX system the makefile provided should be able to make your work pretty straightforward. In case you are trying to build the project using a Windows system, there will be available further instructions. 

The windows instructions have not been fully tested and can be unreliable. 

### Docker

To build and run the docker image you can follow these steps

```shell
make build
make docker
```
If you want to see the logs of the server run 
```shell
make docker-logs
```
After you're finished and want to kill the server you can just run the following commands

```shell
make docker-kill
```

#### Windows

If you are running this within windows you can run the next commands
```shell
docker build src -f src/Dockerfile --tag engie:test
docker run --detach --name=engie engie:test --port 8888:8888
```
To get the logs
```shell
docker logs engie
```
Once ended to kill the server
```shell
docker kill engie
docker rm engie
```

### Python
If you want to get the server running without using docker or you don't have docker set up in your computer, you can run the server using python in your platform. 

To make that you will need to create a virtual environment, install the dependencies and finally run the server. 

```shell
make venv
make flask
```
Or if you're using windows

```cmd
python.exe -m venv venv
./venv/Scripts/Activate.ps1
pip.exe install -r src\requirements.txt
$Env:FLASK_APP = "src\app.py"
$Env:PYTHONPATH = "src"
flask run --host 0.0.0.0 --port 8888
```

After you've finished testing the project just close it using ctrl+C or ctrl+D depending on your platform. 

## Running the tests

I've provided some API tests to make sure that the API runs smoothly. To run them just following the tests command.

```shell
make tests
```

## Cleaning

Once you've finished and to make sure that there are no further conflicts in the future, you can run some cleaning commands that have been provided. 

```shell
make clean
```

## Testing the API

To test the API we have provided a .http requests file compatible with PyCharm that allows you to send HTTP requests using the IDE. And a postman collection that contains the same requests.

If you're using a system with access to curl you can run the following commands to test de API

```shell
curl localhost:8888/
curl localhost:8888/productionplan -X POST -H "Content-Type: application/json" -d @example_payloads/payload1.json
curl localhost:8888/productionplan -X POST -H "Content-Type: application/json" -d @example_payloads/payload2.json
curl localhost:8888/productionplan -X POST -H "Content-Type: application/json" -d @example_payloads/payload3.json
```