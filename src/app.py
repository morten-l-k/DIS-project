from flask import Flask, render_template, redirect, url_for, session, request, flash
import re
import psycopg2
from flask_bcrypt import Bcrypt
import os



app = Flask(__name__ , static_url_path='/static')

# set your own database name, username and password
db = "dbname='XXXX' user='XXXX' host='localhost' password='XXX'" #potentially wrong password
conn = psycopg2.connect(db)
cursor = conn.cursor()


bcrypt = Bcrypt(app)

@app.route("/", methods=['POST','GET'])
def home():
    cur = conn.cursor()
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if request.method == 'POST':
            home_team = request.form['home_team']
            away_team = request.form['away_team']
            cur.execute(f'''SELECT * 
                            FROM results
                            WHERE home_team = '{home_team}' and away_team = '{away_team}' ''')
            matches = list(cur.fetchall())
            length = len(matches)
            
            return redirect(url_for("queryresults", hometeam=home_team, awayteam=away_team))
    
    return render_template("versus.html")

@app.route("/<hometeam>/<awayteam>")
def queryresults(hometeam, awayteam):
    cur = conn.cursor()
    
    cur.execute(f'''SELECT * 
                    FROM results
                    WHERE home_team = '{hometeam}' and away_team = '{awayteam}' ''')
    
    matches=list(cur.fetchall())

    length = len(matches)
    
    return render_template("versusquery.html", content=matches, length=length)

@app.route("/createaccount", methods=['POST', 'GET'])
def createaccount():
    cur = conn.cursor()
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        
        if re.search(r'[A-Z]+([a-z]*|[!@#$%^&*(),.?":{}|<>_]*|[\d]*|[A-Z]*)*', new_username) == None:
            flash('Username must start with a capital letter!', 'username_error')
            return render_template("createaccount.html")
        if re.search(r'([a-z]*|[!@#$%^&*(),.?":{}|<>_]*|[\d]*|[A-Z]*)*[!@#$%^&*(),.?":{}|<>_]+([a-z]*|[!@#$%^&*(),.?":{}|<>_]*|[\d]*|[A-Z]*)*', new_password) == None:
            flash('Password must have one special character!', 'password_error')
            return render_template("createaccount.html")
        cur.execute(f'''select * from users where username = '{new_username}' ''')
        unique = cur.fetchall()
        flash('Account created!')
        if  len(unique) == 0:
            cur.execute(f'''INSERT INTO users(username, password) VALUES ('{new_username}', '{new_password}')''')
            flash('Account created!')
            conn.commit()

            return redirect(url_for("home"))
        else: 
            flash('Username already exists!')


    return render_template("createaccount.html")


@app.route('/login', methods=['POST'])
def do_admin_login():
    cur = conn.cursor()
    username = request.form['username']
    password = request.form['password'] 

    insys = f''' SELECT * from users where username = '{username}' and password = '{password}' '''

    cur.execute(insys)

    ifcool = len(cur.fetchall()) != 0

    if ifcool:
        session['logged_in'] = True
        session['username'] = username
    else:
        flash('wrong password!')
    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route("/profile")
def profile():
    cur = conn.cursor()
    if not session.get('logged_in'):
        return render_template('login.html')
    
    username = session['username']

    return render_template("profile.html", username=username)

@app.route("/updpass", methods=['POST', 'GET'])
def updpass():
    cur = conn.cursor()
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if request.method == 'POST':
            new_password = request.form['password']
            if re.search(r'([a-z]*|[!@#$%^&*(),.?":{}|<>_]*|[\d]*|[A-Z]*)*[!@#$%^&*(),.?":{}|<>_]+([a-z]*|[!@#$%^&*(),.?":{}|<>_]*|[\d]*|[A-Z]*)*', new_password) == None:
                flash('Password must have one special character!', 'password_error')
                return render_template('updpass.html')
            username = session['username']
            updPassSql = f'''UPDATE users SET password = '{new_password}' WHERE username = '{username}' '''
            cur.execute(updPassSql)
            conn.commit()
            return redirect(url_for("home"))
        return render_template('updpass.html')
    
@app.route("/delete-user", methods=['POST'])
def deleteuser():
    cur = conn.cursor()

    user_name = session['username']

    sql_delete = f''' DELETE FROM users
               WHERE username = '{user_name}' '''
    
    print(sql_delete)

    cur.execute(sql_delete)
    conn.commit()
    
    session['logged_in'] = False

    return home()
    

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
