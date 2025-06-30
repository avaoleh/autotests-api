# clients/courses/courses_schema.py

from pydantic import BaseModel, Field
from typing import Optional, List
from clients.users.users_schema import UserSchema as User
from clients.files.files_schema import FileSchema as File


class CourseSchema(BaseModel):
    model_config = {'populate_by_name': True}

    id: str
    title: str
    maxScore: int = Field(..., alias="maxScore")
    minScore: int = Field(..., alias="minScore")
    description: str = Field(..., alias="description")
    estimatedTime: str = Field(..., alias="estimatedTime")
    previewFile: File = Field(..., alias="previewFile")
    createdByUser: User = Field(..., alias="createdByUser")


class CreateCourseRequestSchema(BaseModel):
    model_config = {'populate_by_name': True}

    title: str
    maxScore: int = Field(..., alias="maxScore")
    minScore: int = Field(..., alias="minScore")
    description: str = Field(..., alias="description")
    estimatedTime: str = Field(..., alias="estimatedTime")
    previewFileId: str = Field(..., alias="previewFileId")
    createdByUserId: str = Field(..., alias="createdByUserId")


class UpdateCourseRequestSchema(BaseModel):
    model_config = {'populate_by_name': True}

    title: Optional[str] = None
    maxScore: Optional[int] = None
    minScore: Optional[int] = None
    description: Optional[str] = None
    estimatedTime: Optional[str] = None


class GetCoursesQuerySchema(BaseModel):
    model_config = {'populate_by_name': True}

    userId: str = Field(..., alias="userId")


class CreateCourseResponseSchema(BaseModel):
    course: CourseSchema


class GetCoursesResponseSchema(BaseModel):
    courses: List[CourseSchema]