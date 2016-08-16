# Ouranos
[![Build Status](https://travis-ci.com/lukekearney/research-practicum.svg?token=9AQVD3a9aH85bqC19gfz&branch=master)](https://travis-ci.com/lukekearney/research-practicum)

Ouranos is a Flask web application enabling predictive analytics of room occupancy on the University College Dublin Belfield campus.

  - Using ground truth data collected on campus
  - Development and cross-validation of various predicitive models
  - Implementation of result in a web application
  - Deployment onto Ubuntu virtual machine

You can also:
  - Add new data
  - Drag and drop files into the "Upload new data" section


> Develop a software system that will reflect whether a room is occupied or not
and estimate room occupancy based on wifi log data.
>Teams have freedom to decide on the scope. 

> The application developed also incorporates Received Signal Strength Indicator (RSSI) and audio data.
> This improves the predictive ability of our models answering the binary question: "Is the room occupied?"

### Version
1 . 3

### Tech Stack

Ouranos uses a number of open source projects to work properly:
* [Python 3.5.x] -
* [AngularJS] - HTML enhanced for web apps!
* [Flask] - Mico-web server for Python web apps
* [node.js] - evented I/O for the backend. Ouranos uses this to install front-end dependencies via NPM
* [node-sass] - CSS with more features
* [SQLite] - software library that implements a self-contained, serverless, zero-configuration, transactional SQL database engine.



### Installation

Ouranos requires:
- Node JS
- Python3 
 be installed.

On Linux, some packages (such as Pandas and Sci-kit learn) may need to installed through apt-get. 

To install Ouranos:
```sh
$ git clone https://github.com/lukekearney/research-practicum
```

Run the install script, which will prompt you if you need to install additional technologies
```sh
python install.py
```

Alternatively, if you just need the python dependencies
```sh
pip install -r requirements.txt
```



### Required Libraries

File Handling:              os, sys, subprocess, ZipFile
	
Data Gathering:			    csv, OpenPyXL, time, re

Data Cleaning:              Pandas, NumPy, SQLite3
					
Data Analysis:              Scikit Learn, StatsModels
	
Data Visualization:         MatPlotLib
	
Web App:				    Flask, flask_login, flask_wtf, peewee, flask_peewee, flask_mail

Testing:                    werkzeug, unittest, tempfile

Additional libraries [here]

### Development

Want to contribute? Great!



### Todos
 - Addition of Classes to Time Table
 - Write Tests
 - Add Code Comments


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