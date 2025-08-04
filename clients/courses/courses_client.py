
from httpx import Response
from clients.api_client import APIClient
from clients.courses.courses_schema import (
    CourseSchema,
    CreateCourseRequestSchema,
    UpdateCourseRequestSchema,
    GetCoursesQuerySchema,
    CreateCourseResponseSchema,
)
from clients.private_http_builder import AuthenticationUserSchema, get_private_http_client
import allure
from tools.routes import APIRoutes
from clients.api_coverage import tracker
class CoursesClient(APIClient):
    """
    Клиент для работы с /api/v1/courses
    """

    @allure.step("Get courses")
    # Добавили сбор покрытия для эндпоинта GET /api/v1/courses
    @tracker.track_coverage_httpx(APIRoutes.COURSES)
    def get_courses_api(self, query: GetCoursesQuerySchema) -> Response:

        # Вместо /api/v1/courses используем APIRoutes.COURSES
        return self.get(APIRoutes.COURSES, params=query.model_dump(by_alias=True))

    @allure.step("Get course by id {course_id}")
    # Добавили сбор покрытия для эндпоинта GET /api/v1/courses/{course_id}
    @tracker.track_coverage_httpx(f"{APIRoutes.COURSES}/{{course_id}}")
    def get_course_api(self, course_id: str) -> Response:
        # Вместо /api/v1/courses используем APIRoutes.COURSES
        return self.get(f"{APIRoutes.COURSES}/{course_id}")

    @allure.step("Create course")
    # Добавили сбор покрытия для эндпоинта POST /api/v1/courses
    @tracker.track_coverage_httpx(APIRoutes.COURSES)
    def create_course_api(self, request: CreateCourseRequestSchema) -> Response:
        # Вместо /api/v1/courses используем APIRoutes.COURSES
        return self.post(APIRoutes.COURSES, json=request.model_dump(by_alias=True))

    @allure.step("Update course by id {course_id}")
    # Добавили сбор покрытия для эндпоинта PATCH /api/v1/courses/{course_id}
    @tracker.track_coverage_httpx(f"{APIRoutes.COURSES}/{{course_id}}")
    def update_course_api(self, course_id: str, request: UpdateCourseRequestSchema) -> Response:
        # Вместо /api/v1/courses используем APIRoutes.COURSES
        return self.patch(
            f"{APIRoutes.COURSES}/{course_id}",
            json=request.model_dump(by_alias=True)
        )

    @allure.step("Delete course by id {course_id}")
    # Добавили сбор покрытия для эндпоинта DELETE /api/v1/courses/{course_id}
    @tracker.track_coverage_httpx(f"{APIRoutes.COURSES}/{{course_id}}")
    def delete_course_api(self, course_id: str) -> Response:
        # Вместо /api/v1/courses используем APIRoutes.COURSES
        return self.delete(f"{APIRoutes.COURSES}/{course_id}")


    @allure.step("Delete course by id {course_id}")
    def get_courses(self, query: GetCoursesQuerySchema) -> list[CourseSchema]:
        response = self.get_courses_api(query)
        data = response.json()
        return [CourseSchema(**item) for item in data.get("courses", [])]

    def get_course(self, course_id: str) -> CourseSchema:
        response = self.get_course_api(course_id)
        data = response.json()
        return CourseSchema.model_validate_json(response.text)

    def create_course(self, request: CreateCourseRequestSchema) -> CreateCourseResponseSchema:
        response = self.create_course_api(request)
        return CreateCourseResponseSchema.model_validate_json(response.text)

    def update_course(self, course_id: str, request: UpdateCourseRequestSchema) -> CourseSchema:
        response = self.update_course_api(course_id, request)
        return CourseSchema.model_validate_json(response.text)

    def delete_course(self, course_id: str) -> None:
        response = self.delete_course_api(course_id)
        response.raise_for_status()


def get_courses_client(user: AuthenticationUserSchema) -> CoursesClient:
    return CoursesClient(client=get_private_http_client(user))