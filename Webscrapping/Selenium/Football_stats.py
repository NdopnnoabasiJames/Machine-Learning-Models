from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.webdriver.support.ui import Select
import time

# 1. Keep the browser open after the script finishes
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 2. Set up ChromeDriver
service = Service("/opt/homebrew/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

website_url = "https://www.adamchoi.co.uk/overs/detailed"
driver.get(website_url)

try:
    # Click the button to display all matches
    all_matches_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="page-wrapper"]/div/home-away-selector/div/div/div/div/label[2]'))
    )
    all_matches_button.click()
    print("Button clicked!")

    select_country = Select(driver.find_element(By.ID, 'country'))
    select_country.select_by_visible_text('Spain')

    time.sleep(2)  # Wait for the page to update after selecting the country    

    # 1. Wait for the rows to actually exi st in the DOM
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'tr'))
    )

    # 2. Find all table rows
    matches = driver.find_elements(By.TAG_NAME, 'tr')

    # 3. Create a list to store the data
    all_matches_data = []

    for match in matches:
        cells = match.find_elements(By.TAG_NAME, 'td')
        
        # Check if this is a data row (usually has 4-6 columns)
        if len(cells) >= 4:
            all_matches_data.append({
                'Date': cells[0].text,
                'Home_Team': cells[2].text,  # Changed from cells[1]
                'Score': cells[3].text,       # Changed from cells[2]
                'Away_Team': cells[4].text    # Changed from cells[3]
            })

    # 5. Create the DataFrame
    df = pd.DataFrame(all_matches_data)

    # 6. Display the result
    print(df)
    print(f"Total matches scraped: {len(df)}")

except Exception as e:
    print(f"Something went wrong: {e}")

# Code here runs regardless of whether the 'try' succeeded or failed.
print("Script execution finished.")

driver.quit()