from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from .db import DBBaseClass


class NoteModel(DBBaseClass):
    __tablename__ = 'note'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    desc = Column(String(250))
    # Auto set value on data creation
    create_at = Column(DateTime, default=datetime.now)
    # Auto add value on data update
    update_at = Column(DateTime, nullable=True, onupdate=datetime.now)
