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


def fetch_details_from_api(api_key, imei):
    # Call the SickW API to fetch details based on imei
    service = "30"  # Adjust the service ID based on your requirements
    format_type = "json"  # Adjust the format type (json or html) based on your requirements

    # Construct the curl command
    curl_command = [
        'curl',
        f'https://sickw.com/api.php?format={format_type}&key={api_key}&imei={imei}&service={service}'
    ]

    try:
        # Use subprocess to make a request to the API
        response = subprocess.run(curl_command, capture_output=True, text=True)

        # Check if the curl command was successful (return code 0)
        if response.returncode == 0:
            # Parse the response and extract the details
            try:
                api_response = json.loads(response.stdout)
            except json.JSONDecodeError as json_error:
                print(f"Error decoding JSON response: {json_error}")
                return {}

            # Extract details from the API response
            first_name, last_name = generate_random_name()
            details = {
                # Add dummy data for other fields
                "first_name": f"{first_name}",
                "last_name": f"{last_name}",
                "store_name": "Experimax Houston Heights",
                "address": "301 N Loop W",
                "city": "Houston, Texas",
                "state": "Texas",
                "zip": "77008"
            }

            result_details = api_response.get('result', '')
            if result_details:
                # Extracting "Estimated Purchase Date" and "Purchase Country"
                estimated_purchase_date = re.search(r'Estimated Purchase Date: (\d{4}-\d{2}-\d{2})', result_details)
                purchase_country_match = re.search(r'Purchase Country: (.+?)<br>', result_details)

                # Check if the regex matches were successful
                if estimated_purchase_date and purchase_country_match:
                    estimated_purchase_date = estimated_purchase_date.group(1)
                    purchase_country = purchase_country_match.group(1)

                    # Add these details to the dictionary
                    details["purchase_date"] = estimated_purchase_date
                    details["country_of_purchase"] = purchase_country

            print("Parsed Details:", details)
            return details
        else:
            print(f"Error: Unable to fetch details! failed with return code {response.returncode}")
            return {}
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
        "only tried resetting with itunes, cant get help from store as im not in us currently. icloud status clean, please help me I want to use Apple"
    )
    # Locate the file input by ID
    file_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "files"))
    )
    # Check if the file input is present
    if file_input:
        image_paths = [
            os.path.abspath('./images/screenshot.png'),
            os.path.abspath('./images/screenshot.pdf'),
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


def background_instance(bg_sleep):
    while True:
        # Fetch case details from case.txt
        case_file_path = os.path.abspath('images/case.txt')

        if not os.path.exists(case_file_path):
            with open(case_file_path, 'w') as file:
                file.write('')  # Create an empty file

        try:
            with open(case_file_path, 'r') as file:
                case_id_line = file.readline().strip()
                last_name_line = file.readline().strip()

            if not case_id_line or not last_name_line:
                print("Case details not found in case.txt. Skipping background check.")
                continue

            # Extract case ID and last name
            _, case_id = case_id_line.split(": ")
            _, last_name = last_name_line.split(": ")

            # Create a new Chrome browser instance for background check in headless mode
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless")
            background_driver = webdriver.Chrome(options=chrome_options)

            try:
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
                    print(f"Apple: {modal_text}")
                    print(f"\nBackground check will run every {bg_sleep} minutes")
                except:
                    print("Case ID active @apple_support")
                    #handle case ID found scenario

            finally:
                background_driver.quit()
            
            time.sleep(bg_sleep * 60)

        except Exception as e:
            print(f"An error occurred during background check: {e}")
            continue


if __name__ == "__main__":
    # Prompt user to paste the confirmation link
    confirmation_link = input("Paste the apple support confirmation link: ")
    
    # Check if the confirmation link is valid
    if not is_valid_confirmation_link(confirmation_link):
        print("Invalid confirmation link. Closing.")
    else:
     preference = set_preference()
     bg_sleep = set_bg_sleep()
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
         details = fetch_details_from_api(api_key, imei)
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
    background_thread = threading.Thread(target=background_instance, args=(bg_sleep,))
    background_thread.start()
    background_thread.join()

        
        
        
