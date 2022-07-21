import uuid

from db import db
from db.models.code import Code
from sqlalchemy.exc import IntegrityError
from sqlalchemy_utils.types import UUIDType

# SQLite does not support Enum


class Event(db.Model):
    __tablename__ = "Event"
    id = db.Column(
        UUIDType(binary=False), default=uuid.uuid4, primary_key=True
    )
    code = db.Column(db.String(20), db.ForeignKey(Code.id), nullable=False)
    entity_identifier = db.Column(db.Text(), nullable=False)
    timestamp = db.Column(db.DateTime(), nullable=False)
    auditor_user_id = db.Column(db.Text())
    body = db.Column(db.Text())

    def __repr__(self):
        return (
            f'Event("{self.id}","{self.code}","{self.entity_identifier}",'
            f'"{self.timestamp}","{self.user_id}","{self.body}"'
        )

    def __str__(self):
        return (
            f"{self.id},{self.code},{self.entity_identifier},"
            f"{self.timestamp},{self.user_id},{self.body}"
        )

    def as_dict(self):
        return {
            "id": str(self.id),
            "code": self.code,
            "entity_identifier": self.entity_identifier,
            "timestamp": str(self.timestamp),
            "user_id": self.user_id,
            "body": self.body,
        }


class EventError(Exception):
    """Exception raised for errors in Event management

    Attributes:
        message -- explanation of the error
    """

    def __init__(
        self, message="Sorry, there was a problem, please try later", code=400
    ):
        self.message = message
        self.code = code
        super().__init__(self.message, self.code)


class EventMethods:
    @staticmethod
    def list_events(query: str = None, as_dict=False):
        """
        List events from the database

        Args:
            query (str): String to search key and value for
            as_dict (bool): Return as json (defaults to False)

        Returns:
            A list of event objects
        """

        if query:
            events = Event.query.filter(Event.code.contains(query))
        else:
            events = Event.query.all()
        if as_dict:
            return [event.as_dict() for event in events]
        return events

    @staticmethod
    def get_event(key: str):
        """
        Get an event from the database
        corresponding to a given key

        Args:
            key (str): The event key

        Returns:
            Event object or raises an EventError if none found
        """
        event = Event.query.get(id)
        if not event:
            raise EventError(
                message=f"Event with key '{key}' could not be found"
            )
        return event

    @staticmethod
    def create_event(
        code: str,
        entity_identifier: str,
        timestamp: str,
        user_id: str,
        body: str,
    ):
        """
        Create a new event if none exists

        Args:
            code (str): a code representing the event type
            entity_identifier: (str): the id of the event entity
            timestamp (datetime): a datetime object representing
            the time at which the event occured at source
            user_id (str): the id of the user who triggered the event
            body (str): the changed state as a result of the event
        Returns:
            Event object or None
        """
        try:
            event = Event(
                code=code,
                entity_identifier=entity_identifier,
                timestamp=timestamp,
                user_id=user_id,
                body=body,
            )
            db.session.add(event)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise EventError(
                message="There was an problem with your request", code=400
            )
        return event
