import uuid

from db import db
from sqlalchemy.exc import IntegrityError


class Example(db.Model):
    # TODO : Add UUID column to your model if required
    # id = db.Column(
    #     "id",
    #     db.Text(),
    #     default=lambda: str(uuid.uuid4()),
    #     primary_key=True
    # )
    key = db.Column("key", db.Text(), primary_key=True)
    value = db.Column(db.Text(), default=lambda: str(uuid.uuid4()))

    def __repr__(self):
        return f"<Example value {self.value} for key {self.name}>"

    def as_json(self):
        return {
            "key": self.key,
            "value": self.value,
        }


class ExampleError(Exception):
    """Exception raised for errors in Example management

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Sorry, there was a problem, please try later"):
        self.message = message
        super().__init__(self.message)


class ExampleMethods:
    @staticmethod
    def list_examples(query: str = None, as_json=False):
        """
        List examples from the database

        Args:
            query (str): String to search key and value for
            as_json (bool): Return as json (defaults to False)

        Returns:
            A list of example objects
        """
        if query:
            examples = Example.query.filter(Example.key.contains(query))
        else:
            examples = Example.query.all()
        if as_json:
            return [example.as_json() for example in examples]
        return examples

    @staticmethod
    def get_example(key: str):
        """
        Get an example from the database
        corresponding to a given key

        Args:
            key (str): The example key

        Returns:
            Example object or raises an ExampleError if none found
        """
        example = Example.query.get(key)
        if not example:
            raise ExampleError(
                message=f"Example with key '{key}' could not be found"
            )
        return example

    @staticmethod
    def create_example(key: str, value: str):
        """
        Create a new example if none exists

        Args:
            key (str): The example key
            value (str): The example value

        Returns:
            Example object or None
        """
        try:
            example = Example(key=key, value=value)
            db.session.add(example)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ExampleError(
                message=f"An example with key '{key}' already exists"
            )
        return example
