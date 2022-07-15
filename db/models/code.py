from db import db
from sqlalchemy.exc import IntegrityError


class Code(db.Model):
    __tablename__ = "Code"
    id = db.Column(db.String(5), primary_key=True)
    description = db.Column(db.Text())

    def __init__(self, id=None, description=None):
        self.id = id
        self.description = description

    def __repr__(self):
        return f'Code("{self.id}","{self.description}")'

    def __str__(self):
        return f"({self.id},{self.description})"

    def as_json(self):
        return {"id": self.id, "description": self.description}


class CodeError(Exception):
    """Exception raised for errors in Code management

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Sorry, there was a problem, please try later"):
        self.message = message
        super().__init__(self.message)


class CodeMethods:
    @staticmethod
    def list_codes(query: str = None, as_json=False):
        """
        List codes from the database

        Args:
            query (str): String to search key and value for
            as_json (bool): Return as json (defaults to False)

        Returns:
            A list of code objects
        """
        if query:
            codes = Code.query.filter(Code.id.contains(query))
        else:
            codes = Code.query.all()
        if as_json:
            return [code.as_json() for code in codes]
        return codes

    @staticmethod
    def get_code(key: str):
        """
        Get an code from the database
        corresponding to a given key

        Args:
            key (str): The code key

        Returns:
            Code object or raises an CodeError if none found
        """
        code = Code.query.get(id)
        if not code:
            raise CodeError(
                message=f"Code with key '{key}' could not be found"
            )
        return code

    @staticmethod
    def create_code(id: str, description: str):
        """
        Create a new code if none exists

        Args:
            id (str): a uniqie id for the event type
            description (str): a descrption of the unique event
        Returns:
            Code object or None
        """
        try:
            code = Code(id=id, description=description)
            db.session.add(code)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise CodeError(message=f"An code with id '{id}' already exists")
        return code
