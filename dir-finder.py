import os
import requests
import time
import sys
import tldextract

def print_green(message):
    print(f"\033[92m{message}\033[0m")  # Set text color to green (92) and then reset to default (0)

def print_red(message):
    print(f"\033[91m{message}\033[0m")  # Set text color to red (91) and then reset to default (0)

def print_yellow(message):
    print(f"\033[93m{message}\033[0m")  # Set text color to yellow (93) and then reset to default (0)

def show_popup(message):
    sys.stdout.write(f"\r\033[K{message}")
    sys.stdout.flush()
    time.sleep(1)

def show_progress(current, total):
    percentage = int((current / total) * 100)
    sys.stdout.write(f"\r\033[93m Scanning... {percentage}% complete \033[0m\r")
    sys.stdout.flush()

def is_valid_url(input_url):
    try:
        result = tldextract.extract(input_url)
        return bool(result.domain) and bool(result.suffix)
    except ValueError:
        return False

def find_directories(url):
    global done
    done = False
    total_request_count = 0
    success_count = 0
    failure_count = 0

    url = url.rstrip('/')

    if not is_valid_url(url):
        print_red("Invalid URL. Please enter a valid website URL.")
        return

    start_time = time.time()

    directory_file = "directories.txt"
    if not os.path.isfile(directory_file):
        print(f"Error: File '{directory_file}' not found.")
        return

    try:
        with open(directory_file, 'r') as file:
            directories = file.read().splitlines()
    except FileNotFoundError:
        return

    directory_found = False
    last_popup_message = ""

    for idx, directory in enumerate(directories, start=1):
        full_url = f"{url}{'' if url.endswith('/') else '/'}{directory}"
        response = requests.get(full_url)
        total_request_count += 1

        if response.status_code == 200:
            directory_found = True
            success_count += 1
            print_green(f"Directory found! {full_url}")
            last_popup_message = ""

        else:
            failure_count += 1
            

        show_progress(idx, len(directories))

    done = True

    elapsed_time = time.time() - start_time

    if directory_found:
        show_popup(last_popup_message)
    else:
        print("")

    print_completion_message(total_request_count, success_count, failure_count, elapsed_time)

def print_completion_message(total_request_count, success_count, failure_count, elapsed_time):
    border = "+" + "-" * 78 + "+"
    print(border)
    print("|{:^78}|".format(" Scanning Process Complete "))
    print("|{:^78}|".format("-" * 76))
    print(f"|    \033[93m Total Requests Sent: {total_request_count: <10}\033[0m \033[92m Successful: {success_count: <10}\033[0m \033[91m Failed: {failure_count: <10}\033[0m ")
    print(f"|     Time: {elapsed_time:.2f} seconds")
    print("|{:^78}|".format(" " * 76))
    print(border)

def clear_screen():
    os.system('clear')

def print_welcome_message(website_url):
    print("+----------------------------------------------------------------------------------------+")
    print("|                                                                                        ")
    print("|                          🌟 Welcome to Directory Finder 🌟                             ")
    print("|                                                                                        ")
    print("|                          	 🚀 Made by Fsnake 🚀                                   ")
    print("|                                                                                        ")
    print("|                                                                                        ")
    print(f"| -> Starting scanning process for : {website_url:^34}                                     ")
    print("|                                                                                        ")
    print("+----------------------------------------------------------------------------------------+")

if __name__ == "__main__":
    website_url = input("Enter the website URL : ")
    clear_screen()

    while website_url.lower() != 'exit':
        if is_valid_url(website_url):
            print_welcome_message(website_url)

            global done
            done = False

            try:
                find_directories(website_url)
            except KeyboardInterrupt:
                print("\n--> \033[93m Program stopped. \033[0m <--")
                sys.exit(0)
            
            break  # Exit the loop after the first successful scan
        else:
            print_red("Invalid URL. Please enter a valid website URL.")
            website_url = input("Enter the website URL or 'exit' to quit : ")
            clear_screen()

    print("\nProgram Finished Successfully.")
