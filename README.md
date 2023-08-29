# BrutalForce

![BrutalForce - Banner](https://github.com/Zombrakes/BrutalForce/assets/113418799/bc9f9dc6-b14a-41c7-ad9d-a8063d686773)


## Description

BrutalForce is designed for performing brute-force, rate-limit, and race-condition attacks on web applications by trying different combinations of usernames and passwords, sending very customized requests based on the user input of arguments passed to the script. Script allows users to specify various parameters to control the attack, such as the use a word or regex as a filter for success, requests number per second, number of connections per request, number of connections per second, and more. It supports sending multiple HTTP requests in parallel to increase the speed of the attack using HTTP pipelining, HTTP pipelining is a technique or feature in HTTP 1.1 in which multiple HTTP requests are sent on a single TCP connection without waiting for the corresponding responses. Matching results are defined and highlighted in different color so it could be easily noticed by the user.

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Parameters](#parameters)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Important](#important)

## Installation

1. Clone or download the repository to your local machine:

   ```bash
   git clone https://github.com/Zombrakes/BrutalForce.git
   ```
   
2. Navigate to the script's directory:

```bash
  cd BrutalForce
```

3. Install the required dependencies using pip:

```bash
  pip install -r requirements.txt
```

## Usage
BrutalForce can be used to perform brute-force attacks against a target web application. It supports various parameters that allow you to customize the attack according to your needs include number of requests that could be sent per second, number of connection per each request, maximum connection per second, specify a word or a regex pattern to look for in response as a filter for success, and more.
![BrutalForce - GUI](https://github.com/Zombrakes/BrutalForce/assets/113418799/927de932-a7f1-4d22-9571-eb4628d04aee)

## Parameters

* <target_host>: The target host's IP address or domain name.
* <target_port>: The target host's port number.
* <usernames_file>: Path to a text file containing a list of usernames (one per line).
* <passwords_file>: Path to a text file containing a list of passwords (one per line).
* <requests_per_second>: Number of requests to be sent per second.
* <connections_per_request>: Number of connections to be made per request.
* <connections_per_second>: Maximum number of connections to be sent per second.
  
## Options
-A <API>: Use this option to specify an API for the target's host IP or domain name.
For more detailed information about the available parameters, you can run the script with the -h or --help option:

```bash
  python script.py -h
```

## Examples
Basic bruteforce usage: Using username and password list with success word as word to look for in response:
```bash
  python script.py localhost 8000 usernames.txt passwords.txt 10 5 2 "success"
```

Bruteforce usage with API: Using API with target host's IP address or domain, username, password list, and sucess as a word to look for in response:
```bash
  python script.py localhost 8000 usernames.txt passwords.txt 10 5 2 "success" -A /api/index
```

Race condition (TOCTTOU) or Rate-limit usage, all you need to do is to load empty usernames and passwords lists to trigger send_empty_params flag
```bash
   python script.py localhost 8000 usernames.txt passwords.txt 10 5 2 "success" -A /web
```

**NOTE**: If you going for bruteforce, you need to modify the parameter on line 218 based on your need.

## Contributing
Contributions are welcome! If you find any issues or have ideas for improvements, please open an issue or submit a pull request on the GitHub repository.

## License
BrutalForce is released under MIT license. See [LICENSE](https://github.com/Zombrakes/BrutalForce/blob/main/LICENSE)

## Important
**Remember:** BrutalForce is intended for ethical security testing purposes only. Always obtain proper authorization before testing any web application or API. Unauthorized testing can have legal consequences.
