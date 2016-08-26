![WiSpy Logo](/app/static/WiSpyBanner.png?raw=true "WiSpy Logo")

[![Build Status](https://travis-ci.com/lukekearney/research-practicum.svg?token=9AQVD3a9aH85bqC19gfz&branch=master)](https://travis-ci.com/lukekearney/research-practicum)

WiSpy is a Flask web application predicting room occupancy across the University College Dublin campus based on historical Wi-Fi log data. It also employs RSSI and audio data alongside face detection methods in rooms with a leaking Wi-Fi signal.  

Users can:
  - View predicted occupancy (both occupancy sensing and a continuous headcount) for any room and period for which we have data. 
  - Compare the occupancy of different rooms and classes.
  - Add new data by dragging and dropping files on the "Upload new data" page.

### Version
1 . 3

### Technologies

WiSpy uses a number of open-source projects:
* [Python 3.5.x] - 
* [AngularJS] - HTML enhanced for web apps
* [Flask] - Micro-web framework for Python apps
* [node-sass] - CSS with more features
* [SQLite] - software library that implements a self-contained, serverless, zero-configuration, transactional SQL database engine.
* [node.js] - used to install front-end dependencies via NPM
* Various Python modules used for statistical modelling, database interaction and data gathering, installed via requirements.txt. 

### Installation

WiSpy requires Node.JS Python 3 be installed.

To install WiSpy:
```sh
$ git clone https://github.com/lukekearney/research-practicum
```

Run the install script, which will prompt you if you need to install any dependencies: 
```sh
python install.py
```

Python dependencies are installed via:
```sh
pip install -r requirements.txt
```

License
----

MIT

**Free Software**

[//]: # (These are reference links used in the file. http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [Python 3.5.x]: <https://docs.python.org>
   [Flask]: <http://flask.pocoo.org/>
   [node.js]: <http://nodejs.org>
   [jQuery]: <http://jquery.com>
   [AngularJS]: <http://angularjs.org>
   [node-sass]: <https://github.com/sass/node-sass>
   [SQLite]: <https://www.sqlite.org/>
   [here]: <https://github.com/lukekearney/research-practicum/blob/master/app/static/package.json>
