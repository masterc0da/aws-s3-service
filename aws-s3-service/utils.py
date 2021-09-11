import uuid


def create_bucket_name(bucket_prefix):
    # The generated bucket name must be between 3 and 63 chars long
    """
    :param bucket_prefix:
    :return: bucket name which consists bucket_prefix and generated uuid
    :rtype: str
    """
    return ''.join([bucket_prefix, str(uuid.uuid4())])


def create_temp_file(size, file_name, file_content):
    """
    :param size: number of file_content replication
    :param file_name: file name to be created
    :param file_content: file content
    :return: random file name after file creation
    :rtype: str
    """
    random_file_name = ''.join([str(uuid.uuid4().hex[:6]), file_name])
    with open(random_file_name, 'w') as f:
        f.write(str(file_content) * size)
    return random_file_name
