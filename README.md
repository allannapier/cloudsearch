# cloudsearch

This script will allow you to quickly search both your local directories and a S3 Bucket for a file using a search term.

Please ensure you fill in the s3_bucket and local_path, if you don't wish to search one of them just set the variable to '' and ensure it has been omitted from the locations list underneath.

In order to run once downloaded, run the following command in terminal, change searchphrase to whatever you are looking for, i.e. "invoice 20921"

python3 -m search "searchphrase"
