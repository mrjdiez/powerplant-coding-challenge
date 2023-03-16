.PHONY: venv tests
.EXPORT_ALL_VARIABLES:
FLASK_APP = src/app.py
PYTHONPATH = src

build:
	docker build src -f src/Dockerfile --tag engie:test

docker:
	docker run --detach --name=engie engie:test --port 8888:8888

docker-logs:
	docker logs engie

docker-kill:
	docker kill engie
	docker rm engie

venv:
	python3 -m venv venv
	. ./venv/bin/activate && pip install -r src/requirements.txt
	. ./venv/bin/activate && pip -V

tests:
	. ./venv/bin/activate && python -m unittest discover src/tests -v

flask:
	export FLASK_APP=src/app.py
	export PYTHONPATH=src
	printenv | grep FLASK

	. ./venv/bin/activate && flask run --host=0.0.0.0 --port=8888

clean:
	rm -rf venv
	docker image rm engie:test