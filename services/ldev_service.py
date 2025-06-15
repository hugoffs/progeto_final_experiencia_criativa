import uuid

from models import LDev, db

def list_ldevs():
    return LDev.query.all()

def create_ldev(name: str, latitude: float, longitude: float, locale_id: str) -> LDev:
    ldev = LDev(
        id=str(uuid.uuid4()),
        name=name,
        latitude=latitude,
        longitude=longitude,
        locale_id=locale_id
    )
    db.session.add(ldev)
    db.session.commit()
    return ldev

def get_ldev(ldev_id: str) -> LDev:
    return LDev.query.get_or_404(ldev_id)

def update_ldev(ldev: LDev, **attrs) -> LDev:
    for key, val in attrs.items():
        setattr(ldev, key, val)
    db.session.commit()
    return ldev

def delete_ldev(ldev: LDev) -> None:
    db.session.delete(ldev)
    db.session.commit()
