from flask import Flask,redirect , url_for , render_template , request
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Uzumymw__007'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'mobile-repair'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql=MySQL(app)

def getid():
    cur=mysql.connection.cursor()
    cur.execute('''SELECT customerID FROM gives WHERE dropDate='2021-01-23' ''')
    results=cur.fetchall()
    return results

@app.route("/")
def home():
    id=getid()
    return render_template("status.html", id=id[0])
 
@app.route("/contact", methods = ["POST", "GET"])
def test():
    if request.method == "POST":
        user1 = request.form['nm']
        user2 = request.form['ph']
        user3 = request.form['em']
        user4 = request.form['dt']
        user5 = request.form['dn']
        user6 = request.form['dpd']
        return redirect(url_for("user", usr=user1))
    else:
        return render_template("contact.html")

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

if __name__=="__main__":
    app.run(debug=True)