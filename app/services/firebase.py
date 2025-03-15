# import firebase admin from firebase_admin
import os

from firebase_admin import auth, credentials, initialize_app

cwd = os.getcwd()
relative_path = os.path.join("app", "configs", "firebase.keys.json")
certPath = os.path.join(cwd, relative_path)
deafaultApp = initialize_app(credential=credentials.Certificate(certPath))


async def verifyUserToken(userIdToken: str):
    result = auth.verify_id_token(userIdToken, app=deafaultApp)
    return result
