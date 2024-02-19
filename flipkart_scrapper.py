from time import sleep
import logging
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logging.basicConfig(filename='scraping.log', level=logging.DEBUG)


def find_element_with_retry(driver, by, value, max_attempts=3, delay=2):
    attempt = 0
    while attempt < max_attempts:
        try:
            return WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException as te:
            attempt += 1
            if attempt <= max_attempts:
                print('Retrying...')
                driver.refresh()
                sleep(delay)
            else:
                print('Max attempts reached. Element not found.', te)
                return None
        except Exception as e:
            print('An unexpected error occurred:', e)
            return None


def find_all_elements_with_retry(driver, by, value, max_attempts=3, delay=2):
    attempt = 0
    while attempt < max_attempts:
        try:
            return WebDriverWait(driver, 1).until(
                EC.presence_of_all_elements_located((by, value))
            )
        except TimeoutException as te:
            attempt += 1
            if attempt <= max_attempts:
                print('Retrying...')
                driver.refresh()
                sleep(delay)
            else:
                print('Max attempts reached. Element not found.', te)
                return None
        except Exception as e:
            print('An unexpected error occurred:', e)
            return None


def scrape_product_data(pid):
    try:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0 Chrome/103.0.0.0"
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f'user-agent={user_agent}')
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--ignore-certificate-errors-spki-list')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--disable-3d-apis")
        chrome_options.add_argument("--output=/dev/null")
        chrome_options.add_argument("--window-size=1920,1080")

        driver: WebDriver = webdriver.Chrome(options=chrome_options, service=Service())
        driver.implicitly_wait(5)  # Reduce implicit wait time

        web = f'https://www.flipkart.com/cotton-fabric-undershirt/p/itm120ded1ca7a63?pid={pid}'
        driver.get(web)
        sleep(1)

        is_unknown_issue_occurred = driver.find_elements(By.ID, "retry_btn")
        if len(is_unknown_issue_occurred) > 0:
            data = {
                'fsn': pid,
                'issue': 'Unknown issue occurred on flipkart'
            }
            print(data)
            return data
        else:
            title_element = find_element_with_retry(driver, By.XPATH, "//span[@class='B_NuCI']")
            product_title = title_element.text if title_element else ''
            print('1. Product Title: ', product_title)

            review_rating_elements = driver.find_elements(By.XPATH, "//span[@class='_2_R_DZ']")
            if review_rating_elements:
                review_rating_text = review_rating_elements[0].text
                ratings, reviews = review_rating_text.split(' & ') if ' & ' in review_rating_text else ('0', '0')
            else:
                reviews = '0'
                ratings = '0'
            print('2. Reviews: ', reviews)
            print('3. Ratings: ', ratings)

            highlight_elements = driver.find_elements(By.CLASS_NAME, '_21Ahn-')
            highlights = ', '.join([highlight_element.text for highlight_element in
                                    highlight_elements]) if highlight_elements else 'No highlights found'
            print('4. Highlights: ', highlights)

            description_elements = find_element_with_retry(driver, By.CLASS_NAME, '_1mXcCf')
            descriptions = description_elements.text if description_elements else 'No descriptions found'
            print('5. Descriptions: ', descriptions)

            readmore = find_element_with_retry(driver, By.CLASS_NAME, '_1FH0tX')
            if readmore:
                print('6. Readmore found: ')
                readmore.click()

            other_features_element = find_element_with_retry(driver, By.XPATH,
                                                             '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[9]/div['
                                                             '5]/div/div[2]/div[1]/div[8]/table/tbody/tr[7]/td[2]/ul/li')
            other_features = other_features_element.text if other_features_element else 'No other Features'
            print('7. Other Features: ', other_features)

            is_sold_out = driver.find_elements(By.CLASS_NAME, "_16FRp0")

            data = {
                'fsn': pid,
                'Product Title': product_title,
                'Reviews': reviews,
                'Ratings': ratings,
                'Highlights': highlights,
                'Descriptions': descriptions,
                'Other Features': other_features,
                'Sold Out': bool(is_sold_out)
            }

            img_elements = driver.find_elements(By.CLASS_NAME, 'q6DClP')
            if img_elements:
                print('8. Image: ')
                for i, img_element in enumerate(img_elements, start=1):
                    image_url = img_element.get_attribute('src')
                    data[f'image_{i}'] = image_url
                    print(f"Image {i} URL: {image_url}")

            if is_sold_out:
                print('9. Sold Out')
                data['Sold Out'] = True
            else:
                data['Sold Out'] = False

            return data

    except Exception as e:
        print(f"Exception occurred while scraping product data - {e}: {pid}")
        logging.error(f"Error scraping product {pid}: {e}")
    finally:
        driver.quit()

















































