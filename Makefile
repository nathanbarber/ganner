setup:
	pip install -r compute/requirements.txt
	npm install
	mkdir uploaded compute/.source compute/.gan_source compute/.out

clean:
	# touch first so if one dir empty is both are still cleaned
	touch compute/out/fill uploaded/fill
	rm compute/out/*
	rm compute/.source/*
	rm -r uploaded/*

dry-run:
	python gainer.py

dev:
	npm run start-dev

start:
	npm run start