"""
Module for response serialization in FastAPI.

This module defines Pydantic models for successful and error responses, 
along with a function to structure the response in JSON format.
"""
from typing import Any
from pydantic import BaseModel, conint, constr
from fastapi import (
    status,
    Response
)


class SuccessResponseSerializer(BaseModel):
    """
    Serializer for successful responses.

    Attributes:
        status_code (conint): HTTP status code, default is 200 OK.
        message (constr): Message indicating success, default is "Success".
        data (Any): Optional data payload.
    """
    status_code: conint() = status.HTTP_200_OK
    message: constr() = "Success"
    data: Any = None

class ErrorResponseSerializer(BaseModel):
    """
    Serializer for error responses.

    Attributes:
        status_code (conint): HTTP status code, default is 400 Bad Request.
        message (constr): Message indicating error, default is "Error".
        data (Any): Optional data payload, defaults to None.
    """
    status_code: conint() = status.HTTP_400_BAD_REQUEST
    message: constr() = "Error"
    data: Any = None

def response_structure(serializer, status_code):
    """
    Structure the response in JSON format.

    Args:
        serializer (BaseModel): A Pydantic model instance to serialize.
        status_code (int): HTTP status code for the response.

    Returns:
        Response: A FastAPI Response object with JSON content.
    """
    return Response(
        content = serializer.json(),
        media_type="application/json",
        status_code=status_code
    )
