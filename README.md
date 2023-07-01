ad# E-commerce API
## A real world open source example of django-rest-framework (DRF)
### Project is UP & Running on https://alirezaabavi.pythonanywhere.com/
### some features:
- Compliance with the principles of test writing DRF
- Using JWT for authentication
- Compliance with the principles of clean coding
- Using view counter system
- Using Mysql for db (can be changed)
- Documented and visualized by Swagger & Redoc
#### It's a Django project based on DRF for e-commerce websites
#### Tests will be completed over time
- In terminal: `git clone https://github.com/AlirezaAbavi/ecommerce_api.git`
- cd `/ecommerce_api` Where the manage.py is
- In terminal: `python -m venv venv`
- activate your venv: in windows `cd venv\scripts\activate` in linux: `venv/bin/activate`
- Run `pip install requirements.txt`
- Run `python manage.py collectstatic`
- Run `python manage.py runserver --settings=ecommerce_api.settings.dev`
- Visit http://127.0.0.1:8000/swagger to read the api documentation
####that`s it...
