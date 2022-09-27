# Django Start Project Custom Command
First Create a virtualenv and activate it, then install requirements.

This command Creates a django project with the app which is provided in --app argument.
If setting argument is set to t then settings file will change too.

`python manage.py startproject2 <project name> --app <app name> --setting t`


This command creates serializers and views for the model provided in argument.

`python manage.py createserializers --app <app name> --model <model name>  
`

