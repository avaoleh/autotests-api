
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


class CoursesClient(APIClient):
    """
    Клиент для работы с /api/v1/courses
    """

    def get_courses_api(self, query: GetCoursesQuerySchema) -> Response:
        return self.get("/api/v1/courses", params=query.model_dump(by_alias=True))

    def get_course_api(self, course_id: str) -> Response:
        return self.get(f"/api/v1/courses/{course_id}")

    def create_course_api(self, request: CreateCourseRequestSchema) -> Response:
        return self.post("/api/v1/courses", json=request.model_dump(by_alias=True))

    def update_course_api(self, course_id: str, request: UpdateCourseRequestSchema) -> Response:
        return self.patch(f"/api/v1/courses/{course_id}", json=request.model_dump(by_alias=True))

    def delete_course_api(self, course_id: str) -> Response:
        return self.delete(f"/api/v1/courses/{course_id}")

    # === Методы, возвращающие модели ===

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