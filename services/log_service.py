import uuid
from models import db, Log

def list_logs():
    return Log.query.all()

def create_log(humidity: float, temperature: float, ldev_id: str, is_irrigating: bool = False) -> Log:
    log = Log(
        id=str(uuid.uuid4()),
        humidity=humidity,
        temperature=temperature,
        is_irrigating=is_irrigating,
        ldev_id=ldev_id
    )
    db.session.add(log)
    db.session.commit()
    return log

def get_log(log_id: str) -> Log:
    return Log.query.get_or_404(log_id)

def update_log(log: Log, **attrs) -> Log:
    for key, val in attrs.items():
        setattr(log, key, val)
    db.session.commit()
    return log

def delete_log(log: Log) -> None:
    db.session.delete(log)
    db.session.commit()
