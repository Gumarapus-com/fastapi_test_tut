from typing import Sequence

from sqlalchemy import delete, update, select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import NoteModel


async def create_note(
    db: AsyncSession,
    name: str,
    desc: str | None = None,
) -> NoteModel:
    note = NoteModel(name=name, desc=desc)
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
    name: str | None,
    desc: str | None
) -> None:
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
