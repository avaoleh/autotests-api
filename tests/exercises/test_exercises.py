from http import HTTPStatus

import pytest

from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, \
    GetExercisesResponseSchema
from fixtures.courses import CourseFixture
from fixtures.exercises import ExerciseFixture
from tools.assertions.base import assert_status_code
from tools.assertions.exercises import assert_create_exercise_response, assert_get_exercise_response
from tools.assertions.schema import validate_json_schema


@pytest.mark.exercises
@pytest.mark.regression
class TestExercises:
    def test_create_exercise(
            self,
            exercises_client: ExercisesClient,
    ):
        """
        Тест создания задания через API.

        :param exercises_client: Клиент для работы с заданиями

        """
        # Формируем данные для создания задания, используя ID курса из фикстуры
        request = CreateExerciseRequestSchema()

        # Отправляем POST-запрос на создание задания
        response = exercises_client.create_exercise_api(request)

        # Десериализуем JSON-ответ в Pydantic-модель
        response_data = CreateExerciseResponseSchema.model_validate_json(response.text)

        # Проверяем статус-код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)

        # Проверяем, что данные в ответе соответствуют запросу
        assert_create_exercise_response(request, response_data)

        # Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_get_exercise(
            self,
            exercises_client: ExercisesClient,
            function_exercise: ExerciseFixture):
        """
        Тест получения данных задания по его ID.

        Отправляет GET-запрос к /api/v1/exercises/{exercise_id},
        используя ID задания, созданного фикстурой function_exercise.
        Проверяет статус-код, тело ответа и JSON-схему.
        """
        # 1. Получаем ID задания из фикстуры
        exercise_id = function_exercise.response.exercise.id
        print(f"exercise_id: {exercise_id}")
        # 2. Отправляем GET-запрос на получение задания
        response = exercises_client.get_exercise_api(exercise_id)


        # 3. Проверяем, что код ответа 200 OK
        assert_status_code(response.status_code, HTTPStatus.OK)

        # 4. Десериализуем тело ответа в схему ответа на получение
        response_data = GetExercisesResponseSchema.model_validate_json(response.text)

        # Проверяем, что код ответа 200 OK
        assert_status_code(response.status_code, HTTPStatus.OK)

        # 5. Проверяем тело ответа с помощью новой функции assert
        # Передаем response_data (результат GET) и function_exercise.response (результат POST)
        assert_get_exercise_response(response_data, function_exercise.response)

        # 6. Проверяем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())