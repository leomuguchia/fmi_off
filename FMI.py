#Created for use for a larger iDevice management project
#but this script is open for use and modifications
#script by liomuguchia
#licensed under the GNU Public licence
#feel free to reach me out for consultations 
#github @leomuguchia/@liomuguchia
#instagram @ghost__xo
#buymeacoffee @muguchialio
#script should not be used to breach Apple Inc terms
#I chose not to automate the email verification process 
# to allow the user to receive updates on progress of FMI Off from Apple



import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException  
import os
import json
import subprocess
import re
import subprocess
import json
import webbrowser
import sys
import random
import threading
from datetime import datetime, timedelta
import colorama


def clear_terminal_screen():
    # Clear the terminal screen
    os.system('clear' if os.name == 'posix' else 'cls')

def print_menu():
    # Initialize colorama for cross-platform colored output
    colorama.init(autoreset=True)

    # ASCII art for the "FMI Off" title inside a button-like structure
    title_ascii_art = (
        f"{colorama.Fore.CYAN}"
        "+-----------------------------------------------------+\n"
        "|  ____  _           __  __      _   _               |\n"
        "| | __ )| |_   _ ___\\ \\/ /__  _| |_| |_ ___  _ __   |\n"
        "| |  _ \\| | | | / __|\\  // _ \\| __| __/ _ \\| '_ \\  |\n"
        "| |_) | | |_| \\__ \\/\\  / (_) | |_| || (_) | | | | |\n"
        "|____/|_|\\__,_|___/\\/  \\___/ \\__|\\__\\___/|_| |_| |\n"
        "|                                                     |\n"
        "|               [ FMI Off - iDevice Management ]      |\n"
        "+-----------------------------------------------------+"
    )

    print(title_ascii_art)

    # Menu options
    print("1. Submit FMI Removal Request")
    print("2. Check Existing Cases")
    print("3. Quit")



def get_user_choice():
    # Get user choice and handle invalid input
    default_choice = "1"
    while True:
        choice = input("Select option >").strip()

        if choice in ["1", "2", ""]:
            return choice
        else:
            print("Invalid option. Press Enter for default option")
            
def submit_fmi_removal_request():
    print("\nSubmit FMI Removal Request:")
    print("Requirements:")
    print("- iCloud locked device with no previous owner details")
    print("- IMEI number or serial number")
    print("- SickW API key")
    print("- Apple confirmation link (get from: https://al-support.apple.com/#/additional-support)")
    print("- Note: iPhone should not be in lost mode")
    input("Press Enter to continue...")

def check_existing_cases():
    print("\nCheck Existing Cases:")
    print("1. Check Existing Cases")
    print("2. Provide your own ID and last name to check case progress")
    print("3. Quit")
    option = input("Select option > ").strip()
    return option

def is_valid_confirmation_link(confirmation_link):
    # Check if the provided link matches the expected format
    pattern = r'https://al-support.apple.com/confirm/[a-f0-9]+/[a-z]+_[A-Z]+'
    return re.match(pattern, confirmation_link) is not None


def check_session_expired(driver):
    # Check if "Session Expired" keywords are present in the body of the HTML page
    try:
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'Session Expired')
        )
        print("Session expired. Opening additional support link in default browser.")
        
        # Open the external link in the default system browser
        webbrowser.open('https://al-support.apple.com/#/additional-support', new=2)
        
        print("Closing@0.")
        try:
         driver.quit()
        except Exception as quit_error:
         print(f"Error while quitting the driver: {quit_error}")
        sys.exit(0)
        return True  # Session expired
    except:
        # Check if there is a "Continue" button
        try:
            continue_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.button--primary span'))
            )
            continue_button.click()
            return False  # Continue button found, session not expired
        except:
            print("Closing@0.")
            try:
             driver.quit()
            except Exception as quit_error:
             print(f"Error while quitting the driver: {quit_error}")
            sys.exit(0)
            return True  # Continue button not found, assume session expired

def set_preference():
    default_preference = "cmd"
    print(f"Default preference is '{default_preference}'.")

    while True:
        preference = input("Enter your preference (gui or cmd): ").lower()
        if preference in ["gui", "cmd"]:
            return preference
        elif not preference:
            return default_preference
        else:
            print("Invalid preference. Please enter 'gui' or 'cmd'.")

            
def set_bg_sleep():
    default_sleep = 1
    bg_sleep_input = input(f"Background activity should run after (default: {default_sleep} minute): ")
    
    try:
        bg_sleep = int(bg_sleep_input)
    except ValueError:
        bg_sleep = default_sleep
    
    return bg_sleep


