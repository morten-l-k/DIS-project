Assumes a working Python 3 installation (with python=python3 and pip=pip3).

(1) Run the code below to install the dependencies.
>$ pip install -r requirements.txt

(2) Initialize database: 
IMPORTANT: In 'Results Attributes.SQL' change the full path of the 'results.csv' file which is located in the tmp directory

>$ psql -h hostname -d dbname -U username -W

Create table users:
=# \i 'path/to/src/Create Users.SQL'

Create tabel 'results' and populate data:
=# \i '/path/to/src/Results Attributes.SQL'

(3) In app.py-file set own username and password

(4) Run web-app:

>$ python src/app.py


