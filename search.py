import os 
import glob
import datetime
import boto3
from botocore.exceptions import ClientError
import pprint
import argparse

#PLEASE FILL IN THE TWO VARIABLES BELOW WITH CORRECT DETAILS BEFORE RUNNING
#YOU MUST HAVE YOUR AWS CREDENTIALS SET IN ENVIRONMENT ALREADY, DON'T SAVE THEM IN THE CODE, THAT IS NOT SECURE
s3_bucket = None
local_path = None
locations = ['local','S3']

def index_files(locations,my_path=None):
    filelist = []
    if s3_bucket == None or local_path == None:
        print('You have not set the variables yet for s3_bucket and local_path, please do this before running again.')
        quit()
    else:
        if 'local' in locations:

            for file in glob.iglob(my_path + '/**/*', recursive=True):

                stat_info = os.stat(file)
                # get size of file in bytes
                if os.path.isfile(file):
                    size = round(stat_info.st_size/(1024*1024),2)
                    t = os.path.getmtime(file)
                    fileinfo = {"filename":file,"sizeMB":size,"lastmodified":datetime.datetime.fromtimestamp(t),"provider":"local"}
                    filelist.append(fileinfo)

        if 'S3' in locations:
            s3 = boto3.client('s3')
            for key in s3.list_objects(Bucket=s3_bucket)['Contents']:
                    fileinfo = {"filename":key['Key'],"sizeMB":round(key['Size']/(1024*1024),2),"lastmodified":key['LastModified'],"provider":"S3"}
                    filelist.append(fileinfo)

        return filelist

def search_for_file(filelist,term):
    found = True
    result = []
    while found:
        
        search_result = next((x for x in filelist if term[0] in x["filename"]),None )
        if search_result:
            result.append(search_result)
            filelist.remove(search_result)
        else:
            found = False
        
    return result

parser = argparse.ArgumentParser(description='Search for files')
parser.add_argument('searchterm', metavar='N', type=str, nargs='+',
                    help='a string to search for in filenames')

args = parser.parse_args()

files = index_files(locations,local_path)

pprint.pprint(search_for_file(files,args.searchterm))