def generate_random_name():
    first_names = ["John", "Jane", "Bob", "Alice", "David", "Emma", "Michael", "Olivia", "Daniel", "Sophia"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "García", "Rodriguez", "Martinez"]

    # Generate a random first name and last name
    random_first_name = random.choice(first_names)
    random_last_name = random.choice(last_names)
    return random_first_name, random_last_name


def fetch_details_from_api(api_key, imei, driver):
    try:
        # Construct the API URL
        service = "30"
        api_url = f"https://sickw.com/api.php?format=HTML&key={api_key}&imei={imei}&service={service}"

        # Open a new tab and navigate to the API URL
        new_tab_script = "window.open('{}', '_blank');".format(api_url)
        driver.execute_script(new_tab_script)
        driver.switch_to.window(driver.window_handles[1])

        # Wait for the page to load
        time.sleep(20)

        # Create a directory for screenshots if it doesn't exist
        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, r'swip_screens')
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)

        # Save screenshot
        screenshot_path = os.path.join(final_directory, f'{imei}.png')
        driver.save_screenshot(screenshot_path)

        # Wait for additional time if needed
        time.sleep(2)

        # Get HTML content of the page
        body_content = driver.page_source

        # Extract estimated purchase date from the HTML content
        start_index = body_content.find("Estimated Purchase Date:") + len("Estimated Purchase Date:")
        end_index = body_content.find("iCloud Lock:")
        estimated_purchase_date = body_content[start_index:end_index].strip().replace("<br>", "")

        # Switch back to the original tab
        driver.switch_to.window(driver.window_handles[0])

        # Return the extracted details
        first_name, last_name = generate_random_name()
        details = {
            "purchase_date": estimated_purchase_date,
            "screenshot_path": screenshot_path,
            "first_name": f"{first_name}",
            "last_name": f"{last_name}",
            "store_name": "Experimax Houston Heights",
            "address": "301 N Loop W",
            "city": "Houston, Texas",
            "state": "Texas",
            "zip": "77008"
        }
        return details
    except Exception as e:
        print(f"Error: {e}")
        return {}


def manual_entry_popup():
    # Implement the logic to prompt the user for manual entry
    print("Please enter the following details manually:")
    details = {}
    details["first_name"] = input("First Name: ")
    details["last_name"] = input("Last Name: ")
    details["purchase_date"] = input("Estimated Purchase Date: ")
    details["store_name"] = input("Store name: ")
    details["country_of_purchase"] = input("Country of Purchase: ")
    details["address"] = input("Address: ")
    details["city"] = input("City: ")
    details["state"] = input("State: ")
    details["zip"] = input("ZIP Code: ")

    return details

def get_key():
    # Replace this with your logic to get the IMEI and API key from the user
    imei = input("Enter your IMEI: ")
    api_key = input("Enter your API key: ")

    return imei, api_key

def fill_out_form(driver, details):
    # Wait for the input fields to be present
    first_name_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "Q209907"))
    )
    last_name_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "Q209909"))
    )
    date_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "Q205897"))
    )
    store_name = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "Q205899"))
    )
    country_of_purchase = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "Q221901"))
    )
    address_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "Q221896"))
    )
    city_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "Q221898"))
    )
    state_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "Q221899"))
    )
    zip_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "Q221900"))
    )
    textarea_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "textarea-Q235245"))
    )
    
    # Fill out the form
    first_name_input.send_keys(details["first_name"])
    time.sleep(1)
    
    last_name_input.send_keys(details["last_name"])
    time.sleep(1)
    
    date_input.send_keys(details["purchase_date"])
    time.sleep(1)
    
    store_name.send_keys(details["store_name"])
    time.sleep(1)
    
    select_country = Select(country_of_purchase)
    try:
        select_country.select_by_visible_text(details["country_of_purchase"])
    except Exception as e:
        select_country.select_by_visible_text("United States")
    time.sleep(1)
    
    address_input.send_keys(details["address"])
    time.sleep(1)
    
    city_input.send_keys(details["city"])
    time.sleep(1)
    
    state_input.send_keys(details["state"])
    time.sleep(1)
    
    zip_input.send_keys(details["zip"])
    time.sleep(1)
    
    textarea_element.send_keys(
        "bought from ebay, icloud status clean, please help me i wanna use apple"
    )
    # Locate the file input by ID
    file_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "files"))
    )
    # Check if the file input is present
    if file_input:
        image_paths = [
            details["screenshot_path"],
            details["screenshot_path"],
        ]

        for path in image_paths:
            try:
                file_input.send_keys(path)
                time.sleep(1)  # Adjust the wait time as needed
            except Exception as file_input_error:
                print(f"Error while uploading file: {file_input_error}")
                
    
    # Find the submit button by class
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.customer-form__continue_btn'))
    )

    # Check if the button is not disabled
    if 'disabled' not in submit_button.get_attribute('class'):
        # Retry mechanism for handling page reloads during form submission
        max_retries = 3
        for _ in range(max_retries):
            try:
             # If not disabled, click the submit button
             submit_button.click()
             print("\ndetails_saved@draft")

             time.sleep(5)
        
             continue_button = WebDriverWait(driver, 10).until(
                 EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.button--primary'))
                )
             continue_button.click()
             print("details_saved@submit\n")

             time.sleep(5)

             lookup_case(driver, details)

             break  # Exit the loop if successful
            except (TimeoutException, StaleElementReferenceException) as submit_error:
                print(f"Error during form submission: {submit_error}")
                print("Retrying...")

    else:
        print("Submit button disabled. Exiting.")
        try:
            driver.quit()
        except Exception as quit_error:
            print(f"Error while quitting the driver: {quit_error}")
        sys.exit(1)
        

