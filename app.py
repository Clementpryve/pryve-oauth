import os
import requests
from flask import Flask, redirect, request

app = Flask(__name__)

SHOP          = os.environ.get("SHOP")
CLIENT_ID     = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
SCOPES        = "read_products,write_products,read_files,write_files"
REDIRECT_URI  = os.environ.get("REDIRECT_URI")

@app.route("/")
def index():
    auth_url = (
        f"https://{SHOP}/admin/oauth/authorize"
        f"?client_id={CLIENT_ID}"
        f"&scope={SCOPES}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&grant_options[]=value"
    )
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return f"<h2>Erreur: pas de code. Args: {request.args}</h2>", 400
    r = requests.post(
        f"https://{SHOP}/admin/oauth/access_token",
        json={"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, "code": code}
    )
    data = r.json()
    token = data.get("access_token")
    if token:
        return f"""<html><body style="font-family:sans-serif;padding:40px;background:#f0fff0">
        <h2 style="color:green">✅ TOKEN OBTENU !</h2>
        <p>Copie ce token :</p>
        <textarea style="width:100%;height:80px;font-size:14px">{token}</textarea>
        </body></html>"""
    return f"<h2>Erreur: {data}</h2>", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
