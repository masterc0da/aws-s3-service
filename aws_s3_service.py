import utils
import boto3


def create_bucket(bucket_prefix, s3_connection):
    """
    :param bucket_prefix: bucket prefix name
    :param s3_connection: instance of client connection to s3
    :return: bucket name with uuid + response (dict)
    """
    session = boto3.session.Session()
    current_region = session.region_name
    bucket_name = utils.create_bucket_name(bucket_prefix)
    bucket_response = s3_connection.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': current_region})
    print(bucket_name, current_region)
    return bucket_name, bucket_response


def create_buckets_and_upload_file(s3_client,
                                   s3_resource,
                                   first_bucket_name,
                                   second_bucket_name,
                                   first_file_name):
    """
    Creating two buckets with specified names and upload specified file to them
    :param s3_client: instance of S3 client we are working with
    :param s3_resource: instance of S3  we are working with
    :param first_bucket_name: name of first specified bucket
    :param second_bucket_name: name of second specified bucket
    :param first_file_name: specified name of file to be upload
    :return: names of first,second bucket and of uploaded file
    :rtype: tuple(str, str, str)
    """

    _first_bucket_name, _first_response = create_bucket(
        bucket_prefix=first_bucket_name,
        s3_connection=s3_resource.meta.client)
    print(f"\tFirst bucket name: {first_bucket_name}")

    _second_bucket_name, _second_response = create_bucket(
        bucket_prefix=second_bucket_name, s3_connection=s3_resource)
    print(f"\tSecond bucket name: {_second_bucket_name}")

    _first_file_name = utils.create_temp_file(300, first_file_name, 'f')
    print(f"\tFirst file name: {_first_file_name}")

    s3_resource.Object(_first_bucket_name, _first_file_name).upload_file(
        Filename=_first_file_name)

    return _first_bucket_name, _second_bucket_name, _first_file_name


def copy_to_bucket(
        s3_resource,
        bucket_from_name: str,
        bucket_to_name: str,
        file_name: str):
    """
    Copy from one bucket to another
    :param s3_resource: s3 instance we working with
    :param bucket_from_name: name of bucket we are copying from
    :param bucket_to_name: name of bucket we are copying to
    :param file_name: name of the file we are copying
    :return: void
    """
    copy_source = {
        'Bucket': bucket_from_name,
        'Key': file_name
    }
    s3_resource.Object(bucket_to_name,
                       file_name
                       ).copy(copy_source)


def download_file(s3_resource,
                  bucket_name,
                  file_name
                  ):
    """
    Downloading specified file from specified bucket
    :param s3_resource: instance of S3 we are working with
    :param bucket_name: specified bucket name
    :param file_name: specified file name
    :param path: dir path, default /tmp/
    :return: void, downloading file
    """
    s3_resource.Object(bucket_name,
                       file_name
                       ).download_file(file_name)
    print(f"\tDownloaded File: {file_name} from bucket {bucket_name}")


def enable_bucket_versioning(
        s3_resource,
        bucket_name: str):
    """
    Enables versioning to specific bucket
    :param s3_resource: s3 instance we are working with
    :param bucket_name: bucket name we want to enable for versioning
    :return: void
    """
    bkt_versioning = s3_resource.BucketVersioning(bucket_name)
    bkt_versioning.enable()
    print(bkt_versioning.status)


def bucket_traversal(s3_resource):
    """
    Prints all bucket`s name
    :param s3_resource: s3 instance we are working with
    :return: print all bucket names
    """
    for bucket in s3_resource.buckets.all():
        print(bucket.name)


