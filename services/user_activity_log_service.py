import uuid
from models import db, UserActivityLog


def log_user_action(user_id: str, action: str) -> UserActivityLog:
    entry = UserActivityLog(
        id=str(uuid.uuid4()),
        user_id=user_id,
        action=action
    )
    db.session.add(entry)
    db.session.commit()
    return entry

def list_user_activity_logs(user_id: str = None) -> list[UserActivityLog]:
    query = UserActivityLog.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    return query.order_by(UserActivityLog.created_at.desc()).all()

def get_user_activity_log(log_id: str) -> UserActivityLog:
    return UserActivityLog.query.get_or_404(log_id)

def delete_user_activity_log(entry: UserActivityLog) -> None:
    db.session.delete(entry)
    db.session.commit()
