install:
	pip install -r requirements.txt

cl-out:
	rm ./out/*

dry-run:
	python gainer.py