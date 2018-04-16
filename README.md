# gummy-app

Website is an example found online
Functional tests with Selenium are in gummy/tests folder

To run tests on local machine:
1. Install python3
2. Download chromedriver (https://sites.google.com/a/chromium.org/chromedriver/) and add it to PATH
3. Put project files somewhere and cd to base folder (gummy-app)
4. pip install -r requirements.txt
5. Create .env file in base folder and put following into it
```
SECRET_KEY=dxn=gj(vh40_+%gs=)olt3zt2p$e#zhq+kmkkmi0lge7j+z%tw
DEBUG=True
ALLOWED_HOSTS=.locahost,testserver,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```
6. python manage.py test gummy.tests.tests 
