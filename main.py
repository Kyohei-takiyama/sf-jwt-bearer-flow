# https://help.salesforce.com/s/articleView?id=xcloud.remoteaccess_oauth_jwt_flow.htm&type=5

import requests
import os
import jwt, datetime

from dotenv import load_dotenv


load_dotenv()

# 秘密鍵の読み込み
with open("salesforce.pem", "r") as f:
    private_key = f.read()

# JWTペイロードの作成
now = int(datetime.datetime.utcnow().timestamp())
payload = {
    "iss": os.environ.get("CLIENT_ID"),  # Connected Appのコンシューマー鍵
    "sub": os.environ.get("USER_NAME"),  # 認証するユーザのログインID
    "aud": "https://login.salesforce.com",  # Developer Editionなのでloginを指定（Sandboxならtest）
    "exp": datetime.datetime.utcnow()
    + datetime.timedelta(seconds=30),  # 現在時刻+300秒（5分）
    "iat": now,  # 発行時刻を明示的に追加（オプションですが推奨）
}

# JWTのエンコード（RSA SHA256署名）
jwt_token = jwt.encode(payload, private_key, algorithm="RS256")
print("jwt_token : " + jwt_token)


# JWTを使ってOAuth2.0のアクセストークンを取得
token_url = "https://login.salesforce.com/services/oauth2/token"  # Developer Editionなのでloginを使用
data = {
    "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
    "assertion": jwt_token,  # 先ほど作成したJWT文字列
}
response = requests.post(token_url, data=data)
if response.status_code == 200:
    auth_result = response.json()
    print("Access Token:", auth_result.get("access_token"))
    print("Instance URL:", auth_result.get("instance_url"))
    print("scope:", auth_result.get("scope"))
    print("id:", auth_result.get("id"))
else:
    print("Error:", response.status_code, response.text)

# リクエストヘッダの作成
headers = {
    "Authorization": f"Bearer {auth_result.get('access_token')}",
    "Content-Type": "application/json",
}

# 取引先の情報を取得
url = f"{auth_result.get('instance_url')}/services/data/v52.0/query/?q=SELECT+Id,Name+FROM+Account"
response = requests.get(url, headers=headers)
print(response.status_code)
if response.status_code == 200:
    print(response.json())
