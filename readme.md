# Requirements
- Flask
- Flask-SQLAlchemy
- flask-restful

# Local Development Run
A virtual environment named venv is already present in the folder
Activate the virtual environment by using the command  `venv\Script\activate`.
Run the app.py file using python by running command `python app.py`.


# Folder Structure

- `db_directory` has the sqlite DB. It can be anywhere on the machine. Adjust the path in ``application/config.py`. Repo ships with one required for testing.
- `application` is where our application code is
- `static` - default `static` files folder. It serves at '/static' path. More about it is [here](https://flask.palletsprojects.com/en/2.0.x/tutorial/static/).
- `static` - contains CSS styling. You can edit it. Its currently empty.
- `templates` - Default flask templates folder. Contains all the http templates of the project.
