"""
Tortoise ORM models for the tournament demo.

Separated from the main demo file so aerich can import models without
requiring air, uvicorn, or other dependencies.
"""

from tortoise.models import Model
from tortoise import fields


class Tournament(Model):
    name = fields.CharField(max_length=255)


class Event(Model):
    name = fields.CharField(max_length=255)
    tournament = fields.ForeignKeyField("models.Tournament", related_name="events")
    participants = fields.ManyToManyField("models.Team", related_name="events", through="event_team")


class Team(Model):
    name = fields.CharField(max_length=255)
