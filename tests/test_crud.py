import asyncio
import pytest
from fastapi.exceptions import HTTPException

from app.crud import (
    create_note,
    get_note_by_id,
    get_notes,
    update_note,
    delete_note
)


# # This is the same as using the @pytest.mark.asyncio
# # on all test functions in the module
# pytestmark = pytest.mark.asyncio


class TestCreateNote:
    async def test_success(self, db_session):
        name = 'test_create_note'
        note = await create_note(db_session, name, 'Desc')
        assert note is not None
        assert note.name == name


class TestGetNote:
    async def test_success(self, db_session, a_note):
        note = await get_note_by_id(db_session, a_note.id)
        assert note is not None

    async def test_fail(self, db_session):
        note = await get_note_by_id(db_session, 100)
        assert note is None


class TestGetNotes:
    async def test_empty(self, db_session):
        notes = await get_notes(db_session)
        assert len(notes) <= 1

    async def test_get_list(self, db_session):
        length = 5
        for i in range(length):
            _note = await create_note(
                db_session,
                f'test_get_list_{i}',
                f'Desc {i}'
            )

        notes = await get_notes(db_session)
        assert len(notes) >= length


class TestUpdateNote:
    async def test_success(self, db_session, a_note):
        await update_note(
            db_session,
            a_note.id,
            name='updated name',
            desc='Updated desc'
        )
        note = await get_note_by_id(db_session, a_note.id)

        assert a_note.id == note.id
        assert a_note.name != note.name
        assert a_note.desc != note.desc

    async def test_fail(self, db_session):
        with pytest.raises(HTTPException):
            await update_note(db_session, 100, 'New Note', 'new desc')


class TestDeleteNote:
    async def test_success(self, db_session, a_note):
        await delete_note(db_session, a_note.id)
        note = await get_note_by_id(db_session, a_note.id)
        assert note is None

    async def test_fail(self, db_session):
        with pytest.raises(HTTPException):
            await update_note(db_session, 100, 'New Note', 'new desc')
