# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: zp.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'zp.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x08zp.proto\"F\n\x13TrackDetailsRequest\x12\x0e\n\x06\x61rtist\x18\x01 \x01(\t\x12\r\n\x05\x61lbum\x18\x02 \x01(\t\x12\x10\n\x08\x66ileName\x18\x03 \x01(\t\"\x16\n\x06Result\x12\x0c\n\x04text\x18\x01 \x01(\t2@\n\x10ZenPlayerService\x12,\n\x0bget_details\x12\x14.TrackDetailsRequest\x1a\x07.Resultb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'zp_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_TRACKDETAILSREQUEST']._serialized_start=12
  _globals['_TRACKDETAILSREQUEST']._serialized_end=82
  _globals['_RESULT']._serialized_start=84
  _globals['_RESULT']._serialized_end=106
  _globals['_ZENPLAYERSERVICE']._serialized_start=108
  _globals['_ZENPLAYERSERVICE']._serialized_end=172
# @@protoc_insertion_point(module_scope)
