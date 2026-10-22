import os
import hmac
from functools import wraps

from flask import (
    Flask, request, redirect, session,
    render_template_string, url_for
)

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "change-this-before-deploy")

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "master")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")

HTML = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MASTER YOUSEF ULTIMATE</title>
<style>
*{box-sizing:border-box}
body{
    margin:0;background:#080808;color:#fff;
    font-family:Tahoma,Arial,sans-serif
}
header{
    text-align:center;padding:28px 12px;
    background:linear-gradient(135deg,#101010,#352800);
    border-bottom:2px solid #d6b34b
}
h1{color:#e8c65a;font-size:27px}
.subtitle{color:#ccc;font-size:13px}
.container{max-width:850px;margin:25px auto;padding:15px}
.card{
    background:#151515;border:1px solid #514322;
    border-radius:15px;padding:20px;margin-bottom:18px
}
h2{font-size:18px;color:#e8c65a}
input,button{
    width:100%;padding:14px;margin:8px 0;
    border-radius:9px;font-size:14px
}
input{
    color:white;background:#090909;border:1px solid #444
}
button{
    background:#d6b34b;color:#111;
    border:0;font-weight:bold;cursor:pointer
}
button:hover{background:#f2d77a}
.status{color:#85e5a0}
footer{text-align:center;color:#888;padding:25px}
</style>
</head>
<body>
<header>
<h1>🐺 MASTER YOUSEF</h1>
<div class="subtitle">ULTIMATE CONFIG PANEL</div>
<p>👑 پنل اختصاصی مستر یوسف</p>
</header>

<div class="container">
{% if not logged_in %}
<div class="card">
<h2>🔐 ورود مدیر</h2>
{% if error %}
<p style="color:#ff7777">{{ error }}</p>
{% endif %}
<form method="post" action="/login">
<input name="username" placeholder="نام کاربری" required>
<input name="password" type="password"
placeholder="رمز عبور" required>
<button type="submit">ورود به پنل 👑</button>
</form>
</div>

{% else %}
<div class="card">
<h2>👑 داشبورد اختصاصی</h2>
<p>خوش آمدی به پنل MASTER YOUSEF!</p>
<p>وضعیت سایت: <span class="status">● آنلاین</span></p>
</div>

<div class="card">
<h2>⚡ ساخت و مدیریت کانفیگ</h2>
<p>وضعیت سرور VPN: هنوز متصل نشده است.</p>
<p>برای ساخت کانفیگ واقعی، ابتدا باید سرور و سرویس مدیریت VPN راه‌اندازی شوند.</p>
</div>

<div class="card">
<h2>🔗 مدیریت Subscription</h2>
<p>نام برند ساب: MASTER YOUSEF SUB</p>
<p>پس از اتصال سرور، لینک‌های اشتراک واقعی ایجاد خواهند شد.</p>
</div>

<div class="card">
<h2>📊 اطلاعات پنل</h2>
<p>نام: MASTER YOUSEF ULTIMATE</p>
<p>زیرساخت: Railway</p>
<form action="/logout" method="post">
<button type="submit">خروج از حساب</button>
</form>
</div>
{% endif %}
</div>

<footer>🐺 MASTER YOUSEF © 2026</footer>
</body>
</html>
"""


def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("home"))
        return func(*args, **kwargs)
    return wrapper


@app.route("/")
def home():
    return render_template_string(
        HTML,
        logged_in=bool(session.get("logged_in")),
        error=None
    )


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    if not ADMIN_PASSWORD:
        return render_template_string(
            HTML,
            logged_in=False,
            error="رمز مدیر در تنظیمات Railway تنظیم نشده است."
        ), 503

    valid_user = hmac.compare_digest(username, ADMIN_USERNAME)
    valid_password = hmac.compare_digest(password, ADMIN_PASSWORD)

    if valid_user and valid_password:
        session.clear()
        session["logged_in"] = True
        return redirect(url_for("dashboard"))

    return render_template_string(
        HTML,
        logged_in=False,
        error="نام کاربری یا رمز عبور اشتباه است."
    ), 401


@app.route("/dashboard")
@require_login
def dashboard():
    return render_template_string(
        HTML,
        logged_in=True,
        error=None
    )


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.get("/health")
def health():
    return {
        "status": "ok",
        "project": "MASTER YOUSEF ULTIMATE"
    }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)حت
