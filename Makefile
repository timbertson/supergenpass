eggs:
	./setup_core.py bdist_egg -v
	./setup.py bdist_egg -v

clean:
	rm -rf build dist

list:
	find dist -iname '*.egg' -exec echo --------- \; -exec zipinfo {} \;

info:
	./commonsetup.py

.PHONY: eggs clean list info