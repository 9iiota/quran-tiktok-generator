from selenium import webdriver

# Create a new instance of the Firefox WebDriver
driver = webdriver.Firefox()

# Open the target webpage
driver.get("URL_OF_THE_WEBPAGE")

# Find the file input element by its class name (or another suitable locator)
file_input = driver.find_element_by_class_name("svelte-116rqfv")

# Provide the path to the file you want to upload
file_path = "path/to/your/file.wav"
file_input.send_keys(file_path)

# You might need to submit the form or perform other actions to proceed
# For example:
# submit_button = driver.find_element_by_id("submit-button-id")
# submit_button.click()

# Close the browser window
driver.quit()