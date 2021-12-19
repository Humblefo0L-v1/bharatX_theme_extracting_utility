#Python program to extract the merchant logo, merchant website, primary and secondary colors when given their brand name.
#Tools used: Python, Selenium

#Necessary library imports
from selenium import webdriver
from selenium.webdriver.common import by
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.color import Color
import base64
import io
from PIL import Image
import warnings

#Input the Brand name to be scraped
brandName = input("Enter the brand name: ")

#Setting up Selenium
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

#Google Images search for brand Logo
driver.get("https://images.google.com/")
#Implementing Google Images query search by giving Brand name as an argument
gSearch = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "q")))
gSearch.send_keys(brandName + " logo")
gSearch.send_keys(Keys.RETURN)

logo_thumb = driver.find_elements_by_class_name("Q4LuWd")
logo_thumb[0].click()

logo_image_src = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.CLASS_NAME, "n3VNCb"))).get_attribute("src")
logo_image_src = logo_image_src[22:len(logo_image_src)]

#Utility Function to download Brand Logo
def download_image(download_path, file_name):
    try:
        # #Using requests to fetch image url
        # img_content = requests.get(src_url).content
        image = base64.b64decode(logo_image_src)
        #Typecasting the image filetype to BytesIO
        img_file_type = io.BytesIO(image)
        img = Image.open(img_file_type)
        #Specify the download location
        file_path = download_path + file_name
        #Open the image file and save it to the specified location
        with open(file_path, "wb") as f:
            img.save(f, "PNG")
        print("Extraction Successful")
    #Pass the exception in case of failure
    except Exception as e:
        print('Failed! - ', e)

#Calling the "download_image" function, it takes two arguments: Download location path and filename
download_image(r"C:\Users\HP\Desktop\Python_Scripts\ " , "logo.png")

#Google search for brand website
driver.get("https://www.google.com/")
#Implementing Google Images query search by giving Brand name as an argument
gSearch = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "q")))
gSearch.send_keys(brandName + " website")
gSearch.send_keys(Keys.RETURN)

#Extracting the Brand website through "href" tag
brand_website_result = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".yuRUbf > a"))).get_attribute('href')
print("Brand Website: ", brand_website_result)

#Extracting Primary and Secondary colors
driver.get(brand_website_result)
color_element = driver.find_element_by_tag_name("body")
primary_color = color_element.value_of_css_property('color')
secondary_color = color_element.value_of_css_property('background-color')

print("Primary Color in RGBA format: ",primary_color)
print("Secondary Color in RGBA format: ",secondary_color)
#Converting colors from RGBA to HEX
primary_color = Color.from_string(primary_color).hex
secondary_color = Color.from_string(secondary_color).hex
print("Primary Color in HEX format: ",primary_color)
print("Secondary Color in HEX format: ",secondary_color)
