from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import (
    create_note,
    get_notes,
    get_note_by_id,
    update_note,
    delete_note
)
from .dependencies import get_db_session
from .schemas import (
    CreateNoteParams,
    NoteDetailResponse,
    UpdateNoteParams,
    UpdateNoteResponse
)


router = APIRouter()


@router.get('/{note_id}', response_model=NoteDetailResponse)
async def get(
    note_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    note = await get_note_by_id(db, note_id)
    if note is None:
        raise HTTPException(404, 'Not found')
    return note


@router.put(
    '/{note_id}',
    status_code=202,
    # response_model=UpdateNoteResponse
    response_model=NoteDetailResponse
)
async def update(
    note_id: int,
    args: UpdateNoteParams,
    db: AsyncSession = Depends(get_db_session)
):
    note = await get_note_by_id(db, note_id)
    if note is None:
        raise HTTPException(404, 'Not found')

    await update_note(db, note_id, args.name, args.desc)

    # get note (after updated)
    note = await get_note_by_id(db, note_id)
    return note


@router.delete('/{note_id}', status_code=204)
async def delete(
    note_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    note = await get_note_by_id(db, note_id)
    if note is None:
        raise HTTPException(404, 'Not found')

    await delete_note(db, note_id)


@router.post('/', status_code=201, response_model=NoteDetailResponse)
async def create(
    args: CreateNoteParams,
    db: AsyncSession = Depends(get_db_session)
):
    note = await create_note(db, args.name, args.desc)
    return note


@router.get('/', response_model=list[NoteDetailResponse])
async def get_list(db: AsyncSession = Depends(get_db_session)):
    result = await get_notes(db)
    return result
