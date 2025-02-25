import requests
import time
import re
import os
import random
from colorama import Fore, Style, init
from datetime import datetime

# Initialize colorama for cross-platform color support
init(autoreset=True)

class Logger:
    """Handles logging with timestamps, levels, and colors."""

    @staticmethod
    def log(level, message):
        """Logs a message with timestamp, level, and color."""
        now = datetime.now().strftime("%Y/%m/%d * %H:%M:%S")
        if level == "INFO":
            color = Fore.CYAN
            icon = "ℹ️"
        elif level == "WARNING":
            color = Fore.YELLOW
            icon = "⚠️"
        elif level == "ERROR":
            color = Fore.RED
            icon = "❌"
        else:
            color = Style.RESET_ALL
            icon = ""
        print(f"{color}{now} - {icon} {level} - {message}{Style.RESET_ALL}")

class Logo:
    """Displays a simple logo."""

    def display(self):
        """Displays the logo."""
        banner = f"""{Fore.LIGHTRED_EX}
            (                                        
)\\ )   )           )                      
(()/(( /( ) ( /(  (   (  (      (  
/(_))\\()(/( )\\())))\\ ( )\\ )\\ ))\\ 
(_))(_))/)(_)(_))//((_))\\((_(()/( /((_) 
/ __| |_((_)_| |_(_))(((_| __)(_)(_))   
\\__ |  _/ _` |  _| || (_-| _| || / -_)  
|___/\\__\\__,_|\\__|\\_,_/__|___\\_, \\___|  
                                |__/     
{Style.RESET_ALL}"""
        print(banner)

class Menu:
    """Manages the main menu of the application."""

    def __init__(self):
        self.options = ["Null Payloads", "Exit"]

    def display(self):
        """Displays the menu with a random color."""
        colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
        color = random.choice(colors)

        for i, option in enumerate(self.options):
            print(f"{color}{i + 1}. {option}")
        print(f"{Style.RESET_ALL}")

    def get_choice(self):
        """Gets user input and validates it."""
        while True:
            try:
                choice = int(input(f"\t ☠️ {Fore.BLUE} Enter your choice{Style.RESET_ALL} 👉  "))
                if 1 <= choice <= len(self.options):
                    return choice
                else:
                    print("  Please select a number between 1 and", len(self.options))
            except ValueError:
                print("  Please enter a valid number.")

class ReturnMenu:
    """Handles returning to the main menu."""

    @staticmethod
    def return_to_menu():
        """Prompts the user to press the enter key to return to the main menu."""
        input(f"\n{Fore.RED}Press Enter to back to the main menu{Style.RESET_ALL} 👀  ")

class StatusCodeHandler:
    """Handles different HTTP status codes."""

    @staticmethod
    def handle_504():
        """Handles 504 status code (Link expired)."""
        Logger.log("ERROR", "Link expired. Status code: 504")
        ReturnMenu.return_to_menu()

    @staticmethod
    def handle_200():
        """Handles 200 status code (Continue). Not implement yet"""
        pass 

class RequestHandler:
    """Handles sending HTTP GET requests and displaying results."""

    def __init__(self):
        self.url = ""
        self.interval = 0
        self.request_count = 0
        self.start_time = 0
        self.session = requests.Session()

    def get_url(self):
        """Gets and validates the URL from the user."""
        url_regex = re.compile(
            r"^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w.-]+)+[\w\-._~:/?#[\]@!\$&'()*+,;=.]+$"
        )
        while True:
            self.url = input(f"{Fore.YELLOW}🌐 Enter URL Address: \n{Style.RESET_ALL}\t👉  ")
            print()

            if url_regex.match(self.url):
                if not self.url.startswith("http"):
                    self.url = "https://" + self.url
                    Logger.log("INFO", "Scheme set to https:// by default.")
                    print()
                return True
            else:
                print(f"{Fore.RED}Invalid URL or IP address.\n{Style.RESET_ALL}")

    def get_interval(self):
        """Gets and validates the interval from the user."""
        while True:
            try:
                self.interval = int(input(f"{Fore.YELLOW} ⏱️ Enter interval in seconds: \n{Style.RESET_ALL}\t👉  "))
                return True
            except ValueError:
                print(f"{Fore.RED}Invalid interval. Please enter a number.\n{Style.RESET_ALL}")

    def check_host(self):
        """Checks if the host is up."""
        print()
        Logger.log("INFO", "Checking host...")
        try:
            response = self.session.get(self.url, timeout=20)
            if response.status_code == 504:
                StatusCodeHandler.handle_504()
            
            elif response.status_code:


                Logger.log("INFO", "Host is active.")
                print()
                return True
            else:
                Logger.log("ERROR", "Host is down.")
                ReturnMenu.return_to_menu()
                return False
        except requests.exceptions.RequestException as e:
            Logger.log("ERROR", f"Host is down: {e}")
            ReturnMenu.return_to_menu()
            return False

    def send_request(self):
        """Sends HTTP GET requests and displays results."""
        try:
            response = self.session.get(self.url, timeout=20)
            if response.status_code == 504:
                StatusCodeHandler.handle_504()
                return None
            StatusCodeHandler.handle_200()
            return response.status_code
        except requests.exceptions.RequestException as e:
            Logger.log("ERROR", f"Request failed: {e}")
            ReturnMenu.return_to_menu()
            return None

    def run(self):
        """Runs the request loop."""
        if not self.get_url() or not self.get_interval():
            return
        if not self.check_host():
            return
        self.start_time = time.time()
        self.request_count = 0
        try:
            while True:
                self.request_count += 1
                status_code = self.send_request()
                if status_code is not None:
                    elapsed_time = time.time() - self.start_time
                    hours, remainder = divmod(elapsed_time, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    formatted_time = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
                    print(
                        f"\r{Fore.GREEN}📡 {self.request_count} - {formatted_time} - {self.url} - {self.interval}s - Status: {status_code}{Style.RESET_ALL}",
                        end="",
                    )
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print()
            Logger.log("WARNING", "Request loop stopped.")
            print()
            ReturnMenu.return_to_menu()

def main():
    """Main function to run the application."""
    logo = Logo()
    menu = Menu()
    request_handler = RequestHandler()

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        logo.display()
        menu.display()
        choice = menu.get_choice()

        if choice == 1:
            os.system('cls' if os.name == 'nt' else 'clear')
            logo.display()
            print("\nThis tool sends HTTP GET requests to a specified URL address at a given interval.")
            print("The main goal of this section is to keep alive the host by showing up .\n")
            request_handler.run()
        elif choice == 2:
            Logger.log("INFO", "Exiting...")
            break

main()