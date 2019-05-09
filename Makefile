setup:
	pip install -r compute/requirements.txt
	npm install
	mkdir uploaded

clean:
	# touch first so if one dir empty both are cleaned anyway
	touch compute/out/fill uploaded/fill
	rm compute/out/* && rm -r uploaded/*

dry-run:
	python gainer.py

dev:
	npm run start-dev

start:
	npm run start