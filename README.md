# HACKPHISHER

**Advanced Phishing Simulation Tool for Security Awareness and Penetration Testing**  
A powerful, Python-based Tool designed to create, manage, and deploy realistic phishing campaigns for security testing, training, and awareness — all with full control and customization.

---

## Overview

**HACKPHISHER** is a cutting-edge tool for simulating phishing attacks in controlled environments. It enables security professionals, red teams, and ethical hackers to craft convincing phishing pages, clone real websites, and capture credentials for analysis — all while maintaining ethical boundaries and legal compliance.

Unlike traditional phishing tools that rely on external services or limited templates, **HACKPHISHER** offers:

- **Native Python Implementation**: No dependencies on third-party engines or binaries.
- **Flexible Template Management**: Create, modify, and deploy custom phishing pages.
- **Interactive Credential Capture**: Automatically logs submitted credentials to a secure file.
- **Local Server Integration**: Built-in Flask server for quick deployment and testing.

The tool is designed for:

- **Penetration Testers**: Assess organizational vulnerability to phishing attacks.
- **Security Trainers**: Demonstrate real-world phishing techniques in awareness programs.
- **Red Teams**: Simulate advanced persistent threats (APTs) with realistic scenarios.

---

## Why HACKPHISHER?

Phishing remains one of the most effective attack vectors in cybersecurity. **HACKPHISHER** addresses the need for a customizable, transparent, and ethical tool to:

- **Test Defenses**: Evaluate how well users and systems detect and respond to phishing.
- **Educate Teams**: Provide hands-on examples of phishing tactics.
- **Improve Awareness**: Highlight the sophistication of modern phishing campaigns.

Key advantages:

- **Full Transparency**: Every line of code is open for inspection and modification.
- **Easy Deployment**: Run locally without complex setups.
- **Realistic Simulations**: Clone actual websites or use tailored templates.

---

## Core Features

### 1. Phishing Page Creation
- **Clone Real Websites**: Mirror any webpage by URL or local file.
- **Custom Templates**: Add, remove, or modify phishing templates dynamically.
- **Automatic Form Hijacking**: Inject hidden fields to capture credentials and IPs.

### 2. Credential Capture
- **Real-Time Logging**: Submitted credentials are saved to `credentials.txt`.
- **IP Tracking**: Logs attacker IPs for additional context.
- **Redirect Control**: Redirect victims to a legitimate page after submission.

### 3. Local Server
- **Built-in Flask Server**: Deploy phishing pages instantly on a local port.
- **Port Customization**: Choose any available port (default: `8080`).

### 4. User Experience
- **Interactive Menu**: Easy-to-navigate CLI for all operations.
- **Color-Coded Output**: Clear visual feedback for actions and errors.

---

## Installation Guide

### Prerequisites

- **Python 3.7+**: 
Python 3.7 or higher is required. Verify your Python version by running:

```bash
  python3 --version
```

---

## Step-by-Step Installation

1. Clone the Repository:

```bash
git clone https://github.com/davidvora/HACKPHISHER
cd HACKPHISHER
```

2. Verify Optional Dependencies:

```bash
pip install -r requirements.txt
```

Note: If the above command doesn't work (e.g., due to missing or broken environment), follow the optional steps below to set up a virtual environment and install the dependencies manually.

---

## Optional: Setting up a Virtual Environment

A. Check if `venv` is installed:

```bash
dpkg -s python3-venv
```

B. If it's not installed, install it with:

```bash
sudo apt install python3-venv
```

C. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

D. Now install the Dependencies again:

```bash
pip install -r requirements.txt
```

---

## Usage

1. Run The Tool:

```bash
python3 HACKPHISHER.py -i / --interactive
```

```
██╗  ██╗ █████╗  ██████╗██╗  ██╗  ███████╗██╗  ██╗██╗███████╗██╗  ██╗███████╗██████╗
██║  ██║██╔══██╗██╔════╝██║ ██╔╝  ██╔══██║██║  ██║██║██╔════╝██║  ██║██╔════╝██╔══██╗
███████║███████║██║     █████╔╝   ███████║███████║██║███████╗███████║█████╗  ██████╔╝
██╔══██║██╔══██║██║     ██╔═██╗   ██╔════╝██╔══██║██║╚════██║██╔══██║██╔══╝  ██╔══██╗
██║  ██║██║  ██║╚██████╗██║  ██╗  ██║     ██║  ██║██║███████║██║  ██║███████╗██║   ██║
╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝  ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝

Advanced Modular Phishing tool for Penetration Testing 

[!] WARNING: HACKPHISHER is a powerful offensive security Tool intended for ethical use only.
[!] Any unauthorized, illegal, or malicious use is strictly prohibited and may constitute a criminal offense.
[!] The creator of this Framework take no responsibility for misuse or any resulting damage.

by David Dvora
Version: v1.0

1. Start Phishing Campaign
2. Add New Template  
3. View Captured Credentials
4. Remove Template
5. Exit

Select an option:
```

---

## Examples

### Example 1: Clone Templates:

1. Clone a login Template With URL: (Example)

