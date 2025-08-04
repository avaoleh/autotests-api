from httpx import Response
from clients.api_client import APIClient
from clients.exercises.exercises_schema import (
    ExerciseSchema,
    GetExercisesResponseSchema,
    CreateExerciseRequestSchema,
    UpdateExerciseRequestSchema,
    CreateExerciseResponseSchema,
)
from clients.private_http_builder import AuthenticationUserSchema, get_private_http_client
import allure
from tools.routes import APIRoutes

class ExercisesClient(APIClient):
    """
    Клиент для работы с /api/v1/exercises.
    Предоставляет методы для получения, создания, обновления и удаления заданий.
    """

    @allure.step("Get exercises")
    def get_exercises_api(self, query: dict) -> Response:
        #return self.get("/api/v1/exercises", params=query)
        return self.get(APIRoutes.EXERCISES, params=query)

    @allure.step("Get exercise by id {exercises_id}")
    def get_exercise_api(self, exercise_id: str) -> Response:
        #return self.get(f"/api/v1/exercises/{exercise_id}")
        return self.get(f"{APIRoutes.EXERCISES}/{exercise_id}")

    @allure.step("Create exercise")
    def create_exercise_api(self, request: CreateExerciseRequestSchema) -> Response:
        #return self.post("/api/v1/exercises", json=request.model_dump(by_alias=True))
        return self.post(APIRoutes.EXERCISES, json=request.model_dump(by_alias=True))

    @allure.step("Update exercise")
    def update_exercise_api(self, exercise_id: str, request: UpdateExerciseRequestSchema) -> Response:
        #return self.patch(
        #    f"/api/v1/exercises/{exercise_id}",
            # -----------------------------------------------
        #    json=request.model_dump(by_alias=True, exclude_none=True)
            # -----------------------------------------------
        #)

        return self.patch(
            f"{APIRoutes.EXERCISES}/{exercise_id}",
            json=request.model_dump(by_alias=True, exclude_none=True)
        )

    @allure.step("Delete exercise")
    def delete_exercise_api(self, exercise_id: str) -> Response:
        #return self.delete(f"/api/v1/exercises/{exercise_id}")
        return self.delete(f"{APIRoutes.EXERCISES}/{exercise_id}")

    # === Методы, возвращающие модели ===

    def get_exercises(self, query: dict) -> GetExercisesResponseSchema:
        response = self.get_exercises_api(query)
        return GetExercisesResponseSchema.model_validate_json(response.text)

    def get_exercise(self, exercise_id: str) -> ExerciseSchema:
        response = self.get_exercise_api(exercise_id)
        return ExerciseSchema.model_validate_json(response.text)

    def create_exercise(self, request: CreateExerciseRequestSchema) -> CreateExerciseResponseSchema:
        response = self.create_exercise_api(request)
        return CreateExerciseResponseSchema.model_validate_json(response.text)

    def update_exercise(self, exercise_id: str, request: UpdateExerciseRequestSchema) -> ExerciseSchema:
        response = self.update_exercise_api(exercise_id, request)
        return ExerciseSchema.model_validate_json(response.text)


def get_exercises_client(user: AuthenticationUserSchema) -> ExercisesClient:
    """
    Функция создаёт экземпляр ExercisesClient с уже настроенным HTTP-клиентом.
    :return: Готовый к использованию ExercisesClient.
    """
    return ExercisesClient(client=get_private_http_client(user))