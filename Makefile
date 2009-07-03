dist: clean sgp platform

sgp:
	cd core && ./setup.py sdist

platform:
	cd core && ./setup.py sdist

clean:
	rm -rf {core,platform}/{build*,*.egg-info}

clobber: clean
	rm -rf {core,platform}/dist

list:
	find dist -iname '*.tar.gz' -exec echo --------- \; -exec zipinfo {} \;

info:
	./commonsetup.py

.PHONY: dist clean list info
