artFlask
========

artFlask

Deploying:
install requirements:
mkvirtualenv art_flask
pip install -r requirements.txt

Initialize DB structure:
python
>>> from app import db
>>> db.create_all()

Running:
Just launch run.py

Testing:
For some reason, nosetests by default fails to correctly parse and run tests with no params specified.
So far, the working scheme to run tests using nose:
nosetests tests.art
nosetests tests.person
etc.

