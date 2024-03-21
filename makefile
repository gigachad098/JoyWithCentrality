copyfiles:
	cp $(filepath) .

run:
	python3 search.py asu-domain.txt

compile:
	@echo 'Python solution'

list:
	ls *.py

show:
	cat search.py
	cat utility.py