```
Select an option: 2
Template name: test
Clone type (url/path): url
URL to clone: https://example.com
Redirect URL after submit: https://example.com
Port 1024-9999 (default 8080): 8080
[+] Using localhost 
[+] Page cloned to Templates/test.html
[+] Template 'test' added successfully!

Press Enter to continue...
```

2. Clone a login Template With PATH: (Example)

```
Select an option: 2
Template name: test2
Clone type (url/path): path
Path to HTML file: /path/to/file.html
Redirect URL after submit: https://example.com
Port 1024-9999 (default 8080): 8080
[+] Using localhost 
[+] Page cloned to Templates/test2.html
[+] Template 'test2' added successfully!

Press Enter to continue...
```

3. (Optional) After Cloning Templates You can edit your Saved Templates in `templates.json` with nano or notepad: (Example)

```
{
    "test": {
        "path": "Templates/test.html",
        "redirect_url": "https://example.com",
        "port": 8080,
        "service": "localhost"
    },
    "test2": {
        "path": "Templates/test2.html",
        "redirect_url": "https://example.com",
        "port": 8080,
        "service": "localhost"
    }
}
```

---

### Example 2: Start Phishing Campaign:

1. Start Phishing Attack: (Example)

```
Select an option: 1

Available templates:
1. test
2. test2

Select template: 1
[+] Starting localhost server on port 8080
 * Serving Flask app 'HACKPHISHER'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.                                                                                            
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://10.0.0.99:8080
Press CTRL+C to quit
Press CTRL+C to quit
10.0.0.99 - - [DD/MMM/YYYY HH:MM:SS] "GET / HTTP/1.1" 200 -
[-] Victim IP Found !
[-] Victim's IP : 10.0.0.99
[-] Victim's IP (form):

[-] Login info Found !!

[-] Commit : Sign in
[-] Authenticity_token :                                                                                                 
[-] Add_account : 
[-] Login : test
[-] Password : test
[-] Webauthn-conditional :
[-] Javascript-support : 
[-] Webauthn-support :
[-] Webauthn-iuvpaa-support :
[-] Return_to :
[-] Allow_signup : 
[-] Client_id : 
[-] Integration : 
[-] Required_field_49a7 : 
[-] Timestamp :
[-] Timestamp_secret :

[-] Saved in : credentials.txt
```

---

### Example 3: View Captured Credentials:

1. View Captured Credentials: (Example)

```
Select an option: 3


========== CREDENTIALS CAPTURED ==========
IP: 10.0.0.99                                                                                            
IP (form):                                                                                
User-Agent:                       
Timestamp: YYYY-MM-DD HH:MM:SS.000000                                                                    
commit: Sign in                                                                                          
authenticity_token:                                                                                                      
add_account:                                                                                             
login: test                                                                                              
password: test                                                                                           
webauthn-conditional:                                                                          
javascript-support:                                                                                 
webauthn-support:                                                                           
webauthn-iuvpaa-support:                                                                     
return_to:                                                                      
allow_signup:                                                                                            
client_id:                                                                                               
integration:                                                                                             
required_field_49a7:                                                                                     
timestamp:                                                                                 
timestamp_secret:                       
                                                                                                         
                                                                                                         

Press Enter to continue...
```

---

### Example 4: Remove Template:

1. Delete Template: (Example)

```
Select an option: 4

Available templates:
1. test
2. test2

Select template to remove: 2
[+] Template 'test2' removed successfully!

Press Enter to continue...
```

---

## Notes and Best Practices

### Security Considerations

* Always use in isolated environments - Deploy HACKPHISHER in controlled lab environments or virtual machines
* Regularly update dependencies - Keep Flask and other dependencies updated to avoid security vulnerabilities
* Secure credential storage - Consider encrypting the file for sensitive testing scenarios `credentials.txt`

### Operational Best Practices

* Template validation - Always test cloned templates locally before deploying in production environments
* Port selection - Use non-standard ports to avoid conflicts with existing services
* Log monitoring - Regularly monitor captured credentials during campaigns to detect successful phishing attempts

### Performance Optimization

* Template optimization - Minimize external resources in cloned templates for faster loading times
* Server configuration - For high-volume testing, consider using production WSGI servers instead of Flask's development server
* Resource management - Clean up unused templates regularly to maintain optimal performance

### Legal and Compliance

* Document authorization - Maintain written permission for all phishing testing activities
* Data handling - Follow organizational policies for handling captured credentials and PII
* Testing scope - Clearly define and document the scope of authorized testing activities

### Troubleshooting Common Issues

Port conflicts - Use to identify and resolve port conflicts `netstat -tulpn`
Template cloning failures - Verify network connectivity and target website accessibility
Dependency issues - Use virtual environments to isolate Python dependencies

---

## Ethical Notice

**For Authorized and Ethical Use Only**

1. HACKPHISHER is intended solely for legitimate security testing, training, and research.
2. Unauthorized use against systems or individuals without explicit permission is illegal and unethical.
3. The developer disclaims all liability for misuse or damage caused by this tool.

---

## Author

Developed by [David.dvora]

---

## Acknowledgments

This project was developed with the assistance of advanced AI tools to enhance coding efficiency, structure, and quality.
Special thanks to AI-assisted technologies for supporting the development process.

---
