# Django Tailwind, Django Phonenumbers, Crispy And Daraja Api
pip install django-tailwind

for the latest version use
python -m pip install <a>git+https://github.com/timonweb/django-tailwind.git

* Checkout the official documentation <a>https://django-tailwind.readthedocs.io/en/latest/installation.html
* add tailwind to your INSTALLED_APPS 'tailwind'
* create a 'tailwind' compatible app with the following command `python manage.py tailwind init`
* after the command has run you will be prompted to give a name for your tailwind theme or app
* add the theme app to your INSTALLED_APPS
* add the theme  app to your INSTALLED_APPS and run the `python manage.py tailwind install`
* register the generated theme app so tha django uses it by default `TAILWIND_APP_NAME = 'theme'`
* install tailwind css dependencies `python manage.py tailwind install`
* for windows users you need to define ` NPM_BIN_PATH = 'C:/Program Files/nodejs/npm.cmd'` after installing nodejs
* to use tailwind css classes in html start the development server `python manage.py tailwind start`
* once everything is setup you can create your app to use tailwind
* install django-phonenumber-field library https://django-phonenumber-field.readthedocs.io/en/latest/index.html
* `pip install "django-phonenumber-field[phonenumbers]"`
* use the library to create an additional field on the user table
* when abstracting the User model you need to specify the `AUTH_USER_MODEL='path to your custom user class'` in settings as your custom class
* install crispy library `pip install django-crispy-forms`
* install bootstrap compatible with crispy as a template pack `pip install crispy-bootstrap4` 
* update your INSTALLED_APPS add 'crispy_forms' and 'crispy_bootstrap4'
* set CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4" and CRISPY_TEMPLATE_PACK = "bootstrap4"
this is to set crispy_boostrap4 as default and allowed template pack
* link to daraja Api https://developer.safaricom.co.ke/Documentation



