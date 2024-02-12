# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta
import time
import requests
import mysql.connector

# MySQL database connection settings
db_config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "",
    "database": "practice_auxmeet_db",
}

# Create ChromeOptions object
chrome_options = webdriver.ChromeOptions()
# Add --incognito argument to open Chrome in incognito mode
chrome_options.add_argument("--incognito")
chrome_options.binary_location = "/Applications/Google Chrome.app"

# Initialize the webdriver with ChromeOptions and set implicit wait
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(30)  # Set implicit wait to 30 seconds

# Open the website link
driver.get(
    "https://transcom.avature.net/careers/Register?jobId=249&applicationStep=0&source=Vendor&tags=METACOM"
)

# Connect to the MySQL database outside the loop
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Initialize a counter variable for number of fill out's completed
fill_out_count = 0


# Function to simulate a fill-out
def simulate_fill_out():
    # Increment the fill-out count
    global fill_out_count
    fill_out_count += 1

    # Print a message with the fill-out count
    print("************Fill Out Completed*************")
    print(f"{fill_out_count} Applicant{'s' if fill_out_count > 1 else ''} completed")


# Function to check network status
def check_network_status():
    try:
        response = requests.head(
            "https://transcom.avature.net/careers/Register?jobId=249&applicationStep=0&source=Vendor&tags=METACOM"
        )
        return response.status_code == 200
    except requests.ConnectionError:
        return False


def fill_form_field(field_name, value):
    field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, field_name))
    )
    if value:
        if field.tag_name == "select":
            # For dropdowns
            select = Select(field)
            select.select_by_value(str(value))
        else:
            # For other input fields
            field.clear()
            field.send_keys(value)
    else:
        print(f"{field_name} not available")


# Ask the user for the sleep duration in seconds
sleep_duration = int(
    input("Enter the sleep duration after the final save button (in seconds): ")
)

