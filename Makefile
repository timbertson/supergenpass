eggs: sgp platform

sgp:
	make clean # this must happen EVERY TIME
	./setup-core.py bdist_egg

platform:
	make clean # this must happen EVERY TIME
	./setup-platform.py bdist_egg

clean:
	rm -rf build build.* *.egg-info

clobber: clean
	rm -rf dist

list:
	find dist -iname '*.egg' -exec echo --------- \; -exec zipinfo {} \;

info:
	./commonsetup.py

.PHONY: eggs clean list info