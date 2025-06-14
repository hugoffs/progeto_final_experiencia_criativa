import uuid
from models.db import db
from models.team_model import Team

def create_team(name: str) -> Team:
    team = Team(id=str(uuid.uuid4()), name=name)
    db.session.add(team)
    db.session.commit()
    return team

def list_teams() -> list[Team]:
    return Team.query.all()

def get_team(team_id: str) -> Team:
    return Team.query.get_or_404(team_id)

def update_team(team: Team, **attrs) -> Team:
    for key, value in attrs.items():
        setattr(team, key, value)
    db.session.commit()
    return team

def delete_team(team: Team) -> None:
    db.session.delete(team)
    db.session.commit()
