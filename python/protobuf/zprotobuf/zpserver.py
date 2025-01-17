import grpc
from protos_py import zp_pb2
from protos_py import zp_pb2_grpc
from concurrent import futures


class ZenplayerServicer(zp_pb2_grpc.ZenPlayerServiceServicer):

    def get_details(self, request, context):
        """ Return the details of the track."""
        return Results(text="Yebo baby!!!")


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    zp_pb2_grpc.add_ZenPlayerServiceServicer_to_server(
        ZenplayerServicer(), server
    )

    server.add_insecure_port('[::]:9019')
    server.start()
    print("Server started!")
    server.wait_for_termination()


main()
