from flask import Flask , redirect , url_for , render_template 
from flask_mysqldb import MySQL



app=Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='rootroot'
app.config['MYSQL_DB']='mobilerepair'
app.config['MYSQL_CURSORCLASS']= 'DictCursor' 

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
 


@app.route("/contact")
def test():
    return render_template("contact.html")




if __name__=="__main__":
    app.run(debug=True)
