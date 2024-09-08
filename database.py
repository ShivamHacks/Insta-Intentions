"""

API surface

add/<user_id>/<username>

get_like_count/<user_id>

"""

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import uuid
import inspect

COLLECTION_NAME = "InstaIntentions"


class Database:

    def __init__(self):
        cred = credentials.Certificate("cloud_creds.json")
        app = firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def create_user_id(self):
        user_id = str(uuid.uuid4())
        doc = self.db.collection(COLLECTION_NAME).document(user_id)
        # TODO: verify that object creation worked
        doc.set({"liked_usernames": [], "uuids_that_have_liked": [], "like_count": 0})
        return {"status": "success", "user_id": user_id}

    def add_liked_username(self, user_id, username):
        # TODO: do parameter validation
        doc = self.db.collection(COLLECTION_NAME).document(user_id)
        doc.set({"liked_usernames": firestore.ArrayUnion([username])}, merge=True)
        return {"status": "success"}
