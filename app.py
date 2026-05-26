import os
import requests
from flask import Flask, request, redirect

app = Flask(__name__)

SHOP          = "pryve.myshopify.com"
CLIENT_ID     = "560a69204609c2130ce9d0e4fa544661"
CLIENT_SECRET = "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"
SCOPES        = "read_products,write_products,read_files,write_files"
REDIRECT_URI  = "https://pryve-oauth.onrender.com/callback"

@app.route("/")
def index():
    auth_url = (
        f"https://{SHOP}/admin/oauth/authorize"
        f"?client_id={CLIENT_ID}"
        f"&scope={SCOPES}"
        f"&redirect_uri={REDIRECT_URI}"
    )
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "<h2>Erreur: pas de code</h2>", 400
    r = requests.post(
        f"https://{SHOP}/admin/oauth/access_token",
        json={"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, "code": code}
    )
    data = r.json()
    token = data.get("access_token")
    if token:
        return f"""<html><body style="font-family:sans-serif;padding:40px">
        <h2 style="color:green">TOKEN OBTENU !</h2>
        <textarea style="width:100%;height:80px">{token}</textarea>
        </body></html>"""
    return f"<h2>Erreur: {data}</h2>", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
