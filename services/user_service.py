import uuid
from werkzeug.exceptions import BadRequest

from models import User, db

def list_users():
    return User.query.all()

def create_user(name: str, email: str, password: str, role: str = 'user', team_id: str = None) -> User:
    if User.query.filter_by(email=email).first():
        raise BadRequest(f"E-mail '{email}' já cadastrado.")
    user = User(
        id=str(uuid.uuid4()),
        name=name,
        email=email,
        role=role,
        team_id=team_id
    )
    user.password = password
    db.session.add(user)
    db.session.commit()
    return user

def get_user(user_id: str) -> User:
    return User.query.get_or_404(user_id)

def update_user(user: User, **attrs) -> User:
    # evita sobrescrever id ou created_at
    if 'name' in attrs:
        user.name = attrs['name']
    if 'email' in attrs and attrs['email'] != user.email:
        if User.query.filter_by(email=attrs['email']).first():
            raise BadRequest(f"E-mail '{attrs['email']}' já cadastrado.")
        user.email = attrs['email']
    if 'password' in attrs:
        user.password = attrs['password']
    if 'role' in attrs:
        user.role = attrs['role']
    if 'team_id' in attrs:
        user.team_id = attrs['team_id']
    db.session.commit()
    return user

def delete_user(user: User) -> None:
    db.session.delete(user)
    db.session.commit()
