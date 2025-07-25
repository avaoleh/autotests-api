from clients.exercises.exercises_schema import ExerciseSchema, CreateExerciseRequestSchema, \
    CreateExerciseResponseSchema, GetExercisesResponseSchema

from tools.assertions.base import assert_equal


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