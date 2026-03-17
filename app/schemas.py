from pydantic import BaseModel, ConfigDict


class BaseNoteSchema(BaseModel):
    name: str
    desc: str | None


class CreateNoteParams(BaseNoteSchema):
    ...


class NoteDetailResponse(BaseNoteSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int

    # class Config:
    #     # to be able to load sqlalchemy model
    #     from_attributes = True


class UpdateNoteParams(BaseNoteSchema):
    ...


class UpdateNoteResponse(BaseModel):
    success: bool
