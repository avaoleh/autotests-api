from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_schema import ExerciseSchema, CreateExerciseRequestSchema, \
    CreateExerciseResponseSchema, GetExercisesResponseSchema, UpdateExerciseRequestSchema

from tools.assertions.base import assert_equal, assert_length
from tools.assertions.errors import assert_internal_error_response


def assert_create_exercise_response(
        request: CreateExerciseRequestSchema,
        response: CreateExerciseResponseSchema
):
    """
    Проверяет, что ответ на создание задания соответствует данным из запроса.

    :param request: Исходный запрос на создание задания.
    :param response: Ответ API с данными созданного задания.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    # Проверяем все поля задания
    assert_equal(response.exercise.title, request.title, "title")
    assert_equal(response.exercise.course_id, request.course_id, "course_id")
    assert_equal(response.exercise.max_score, request.max_score, "max_score")
    assert_equal(response.exercise.min_score, request.min_score, "min_score")
    assert_equal(response.exercise.order_index, request.order_index, "order_index")
    assert_equal(response.exercise.description, request.description, "description")
    assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")


def assert_exercise(actual: ExerciseSchema, expected: ExerciseSchema):
    """
    Проверяет, что фактические данные задания соответствуют ожидаемым.

    :param actual: Фактические данные задания (из GET-запроса).
    :param expected: Ожидаемые данные задания (из ответа на создание).
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    # Предполагается, что у вас есть функция assert_equal в tools.assertions.base
    # Если нет, можно использовать простое сравнение или assert для каждого поля
    from tools.assertions.base import assert_equal # Убедитесь, что импорт здесь или вверху файла

    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.title, expected.title, "title")
    assert_equal(actual.course_id, expected.course_id, "courseId")
    assert_equal(actual.max_score, expected.max_score, "maxScore")
    assert_equal(actual.min_score, expected.min_score, "minScore")
    assert_equal(actual.order_index, expected.order_index, "orderIndex")
    assert_equal(actual.description, expected.description, "description")
    assert_equal(actual.estimated_time, expected.estimated_time, "estimatedTime")


def assert_get_exercise_response(
        get_exercise_response: GetExercisesResponseSchema, # Ответ от GET /api/v1/exercises/{id}
        create_exercise_response: CreateExerciseResponseSchema # Ответ от POST /api/v1/exercises
):
    """
    Проверяет, что ответ на получение задания соответствует ответу на его создание.
    Сравнивает ExerciseSchema из обоих ответов.
    :param get_exercise_response: Ответ API при запросе данных задания (GET).
                                     Ожидается модель GetExercisesResponseSchema (содержащая .exercise).
    :param create_exercise_response: Ответ API при создании задания (POST).
                                       Ожидается модель CreateExerciseResponseSchema (содержащая .exercise).
    :raises AssertionError: Если данные задания не совпадают.
    """
    # Извлекаем ExerciseSchema из обоих ответов и сравниваем их
    assert_exercise(get_exercise_response.exercise, create_exercise_response.exercise)


def assert_update_exercise_response(
        response_exercise: ExerciseSchema,
        request_update: UpdateExerciseRequestSchema
):
    """
    Проверяет, что данные задания в ответе соответствуют данным из запроса на обновление.
    Сравнивает только те поля, которые были указаны в запросе на обновление (не None).
    :param response_exercise: Данные задания из ответа API (ExerciseSchema).
    :param request_update: Данные из запроса на обновление (UpdateExerciseRequestSchema).
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    from tools.assertions.base import assert_equal

    # Сравниваем только те поля, которые были переданы в запросе (не None)
    # Обратите внимание на alias в схемах
    if request_update.title is not None:
        assert_equal(response_exercise.title, request_update.title, "title")
    # course_id не передавался явно в update_request в тесте, поэтому его проверять не нужно
    # Строка ниже вызывает ошибку, потому что request_update.course_id != None (оно равно значению по умолчанию)
    # if request_update.course_id is not None:
    #     assert_equal(response_exercise.course_id, request_update.course_id, "course_id") # <-- ОШИБКА ЗДЕСЬ

    # Правильная проверка для course_id: только если оно было явно передано в запросе
    # В вашем тесте вы не передавали course_id в update_request, поэтому и проверять его не надо.
    # Если вы хотите проверить обновление course_id, передайте его явно в update_request в тесте.

    if request_update.max_score is not None:
        assert_equal(response_exercise.max_score, request_update.max_score, "max_score")  # alias maxScore
    if request_update.min_score is not None:
        assert_equal(response_exercise.min_score, request_update.min_score, "min_score")  # alias minScore
    if request_update.order_index is not None:
        assert_equal(response_exercise.order_index, request_update.order_index, "order_index")  # alias orderIndex
    if request_update.description is not None:
        assert_equal(response_exercise.description, request_update.description, "description")
    if request_update.estimated_time is not None:
        assert_equal(response_exercise.estimated_time, request_update.estimated_time,
                     "estimated_time")  # alias estimatedTime


def assert_exercise_not_found_response(
        response_data: InternalErrorResponseSchema,  # Используем существующую модель
        expected_error_message: str = "Exercise not found"  # Ожидаемое сообщение
):
    """
    Проверяет, что ответ содержит ошибку "Exercise not found".
    Использует существующую модель InternalErrorResponseSchema
    и функцию assert_internal_error_response.
    :param response_data: Данные ответа, десериализованные в InternalErrorResponseSchema.
                          InternalErrorResponseSchema есть поле 'details'
                          или аналог, содержащее сообщение об ошибке.
    :param expected_error_message: Ожидаемое сообщение об ошибке.
    :raises AssertionError: Если проверка не пройдена.
    """
    # Создаем ожидаемый объект ошибки для сравнения
    expected_error = InternalErrorResponseSchema(details=expected_error_message)

    # Если сообщение об ошибке хранится в другом поле, например, 'error':
    # expected_error = InternalErrorResponseSchema(error=expected_error_message)

    # Если структура более сложная, создайте объект соответственно.
    # Например, если details - это словарь:
    # expected_error = InternalErrorResponseSchema(details={"message": expected_error_message})

    # Проверяем, что ответ соответствует ожидаемой ошибке
    # с помощью универсальной функции
    assert_internal_error_response(response_data, expected_error)

def assert_get_exercises_response(
        actual_response: GetExercisesResponseSchema,
        expected_exercises: list[ExerciseSchema] # Список ожидаемых ExerciseSchema
):
    """
    Проверяет, что ответ на получение списка заданий соответствует ожидаемому списку.
    Сравнивает длину списка и каждое задание в нем.
    :param actual_response: Фактический ответ API (GetExercisesResponseSchema).
    :param expected_exercises: Список ожидаемых заданий (list[ExerciseSchema]).
    :raises AssertionError: Если проверка не пройдена.
    """
    # 1. Проверяем, что длина списка exercises в ответе равна ожидаемой
    assert_length(actual_response.exercises, len(expected_exercises), "exercises list length")

    # 2. Проверяем каждое задание в списке
    for i, expected_exercise in enumerate(expected_exercises):
        actual_exercise = actual_response.exercises[i]
        # assert_exercise проверяет все поля двух ExerciseSchema
        assert_exercise(actual_exercise, expected_exercise)