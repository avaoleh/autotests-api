
from clients.exercises.exercises_client import get_exercises_client, CreateExerciseRequestSchema
from clients.courses.courses_client import get_courses_client, CreateCourseRequestSchema
from clients.files.files_client import get_files_client
from clients.files.files_schema import CreateFileRequestSchema
from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema
from clients.private_http_builder import AuthenticationUserSchema


# Шаг 1: Создаем пользователя
public_users_client = get_public_users_client()
create_user_request = CreateUserRequestSchema()
create_user_response = public_users_client.create_user(create_user_request)
print("Create user data:", create_user_response)

# Инициализируем клиенты для дальнейших действий
authentication_user = AuthenticationUserSchema(
    email=create_user_request.email,
    password=create_user_request.password
)

files_client = get_files_client(authentication_user)
courses_client = get_courses_client(authentication_user)
exercises_client = get_exercises_client(authentication_user)

# Шаг 2: Загружаем файл
# create_file_request = CreateFileRequestSchema(
#     filename="image.png",
#     directory="courses",
#     upload_file="./testdata/files/image.png"
# )
create_file_request = CreateFileRequestSchema(upload_file="./testdata/files/image.png")

create_file_response = files_client.create_file(create_file_request)
print('Create file data:', create_file_response)

# Шаг 3: Создаем курс
create_course_request = CreateCourseRequestSchema(
    previewFileId=create_file_response.file.id,
    createdByUserId=create_user_response.user.id
)
create_course_response = courses_client.create_course(create_course_request)
print('Create course data:', create_course_response)

# Шаг 4: Создаем задание
create_exercise_request = CreateExerciseRequestSchema()
create_exercise_response = exercises_client.create_exercise(create_exercise_request)
print('Create exercise data:', create_exercise_response)