eggs: core_egg main_egg

core_egg:
	make clean # this must happen EVERY TIME
	./setup_core.py bdist_egg

main_egg:
	make clean # this must happen EVERY TIME
	./setup.py bdist_egg

clean:
	rm -rf build build.* *.egg-info

clobber: clean
	rm -rf dist

list:
	find dist -iname '*.egg' -exec echo --------- \; -exec zipinfo {} \;

info:
	./commonsetup.py

.PHONY: eggs clean list info