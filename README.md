usage: script.py [-h] [-v] [-u SINGLE_DOMAIN] [file_path]

Check Git vulnerability of domains in a file or scan a single domain.

positional arguments:
  file_path             Path to the file containing domain names

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Enable verbose mode
  -u SINGLE_DOMAIN, --single_domain SINGLE_DOMAIN

  python script.py -u example.com
  python script.py ~/root/domain.txt -v 
