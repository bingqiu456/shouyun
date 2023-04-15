import sqlite3

image_check = {} # 图片验证码的缓存
account = "" # 账号用户名
password = "" # 账号密码

conn_cookie = sqlite3.connect("data/login.db") # 登录加载（cookie）
conn_login_token = sqlite3.connect("data/config.db") # 加载登录令牌

d = conn_cookie.cursor().execute("SELECT * from `login`").fetchone()
e = conn_login_token.cursor().execute("SELECT * from `Token`").fetchone()

cookies_login = {"PHPSESSID":d[0],"Token":d[1],"User":d[2]} # cookie
token_p = e[0] # 登录令牌


