Assumes a working Python 3 installation (with python=python3 and pip=pip3).

(1) Run the code below to install the dependencies.
>$ pip install -r requirements.txt

(2) Initialize database: 
IMPORTANT: In 'Results Attributes.SQL' change the full path of the 'results.csv' file which is located in the tmp directory

RUN:
>$ psql -U dbownername -d dbname

Create table users:
=# \i 'path/to/src/Create Users.SQL'

Create tabel 'results' and populate data:
=# \i '/path/to/src/Results Attributes.SQL'

(3) In app.py-file set own username and password

(4) Run web-app:

>$ python src/app.py

----------------------------------------------------------------------------------------------

# How to use the application:

(1) Create account / You start by pressing the 'Create Account' button, you then get to page where you choose your username and password. The username must contain a capital letter, and the password must have atleast one special character (!@#$%^&*(),.?":{}|<>_)

(2) Login / Now you can login on your account by typing in your username and password.

(3) Frontpage / you see two fields, one for home team and one for away team - these country names must start with a capital letter - click search - all matches with given teams as home and away team will be visible underneath (e.g. home team = "Denmark" and away team "Sweden", click search - will show all matches, where Denmark played against Sweden as home team)

(4) Profile / Here you can update your accounts password (still required to have at least one special character) - will transfer you to the update password page - you can also delete your profile, and be retransfered to the login screen 






