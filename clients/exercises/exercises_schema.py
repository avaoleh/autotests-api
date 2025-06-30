# clients/exercises/exercises_schema.py

from pydantic import BaseModel, Field
from typing import List, Optional


class ExerciseSchema(BaseModel):
    model_config = {'populate_by_name': True}

    id: str
    title: str
    courseId: str = Field(..., alias="courseId")
    maxScore: int = Field(..., alias="maxScore")
    minScore: int = Field(..., alias="minScore")
    orderIndex: int = Field(..., alias="orderIndex")
    description: str = Field(..., alias="description")
    estimatedTime: str = Field(..., alias="estimatedTime")


class CreateExerciseRequestSchema(BaseModel):
    model_config = {'populate_by_name': True}

    title: str
    courseId: str = Field(..., alias="courseId")
    maxScore: int = Field(..., alias="maxScore")
    minScore: int = Field(..., alias="minScore")
    orderIndex: int = Field(..., alias="orderIndex")
    description: str = Field(..., alias="description")
    estimatedTime: str = Field(..., alias="estimatedTime")


class GetExercisesResponseSchema(BaseModel):
    exercises: List[ExerciseSchema]


class CreateExerciseResponseSchema(BaseModel):
    exercise: ExerciseSchema


class UpdateExerciseRequestSchema(BaseModel):
    model_config = {'populate_by_name': True}

    title: Optional[str] = None
    courseId: Optional[str] = None
    maxScore: Optional[int] = None
    minScore: Optional[int] = None
    orderIndex: Optional[int] = None
    description: Optional[str] = None
    estimatedTime: Optional[str] = None
