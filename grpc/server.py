from concurrent import futures
import grpc
import grpc_pb2_grpc
import grpc_pb2


class TaskService(grpc_pb2_grpc.TaskServiceServicer):
    def __init__(self):
        self.db = dict()

    def CreateTask(self, request, context):
        if request.id.id in self.db:
            self.db[request.id.id].append(grpc_pb2.TaskResponse(num=len(self.db[request.id.id]) + 1, text=request.text, is_completed=False))
        else:
            self.db[request.id.id] = [grpc_pb2.TaskResponse(num=1, text=request.text, is_completed=False)]
        return grpc_pb2.OperationResponse(text='Task created')

    def GetTasks(self, request, context):
        if request.id in self.db:
            for task in self.db[request.id]:
                yield task

    def UpdateTask(self, request, context):
        if request.id.id in self.db:
            self.db[request.id.id][request.num - 1].text = request.text
            self.db[request.id.id][request.num - 1].is_completed = False
            return grpc_pb2.OperationResponse(text='Task updated')
        return grpc_pb2.OperationResponse(text='Task not found')

    def CompleteTask(self, request, context):
        if request.id.id in self.db and (request.num - 1) < len(self.db[request.id.id]):
            self.db[request.id.id][request.num - 1].is_completed = True
            return grpc_pb2.OperationResponse(text='Task completed')
        return grpc_pb2.OperationResponse(text='Task not found')

    def RemoveTask(self, request, context):
        if request.id.id in self.db and (request.num - 1) < len(self.db[request.id.id]):
            for i in range(request.num, len(self.db[request.id.id])):
                self.db[request.id.id][i].num -= 1
            self.db[request.id.id].pop(request.num - 1)
            return grpc_pb2.OperationResponse(text='Task removed')
        return grpc_pb2.OperationResponse(text='Task not found')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grpc_pb2_grpc.add_TaskServiceServicer_to_server(TaskService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()