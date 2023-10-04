from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app= Flask(__name__)
mysql = MySQL(app)


app.config ['MYSQL_HOST'] = 'localhost'
app.config ['MYSQL_USER'] = 'root'
app.config ['MYSQL_PASSWORD'] = "peloris_100"
app.config ['MYSQL_DB'] = 'management_system'

@app.route("/", methods = ['GET','POST']) 
def index():
    if request.method == 'POST':
        username= request.form['username']
        email= request.form['email']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name,email) values (%s,%s)",(username,email))
        mysql.connection.commit()
        cur.close()
        return "Successfully updated Record in Database"
    return render_template('index.html')

@app.route("/users")
def getusers():
    cur = mysql.connection.cursor()
    user = cur.execute("SELECT * FROM users")
    if user >0:
        userDetails = cur.fetchall()
    return render_template('users.html', myuser=userDetails)




in_memory_datastore = {
   "COBOL" : {"name": "COBOL", "publication_year": 1960, "contribution": "record data"},
   "ALGOL" : {"name": "ALGOL", "publication_year": 1958, "contribution": "scoping and nested functions"},
   "APL" : {"name": "APL", "publication_year": 1962, "contribution": "array processing"},
}

@app.get('/programming_languages')
def list_programming_languages():
   return {"programming_languages":list(in_memory_datastore.values())}

@app.route('/programming_languages/<programming_language_name>')
def get_programming_language(programming_language_name):
   return in_memory_datastore[programming_language_name]



        
if __name__ == "__main__":
    app.run(debug=True)