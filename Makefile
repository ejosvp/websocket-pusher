build:
	docker build --force-rm -t deli-ws-server .

bash:
	docker run -it --rm deli-ws-server bash

run:
	docker run -d -p 8084:1234 -p 8085:1235 --name ws-server deli-ws-server

start:
	docker start ws-server

stop:
	docker stop ws-server

rm:
	docker rm ws-server

deps:
	pip install --no-cache-dir -r requirements.txt

.PHONY: build bash run deps start stop rm