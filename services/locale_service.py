import uuid

from models import Locale, db

def list_locales():
    return Locale.query.all()

def create_locale(name: str, team_id: str, note: str = None) -> Locale:
    locale = Locale(
        id=str(uuid.uuid4()),
        name=name,
        note=note,
        team_id=team_id
    )
    db.session.add(locale)
    db.session.commit()
    return locale

def get_locale(locale_id: str) -> Locale:
    return Locale.query.get_or_404(locale_id)

def update_locale(locale: Locale, **attrs) -> Locale:
    for key, val in attrs.items():
        setattr(locale, key, val)
    db.session.commit()
    return locale

def delete_locale(locale: Locale) -> None:
    db.session.delete(locale)
    db.session.commit()