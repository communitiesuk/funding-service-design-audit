from db import db
from sqlalchemy import exc


def add_data(data, error_handler):
    try:
        db.session.add(data)
        db.session.commit()
    except exc.IntegrityError as e:
        db.session.rollback()
        raise error_handler(message=e.orig.args[0], code=400)
    except exc.OperationalError as e:
        db.session.rollback()
        raise error_handler(message=e.orig.args[0], code=400)
