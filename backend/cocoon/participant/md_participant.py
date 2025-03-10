# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from datetime import datetime
from enum import Enum, auto
from pydantic import BaseModel, Field
from reddevil.core import DbBase


class Gender(str, Enum):
    M = "M"
    F = "F"


class ParticipantCategory(str, Enum):
    OPEN = "open"
    M1800 = "m1800"
    SEN = "sen"


class ParticipantDB(BaseModel):
    """
    the participant model as used in the database
    is normally not exposed
    """

    badgemimetype: str
    badgeimage: bytes
    badgelength: int
    birthyear: int
    category: ParticipantCategory
    chesstitle: str
    enabled: bool
    emails: list[str]
    first_name: str
    gender: Gender
    idbel: str
    idclub: str | None
    idfide: str | None
    locale: str
    last_name: str
    nationalityfide: str | None
    payment_id: str | None = None
    present: datetime | None
    ratingbel: int
    ratingfide: int
    registrationtime: datetime
    remarks: str
    _id: str
    _version: int
    _documenttype: str
    _creationtime: datetime
    _modificationtime: datetime


class ParticipantDetail(BaseModel):
    """
    the detailed participant model
    """

    badgemimetype: str | None = ""
    badgelength: int | None = 0
    birthyear: int
    category: ParticipantCategory
    chesstitle: str
    enabled: bool
    emails: list[str]
    first_name: str
    gender: Gender
    id: str
    idbel: str
    idclub: str | None
    idfide: str | None
    locale: str
    last_name: str
    nationalityfide: str | None
    payment_id: str | None = None
    present: datetime | None
    ratingbel: int
    ratingfide: int
    registrationtime: datetime
    remarks: str
    creationtime: datetime = Field(alias="_creationtime")


class ParticipantUpdate(BaseModel):
    """
    participant update model
    """

    badgemimetype: str | None = None
    badgeimage: bytes | None = None
    badgelength: int | None = None
    birthyear: int | None = None
    category: ParticipantCategory | None = None
    chesstitle: str | None = None
    enabled: bool | None = None
    emails: list[str] | None = None
    first_name: str | None = None
    gender: Gender | None = None
    idbel: str | None = None
    idclub: str | None = None
    idfide: str | None = None
    locale: str | None = None
    last_name: str | None = None
    nationalityfide: str | None = None
    payment_id: str | None = None
    present: datetime | None = None
    ratingbel: int | None = None
    ratingfide: int | None = None
    remarks: str | None = None


class Participant(BaseModel):
    """
    the participant model
    """

    badgemimetype: str | None = None
    badgelength: int | None = None
    birthyear: int | None = None
    category: ParticipantCategory | None = None
    chesstitle: str | None = None
    enabled: bool | None = None
    emails: list[str] | None = None
    first_name: str | None = None
    gender: Gender | None = None
    idbel: str | None = None
    idclub: str | None = None
    idfide: str | None = None
    locale: str | None = None
    last_name: str | None = None
    nationalityfide: str | None = None
    payment_id: str | None = None
    present: datetime | None = None
    ratingbel: int | None = None
    ratingfide: int | None = None
    registrationtime: datetime | None = None
    remarks: str | None = None


class ParticipantItem(BaseModel):
    """
    validator for public view of a enrollment
    """

    badgelength: int | None = 0
    birthyear: int
    category: ParticipantCategory
    chesstitle: str | None
    enabled: bool | None = True
    first_name: str
    gender: Gender
    id: str
    idbel: str
    idclub: str | None
    idfide: str | None
    last_name: str
    nationalityfide: str | None = "BEL"
    payment_id: str | None = None
    ratingbel: int | None = 0
    ratingfide: int | None = 0
    registrationtime: datetime | None = None


class DbParticpant(DbBase):
    COLLECTION = "participant"
    DOCUMENTTYPE = ParticipantDB
    VERSION = 1
