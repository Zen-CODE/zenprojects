# ZPProtobuf - ZenPlayer Protobuf Interface

This project provides a protobuf interface for ZenPlayer.

# Development

In order to compile the protocol files:
```bash
python -m grpc_tools.protoc -I./protos protos/zp.proto --python_out=. --grpc_python_out=.
```