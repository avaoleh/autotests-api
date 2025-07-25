import pytest
from pydantic import BaseModel

from clients.exercises.exercises_client import get_exercises_client, ExercisesClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema
from fixtures.courses import CourseFixture
from fixtures.users import UserFixture

class ExerciseFixture(BaseModel):
    """
    Фикстура, содержащая данные о запросе на создание задания
    и ответе от сервиса.
    """
    request: CreateExerciseRequestSchema
    response: CreateExerciseResponseSchema


@pytest.fixture
def exercises_client_(function_course: CourseFixture) -> ExercisesClient:
    """
    Фикстура для создания клиента API заданий.
    Использует аутентификацию от пользователя, связанного с курсом.
    """
    return get_exercises_client(function_course.authentication_user)

# Исправленная фикстура: теперь зависит от function_user, а не пытается получить
# authentication_user из function_course
@pytest.fixture
def exercises_client(function_user: UserFixture) -> ExercisesClient:
    """
    Фикстура для создания клиента API заданий.
    Использует аутентификацию от пользователя, связанного с курсом.
    (Предполагается, что это тот же пользователь, который создал курс).
    """
    return get_exercises_client(function_user.authentication_user)


@pytest.fixture
def function_exercise(
    exercises_client: ExercisesClient,
    function_course: CourseFixture # Эта зависимость нужна для получения course_id
) -> ExerciseFixture:
    """
    Создаёт тестовое задание с использованием корректного course_id из function_course.
    Возвращает объект ExerciseFixture с запросом и ответом.
    """

    # Исправлено: получаем ID курса через function_course.response.course.id
    request = CreateExerciseRequestSchema(
        course_id=function_course.response.course.id  # Указываем реальный ID курса
        # Поля title, max_score и т.д. будут заполнены значениями по умолчанию из фабрик
    )
    # Отправляем запрос на создание задания
    response = exercises_client.create_exercise(request) # Используем метод, возвращающий модель
    return ExerciseFixture(request=request, response=response)