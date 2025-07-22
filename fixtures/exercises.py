import pytest
from pydantic import BaseModel

from clients.exercises.exercises_client import get_exercises_client, ExercisesClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema
from fixtures.courses import CourseFixture


class ExerciseFixture(BaseModel):
    """
    Фикстура, содержащая данные о запросе на создание задания
    и ответе от сервиса.
    """
    request: CreateExerciseRequestSchema
    response: CreateExerciseResponseSchema


@pytest.fixture
def exercises_client(function_course: CourseFixture) -> ExercisesClient:
    """
    Фикстура для создания клиента API заданий.
    Использует аутентификацию от пользователя, связанного с курсом.
    """
    return get_exercises_client(function_course.authentication_user)


@pytest.fixture
def function_exercise(exercises_client: ExercisesClient, function_course: CourseFixture) -> ExerciseFixture:
    """
    Создаёт тестовое задание с использованием корректного course_id из function_course.
    Возвращает объект ExerciseFixture с запросом и ответом.
    """

    request = CreateExerciseRequestSchema(
        course_id=function_course.response.course_id  # Указываем реальный ID курса
    )
    response = exercises_client.create_exercise(request)
    return ExerciseFixture(request=request, response=response)