from flask import Flask, request, Response
import os
import hmac

app = Flask(__name__)

@app.before_request
def check_password():
    password = os.environ.get("APP_PASSWORD")

    if not password:
        return Response(
            "Password setup required",
            status=503
        )

    auth = request.authorization

    if auth and auth.username == "admin":
        if hmac.compare_digest(
            (auth.password or "").encode("utf-8"),
            password.encode("utf-8")
        ):
            return None

    return Response(
        "Login required",
        status=401,
        headers={
            "WWW-Authenticate": 'Basic realm="AI Video Studio"'
        }
    )

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>AI Video Studio</title>
    <style>
    body {
        background: #101018;
        color: white;
        font-family: sans-serif;
        padding: 24px;
    }
    textarea, select, button {
        width: 100%;
        padding: 14px;
        margin: 12px 0;
        box-sizing: border-box;
        border-radius: 12px;
        font-size: 16px;
    }
    button {
        background: #7950f2;
        color: white;
        border: none;
    }
    </style>
    </head>
    <body>
    <h1>AI Video Studio</h1>
    <p>自分専用AI動画生成アプリ</p>
    <input type="file" accept="image/*">
    <textarea placeholder="生成したい動画の内容を入力"></textarea>
    <select>
        <option>5秒</option>
        <option>10秒</option>
    </select>
    <button onclick="alert('AI APIの接続設定が必要です')">
        AI動画を生成
    </button>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
