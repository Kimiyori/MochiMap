import datetime
import uuid
from enum import Enum
from random import choice, randint, random
from typing import TypeVar, Union, get_args, get_origin

import faker
import sqlalchemy as sa
from pydantic import BaseModel

faker = faker.Faker()


ModelType = TypeVar("ModelType", bound=BaseModel)


def model_to_dict(model: BaseModel) -> dict:
    """Convert a SQLAlchemy model instance into a dictionary."""
    return {
        column.key: getattr(model, column.key)
        for column in sa.inspect(model).mapper.column_attrs
        if getattr(model, column.key)
    }

def generate_mock_data(
    schema: ModelType, manual_values: dict | None = None, as_dict=False
) -> ModelType:
    """
    Populate all fields in a Pydantic schema with mock data,
    allowing manual override of specific fields.

    Args:
        schema (BaseModel): The Pydantic model to populate.
        manual_values (dict): A dictionary of field names and values to manually assign.

    Returns:
        BaseModel: An instance of the schema with populated data.
    """

    def get_mock_value(field_type, field_name, manual_nested_values={}):
        origin = get_origin(field_type)
        args = get_args(field_type)
        if origin is list:
            # Handle list types
            return [
                get_mock_value(args[0], field_name, manual_nested_values)
                for _ in range(randint(1, 3))
            ]
        if origin is dict:
            # Handle dictionary types
            key_type, value_type = args
            return {
                faker.word(): get_mock_value(
                    value_type, field_name, manual_nested_values
                )
                for _ in range(randint(1, 3))
            }
        if origin is Union:
            # Handle Union types (e.g., Optional)
            return (
                get_mock_value(args[0], field_name, manual_nested_values)
                if args and args[0] is not type(None)
                else None
            )
        if field_type is str:
            return faker.word() if "name" not in field_name else faker.name()
        if field_type is int:
            return faker.random_int(min=1, max=100)
        if field_type is float:
            return faker.random_number(digits=2, fix_len=False)
        if field_type is bool:
            return faker.boolean()
        if field_type is datetime.date:
            return faker.date_this_decade()
        if field_type is uuid.UUID:
            return uuid.uuid4()
        if field_type is datetime.datetime:
            return faker.date_time_this_decade()
        if isinstance(field_type, type) and issubclass(field_type, Enum):
            # Handle Enum types
            return choice(list(field_type))
        if isinstance(field_type, type) and issubclass(field_type, BaseModel):
            return generate_mock_data(
                field_type, manual_values.get(field_name, {}), as_dict
            )
        # Default fallback for unsupported types
        return None

    mock_data = {}
    manual_values = manual_values or {}
    for field_name, field_info in schema.__fields__.items():
        if field_name in manual_values:
            if issubclass(field_info.type_, BaseModel):
                if isinstance(manual_values[field_name], dict):
                    mock_data[field_name] = generate_mock_data(
                        field_info.type_, manual_values[field_name], as_dict
                    )
                elif isinstance(manual_values[field_name], list):
                    mock_data[field_name] = [
                        generate_mock_data(field_info.type_, val, as_dict)
                        for val in manual_values[field_name]
                    ]
            else:
                # Use the manually provided value
                mock_data[field_name] = manual_values[field_name]
            manual_values.pop(field_name)
        else:
            # Generate mock value
            field_type = field_info.type_
            if get_origin(field_info.outer_type_) is list:
                mock_data[field_name] = [
                    get_mock_value(field_info.type_, field_name)
                    for _ in range(randint(1, 3))
                ]
            else:
                mock_data[field_name] = get_mock_value(field_type, field_name)
    while manual_values:
        field_name, manual_value = (
            manual_values.popitem()
            if isinstance(manual_values, dict)
            else (None, manual_values.pop())
        )

        mock_data[field_name] = manual_value
    return mock_data if as_dict else schema(**mock_data)


def generate_mock_data_sqlalchemy(
    model: ModelType,
    manual_values: dict | None = None,
    as_dict: bool = False,
    all_fields: bool = False,
) -> ModelType:
    """
    Populate all fields in a SQLAlchemy model with mock data, allowing manual override of specific fields.

    Args:
        model (DeclarativeBase): The SQLAlchemy model class to populate.
        manual_values (dict): A dictionary of field names and values to manually assign.

    Returns:
        DeclarativeBase: An instance of the SQLAlchemy model with populated data.
    """

    def get_mock_value_for_sqlalchemy_type(column_type, column_name):
        """
        Generate mock data for a specific SQLAlchemy column type.

        Args:
            column_type: The SQLAlchemy column type.
            column_name: The name of the column.

        Returns:
            Any: Mock data for the column.
        """
        if isinstance(column_type, sa.String):
            return faker.word() if "name" not in column_name else faker.name()
        if isinstance(column_type, sa.Integer):
            return faker.random_int(min=1, max=100)
        if isinstance(column_type, sa.Float):
            return faker.random_number(digits=2, fix_len=False)
        if isinstance(column_type, sa.Boolean):
            return faker.boolean()
        if isinstance(column_type, sa.Date):
            return faker.date_this_decade()
        if isinstance(column_type, sa.DateTime):
            return faker.date_time_this_decade()
        if isinstance(column_type, sa.UUID):
            return uuid.uuid4()
        if isinstance(column_type, sa.Enum):
            # Generate a random value from the Enum options
            return random.choice(column_type.enums)
        # Default fallback for unsupported types
        return None

    manual_values = manual_values or {}
    mock_data = {}

    for column in model.__table__.columns:
        column_name = column.name
        column_type = column.type
        is_required = (
            (
                not column.nullable or not column.foreign_keys
            )  # Includes columns with foreign keys
            and column_name != "id"
            and not column.default
        )

        if all_fields or is_required:
            # Generate mock data based on the column type
            mock_data[column_name] = get_mock_value_for_sqlalchemy_type(
                column_type, column_name
            )
        if column_name in manual_values:
            # Use the manually provided value
            mock_data[column_name] = manual_values[column_name]
    return model_to_dict(model(**mock_data)) if as_dict else model(**mock_data)
