from typing import Sequence

from sqlalchemy import delete, insert, update, select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import NoteModel


async def create_note(
    db: AsyncSession,
    name: str,
    desc: str | None = None,
) -> NoteModel:
    # query = insert(NoteModel).values(name=name, desc=desc)
    # await db.execute(query)
    # await db.commit()

    note = NoteModel()
    note.name = name
    note.desc = desc
    db.add(note)
    print(await db.commit())
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
) -> None:
    # if name:
    #     note.name = name
    # if desc:
    #     note.desc = desc
    #
    # db.add(note)
    # await db.commit()
    # return note
    query = (
        update(NoteModel)
        .values(name=name, desc=desc)
        .where(NoteModel.id == note_id)
    )
    await db.execute(query)
    await db.commit()


async def delete_note(db: AsyncSession, note_id: int) -> None:
    query = delete(NoteModel).where(NoteModel.id == note_id)
    await db.execute(query)
    await db.commit()
