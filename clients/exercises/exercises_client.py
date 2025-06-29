from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient


class GetExercisesQueryDict(TypedDict):
    """
    Описание структуры параметров запроса на получение списка заданий.
    """
    courseId: str  # (query parameter)


class CreateExerciseRequestDict(TypedDict):
    """
    Описание структуры тела запроса для создания задания.
    """
    title: str
    courseId: str
    maxScore: int
    minScore: int
    orderIndex: int
    description: str
    estimatedTime: str


class UpdateExerciseRequestDict(TypedDict, total=False):
    """
    Описание структуры тела запроса для частичного обновления задания.
    Все поля необязательны.
    """
    title: str
    courseId: str
    maxScore: int
    minScore: int
    orderIndex: int
    description: str
    estimatedTime: str


class ExercisesClient(APIClient):
    """
    Клиент для работы с API эндпоинта /api/v1/exercises.
    Предоставляет методы для получения, создания, обновления и удаления заданий.
    """

    def get_exercises_api(self, query: GetExercisesQueryDict) -> Response:
        """
        Получить список заданий по идентификатору курса.

        :param query: Словарь с параметром courseId.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get("/api/v1/exercises", params=query)

    def get_exercise_api(self, exercise_id: str) -> Response:
        """
        Получить информацию о конкретном задании по его идентификатору.

        :param exercise_id: Идентификатор задания (UUID).
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(f"/api/v1/exercises/{exercise_id}")

    def create_exercise_api(self, request: CreateExerciseRequestDict) -> Response:
        """
        Создать новое задание.

        :param request: Словарь с данными нового задания.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post("/api/v1/exercises", json=request)

    def update_exercise_api(self, exercise_id: str, request: UpdateExerciseRequestDict) -> Response:
        """
        Обновить данные существующего задания.

        :param exercise_id: Идентификатор задания (UUID).
        :param request: Словарь с обновляемыми полями.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.patch(f"/api/v1/exercises/{exercise_id}", json=request)

    def delete_exercise_api(self, exercise_id: str) -> Response:
        """
        Удалить задание по его идентификатору.

        :param exercise_id: Идентификатор задания (UUID).
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.delete(f"/api/v1/exercises/{exercise_id}")