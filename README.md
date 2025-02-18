```mermaid
sequenceDiagram
    participant Client as Pythonクライアント
    participant JWT as JWT生成
    participant SF as Salesforce OAuthエンドポイント
    participant API as Salesforce API

    Client->>JWT: 秘密鍵を用いてJWTペイロードを作成
    JWT-->>Client: 署名済みJWTトークン
    Client->>SF: JWTトークンをPOSTリクエストで送信
    SF-->>Client: アクセストークン（Bearer Token）を返却
    Client->>API: アクセストークンを使用してAPIリクエスト送信
    API-->>Client: APIレスポンス

```

## 自己証明書の作成

```bash
## 1. 秘密鍵の生成（2048 ビット RSA）

openssl genrsa -out salesforce.pem 2048

## 2. 証明書署名要求(CSR)の作成

openssl req -new -key salesforce.pem -out salesforce.csr

## （上記コマンド実行時に組織名やホスト名など幾つか質問されるので適宜入力）

## 3. 自己署名証明書の作成（有効期限 365 日）

openssl x509 -req -days 365 -signkey salesforce.pem -in salesforce.csr -out salesforce.crt

## 4. 不要になった CSR の削除

rm salesforce.csr

```

## python 設定

### 仮想環境の作成

```bash

python3 -m venv venv

. venv/bin/activate

pip install -r requirements.txt

```