def lookup_case(driver, details):
    # Wait for the next page to load after form submission
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[@class='thank-you__case']"))
        )
    except TimeoutException:
        print("Case ID not found on the page.")
        return None
    
    # Get the case ID element
    case_id_element = driver.find_element(By.XPATH, "//p[@class='thank-you__case']")

    # Extract the case ID text
    case_id_text = case_id_element.text

    # Extract the actual case ID (adjust the extraction logic based on the actual HTML structure)
    match = re.search(r'Your Apple Support Case ID: (\d+)', case_id_text)

    if match:
        # If a match is found, extract the case ID
        case_id = match.group(1)

        # Save case details to case.txt
        save_case_details(case_id, details['last_name'])

        filename = f"{details['last_name']}@{case_id}"
        capture_screenshot(driver, filename)
    
        print("Success! \nWe will now close this @instance")
        print("Background checks for your case status runs after every 30 minutes")
        print("Do not close this window(*optional! 4 optimal results)")
        print("keep tabs 'n' 'goodluck' '_'")
        time.sleep(10)
    
        print("Closing@1")
        driver.quit()
    else:
        print("Case ID not found in the expected format on the page.")
        print("Closing@1\n\n")
        driver.quit()

    
def save_case_details(case_id, last_name):
    case_file_path = os.path.abspath('images/case.txt')

    if not os.path.exists(case_file_path):
        with open(case_file_path, 'w') as file:
            file.write('')  # Create an empty file

    # Save case details to case.txt
    with open(case_file_path, 'w') as file:
        file.write(f"Case ID: {case_id}\n")
        file.write(f"Last Name: {last_name}\n")

def capture_screenshot(driver, filename):
    driver.save_screenshot(f'images/{filename}.png')


def background_instance(bg_sleep, run_counter, source):
    while True:
        run_counter += 1

        if source == "existing":
            # Fetch case details from case.txt
            case_file_path = os.path.abspath('images/case.txt')

            if not os.path.exists(case_file_path):
                print("No existing cases!")
                print("Closing@0")
                sys.exit(0)

            try:
                with open(case_file_path, 'r') as file:
                    case_id_line = file.readline().strip()
                    last_name_line = file.readline().strip()

                if not case_id_line or not last_name_line:
                    print("Case details not found in case.txt. Skipping background check.")
                    print("Closing@0")
                    sys.exit(0)

                # Extract case ID and last name
                _, case_id = case_id_line.split(": ")
                _, last_name = last_name_line.split(": ")

            except Exception as e:
                print(f"Error while reading case details: {e}")
                continue

        elif source == "new":
            while True:
                case_id = input("Enter your Case ID from Apple: ").strip()
                last_name = input("Enter the last name used for that case: ").strip()

                if case_id and last_name and len(case_id) >= 8:
                    break
                elif len(case_id) < 8:
                    print("Case ID should be at least 8 characters. Please try again.")
                else:
                    print("Both Case ID and last name are required. Please try again.")

        else:
            print("Invalid source. Exiting.")
            return None

        try:
            # Create a new Chrome browser instance for background check in headless mode
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless")
            background_driver = webdriver.Chrome(options=chrome_options)

            background_driver.get('https://getsupport.apple.com/activity')

            # Explicit wait for the case-id input field
            case_id_input = WebDriverWait(background_driver, 10).until(
                EC.presence_of_element_located((By.ID, 'case-id'))
            )
            case_id_input.clear()
            case_id_input.send_keys(case_id)

            # Wait for 2 seconds for the last name input to appear
            time.sleep(2)
            # Enter the last name
            last_name_input = background_driver.find_element(By.ID, 'last-name')
            last_name_input.clear()
            last_name_input.send_keys(last_name)

            # Similar waits for other input fields...

            # Wait for the submit button to be clickable
            submit_button = WebDriverWait(background_driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.case-lookup-submit'))
            )
            submit_button.click()

            # Wait for the next page to load
            time.sleep(5)

            # Check for the "Case Mismatch" modal
            try:
                mismatch_modal = background_driver.find_element(By.CSS_SELECTOR, 'div.case-mismatch-modal')
                modal_text = mismatch_modal.text
                print(f"Case ID {run_counter}: {modal_text}")
                print(f"\nBackground check will run every {bg_sleep} minutes")

            except:
                print(f"Case ID {run_counter}: Case is active @apple_support")
                # handle case ID found scenario

            finally:
                background_driver.quit()

            time.sleep(bg_sleep * 60)

        except Exception as e:
            print(f"An error occurred during background check: {e}")
            continue

