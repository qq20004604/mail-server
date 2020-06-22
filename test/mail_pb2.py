# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mail.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='mail.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\nmail.proto\"Z\n\x13SendTextMailRequest\x12\x10\n\x08receiver\x18\x01 \x03(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\x12\x11\n\tsecretkey\x18\x04 \x01(\t\".\n\x11SendTextMailReply\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x05\x12\x0b\n\x03msg\x18\x02 \x01(\t2L\n\x12MailManagerService\x12\x36\n\x08SendMail\x12\x14.SendTextMailRequest\x1a\x12.SendTextMailReply\"\x00\x62\x06proto3')
)




_SENDTEXTMAILREQUEST = _descriptor.Descriptor(
  name='SendTextMailRequest',
  full_name='SendTextMailRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='receiver', full_name='SendTextMailRequest.receiver', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='title', full_name='SendTextMailRequest.title', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='content', full_name='SendTextMailRequest.content', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='secretkey', full_name='SendTextMailRequest.secretkey', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=14,
  serialized_end=104,
)


_SENDTEXTMAILREPLY = _descriptor.Descriptor(
  name='SendTextMailReply',
  full_name='SendTextMailReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='code', full_name='SendTextMailReply.code', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='msg', full_name='SendTextMailReply.msg', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=106,
  serialized_end=152,
)

DESCRIPTOR.message_types_by_name['SendTextMailRequest'] = _SENDTEXTMAILREQUEST
DESCRIPTOR.message_types_by_name['SendTextMailReply'] = _SENDTEXTMAILREPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SendTextMailRequest = _reflection.GeneratedProtocolMessageType('SendTextMailRequest', (_message.Message,), {
  'DESCRIPTOR' : _SENDTEXTMAILREQUEST,
  '__module__' : 'mail_pb2'
  # @@protoc_insertion_point(class_scope:SendTextMailRequest)
  })
_sym_db.RegisterMessage(SendTextMailRequest)

SendTextMailReply = _reflection.GeneratedProtocolMessageType('SendTextMailReply', (_message.Message,), {
  'DESCRIPTOR' : _SENDTEXTMAILREPLY,
  '__module__' : 'mail_pb2'
  # @@protoc_insertion_point(class_scope:SendTextMailReply)
  })
_sym_db.RegisterMessage(SendTextMailReply)



_MAILMANAGERSERVICE = _descriptor.ServiceDescriptor(
  name='MailManagerService',
  full_name='MailManagerService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=154,
  serialized_end=230,
  methods=[
  _descriptor.MethodDescriptor(
    name='SendMail',
    full_name='MailManagerService.SendMail',
    index=0,
    containing_service=None,
    input_type=_SENDTEXTMAILREQUEST,
    output_type=_SENDTEXTMAILREPLY,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_MAILMANAGERSERVICE)

DESCRIPTOR.services_by_name['MailManagerService'] = _MAILMANAGERSERVICE

# @@protoc_insertion_point(module_scope)
