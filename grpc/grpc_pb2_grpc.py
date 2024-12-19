# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT! python -m grpc_tools.protoc -I./grpc/ --python_out=./grpc/ --grpc_python_out=./grpc/ grpc.proto
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import grpc_pb2 as grpc__pb2

GRPC_GENERATED_VERSION = '1.68.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in grpc_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class TaskServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateTask = channel.unary_unary(
                '/tasklist.TaskService/CreateTask',
                request_serializer=grpc__pb2.Task.SerializeToString,
                response_deserializer=grpc__pb2.OperationResponse.FromString,
                _registered_method=True)
        self.GetTasks = channel.unary_stream(
                '/tasklist.TaskService/GetTasks',
                request_serializer=grpc__pb2.ChatId.SerializeToString,
                response_deserializer=grpc__pb2.TaskResponse.FromString,
                _registered_method=True)
        self.UpdateTask = channel.unary_unary(
                '/tasklist.TaskService/UpdateTask',
                request_serializer=grpc__pb2.TaskUpdate.SerializeToString,
                response_deserializer=grpc__pb2.OperationResponse.FromString,
                _registered_method=True)
        self.CompleteTask = channel.unary_unary(
                '/tasklist.TaskService/CompleteTask',
                request_serializer=grpc__pb2.TaskIdent.SerializeToString,
                response_deserializer=grpc__pb2.OperationResponse.FromString,
                _registered_method=True)
        self.RemoveTask = channel.unary_unary(
                '/tasklist.TaskService/RemoveTask',
                request_serializer=grpc__pb2.TaskIdent.SerializeToString,
                response_deserializer=grpc__pb2.OperationResponse.FromString,
                _registered_method=True)


class TaskServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateTask(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTasks(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateTask(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CompleteTask(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RemoveTask(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TaskServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateTask': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateTask,
                    request_deserializer=grpc__pb2.Task.FromString,
                    response_serializer=grpc__pb2.OperationResponse.SerializeToString,
            ),
            'GetTasks': grpc.unary_stream_rpc_method_handler(
                    servicer.GetTasks,
                    request_deserializer=grpc__pb2.ChatId.FromString,
                    response_serializer=grpc__pb2.TaskResponse.SerializeToString,
            ),
            'UpdateTask': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateTask,
                    request_deserializer=grpc__pb2.TaskUpdate.FromString,
                    response_serializer=grpc__pb2.OperationResponse.SerializeToString,
            ),
            'CompleteTask': grpc.unary_unary_rpc_method_handler(
                    servicer.CompleteTask,
                    request_deserializer=grpc__pb2.TaskIdent.FromString,
                    response_serializer=grpc__pb2.OperationResponse.SerializeToString,
            ),
            'RemoveTask': grpc.unary_unary_rpc_method_handler(
                    servicer.RemoveTask,
                    request_deserializer=grpc__pb2.TaskIdent.FromString,
                    response_serializer=grpc__pb2.OperationResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'tasklist.TaskService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('tasklist.TaskService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class TaskService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateTask(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/tasklist.TaskService/CreateTask',
            grpc__pb2.Task.SerializeToString,
            grpc__pb2.OperationResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetTasks(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/tasklist.TaskService/GetTasks',
            grpc__pb2.ChatId.SerializeToString,
            grpc__pb2.TaskResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UpdateTask(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/tasklist.TaskService/UpdateTask',
            grpc__pb2.TaskUpdate.SerializeToString,
            grpc__pb2.OperationResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def CompleteTask(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/tasklist.TaskService/CompleteTask',
            grpc__pb2.TaskIdent.SerializeToString,
            grpc__pb2.OperationResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def RemoveTask(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/tasklist.TaskService/RemoveTask',
            grpc__pb2.TaskIdent.SerializeToString,
            grpc__pb2.OperationResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)