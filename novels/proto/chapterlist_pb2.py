# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chapterlist.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11\x63hapterlist.proto\x12\x08\x63hapters\"\xa8\x01\n\x07\x43hapter\x12\x10\n\x08novel_id\x18\x01 \x01(\x05\x12\r\n\x05title\x18\x02 \x01(\t\x12\x11\n\ttimestamp\x18\x03 \x01(\t\x12\r\n\x05index\x18\x04 \x01(\x05\x12\x12\n\nsubchapter\x18\x05 \x01(\x05\x12\x13\n\x0bnovel_title\x18\x06 \x01(\t\x12\x11\n\timage_url\x18\x07 \x01(\t\x12\x0e\n\x06\x61uthor\x18\x08 \x01(\t\x12\x0e\n\x06images\x18\t \x01(\t\"^\n\x0c\x43haptersList\x12#\n\x08\x63hapters\x18\x01 \x03(\x0b\x32\x11.chapters.Chapter\x12\x13\n\x0btotal_pages\x18\x02 \x01(\x05\x12\x14\n\x0c\x63urrent_page\x18\x03 \x01(\x05\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chapterlist_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CHAPTER._serialized_start=32
  _CHAPTER._serialized_end=200
  _CHAPTERSLIST._serialized_start=202
  _CHAPTERSLIST._serialized_end=296
# @@protoc_insertion_point(module_scope)
