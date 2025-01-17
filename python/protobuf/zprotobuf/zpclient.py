import grpc
import zp_pb2
import zp_pb2_grpc


def run():
    with grpc.insecure_channel("0.0.0.0:9019") as channel:
        stub = zp_pb2_grpc.ZenPlayerServiceStub(channel)
        response = stub.get_details(
            zp_pb2.TrackDetailsRequest(
                artist="Bob", album="Dylan", fileName="Bobby"))

        print("response = " + str(response.text))

if __name__ == "__main__":
    run()
