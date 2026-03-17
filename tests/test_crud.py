import pytest
from fastapi.exceptions import HTTPException

from app.crud import (
    create_note,
    get_note_by_id,
    get_notes,
    update_note,
    delete_note
)


# This is the same as using the @pytest.mark.anyio
# on all test functions in the module
pytestmark = pytest.mark.anyio


class TestCreateNote:
    async def test_success(self, db_session):
        note = await create_note(db_session, 'test_create_note', 'Desc')
        assert note is not None


class TestGetNote:
    async def test_success(self, db_session):
        _note = await create_note(db_session, 'test_get_note', 'Desc')
        note = await get_note_by_id(db_session, _note.id)
        assert note is not None

    async def test_fail(self, db_session):
        note = await get_note_by_id(db_session, 100)
        assert note is not None


class TestGetNotes:
    async def test_empty(self, db_session):
        notes = await get_notes(db_session)
        assert len(notes) == 0

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
    async def test_success(self, db_session):
        _note = await create_note(db_session, 'test update note', 'Desc')
        await update_note(
            db_session,
            _note.id,
            name='updated name',
            desc='Updated desc'
        )
        note = await get_note_by_id(db_session, _note.id)

        assert _note.id == note.id
        assert _note.name != note.name
        assert _note.desc != note.desc

    async def test_fail(self, db_session):
        with pytest.raises(HTTPException):
            await update_note(db_session, 100, 'New Note', 'new desc')


class TestDeleteNote:
    async def test_success(self, db_session):
        _note = await create_note(db_session, 'test update note', 'Desc')
        await delete_note(db_session, _note.id)

        note = await get_note_by_id(db_session, _note.id)
        assert note is None

    async def test_fail(self, db_session):
        with pytest.raises(HTTPException):
            await update_note(db_session, 100, 'New Note', 'new desc')