if __name__ == "__main__":
    clear_terminal_screen()
    print_menu()
    user_choice = get_user_choice()
    
    if user_choice == "1" or user_choice == "":
     submit_fmi_removal_request()
     
     # Prompt user to paste the confirmation link
     confirmation_link = input("Paste the apple support confirmation link: ")
    
     # Check if the confirmation link is valid
     if not is_valid_confirmation_link(confirmation_link):
         print("Invalid confirmation link. Closing.")
     else:
         preference = set_preference()
         # Create a new Chrome browser instance for background check
         if preference == "gui":
             driver = webdriver.Chrome()
         else:
             # Create a new Chrome browser instance for background check in headless mode
             chrome_options = webdriver.ChromeOptions()
             chrome_options.add_argument("--headless")
             driver = webdriver.Chrome(options=chrome_options)

         # Open the provided confirmation link
         driver.get(confirmation_link)
         print(f"Checking for session validity: {confirmation_link}")
     
         # Check if the session has expired
         if check_session_expired(driver):
             driver.quit()  # Session expired, exit the script

         # Check for the "Continue" button
         try:
             continue_button = WebDriverWait(driver, 10).until(
                 EC.visibility_of_element_located((By.CSS_SELECTOR, 'button.button--primary'))
                )

             # Click the "Continue" button
             continue_button.click()
         except StaleElementReferenceException:
              # If a stale element exception occurs, re-find the element and click again
             continue_button = WebDriverWait(driver, 10).until(
                 EC.visibility_of_element_located((By.CSS_SELECTOR, 'button.button--primary'))
                )
             continue_button.click()

         # Prompt user to choose between auto and manual entry
         print("*Hint: Auto fetches the device details based on device IMEI/SN ")
         user_choice = input("Choose 'auto' or 'manual' entry (default: auto): ").lower()

         # Set default choice to "auto" if the user doesn't provide any input
         user_choice = user_choice if user_choice in ['auto', 'manual'] else 'auto'

         if user_choice == 'auto':
             # You need to provide the SickW API key and imei
             imei, api_key = get_key()
             details = fetch_details_from_api(api_key, imei, driver)
         elif user_choice == 'manual':
             details = manual_entry_popup() 
         else:
             print("Invalid choice. Closing.")

         # Rest of the logic to fill out the form
         if details:
             fill_out_form(driver, details)
         else:
             print("Closing due to missing details.")
             sys.exit(1)
            

         # Start the background instance as a separate thread
         bg_sleep = set_bg_sleep()
         run_counter = 0
         source = "existing"
         background_thread = threading.Thread(target=background_instance, args=(bg_sleep, run_counter,source))
         background_thread.start()
         background_thread.join()

    elif user_choice == "2":
        option = check_existing_cases()  

        if option == "1":
            source = "existing"
        elif option == "2":
            source = "new"
        elif option == "3":
            sys.exit(0)  
        else:
            print("Invalid choice. Closing.")
            sys.exit(1)

        bg_sleep = set_bg_sleep()
        run_counter = 0

        background_thread = threading.Thread(target=background_instance, args=(bg_sleep, run_counter, source))
        background_thread.start()
        background_thread.join()
