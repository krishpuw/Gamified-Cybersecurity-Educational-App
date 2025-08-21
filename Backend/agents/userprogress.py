# userprogress.py
from model import db, User

def get_user_xp(user_id: int) -> int:
    u = User.query.get(user_id)
    if not u: 
        print(f"[WARN] User {user_id} not found, returning XP=0")
        return {"xp": 0, "level": 1}
    
    return {"xp": int(u.xp), "level": int(u.level)}

def get_user_level(user_id: int) -> int:
    u = User.query.get(user_id)
    if not u: 
        print(f"[WARN] User {user_id} not found, returning XP=0")
        return {"xp": 0, "level": 1}
    return {"xp": int(u.xp), "level": int(u.level)}