# from time import sleep
# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.webdriver import WebDriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
#
#
# def find_element_with_retry(driver, by, value, max_attempts=3, delay=2):
#     attempt = 0
#     while attempt < max_attempts:
#         try:
#             return WebDriverWait(driver, 1).until(
#                 EC.presence_of_element_located((by, value))
#             )
#         except TimeoutException as te:
#             attempt += 1
#             if attempt <= max_attempts:
#                 print('Retrying...')
#                 driver.refresh()
#                 sleep(delay)
#             else:
#                 print('Max attempts reached. Element not found.', te)
#                 return None
#         except Exception as e:
#             print('An unexpected error occurred:', e)
#             return None
#
#
# def find_all_elements_with_retry(driver, by, value, max_attempts=3, delay=2):
#     attempt = 0
#     while attempt < max_attempts:
#         try:
#             return WebDriverWait(driver, 1).until(
#                 EC.presence_of_all_elements_located((by, value))
#             )
#         except TimeoutException as te:
#             attempt += 1
#             if attempt <= max_attempts:
#                 print('Retrying...')
#                 driver.refresh()
#                 sleep(delay)
#             else:
#                 print('Max attempts reached. Element not found.', te)
#                 return None
#         except Exception as e:
#             print('An unexpected error occurred:', e)
#             return None
#
#
# def scrape_product_data(pid):
#
#     try:
#         user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0 Chrome/103.0.0.0"
#         chrome_options = webdriver.ChromeOptions()
#         chrome_options.add_argument(f'user-agent={user_agent}')
#         chrome_options.add_argument('--headless')
#         chrome_options.add_argument('--no-sandbox')
#         chrome_options.add_argument('--ignore-certificate-errors-spki-list')
#         chrome_options.add_argument('--ignore-ssl-errors')
#         chrome_options.add_argument('--disable-dev-shm-usage')
#         chrome_options.add_argument("--disable-gpu")
#         chrome_options.add_argument("--disable-logging")
#         chrome_options.add_argument("--log-level=3")
#         chrome_options.add_argument("--disable-3d-apis")
#         chrome_options.add_argument("--output=/dev/null")
#         chrome_options.add_argument("--window-size=1920,1080")
#
#         driver: WebDriver = webdriver.Chrome(options=chrome_options, service=Service())
#         driver.implicitly_wait(5)  # Reduce implicit wait time
#
#         web = f'https://www.flipkart.com/cotton-fabric-undershirt/p/itm120ded1ca7a63?pid={pid}'
#         driver.get(web)
#         sleep(1)
#         product_title = ''
#
#         is_unknown_issue_occurred = driver.find_elements(By.ID, "retry_btn")
#         if len(is_unknown_issue_occurred) > 0:
#             data = {
#                 'fsn': pid,
#                 'issue': 'Unknown issue occurred on flipkart'
#             }
#             print(data)
#             return data
#         else:
#             title_element = find_element_with_retry(driver, By.XPATH, "//span[@class='B_NuCI']")
#             if title_element:
#                 product_title = title_element.text
#             print('1. Product Title: ', product_title)
#             try:
#                 review_rating_elements = WebDriverWait(driver, 1).until(
#                     EC.presence_of_all_elements_located((By.XPATH, "//span[@class='_2_R_DZ']"))
#                 )
#
#                 if review_rating_elements:
#                     review_rating_text = review_rating_elements[0].text
#
#                     if ' & ' in review_rating_text:
#                         ratings_text, reviews_text = review_rating_text.split(' & ')
#                         ratings = ratings_text.split()[0]
#                         reviews = reviews_text.split()[0]
#                     else:
#                         reviews = '0'
#                         ratings = '0'
#                 else:
#                     reviews = '0'
#                     ratings = '0'
#
#             except TimeoutException as t:
#                 print("TimeoutException", t)
#                 reviews = '0'
#                 ratings = '0'
#
#             except NoSuchElementException as e:
#                 print('No such reviews and ratings found', e)
#                 reviews = '0'
#                 ratings = '0'
#             print('2. Reviews: ', reviews)
#             print('3. Ratings: ', ratings)
#
#             highlight_elements = find_all_elements_with_retry(driver, By.CLASS_NAME, '_21Ahn-')
#             if highlight_elements:
#                 highlights_text = ', '.join([highlight_element.text for highlight_element in highlight_elements])
#                 highlights = highlights_text
#             else:
#                 highlights = 'No highlights found'
#                 print('No highlights found')
#             print('4. Highlights: ', highlights)
#
#             description_elements = find_element_with_retry(driver, By.CLASS_NAME, '_1mXcCf')
#             if description_elements:
#                 descriptions = description_elements.text
#             else:
#                 descriptions = 'No descriptions found'
#             print('5. Descriptions: ', descriptions)
#
#             readmore = find_element_with_retry(driver, By.CLASS_NAME, '_1FH0tX')
#             if readmore:
#                 print('6. Readmore found: ')
#                 readmore.click()
#
#             other_features_element = find_element_with_retry(driver, By.XPATH,
#                                                              '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[9]/div['
#                                                              '5]/div/div[2]/div[1]/div[8]/table/tbody/tr[7]/td[2]/ul/li')
#             if other_features_element:
#                 other_features = other_features_element.text
#             else:
#                 other_features = 'No other Features'
#             print('7. Other Features: ', other_features)
#             is_sold_out = driver.find_elements(By.CLASS_NAME, "_16FRp0")
#
#             data = {
#                 'fsn': pid,
#                 'Product Title': product_title,
#                 'Reviews': reviews,
#                 'Ratings': ratings,
#                 'Highlights': highlights,
#                 'Descriptions': descriptions,
#                 'Other Features': other_features,
#                 'Sold Out': bool(is_sold_out)
#             }
#
#             img_elements = find_all_elements_with_retry(driver, By.CLASS_NAME, 'q6DClP')
#             if img_elements:
#                 print('8. Image: ')
#                 for i, img_element in enumerate(img_elements, start=1):
#                     image_url = img_element.get_attribute('src')
#                     data[f'image_{i}'] = image_url
#                     print(f"Image {i} URL: {image_url}")
#
#             is_sold_out = driver.find_elements(By.CLASS_NAME, "_16FRp0")
#
#             if len(is_sold_out) != 0:
#                 print('9. Sold Out')
#                 data['Sold Out'] = True
#             else:
#
#                 data['Sold Out'] = False
#
#             return data
#
#     except Exception as e:
#         print(f"Exception occurred while scraping product data - {e}: {pid}")
#     finally:
#         driver.quit()