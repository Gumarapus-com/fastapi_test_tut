from typing import Sequence

from sqlalchemy import delete, insert, update, select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import NoteModel


async def create_note(
    db: AsyncSession,
    name: str,
    desc: str | None = None,
) -> NoteModel:
    # -- Another way to use SQLAlchemy query --
    #
    # query = insert(NoteModel).values(name=name, desc=desc)
    # await db.execute(query)
    # await db.commit()

    note = NoteModel()
    note.name = name
    note.desc = desc
    db.add(note)
    await db.commit()
    return note


async def get_notes(db: AsyncSession) -> Sequence[NoteModel]:
    query = select(NoteModel)
    entry = await db.scalars(query)
    return entry.all()


async def get_note_by_id(db: AsyncSession, note_id: int) -> NoteModel | None:
    query = select(NoteModel).where(NoteModel.id == note_id)
    entry = await db.scalars(query)
    return entry.one_or_none()


async def update_note(
    db: AsyncSession,
    note_id: int,
    name: str | None = None,
    desc: str | None = None
) -> bool:
    query = (
        update(NoteModel)
        .values(name=name, desc=desc)
        .where(NoteModel.id == note_id)
    )
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0


async def delete_note(db: AsyncSession, note_id: int) -> bool:
    query = delete(NoteModel).where(NoteModel.id == note_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0
