import boto3

import aws_s3_service

S3_CLIENT = None
S3_RESOURCE = None
S3_CLIENT = None
S3_RESOURCE = None
FIRST_BUCKET_NAME = "dima-aws-first-bucket"
SECOND_BUCKET_NAME = "dima-aws-second-bucket"
FIRST_FILE_NAME = "first-file.txt"
SECOND_FILE_NAME = "second-file.txt"
THIRD_FILE_NAME = "third-file.txt"


def main(s3_client, s3_resource):

    # Creating 2 buckets and uploading file
    print("Stage 1. Creating 2 buckets, and uploading the file")
    (first_bucket_name,
     second_bucket_name,
     first_file_name) = aws_s3_service.create_buckets_and_upload_file(s3_client,
                                                                      s3_resource,
                                                                      FIRST_BUCKET_NAME,
                                                                      SECOND_BUCKET_NAME,
                                                                      FIRST_FILE_NAME)
    # Downloading specified file
    print("Stage 2. Downloading specified file ")
    aws_s3_service.download_file(s3_resource,
                                 first_bucket_name,
                                 first_file_name)

    # Copying file between specified buckets
    print("Stage 3. Copying file between specified buckets")
    aws_s3_service.copy_to_bucket(S3_RESOURCE,
                                  first_bucket_name,
                                  second_bucket_name,
                                  first_file_name)

    # Deleting first file from second bucket
    print("Stage 4. Deleting specified file from specified bucket.")
    print(f"Deleting {first_file_name} from\n\t{second_bucket_name}")
    aws_s3_service.delete_file_from_bucket(first_file_name, s3_resource, second_bucket_name)

    # ACL. Creating second file in first bucket and granting ACL
    print("Stage 5. Creating second file in first bucket and granting ACL")
    second_file_name = aws_s3_service.acl(s3_resource,
                                          first_bucket_name,
                                          SECOND_FILE_NAME)
    print(f"Created file name {second_file_name} ")

    # Creating/Uploading of encrypted file into first bucket
    print("Stage 6. Creating/Uploading of encrypted file into first bucket ")
    third_file_name = aws_s3_service.create_encrypted_file_and_upload(s3_resource,
                                                                      first_bucket_name,
                                                                      THIRD_FILE_NAME)

    # Storage. Reloading specified file with encryption and STANDARD_IA storage class
    print("Stage 7. Reloading specified file with encryption and STANDARD_IA storage class")
    aws_s3_service.storage(s3_resource,
                           first_bucket_name,
                           third_file_name)

    # Versioning. Adding new files as version of existing files
    print("Stage 8. Adding new files as version of existing files")
    aws_s3_service.add_versioning(s3_resource, first_bucket_name, first_file_name)

    # Buckets Traversal
    print("Stage 9. Traverse all buckets in s3 instance.")
    aws_s3_service.bucket_traversal(s3_resource)

    # Objects Traversal
    print("Stage 10. Traverse all objects in specified bucket")
    aws_s3_service.print_objects(s3_resource.Bucket(first_bucket_name))

    # Delete all objects in specified buckets
    print("Stage 11. Delete all objects in buckets")
    aws_s3_service.delete_all_objects_in_bucket(s3_resource, first_bucket_name)
    aws_s3_service.delete_all_objects_in_bucket(s3_resource, second_bucket_name)

    # Deleting buckets
    print("Stage 12. Delete all buckets")
    # aws_s3_service.delete_bucket(first_bucket_name, s3_resource)
    # aws_s3_service.delete_bucket(second_bucket_name, s3_resource)
    aws_s3_service.delete_all_buckets(s3_client, s3_resource)


if __name__ == '__main__':
    S3_CLIENT = boto3.client('s3')
    S3_RESOURCE = boto3.resource('s3')

    main(S3_CLIENT, S3_RESOURCE)
