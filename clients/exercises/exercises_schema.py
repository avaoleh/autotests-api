
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from tools.fakers import fake


class ExerciseSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    course_id: str = Field(alias="courseId")
    max_score: int = Field(alias="maxScore")
    min_score: int = Field(alias="minScore")
    order_index: int = Field(alias="orderIndex")
    description: str = Field(alias="description")
    estimated_time: str = Field(alias="estimatedTime")


class CreateExerciseRequestSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    title: str = Field(default_factory=fake.sentence)
    course_id: str = Field(alias="courseId", default_factory=fake.uuid4)
    max_score: int = Field(alias="maxScore", default_factory=fake.max_score)
    min_score: int = Field(alias="minScore", default_factory=fake.min_score)
    order_index: int = Field(alias="orderIndex", default_factory=fake.integer)
    description: str = Field(alias="description", default_factory=fake.text)
    estimated_time: str = Field(alias="estimatedTime", default_factory=fake.estimated_time)


class GetExercisesResponseSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    exercises: List[ExerciseSchema]


class CreateExerciseResponseSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    exercise: ExerciseSchema


class UpdateExerciseRequestSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    title: Optional[str] = Field(default=None)
    course_id: Optional[str] = Field(alias="courseId", default=None)
    max_score: Optional[int] = Field(alias="maxScore", default=None)
    min_score: Optional[int] = Field(alias="minScore", default=None)
    order_index: Optional[int] = Field(alias="orderIndex", default=None)
    description: Optional[str] = Field(alias="description", default=None)
    estimated_time: Optional[str] = Field(alias="estimatedTime", default=None)