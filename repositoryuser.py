from sqlalchemy.orm import Session
from models import UserModel
from typing import Dict, Any
from sqlalchemy.exc import SQLAlchemyError

class UserRepository:
    def __init__(self, sess: Session):
        self.sess: Session = sess

    def create_user(self, signup: UserModel) -> Dict[str, Any]:
        try:
            self.sess.add(signup)
            self.sess.commit()
        except SQLAlchemyError as e:
            print(f"Error creating user: {e}")
            return {"success": False, "error": str(e)}
        return {"success": True}

    def get_user(self):
        return self.sess.query(UserModel).all()

    def get_user_by_username(self, username: str):
        return self.sess.query(UserModel).filter(UserModel.username == username).first()

    def update_user(self, id: int, details: Dict[str, Any]) -> Dict[str, Any]:
        try:
            self.sess.query(UserModel).filter(UserModel.id == id).update(details)
            self.sess.commit()
        except SQLAlchemyError as e:
            print(f"Error updating user: {e}")
            return {"success": False, "error": str(e)}
        return {"success": True}

    def delete_user(self, id: int) -> Dict[str, Any]:
        try:
            self.sess.query(UserModel).filter(UserModel.id == id).delete()
            self.sess.commit()
        except SQLAlchemyError as e:
            print(f"Error deleting user: {e}")
            return {"success": False, "error": str(e)}
        return {"success": True}