def acl(s3_resource,
        bucket_name,
        file_name):
    """
    Creating file in S3 and granting different ACL permissions.
    :param s3_resource: instance of s3 we are working with
    :param bucket_name: specified bucket name
    :param file_name: specified file name
    :return: name of created and uploaded file
    """
    print(f"\tCreate and upload {file_name} ot\n\t\t{bucket_name}")
    _file_name = utils.create_temp_file(400, file_name, 's')
    _object = s3_resource.Object(bucket_name, file_name)
    _object.upload_file(
        _file_name,
        ExtraArgs={
            'ACL': 'public-read'}
    )
    print(f"\tFile name to be uploaded: {_file_name}")

    _object_acl = _object.Acl()
    print(f"\tGrants public permissions:\n\t{_object_acl.grants}")

    _response = _object_acl.put(ACL='private')
    print(f"\tGrants private permissions:\n\t{_object_acl.grants}")

    return _file_name


def create_encrypted_file_and_upload(s3_resource,
                                     bucket_name,
                                     file_name):
    """
    Creating file with specified file name in S3 bucket and encrypting it with AES256.
    :param s3_resource: instance of S3 we are working with
    :param bucket_name: specified bucket name we are working with
    :param file_name: specified file name to be encrypted
    :return: name of encrypted file
    """

    _file_name = utils.create_temp_file(300, file_name, 't')
    _object = s3_resource.Object(bucket_name, _file_name)
    _object.upload_file(
        _file_name,
        ExtraArgs={
            'ServerSideEncryption': 'AES256'}
    )
    print(f"\tUploaded file name: {_file_name}")
    print(f"\tUploaded file encryption: {_object.server_side_encryption}")

    return _file_name


def storage(s3_resource,
            bucket_name,
            file_name):
    """
    Reloading specified file with encryption and STANDARD_IA storage class
    :param s3_resource: instance of S3 we are working with
    :param bucket_name: specified bucket name we are working with
    :param file_name: specified file name to be reloaded
    :return:
    """

    _object = s3_resource.Object(
        bucket_name,
        file_name
    )

    _object.upload_file(
        file_name,
        ExtraArgs={
            'ServerSideEncryption': 'AES256',
            'StorageClass': 'STANDARD_IA'}
    )

    _object.reload()
    print(f"\t Reloading storage class: {_object.storage_class}")


def add_versioning(s3_resource,
                   bucket_name,
                   file_name):
    """
    Adding new file as version of existing file.
    :param s3_resource: instance of S3 we are working with
    :param bucket_name: specified bucket name we are working with
    :param file_name: specified file name
    :return: void
    """

    enable_bucket_versioning(s3_resource, bucket_name)

    print(f"\tAdd versioning to {file_name}")
    s3_resource.Object(
        bucket_name,
        file_name
    ).upload_file(
        file_name)

    print(f"First file Version ID:{s3_resource.Object(bucket_name, file_name).version_id}")


def print_objects(bucket):
    """
    Print all objects in bucket
    :param bucket: instance of bucket
    :return:printing all object names in the specified bucket
    """
    for obj in bucket.objects.all():
        print(obj.key)


def delete_file_from_bucket(first_file_name, s3_resource, second_bucket_name):
    s3_resource.Object(second_bucket_name, first_file_name).delete()


def delete_all_objects_in_bucket(s3_resource,
                                 bucket_name):
    """
    Deletes all objects and their versions in specified bucket
    :param s3_resource: instance of s3 we are working with
    :param bucket_name: name of specified bucket
    :return: void
    """
    res = []
    s3_bucket = s3_resource.Bucket(bucket_name)
    s3_bucket.object_versions.all().delete()
    s3_bucket.objects.all().delete()


def delete_all_buckets(s3_client, s3_resource):
    """
    :param s3_client: instance of S3 client we are working with
    :param s3_resource: instance of S3 we are working with
    :return:
    """
    buckets = s3_client.list_buckets()

    for bucket in buckets['Buckets']:
        s3_bucket = s3_resource.Bucket(bucket['Name'])
        s3_bucket.objects.all().delete()
        print(f"All objects in Bucket: {s3_bucket} were deleted")
        s3_bucket.delete()
        print(f"Bucket {s3_bucket} was deleted")



def delete_bucket(bucket_name, s3_resource):
    s3_resource.Bucket(bucket_name).delete()
