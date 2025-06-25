# Импорт библиотек
import grpc
import course_service_pb2
import course_service_pb2_grpc


def run():
    """
    Подключение к gRPC серверу и вызов метода GetCourse.
    """
    # Устанавливаем соединение с сервером
    with grpc.insecure_channel('localhost:50051') as channel:
        # Создаём клиентский stub (заглушку), через которую будем вызывать методы
        stub = course_service_pb2_grpc.CourseServiceStub(channel)

        # Формируем запрос
        request = course_service_pb2.GetCourseRequest(course_id="api-course")

        # Вызываем удалённый метод GetCourse
        response = stub.GetCourse(request)

        # Выводим полученный ответ
        print(response)


# Точка входа в клиентское приложение
if __name__ == '__main__':
    run()