from pydantic import BaseModel, ConfigDict


class BaseNoteSchema(BaseModel):
    name: str
    desc: str | None


class CreateNoteParams(BaseNoteSchema):
    ...


class NoteDetailResponse(BaseNoteSchema):
    # Configured to be able to load DB models data
    model_config = ConfigDict(from_attributes=True)

    id: int


class UpdateNoteParams(BaseNoteSchema):
    ...
