from flask import Flask, request, render_template,session
import ibm_db
app = Flask(__name__)
app.secret_key = "_ab+d=5"
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30756;UID=typ41627;PWD=WXxryTE4Oroyp0V0;SECURITY=SSL;SSLCERTIFICATE=DigiCertGlobalRootCA.crt",'','')
print(ibm_db.active(conn))
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        global uname
        uname = request.form['username']
        pword = request.form['password']
        print(uname, pword)
        sql = "SELECT * FROM REGISTRATION WHERE USERNAME = ? AND PASSWORD = ?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt, 1, uname)
        ibm_db.bind_param(stmt,2,pword)
        ibm_db.execute(stmt)
        out = ibm_db.fetch_assoc(stmt)
        print(out)
        if out != False:
            r = out['ROLE']
            r = r.strip()
            session['username'] = uname
            session['emailid'] = out['MAILID']
            
            if out['ROLE'] == '0':
                return render_template("Admin.html",Adname = uname, Ademail = out['MAILID'] )
            elif out['ROLE'] == '1':
                return render_template("student.html",SdName = uname, SdEmail = out['MAILID'])
            else: 
                return render_template("faculty.html",Fname = uname, Femail = out['MAILID'])
        else: 
            msg = "Invalid Credentials"
            return render_template("login.html",message1= msg)
    return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def regsiter():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        pword = request.form['password']
        role = request.form['role']
        role = str(role)
        uname = request.form['uname']
        print(uname,email,pword,role)
        sql = "SELECT * FROM REGISTRATION WHERE USERNAME=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt, 1, uname)
        ibm_db.execute(stmt)
        out = ibm_db.fetch_assoc(stmt)
        print(out)
        r = out['ROLE']
        if out != False:
            msg = "Already Registered"
            return render_template("register.html",msg = msg)
        else:
            sql = "INSERT INTO REGISTRATION VALUES(?,?,?,?,?)"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, name)
            ibm_db.bind_param(stmt, 2,email)
            ibm_db.bind_param(stmt, 3, pword)
            ibm_db.bind_param(stmt, 4, role)
            ibm_db.bind_param(stmt, 5, uname)
            ibm_db.execute(stmt)
            msg = "Registered"
            return render_template("register.html", msg =msg)

    return render_template("register.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=False)
