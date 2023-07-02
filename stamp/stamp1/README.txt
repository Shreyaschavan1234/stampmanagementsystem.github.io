install virtual environment by typing follwing command in terminal:
    pip install virtualenvwrapper-win

create a virtual environment by any name u want...
example:
    mkvirtualenv any_name

Enter in the virtual environment...
example:
    workon any_name
[By default it gets entered after creattion of the environment. But in case you lose it, type the above command]

Extract the project and open the project in vs code from the root folder (where manage.py file can be called)

The type the following command in the terminal:
    pip install - r requirements.txt

This will install the required packages for thw project.

Create the database with the same name mentioned in settings.py.

Then apply migration by following command:
    python manage.py migrate

Then run the project
    python manage.py runserver