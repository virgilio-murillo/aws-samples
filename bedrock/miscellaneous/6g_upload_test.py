import os
import boto3
from config import *
import base64
from urllib.parse import urlparse
import random
import string
import time
import time
from datetime import timedelta

print(boto3.__version__)

bedrock_agent = boto3.Session().client('bedrock-agent')

def generate_random_code():
    # Generate 4 random characters (uppercase letters)
    characters = ''.join(random.choices(string.ascii_uppercase, k=4))
    
    # Generate 12 digit number combining timestamp and random numbers
    timestamp = str(int(time.time()))
    random_digits = ''.join(random.choices(string.digits, k=6))
    number = (timestamp + random_digits)[-12:]  # Ensure 12 digits
    
    return characters, number

def s3_upload(s3_location):
    
    random_code = generate_random_code()
    documentIdentifier = str(random_code[0]) + str(random_code[1]) 
    document = { 
        'content':{
            'dataSourceType': 'CUSTOM',
            'custom':{
                'customDocumentIdentifier': {
                    'id': documentIdentifier
                },
                's3Location': {
                    'bucketOwnerAccountId': bucket_owner_account,
                    'uri': s3_location
                },
                'sourceType': 'S3_LOCATION'
            }
        }
    }
    
    documents = [document]

    response = bedrock_agent.ingest_knowledge_base_documents(
        dataSourceId = data_source_id, documents = documents, knowledgeBaseId = knowledgebase_id
    )
    return response



bucket_name = 'mainbucketrockhight5461'
s3_folder = 'test/knowledge-bases/pdffiles/'
s3_folder_uri = 's3://' + bucket_name + '/' + s3_folder 

# first we test the function
s3_uri = "s3://mainbucketrockhight5461/test/knowledge-bases/pdffiles/00627fcf4add0ded.pdf"
response = s3_upload(s3_uri)
print(response)


def append_to_file(filename, content):
    """
    Appends a string to a file. If the file doesn't exist, it creates it.
    
    :param filename: The name of the file to append to
    :param content: The string content to append
    """
    try:
        with open(filename, 'a') as file:
            file.write(content)
        print(f"Successfully appended content to {filename}")
    except IOError as e:
        print(f"An error occurred while appending to the file: {e}")

# Example usage:
# append_to_file('example.txt', 'This is some content to append.\n')

def traverse_s3_folder(bucket_name, folder_path):
    s3 = boto3.client('s3')
    
    # List objects in the specified folder
    paginator = s3.get_paginator('list_objects_v2')
    print(paginator)
    pages = paginator.paginate(Bucket=bucket_name, Prefix=folder_path)
    print(type(pages))
    counter = 0

    processed_files = 0
    total_time = 0
    start_time = time.time()
    
    for page in pages:
        if 'Contents' in page:
            for obj in page['Contents']:
                # Get the full S3 URI
                s3_uri = f"s3://{bucket_name}/{obj['Key']}"
                if obj['Size'] == 0:
                    continue
                
                # Call the s3_upload function and measure the time
                start_upload = time.time()
                try:
                    response = s3_upload(s3_uri)
                except:
                    print("error")    
                end_upload = time.time()
                
                upload_time = end_upload - start_upload
                total_time += upload_time
                processed_files += 1

                # Calculate average time and estimated time remaining
                avg_time = total_time / processed_files
                estimated_remaining = avg_time * (total_files - processed_files)

                if counter == 0 or counter == 5 or counter % 300 == 0:
                    print(response)
                    log = f"\rProcessed: {processed_files}/{total_files} |"
                    log +=  f"Progress: {processed_files/total_files*100:.2f}% |"
                    log += f" Avg time per file: {avg_time:.2f}s"
                    log += f"| Est. time remaining: {timedelta(seconds=int(estimated_remaining))}"
                    print(log,end='', flush=True)
                    append_to_file('log.txt',log)
                    append_to_file('log.txt', str(response))
                counter +=1

total_files = 83000
# Example usage
bucket_name = 'mainbucketrockhight5461'
folder_path = 'test/knowledge-bases/pdffiles/'

traverse_s3_folder(bucket_name, folder_path)


# we will list all the files with https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/client/list_knowledge_base_documents.html
response = bedrock_agent.list_knowledge_base_documents(
    dataSourceId=data_source_id,
    knowledgeBaseId=knowledgebase_id,
    maxResults=123,
)

print(len(response['documentDetails']))


print(response['nextToken'])
nextToken = response['nextToken']

# we will list all the files with https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/client/list_knowledge_base_documents.html
def list_section(nextToken):
    response = bedrock_agent.list_knowledge_base_documents(
        dataSourceId=data_source_id,
        knowledgeBaseId=knowledgebase_id,
        maxResults=123,
        nextToken = nextToken
    )
    return response

docsize = 5
sm = 0
counter = 0
while docsize > 1:
    response = list_section(nextToken)
    if 'nextToken' not in response:
        break
    nextToken = response['nextToken']
    sm += len(response['documentDetails'])
    if counter == 0 or counter == 7 or counter == 49 or counter %100 == 0:
        print(f"sum: {sm}, counter: {counter}")
    counter +=1
print(sm)


print(new_response['documentDetails'])





