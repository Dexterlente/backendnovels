# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: novels.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cnovels.proto\x12\x06novels\"M\n\x05Novel\x12\x10\n\x08novel_id\x18\x01 \x01(\x05\x12\r\n\x05title\x18\x02 \x01(\t\x12\x11\n\timage_url\x18\x03 \x01(\t\x12\x10\n\x08synopsis\x18\x04 \x01(\t\"U\n\tNovelList\x12\x1d\n\x06novels\x18\x01 \x03(\x0b\x32\r.novels.Novel\x12\x13\n\x0btotal_pages\x18\x02 \x01(\x05\x12\x14\n\x0c\x63urrent_page\x18\x03 \x01(\x05\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'novels_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _NOVEL._serialized_start=24
  _NOVEL._serialized_end=101
  _NOVELLIST._serialized_start=103
  _NOVELLIST._serialized_end=188
# @@protoc_insertion_point(module_scope)
