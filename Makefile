0: VERSION
	mkzero-gfxmonk -p supergenpass_platform -p setup.py -p sgp-platform

dist: clean core platform

core:
	cd core && ./setup.py sdist

platform:
	cd platform && ./setup.py sdist

clean:
	rm -rf {core,platform}/{*.egg-info}

clobber: clean
	rm -rf {core,platform}/dist

list:
	find dist -iname '*.tar.gz' -exec echo --------- \; -exec zipinfo {} \;


.PHONY: dist clean list info platform core 0
