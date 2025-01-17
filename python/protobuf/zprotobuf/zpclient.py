import grpc
from protos_py import zp_pb2
from protos_py import zp_pb2_grpc


def run():
    with grpc.insecure_channel("0.0.0.0:9019") as channel:
        stub = zp_pb2_grpc.ZenPlayerServiceStub(channel)
        response = stub.get_details(
            zp_pb2.TrackDetailsRequest("Bob", "Dylan", "Bobby"))

        print("response = " + str(response.results))

if __name__ == "__main__":
    run()
