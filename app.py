# 初始化資料庫連線
import pymongo
client = pymongo.MongoClient("<你的mongodb cluster uri>")
db=client.member_system
print("資料庫連線成功")

# 初始化Flask伺服器
from flask import *

app = Flask(__name__,
            static_folder="static",
            static_url_path="/static")
app.secret_key = "my secret key"


# 處理路由
@app.route("/")
def index():
    if 'username' in session:
        return redirect("/member")
    return render_template("index.html")

# 會員頁面
@app.route("/member")
def member():
    if 'username' in session:
        return render_template("member.html", username=session['username'])
    return redirect("/")

# /error?msg=錯誤訊息
@app.route("/error")
def error():
    message = request.args.get("msg", "")
    return render_template("error.html", message=message)

# 註冊頁面
@app.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    if password != confirm_password:
        return jsonify(success=False, message="密碼與確認密碼不同")

    collection = db.users
    if collection.find_one({"$or": [{"username": username}, {"email": email}]}):
        return jsonify(success=False, message="帳號或信箱已存在")

    collection.insert_one({
        "username": username,
        "email": email,
        "password": password
    })
    return jsonify(success=True)

# 登入頁面
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    collection = db.users
    user = collection.find_one({"username": username, "password": password})

    if user:
        session['username'] = username
        return redirect("/member")
    return redirect(url_for('error', msg="帳號或密碼錯誤"))

# 登出
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/")

# 啟動伺服器
if __name__ == "__main__":
    app.run(port=8080, debug=True)
