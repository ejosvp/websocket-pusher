build:
	docker build --force-rm -t deli-ws-server .

bash:
	docker run -it --rm deli-ws-server bash

run:
	docker run -d deli-ws-server

deps:
	pip install --no-cache-dir -r requirements.txt

.PHONY: build bash run deps