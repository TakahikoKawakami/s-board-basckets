# LOOK INTO BASKETS
this app is to analyze transactions in your store with SMAREGI services.

# use languages
- python 3.8.0
- mysql
- pug

# use flameworks
- responder v1.3.0
- tortoise-orm v0.20.0
- jinja2 (pug extensions)

# usage
`git clone`  
`pip install -r requirements.txt`  
if you use pipenv, 
`pipenv install -r requirements.txt`
`python3 run.py`  
or if you use vs-code, you can run for debug named "Python: Responder".  

`cd app/static && npm install`

`sudo apt install -y ruby && gem install -y ultrahook`

in devcontainer, to catch webhook from smaregi, exec command as following:
`ultrahook look-into-baskets http://0.0.0.0:5500/webhook`
