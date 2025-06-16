import uuid

from models import Routine, db

def list_routines():
    return Routine.query.all()

def create_routine(temperature=None, humidity=None, begin_time=None,
                    end_time=None, liters_of_water=0, locale_id=None):
    routine = Routine(
        id=str(uuid.uuid4()),
        temperature=temperature,
        humidity=humidity,
        begin_time=begin_time,
        end_time=end_time,
        liters_of_water=liters_of_water,
        locale_id=locale_id
    )
    db.session.add(routine)
    db.session.commit()
    return routine

def get_routine(routine_id):
    return Routine.query.get_or_404(routine_id)

def update_routine(routine, **attrs):
    for key, val in attrs.items():
        setattr(routine, key, val)
    db.session.commit()
    return routine

def delete_routine(routine):
    db.session.delete(routine)
    db.session.commit()
