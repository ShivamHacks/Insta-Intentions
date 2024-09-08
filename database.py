import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import uuid
import json

USER_TABLE = "InstaIntentions_Users"
INSTA_HANDLE_TABLE = "InstaHandles_Handles"


class Database:

    def __init__(self):
        cred = credentials.Certificate(".cloud_creds.json")
        app = firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def create_user_id(self):
        user_id = str(uuid.uuid4())
        doc = self.db.collection(USER_TABLE).document(user_id)
        doc.set(
            {
                "insta_handles_you_like": [],
                "insta_handle": None,
                "verified": False,
            }
        )
        return {"status": "success", "user_id": user_id}

    def add_liked_username(self, user_id, username):
        if user_id == "":
            return {"status": "error", "message": "User ID cannot be empty"}
        if username == "":
            return {"status": "error", "message": "Username cannot be empty"}
        user_doc = self.db.collection(USER_TABLE).document(user_id)
        if not user_doc.get().exists:
            return {"status": "error", "message": "User does not exist"}
        user_doc.set(
            {"insta_handles_you_like": firestore.ArrayUnion([username])}, merge=True
        )
        # TODO: verify a username exists before adding it to the table
        insta_handle_doc = self.db.collection(INSTA_HANDLE_TABLE).document(username)
        insta_handle_doc.set(
            {"uids_that_have_liked": firestore.ArrayUnion([user_id])}, merge=True
        )
        return {"status": "success"}

    def get_people_that_have_liked(self, insta_handle):
        if insta_handle == "":
            return {"status": "error", "message": "Instagram handle cannot be empty"}
        result = {
            "status": "success",
            "verified_insta_handles_that_have_liked": [],
            "unverified_uuids_that_have_liked": 0,
        }
        insta_handle_doc = self.db.collection(INSTA_HANDLE_TABLE).document(insta_handle)
        if not insta_handle_doc.get().exists:
            return result
        for uid in insta_handle_doc.get().to_dict()["uids_that_have_liked"]:
            user_doc = self.db.collection(USER_TABLE).document(uid)
            if user_doc.get().exists and user_doc.get().to_dict()["verified"]:
                result["verified_insta_handles_that_have_liked"].append(
                    user_doc.get().to_dict()["insta_handle"]
                )
            else:
                result["unverified_uuids_that_have_liked"] += 1
        return result

    def is_user_verified(self, user_id):
        if user_id == "":
            return {"status": "error", "message": "User ID cannot be empty"}
        doc = self.db.collection(USER_TABLE).document(user_id)
        if not doc.get().exists:
            return {"status": "error", "message": "User does not exist"}
        return {"status": "success", "result": doc.get().to_dict()["verified"]}

    def verify_user(self, user_id, insta_handle):
        if user_id == "":
            return {"status": "error", "message": "User ID cannot be empty"}
        if insta_handle == "":
            return {"status": "error", "message": "Instagram handle cannot be empty"}
        doc = self.db.collection(USER_TABLE).document(user_id)
        if not doc.get().exists:
            return {"status": "error", "message": "User does not exist"}
        doc.set({"verified": True, "insta_handle": insta_handle}, merge=True)
        return {"status": "success"}

    # Debug only method, not used in production
    def dump_full_database(self):
        users = self.db.collection(USER_TABLE).stream()
        insta_handles = self.db.collection(INSTA_HANDLE_TABLE).stream()
        user_data = {user.id: user.to_dict() for user in users}
        insta_handle_data = {
            insta_handle.id: insta_handle.to_dict() for insta_handle in insta_handles
        }
        return {"users": user_data, "insta_handles": insta_handle_data}

    # Debug only method, not used in production
    def process_function_calls(self, function_calls):
        results = []
        for call in function_calls:
            method_name = call.function.name
            method = getattr(self, method_name, None)
            if method:
                arguments = json.loads(call.function.arguments)
                result = method(**arguments)
                results.append({"tool_call_id": call.id, "output": str(result)})
            else:
                results.append(
                    {"tool_call_id": call.id, "output": "Function not found"}
                )
        return results
