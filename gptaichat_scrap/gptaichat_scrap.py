from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, sys

def typing_effect(text, delay=0.005):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print('\n')

brave_options = ChromeOptions()

brave_options.binary_location = '/usr/bin/brave-browser'
brave_options.headless = True
brave_options.add_argument('--headless=new')

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
brave_options.add_argument(f"user-agent={user_agent}")

chromedriver_autoinstaller.install()

driver = webdriver.Chrome(options = brave_options, service = ChromeService())

url = 'https://gptaichat.org/'

wait = WebDriverWait(driver, 30)

AI_MSG_COUNTER = 1

try:
    print('Wait...')
    driver.get(url)
    print('Connected (enter "q" to exit)\n')

    textarea = wait.until(EC.presence_of_element_located((By.XPATH, '//textarea[@class="auto-expand wpaicg-chat-shortcode-typing"]')))

    while True:
        prompt = input('Prompt: ')

        if prompt == 'q':
            break

        textarea.send_keys(prompt)
        time.sleep(0.5)
        textarea.send_keys(Keys.ENTER)

        while True:
            answers = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//span[@class="wpaicg-chat-message"]')))

            if len(answers) == AI_MSG_COUNTER + 1:
                AI_MSG_COUNTER += 1
                typing_effect(answers[-1].text)
                break

except Exception as e:
    print(f'error : {e}')

finally:
    driver.close()
    driver.quit()
