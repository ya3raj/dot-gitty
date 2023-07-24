## Check Git Exposed in domains in a file or scan a single domain.
Scans using both http and https

usage: python dotgitty.py [-h] [-v] [-u SINGLE_DOMAIN] [file_path]

positional arguments:
  file_path          Path to the file containing domain names

optional arguments:
 *  -h, --help            show this help message and exit 
 *  -v, --verbose         Enable verbose mode 
 *  -u SINGLE_DOMAIN, --single_domain SINGLE_DOMAIN 

## For Single url 
python script.py -u example.com 

## For list of Urls
python script.py ~/root/domains.txt -v 

## Make sur you use the -v command or else you will see an empty terminal!!!