while True:  # Continuously check for new records

    # Execute a query to retrieve new applicants added in the database
    cursor.execute(
        "SELECT * FROM applicants WHERE processed = 0 AND created_at >= CURDATE() ORDER BY created_at ASC"
    )
    applicant_data_list = cursor.fetchall()

    if not applicant_data_list:
        print("No new applicants found. Exiting...")
        break  # Exit the loop if no new records are found

    for applicant_data in applicant_data_list:
        if applicant_data[35].date() >= datetime.now().date():

            fill_form_field("1401", applicant_data[47])  # Transcom dropdown
            fill_form_field("1402", applicant_data[9])  # Last Name
            fill_form_field("1403", applicant_data[7])  # First Name
            fill_form_field("1404", applicant_data[8])  # Middle Name
            fill_form_field("1405", applicant_data[38])  # Suffix
            fill_form_field("1479", applicant_data[11])  # Contact Number
            fill_form_field("1480", applicant_data[11])  # Alternate Contact Number
            fill_form_field("1408", applicant_data[10])  # Email
            fill_form_field("1409", applicant_data[10])  # Alternate Email

            # Wait for the Region dropdown to be clickable
            dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "span.select2-selection__arrow")
                )
            )

            # Check for an overlay element like cookies and close it
            try:
                cookies_overlay = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "cookies"))
                )
                cookies_overlay.click()
                # Introduce a small delay to wait for the overlay to disappear
                time.sleep(2)  # Adjust the time as needed
            except:
                pass  # Continue if no overlay is found or if it fails to close

            # Scroll the dropdown into view
            driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)

            # Use ActionChains to move to the element and click
            ActionChains(driver).move_to_element(dropdown).click().perform()

            # Display data from the applicants table
            desired_option_text = applicant_data[45]

            # Wait for the desired option to be clickable
            desired_option = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//li[contains(text(), '{desired_option_text}')]")
                )
            )

            desired_option.click()

            # Identifier for Province dropdown
            province_dropdown_identifier = "1412"

            # Dynamic CSS selector for the Province dropdown
            province_dropdown_css_selector = f"span.select2Container{province_dropdown_identifier} .select2-selection__arrow"

            # Wait for the Province dropdown to be clickable
            province_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, province_dropdown_css_selector)
                )
            )

            # Use ActionChains to move to the element and click
            ActionChains(driver).move_to_element(province_dropdown).click().perform()

            # Display data from the applicants table
            desired_province_option_text = applicant_data[48]

            # Wait for the desired option in Province to be clickable
            desired_province_option = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        f"//li[contains(text(), '{desired_province_option_text}')]",
                    )
                )
            )

            # Click on the desired Province option
            desired_province_option.click()

            # Identifier for City/Municipality dropdown
            city_dropdown_identifier = "1413"

            # Dynamic CSS selector for the City/Municipality dropdown
            city_dropdown_css_selector = f"span.select2Container{city_dropdown_identifier} .select2-selection__arrow"

            # Wait for the City/Municipality dropdown to be clickable
            city_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, city_dropdown_css_selector)
                )
            )

            # Use ActionChains to move to the element and click
            ActionChains(driver).move_to_element(city_dropdown).click().perform()

            # Display data from the applicants table
            desired_city_option_text = applicant_data[51]

            # Wait for the desired option in City/Municipality to be clickable
            desired_city_option = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//li[contains(text(), '{desired_city_option_text}')]")
                )
            )

            # Click on the desired City/Municipality option
            desired_city_option.click()

            # Fill House Number and Street Address fields
            fill_form_field("1414", applicant_data[39])
            # Fill Zip Code fields
            fill_form_field("1415", applicant_data[40])

            # Find and select a value in the What is your highest educational attainment? dropdown
            educational_dropdown = driver.find_element(By.NAME, "1416")
            educational_select = Select(educational_dropdown)
            fill_form_field("1416", applicant_data[46])

            # Identifier for How did you learn about Transcom open positions? dropdown
            learn_about_transcom_dropdown_identifier = "1417"

            # Dynamic CSS selector for How did you learn about Transcom dropdown
            learn_about_transcom_dropdown_css_selector = f"span.select2Container{learn_about_transcom_dropdown_identifier} .select2-selection__arrow"

            # Wait for How did you learn about Transcom dropdown to be clickable
            learn_about_transcom_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, learn_about_transcom_dropdown_css_selector)
                )
            )

            # Use ActionChains to move to the element and click
            ActionChains(driver).move_to_element(
                learn_about_transcom_dropdown
            ).click().perform()

            # Display the data from applicants table
            desired_learn_about_option_text = applicant_data[42]

            # Wait for the desired option in How did you learn about Transcom to be clickable
            desired_learn_about_option = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        f"//li[contains(text(), '{desired_learn_about_option_text}')]",
                    )
                )
            )

            # Click on the desired option in How did you learn about Transcom
            desired_learn_about_option.click()

            # Fill the Were you referred by someone to apply in Transcom? fields
            is_referred_dropdown = driver.find_element(By.NAME, "1418")
            is_referred_select = Select(is_referred_dropdown)
            fill_form_field("1418", applicant_data[52])

            # Find and select a value in the Referred by dropdown
            referred_by_dropdown = driver.find_element(By.NAME, "1419")
            referred_by_select = Select(referred_by_dropdown)
            fill_form_field("1419", "9037")

            # Fill the Please input Full Name of the referrer fields
            fill_form_field("1420", "Metacom")
            # Fill the Password fields
            fill_form_field("1421", "Metacom12345")
            # Fill the Password Confirmation fields
            fill_form_field("1422", "Metacom12345")

            checkbox = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "1423"))
            )

            # Check if there is any overlay element like cookies and close it
            cookies_overlay = driver.find_element(By.CLASS_NAME, "cookies")
            if cookies_overlay.is_displayed():
                cookies_overlay.click()

            # Introduce a small delay to wait for the overlay to disappear
            time.sleep(2)  # Adjust the time as needed

            # Scroll the checkbox into view
            driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
            checkbox.click()

            # Assuming driver is your webdriver instance
            save_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "saveButton"))
            )

            # Check if there is any overlay element like cookies and close it
            cookies_overlay = driver.find_element(By.CLASS_NAME, "cookies")
            if cookies_overlay.is_displayed():
                cookies_overlay.click()
            # Introduce a small delay to wait for the overlay to disappear
            time.sleep(2)  # Adjust the time as needed

            # Scroll the save button into view
            driver.execute_script("arguments[0].scrollIntoView(true);", save_button)
            save_button.click()

            # Fill the Are you 18, Are you 18 eligible to work in the ph?, and Are you amenable to train and/or work onsite? fields
            fill_form_field("1381", "37")
            fill_form_field("1382", "37")
            fill_form_field("1383", "37")

            # Find and select a value in the Do you have BPO/Call Center experience? dropdown
            have_bpo_exp_dropdown = driver.find_element(By.NAME, "1384")
            have_bpo_exp_select = Select(have_bpo_exp_dropdown)
            fill_form_field("1384", "38")
            # Find and select a value in the Do you have BPO/Call Center experience? dropdown
            have_work_exp_dropdown = driver.find_element(By.NAME, "1386")
            have_work_exp_select = Select(have_work_exp_dropdown)
            fill_form_field("1386", "38")

            # Set fields with IDs "1391," "1392," and "1393" to be filled with "N/A"
            fill_form_field("1391", "N/A")
            fill_form_field("1392", "N/A")
            fill_form_field("1393", "N/A")

            # Find and select a value in the Do you have BPO/Call Center experience? dropdown
            previous_employee_dropdown = driver.find_element(By.NAME, "1394")
            previous_employee_select = Select(have_bpo_exp_dropdown)
            fill_form_field("1394", "38")

            # Find and select a value in the Do you have BPO/Call Center experience? dropdown
            is_visit_dropdown = driver.find_element(By.NAME, "1397")
            is_visit_select = Select(is_visit_dropdown)
            fill_form_field("1397", "37")

            # Get the current date
            current_date = datetime.now()

            # Calculate the date 1 day after the current date
            new_date = current_date + timedelta(days=1)

            # Format the new date as a string in the 'yyyy-mm-dd' format
            formatted_date = new_date.strftime("%Y-%m-%d")

            # Find the input element by its ID
            input_element = driver.find_element(By.ID, "1398")

            # Perform actions on the input element (e.g., entering text)
            input_element.send_keys(formatted_date)

            # Assuming driver is your webdriver instance
            final_save_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "saveButton"))
            )

            # Check if there is any overlay element like cookies and close it
            cookies_overlay = driver.find_element(By.CLASS_NAME, "cookies")
            if cookies_overlay.is_displayed():
                cookies_overlay.click()
            # Introduce a small delay to wait for the overlay to disappear
            time.sleep(2)  # Adjust the time as needed

            # Scroll the save button into view
            driver.execute_script(
                "arguments[0].scrollIntoView(true);", final_save_button
            )
            final_save_button.click()

            # Sleep for the specified duration
            time.sleep(sleep_duration)
            # Log the completion of the form
            simulate_fill_out()
            # # Find and select a value in the How long is your total work experience in other industries? dropdown
            # total_work_exp_dropdown = driver.find_element(By.NAME, "1385")
            # total_work_exp_select = Select(total_work_exp_dropdown)
            # fill_form_field("1385", "3508547")

            #  # Find and select a value in the How long is your total work experience in other industries? dropdown
            # total_work_exp_other_dropdown = driver.find_element(By.NAME, "1387")
            # total_work_exp_other_select = Select(total_work_exp_dropdown)
            # fill_form_field("1387", "3508548")

            # # Find and select a value in the Do you have BPO/Call Center experience? dropdown
            # type_of_bpo_dropdown = driver.find_element(By.NAME, "1388")
            # type_of_bpo_select = Select(type_of_bpo_dropdown)
            # fill_form_field("1388", "8960")

            data_filled = True
            # Mark the applicant as processed
            cursor.execute(
                "UPDATE applicants SET processed = 1 WHERE applicant_id = %s",
                (applicant_data[0],),
            )
            conn.commit()
            # time.sleep(10)  # Adjust the time as needed
            # Reset the browser session
            # Check network status before opening the URL
            if check_network_status():
                # Open the website link only if the network status is 200
                redirect_url = "https://transcom.avature.net/careers/Register?jobId=249&applicationStep=0&source=Vendor&tags=METACOM"
                driver = webdriver.Chrome(options=chrome_options)
                driver.get(redirect_url)
            else:
                print("Network status is not 200. Skipping opening the URL.")
# Close the MySQL connection outside the loop
cursor.close()
conn.close()
