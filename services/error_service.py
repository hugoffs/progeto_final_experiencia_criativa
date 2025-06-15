import uuid

from models import db, Error

def list_errors():
    return Error.query.all()

def create_error(message: str, ldev_id: str) -> Error:
    err = Error(
        id=str(uuid.uuid4()),
        message=message,
        ldev_id=ldev_id
    )
    db.session.add(err)
    db.session.commit()
    return err

def get_error(error_id: str) -> Error:
    return Error.query.get_or_404(error_id)

def update_error(err: Error, **attrs) -> Error:
    for key, val in attrs.items():
        setattr(err, key, val)
    db.session.commit()
    return err

def delete_error(err: Error) -> None:
    db.session.delete(err)
    db.session.commit()
