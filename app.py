
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
        return render_template('base.html')
    
@app.route("/mypage")
def mypage():
    if "user_id" in session:
        return render_template('mypage.html')
        
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


#ログイン回り
@app.route("/login")
def login():
        return render_template("login.html")

# セッションをここでとる
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



# 運搬先登録ページ表示
# ここを固定ページにした方がいい気がする
@app.route("/carry")
def carry():
    if "user_id" in session:
        return render_template('carryregi.html')
        
    else:
        return redirect("/login")

# # 運搬先登録
# @app.route("/carry_py",methods["POST"])
# def carry_post():
#     trans_id = request.form.get("")
#     point_dep = request.form.get("")
#     destnaition = request.form.get('')
#     distance = request.form.get('')
#     conn = sqlite3.connect('teamotake.db')
#     c  = conn.cursor()
#     c.execute("insert into transport values(null,?,?,?,?,?)", (trans_id,point_dep,destnaition,distance,))
#     conn.commit()
#     c.close()

#     return redirect("/home")


# @app.route("/reserve")
# def reserve():
    # if "user_id" in session:
    #     return render_template('reserve.html')
        
    # else:
    #     return redirect("/login")

# @app.route("reserve_py",methods=["POST"])
# def reserve_py():
#     res_id = request.form.get("")
#     tran_id = request.form.get("")
#     user_id = session[]
#     date = datetime.datetime.now()
#     delete_flag = request.form.get("")
#     conn = sqlite3.connect("teamotake.db")
#     c = conn.cursor()
#     c.execute("insert into reserve values(null,?,?,?,?,?"),(res_id,tran_id)
#     conn.commit()
#     c.close()
#     return redirect("/home")



@app.errorhandler(404)
def page_not_found(error):
    return "見つからないよ"



if __name__ == "__main__":
    app.run(debug=True)