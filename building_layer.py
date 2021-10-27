import argparse
import os

import boto3


def read_zip_file(zip_path):
    def file_get_contents(filename):
        with open(filename) as f:
            return f.read()

    return "fileb://" + zip_path


parser = argparse.ArgumentParser(description="Building Layer")
parser.add_argument("--layer_name", default="slayer-site-packages", type=str)
parser.add_argument("--layer_description", default="", type=str)
parser.add_argument("--bucket_name", default="flaner-layer-test", type=str)
parser.add_argument("--is_windows", default=False, type=bool)
parser.add_argument("--all_profile", default=False, type=bool)

ALL_PROFILE = ["default"]

opt = parser.parse_args()

layer_name = opt.layer_name
layer_description = opt.layer_description
bucket_name = opt.bucket_name

is_windows = opt.is_windows
print("We are running on windows: {}".format(is_windows))

"""
We start by zipping our layer. We assume that \python already holds everything.
"""
if is_windows == False:
    cmd = "zip -r slayer-site-packages.zip python"
    os.system("rm -rf slayer-site-packages.zip")
    print("Zip layers deleted. Can now be replaced.")
    os.system(cmd)
else:
    import shutil

    shutil.make_archive("slayer-site-packages", "zip", "python")

layer_zip_path = "slayer-site-packages.zip"

def upload_and_build_layer(full_bucket_name):
    # We now upload our zip file to a bucket
    s3_client.upload_file(layer_zip_path, full_bucket_name, layer_zip_path)

    #We now call the lambda client, and push a Layer with this zip file.
    #We currently assume our runtime as Python 3.8
    curr_runtime = ["python3.8"]

    lambda_client.publish_layer_version(
        LayerName=layer_name,
        Description=layer_description,
        Content={"S3Bucket": full_bucket_name, "S3Key": layer_zip_path},
        CompatibleRuntimes=curr_runtime,
    )

if opt.all_profile:
    for aws_profile in ALL_PROFILE:
        print("Uploading with the profile : ")
        print(aws_profile)
        session = boto3.Session(profile_name=aws_profile, region_name="eu-west-1")
        s3_client = session.client("s3")
        lambda_client = session.client("lambda")
        to_add = "" if aws_profile == "default" else aws_profile.split("_")[0]
        print("and the bucket:")
        print(bucket_name + to_add)
        upload_and_build_layer(bucket_name + to_add)
        del session
else:
    s3_client = boto3.client("s3")
    lambda_client = boto3.client("lambda")
    upload_and_build_layer(bucket_name)

