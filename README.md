[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

# Joogle

A search engine made for CSI 4107. Currently supports searching the uOttawa CSI course catalogue.



## Instructions

### Live Site

To save time, it is recommended that you go to http://joogle-csi4107.herokuapp.com, where you will find the project live. This will save you the time of downloading any dependencies. However, if you wish to execute locally, follow the instructions below.

### Local Installation

First, in your shell, run:

```shell
$ ./install.sh # or install.bat on windows
```

This will install several Python packages, as well as download stopwords and a lemmatizer from `nltk`. 

Then, to run the app, run:

```shell
$ python app.py
```

Then, navigate to http://localhost:4999/ to access the app (or http://127.0.0.1:4999 if this fails).