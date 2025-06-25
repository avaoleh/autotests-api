# Импорт библиотек
from concurrent import futures  # Для многопоточности
import grpc  # Основной модуль gRPC
import course_service_pb2  # Сгенерированные сообщения
import course_service_pb2_grpc  # Сгенерированный серверный интерфейс


# Реализация серверного класса, наследуемого от Servicer
class CourseService(course_service_pb2_grpc.CourseServiceServicer):
    def GetCourse(self, request, context):
        """
        Обработчик метода GetCourse.
        Получает запрос с course_id и возвращает статичный ответ.
        """
        print("Received request for course_id:", request.course_id)

        # Формируем ответ
        return course_service_pb2.GetCourseResponse(
            course_id=request.course_id,
            title="API Python",
            description="playwright API AQA Python"
        )


def serve():
    """
    Запуск gRPC сервера.
    Сервер слушает порт 50051 и обслуживает запросы.
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Регистрируем реализацию сервиса в сервере
    course_service_pb2_grpc.add_CourseServiceServicer_to_server(CourseService(), server)

    # Настраиваем прослушивание на порту 50051
    server.add_insecure_port('[::]:50051')

    print("Server is running on port 50051...")

    # Запускаем сервер
    server.start()

    # Ждём завершения работы сервера
    server.wait_for_termination()


# Точка входа в программу
if __name__ == '__main__':
    serve()