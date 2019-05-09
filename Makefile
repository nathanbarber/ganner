install:
	pip install -r compute/requirements.txt
	npm install

cl-out:
	rm ./out/*

dry-run:
	python gainer.py

dev:
	npm run start-dev

start:
	npm run start