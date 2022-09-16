Run
===========

Clone repository

Install Python 3.10.0

Create and activate a virtualenv
```
py -m venv venv
./venv/Scripts/activate
```

Install requirements
```
pip install -r requirements.txt
```

Set flask variables
Windows cmd:
```
set FLASK_APP=flaskr
set FLASK_ENV=development
```
Powershell:
```
$env:FLASK_APP = "flaskr"
$env:FLASK_ENV = "development"
```

Initialize the database and run application
```
flask init-db
flask run
```

Go to [your local network address]/tuner/config (flask will display address in command line) and select an audio device!

For example: http://127.0.0.1:5000/tuner/config