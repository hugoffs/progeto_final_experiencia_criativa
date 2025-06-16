#team_service.py
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
    print(f"Tentando deletar o time ID: {team.id}, Nome: {team.name}")
    try:
        db.session.delete(team)
        db.session.commit()
        print(f"Time ID: {team.id} deletado e commitado com sucesso.")
    except Exception as e:
        db.session.rollback() # Importante reverter em caso de erro no commit
        print(f"Erro ao deletar time ID: {team.id} do banco: {str(e)}")
        raise # Re-levanta a exceção para ser tratada pela rota do controller
