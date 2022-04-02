SRC = xdgprefs requirements.txt setup.py

build-wheel: $(SRC)
	python setup.py bdist_wheel

install: $(SRC)
	python setup.py install

clean:
	rm -rf build dist XDG_Prefs.egg-info
