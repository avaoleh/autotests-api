
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from clients.users.users_schema import UserSchema as User
from clients.files.files_schema import FileSchema as File

from tools.fakers import fake

class CourseSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    max_score: int = Field(alias="maxScore")
    min_score: int = Field(alias="minScore")
    description: str = Field(alias="description")
    estimated_time: str = Field(alias="estimatedTime")
    preview_file: File = Field(alias="previewFile")
    created_by_user: User = Field( alias="createdByUserId")


class CreateCourseRequestSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    title: str = Field(default_factory=fake.sentence)
    max_score: int = Field(alias="maxScore", default_factory=fake.max_score)
    min_score: int = Field(alias="minScore", default_factory=fake.min_score)
    description: str = Field(default_factory=fake.text)
    estimated_time: str = Field(alias="estimatedTime", default_factory=fake.estimated_time)
    preview_file_id: str = Field(alias="previewFileId", default_factory=fake.uuid4)
    created_by_user_id: str = Field(alias="createdByUserId", default_factory=fake.uuid4)


class UpdateCourseRequestSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    title: str | None = Field(default_factory=fake.sentence)
    max_score: int | None = Field(alias="maxScore", default_factory=fake.max_score)
    min_score: int | None = Field(alias="minScore", default_factory=fake.min_score)
    description: str | None = Field(default_factory=fake.text)
    estimated_time: str | None = Field(alias="estimatedTime", default_factory=fake.estimated_time)


class GetCoursesQuerySchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias="userId")


class CreateCourseResponseSchema(BaseModel):
    course: CourseSchema


class GetCoursesResponseSchema(BaseModel):
    courses: List[CourseSchema]

class UpdateCourseResponseSchema(BaseModel):
    """
    Описание структуры ответа обновления курса.
    """
    course: CourseSchema