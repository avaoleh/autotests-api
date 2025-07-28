from http import HTTPStatus

import pytest
import json

from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, \
    GetExercisesResponseSchema, ExerciseSchema, UpdateExerciseRequestSchema
from fixtures.courses import CourseFixture
from fixtures.exercises import ExerciseFixture
from tools.assertions.base import assert_status_code, assert_equal
from tools.assertions.exercises import assert_create_exercise_response, assert_get_exercise_response, \
    assert_update_exercise_response, assert_exercise_not_found_response, assert_get_exercises_response
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
        response_data = CreateExerciseResponseSchema.model_validate_json(response.text)
        # Извлекаем ExerciseSchema для assert_get_exercise_response
        exercise_from_get = response_data.exercise

        # 5. Проверяем тело ответа с помощью новой функции assert
        # Передаем ExerciseSchema из GET и ExerciseSchema из POST (function_exercise.response.exercise)
        assert_get_exercise_response(exercise_from_get, function_exercise.response.exercise)

        # 6. Проверяем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_update_exercise(
            self,
            exercises_client: ExercisesClient,
            function_exercise: ExerciseFixture # Используем фикстуру, которая создает задание
    ):
        """
        Тест обновления данных задания по его ID.
        Выполняет PATCH-запрос к /api/v1/exercises/{exercise_id}.
        Проверяет статус-код, тело ответа и JSON-схему.
        :param exercises_client: Клиент для работы с заданиями.
        :param function_exercise: Фикстура, содержащая данные созданного задания.
        """
        # 1. Получаем ID задания из фикстуры
        exercise_id = function_exercise.response.exercise.id
        print(f"Updating exercise with ID: {exercise_id}")

        # 2. Формируем данные для обновления задания
        # Обновим, например, title и description
        update_request = UpdateExerciseRequestSchema(
            title="Новое название задания",
            description="Новое описание задания"
            # Остальные поля остаются None и не будут отправлены в запросе
            # благодаря exclude_none=True в update_exercise_api
        )
        print(f"Update request JSON being prepared: {json.dumps(update_request.model_dump(by_alias=True, exclude_none=True), indent=2, ensure_ascii=False)}")
        print(f"Update request JSON being sent: {json.dumps(update_request.model_dump(by_alias=True), indent=2, ensure_ascii=False)}")

        # 3. Отправляем PATCH-запрос на обновление задания
        # Используем метод, возвращающий httpx.Response
        response_api = exercises_client.update_exercise_api(exercise_id, update_request)
        print(f"Response status code: {response_api.status_code}")
        print(f"Response text: {response_api.text}")

        # 4. Проверяем статус-код ответа
        assert_status_code(response_api.status_code, HTTPStatus.OK)

        # 5. Десериализуем JSON-ответ в Pydantic-модель
        update_response_wrapper = CreateExerciseResponseSchema.model_validate_json(response_api.text)
        updated_exercise_data = update_response_wrapper.exercise # Извлекаем ExerciseSchema

        # 6. Проверяем, что данные в ответе соответствуют запросу на обновление
        # Передаем ExerciseSchema из ответа и UpdateExerciseRequestSchema из запроса
        assert_update_exercise_response(updated_exercise_data, update_request)

        # 7. Проверяем, что неизмененные поля остались такими же, как в оригинальном задании
        # (кроме тех, которые были обновлены)
        original_exercise = function_exercise.response.exercise
        # Проверяем поля, которые НЕ обновлялись
        assert_equal(updated_exercise_data.id, original_exercise.id, "id")
        assert_equal(updated_exercise_data.course_id, original_exercise.course_id, "course_id")
        assert_equal(updated_exercise_data.max_score, original_exercise.max_score, "max_score")
        assert_equal(updated_exercise_data.min_score, original_exercise.min_score, "min_score")
        assert_equal(updated_exercise_data.order_index, original_exercise.order_index, "order_index")
        # Проверяем, что обновленные поля действительно изменились (если они были в запросе)
        # Эти проверки уже сделаны в assert_update_exercise_response, но можно добавить явно
        # assert_equal(updated_exercise_data.title, update_request.title, "title (after update)")
        # assert_equal(updated_exercise_data.description, update_request.description, "description (after update)")

    def test_delete_exercise(
            self,
            exercises_client: ExercisesClient,
            function_exercise: ExerciseFixture # Используем фикстуру, которая создает задание
    ):
        """
        Тест удаления задания по его ID и проверка, что оно действительно удалено.
        Выполняет DELETE-запрос к /api/v1/exercises/{exercise_id}.
        Затем выполняет GET-запрос к тому же ID и проверяет ошибку 404.
        :param exercises_client: Клиент для работы с заданиями.
        :param function_exercise: Фикстура, содержащая данные созданного задания.
        """
        # 1. Получаем ID задания из фикстуры
        exercise_id = function_exercise.response.exercise.id
        print(f"Deleting exercise with ID: {exercise_id}")

        # 2. Отправляем DELETE-запрос на удаление задания
        delete_response = exercises_client.delete_exercise_api(exercise_id)

        # 3. Проверяем статус-код ответа на удаление
        assert_status_code(delete_response.status_code, HTTPStatus.OK)
        # Или, если DELETE должен возвращать 204 No Content (часто используемый стандарт)
        # assert_status_code(delete_response.status_code, HTTPStatus.NO_CONTENT)

        # 4. Отправляем GET-запрос на получение удаленного задания
        get_response_after_delete = exercises_client.get_exercise_api(exercise_id)

        # 5. Проверяем статус-код ответа на GET (должен быть 404 Not Found)
        assert_status_code(get_response_after_delete.status_code, HTTPStatus.NOT_FOUND)

        # 6. Проверяем тело ответа на GET (должно содержать ошибку "Exercise not found")
        # Десериализуем ответ об ошибке
        # десериализовать JSON ответа в модель ошибки
        error_response_data = InternalErrorResponseSchema.model_validate_json(get_response_after_delete.text)
        # Проверяем, что ошибка соответствует ожидаемой
        assert_exercise_not_found_response(error_response_data)

        # 7. Провалидируем JSON schema ответа на ошибку
        validate_json_schema(get_response_after_delete.json(), error_response_data.model_json_schema())

    def test_get_exercises(
            self,
            exercises_client: ExercisesClient,
            function_exercise: ExerciseFixture, # Создает одно задание и обеспечивает course_id
            # function_course: CourseFixture # Не обязательно, если function_exercise дает нужный course_id
    ):
        """
        Тест получения списка заданий по course_id.
        Выполняет GET-запрос к /api/v1/exercises с параметром courseId.
        Проверяет статус-код, тело ответа и JSON-схему.
        :param exercises_client: Клиент для работы с заданиями.
        :param function_exercise: Фикстура, создающая одно тестовое задание.
                               Используется для получения course_id.
        """
        # 1. Получаем ID курса из созданного задания
        # Предполагаем, что задание привязано к курсу
        course_id = function_exercise.request.course_id # Или function_exercise.response.exercise.course_id
        print(f"Getting exercises for course ID: {course_id}")

        # 2. Формируем параметры запроса
        # ИСПРАВЛЕНО: Имя параметра должно соответствовать спецификации API - "courseId"
        # ---------------------------------------------------------------
        query_params = {"courseId": course_id}
        # ---------------------------------------------------------------

        # 3. Отправляем GET-запрос на получение списка заданий
        response_api = exercises_client.get_exercises_api(query_params)

        # 4. Проверяем статус-код ответа
        # Добавим отладочный вывод в случае ошибки
        if response_api.status_code != HTTPStatus.OK:
             print(f"Error response text: {response_api.text}")
        assert_status_code(response_api.status_code, HTTPStatus.OK)

        # 5. Десериализуем JSON-ответ в Pydantic-модель
        response_data = GetExercisesResponseSchema.model_validate_json(response_api.text)

        # 6. Проверяем тело ответа
        # Мы ожидаем, что в списке будет как минимум одно задание,
        # созданное фикстурой function_exercise.
        expected_exercises_list = [function_exercise.response.exercise]
        assert_get_exercises_response(response_data, expected_exercises_list)

        # 7. Провалидируем JSON-схему ответа
        validate_json_schema(response_api.json(), response_data.model_json_schema())

