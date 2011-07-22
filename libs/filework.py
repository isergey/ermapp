# encoding: utf-8 -*-
import uuid
import binascii

def save_content_to_file(upload_file, dir_path, file_name='', file_ext='tmp'):
    print type(file)
    if dir_path[-1] != '/':
        dir_path += '/'

    if not file_name:
        file_name = str(binascii.crc32(str(uuid.uuid4()))&0xffffffff) + '.' + file_ext

    file_path = dir_path + file_name
    destination = open(file_path, 'wb+')
    for chunk in upload_file.chunks():
        destination.write(chunk)
    destination.close()

    return file_path