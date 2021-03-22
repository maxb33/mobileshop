from flask import Flask , redirect , url_for , render_template 
from flask_mysqldb import MySQL



app=Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='rootroot'
app.config['MYSQL_DB']='mobilerepair'
app.config['MYSQL_CURSORCLASS']= 'DictCursor'

mysql=MySQL(app)

@app.route("/")
def home():
    # cur=mysql.connection.cursor()
    # cur.execute('''SELECT imeiNumber,os FROM device WHERE os='mac' ''')
    # results=cur.fetchall()
    # print(results)



    return render_template("status.html")
 


@app.route("/test")
def test():
    return render_template("new.html")




if __name__=="__main__":
    app.run(debug=True)
