import sys
import requests
import argparse

# ANSI escape codes for color formatting
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Display the colorful message
message = f"{GREEN}Coded by {YELLOW}ya3raj{CYAN}!{RESET}"
print(message)

def get_response_status(domain):
    try:
        http_url = f"http://{domain}"
        https_url = f"https://{domain}"
        http_response = requests.head(http_url, verify=True, timeout=5)  # Enable SSL certificate verification and set timeout
        https_response = requests.head(https_url, verify=True, timeout=5)  # Enable SSL certificate verification and set timeout
        
        http_status = http_response.status_code
        https_status = https_response.status_code
        return domain, http_status, https_status
    except requests.RequestException as e:
        return domain, None, None

def check_git_vulnerability(domain, http_status, https_status, vulnerable_domains, verbose=False):
    try:
        http_git_url = f"http://{domain}/.git/HEAD"
        https_git_url = f"https://{domain}/.git/HEAD"
        
        http_response = requests.get(http_git_url, verify=True, timeout=5)  # Enable SSL certificate verification and set timeout
        https_response = requests.get(https_git_url, verify=True, timeout=5)  # Enable SSL certificate verification and set timeout
        
        if "refs/heads" in http_response.text or "refs/heads" in https_response.text:
            vulnerable_domains.append((domain, http_status, https_status))
            print(f"{GREEN}{domain} is vulnerable.{RESET} (HTTP: {http_status}, HTTPS: {https_status})")
        elif verbose:
            print(f"{domain} is not vulnerable. (HTTP: {http_status}, HTTPS: {https_status})")
    except requests.RequestException:
        if verbose:
            print(f"Error accessing {domain}. It may not be reachable or the .git directory is not exposed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check Git vulnerability of domains in a file or scan a single domain.")
    parser.add_argument("file_path", nargs="?", help="Path to the file containing domain names")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
    parser.add_argument("-u", "--single_domain", help="Scan a single domain for Git vulnerability")
    args = parser.parse_args()
    
    if args.single_domain and args.file_path:
        print("Please provide either a file path or a single domain to scan, not both.")
        sys.exit(1)
    
    if args.single_domain:
        domain_list = [args.single_domain]
    elif args.file_path:
        try:
            with open(args.file_path, "r") as file:
                domain_list = file.read().splitlines()
        except FileNotFoundError:
            print("File not found.")
            sys.exit(1)
    else:
        print("Please provide either a file path or a single domain to scan.")
        sys.exit(1)
    
    if args.verbose:
        if args.single_domain:
            print(f"Scanning domain: {args.single_domain}")
        else:
            print("Checking for duplicate domains...")
        
        # Remove duplicate domains
        domain_list = list(set(domain_list))
        
        if not args.single_domain:
            print("Unique domains:", domain_list)
            print("Checking domain reachability and Git vulnerabilities...")
        
    # Check reachability and Git vulnerabilities
    vulnerable_domains = []
    for domain, http_status, https_status in map(get_response_status, domain_list):
        check_git_vulnerability(domain, http_status, https_status, vulnerable_domains, args.verbose)
    
    if args.verbose and not args.single_domain:
        print("\nVulnerable Domains:")
        for domain, http_status, https_status in vulnerable_domains:
            print(f"{GREEN}{domain} is vulnerable.{RESET} (HTTP: {http_status}, HTTPS: {https_status})")
