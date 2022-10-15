
from calendar import leapdays
from cgitb import html
from crypt import methods
from fileinput import filename
from socket import AddressFamily
from flask import Flask,render_template , request ,redirect ,session
import requests , sqlite3 ,datetime
from bs4 import BeautifulSoup
from werkzeug.utils import secure_filename


app = Flask(__name__)

app.secret_key = "otakesan"


@app.route("/home" , methods=["GET" ,"POST"])
def home():
    if "user_id" in session:
        return render_template('home.html')
    else:
        return render_template('secret.html')
    
@app.route("/mypage")
def mypage():
    if "user_id" in session:
        conn = sqlite3.connect('teamotake.db')
        c = conn.cursor()
        user_id = session["user_id"]
        c.execute("select * from reserve where member_id = ?",(user_id,))
        carry_datas = c.fetchall()
        if len(carry_datas) == 0 :
            return render_template("mypage1.html")
        elif len(carry_datas) ==3:
            return render_template("mypage4.html", carry_list0 = carry_datas[0] ,carry_list1 = carry_datas[1],carry_list2 = carry_datas[2])
        elif len(carry_datas) == 2:
            return render_template("mypage3.html", carry_list0 = carry_datas[0] ,carry_list1 = carry_datas[1])
        elif len(carry_datas) == 1:
            return render_template("mypage2.html", carry_list0 = carry_datas[0]) 
        else:
            return render_template("mypage2.html", carry_list0 = carry_datas[0])
        
    else:
        return redirect('/login')
    
@app.route("/signup")
def signup():
    if "user_id" in session:
        return render_template('home.html')

    else:
        return render_template("signup.html")

@app.route("/signup_py", methods=["POST"])
def signup_post():
    user_name = request.form.get("user_name")
    address = request.form.get('adress')
    mail = request.form.get('mail')
    phon = request.form.get('phon')
    password = request.form.get("pass")
    conn = sqlite3.connect('teamotake.db')
    c  = conn.cursor()
    c.execute("insert into member values(null,?,?,?,?,?,1)", (user_name,address,mail,phon,password))
    conn.commit()
    c.close()

    return redirect("/signup")

@app.route("/login")
def login():
        return render_template("login.html")

@app.route("/login_py", methods=["POST"])
def login_post():
    mail = request.form.get("mail")
    password = request.form.get("pass")
    conn = sqlite3.connect('teamotake.db')
    c  = conn.cursor()
    c.execute("select * from member where mail = ? AND password = ?",(mail,password))
    user = c.fetchall()
    c.close()
    print(user)
    if user == []:
        return redirect('/login')

    else:
        session["user_id"] = user[0][0]
        return redirect('/home')


@app.route("/logout")
def logout():
    session.pop("user_id",None)
    return redirect("/home")

@app.route("/carry")
def carry():
    if "user_id" in session:
        return render_template('carryregi.html')
        
    else:
        return redirect("/login")

@app.route("/carry_py",methods=["POST"])
def carry_post():
    productname = request.form.get('productname')
    productbox = request.form.get("productbox")
    weight = request.form.get('weight')
    deli_time = request.form.get('deli_time')
    remarks = request.form.get('remarks')
    conn = sqlite3.connect('teamotake.db')
    c  = conn.cursor()
    member_id = session["user_id"]
    c.execute("insert into reserve values(null,1,?,?,?,?,?,?,null)", (productname,productbox,weight,deli_time,remarks,member_id))
    conn.commit()
    c.close()

    return redirect("/home")

@app.route("/carry1")
def carry1():
    if "user_id" in session:
        return render_template('carryregi1.html')
        
    else:
        return redirect("/login")

@app.route("/carry1_py",methods=["POST"])
def carry_post1():
    productname = request.form.get('productname')
    productbox = request.form.get("productbox")
    weight = request.form.get('weight')
    deli_time = request.form.get('deli_time')
    remarks = request.form.get('remarks')
    conn = sqlite3.connect('teamotake.db')
    c  = conn.cursor()
    member_id = session["user_id"]
    c.execute("insert into reserve values(null,1,?,?,?,?,?,?,null)", (productname,productbox,weight,deli_time,remarks,member_id))
    conn.commit()
    c.close()

    return redirect("/home")

@app.errorhandler(404)
def page_not_found(error):
    return "見つからないよ"

if __name__ == "__main__":
    app.run(debug=True)