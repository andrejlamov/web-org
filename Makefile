CPU := $(shell uname -m)
ifneq ($(CPU), x86_64)
	CPU = x86
endif

MINICONDA = Miniconda-latest-Linux-$(CPU).sh

SEM_TAG := 2.1.8
JQ_VER := 2.2.0
D3_VER := v3


all: env/bin/python static
	env/bin/python server.py

env/bin/python: 
	curl https://repo.continuum.io/miniconda/$(MINICONDA) -o miniconda.sh
	sh miniconda.sh -b -p ./env
	env/bin/pip install --upgrade pip
	env/bin/pip install -r requirements.txt

static: 
	mkdir -p static static/semantic
	ln -sf ../templates/index.css static/index.css
	curl https://codeload.github.com/Semantic-Org/Semantic-UI-CSS/tar.gz/$(SEM_TAG) | tar xzv -C static/semantic --strip-components=1
	cd static && curl  http://code.jquery.com/jquery-$(JQ_VER).min.js -o jquery.min.js
	cd static && curl -O http://d3js.org/d3.v3.min.js
	cd static && curl -O http://cdnjs.cloudflare.com/ajax/libs/socket.io/1.3.5/socket.io.min.js

clean:
	rm -rf env static $(MINICONDA) *.pyc miniconda.sh
