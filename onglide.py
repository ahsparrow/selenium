import argparse
import shutil
import time

from PIL import Image, ImageDraw, ImageFont

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
def send_keys(element, key_str):
    for k in key_str:
        element.send_keys(k)
        time.sleep(0.5)

def resize_image(image_filename, width=0, height=0):
    image = Image.open(image_filename)
    w, h = image.width, image.height

    new_w = width
    new_h = h * width // w
    resized_image = image.resize((new_w, new_h))

    return resized_image

def get_class(class_name, map_filename, results_filename):
    options = Options()
    options.add_argument("--app=https://www.google.com")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("headless")

    with webdriver.Chrome(options=options) as driver:
        driver.implicitly_wait(10)
        driver.set_window_size(1920, 1080)

        driver.get(f"https://wwgc.onglide.com/?className={class_name}")
        time.sleep(10)

        navbar = driver.find_element(By.CLASS_NAME, "navbar")
        results = driver.find_element(By.CLASS_NAME, "resultsOverlay")
        sponsor = driver.find_element(By.CLASS_NAME, "sponsor")
        overlays = driver.find_element(By.CLASS_NAME, "overlays")
        map = driver.find_element(By.CLASS_NAME, "resizingMap")
        map_wrapper = driver.find_element(By.ID, "deckgl-wrapper")

        # Get the results
        try:
            units_button = driver.find_element(By.XPATH, '//button[@title="Switch to imperial units"]')
            units_button.click()
        except NoSuchElementException:
            pass

        driver.execute_script("arguments[0].style.visibility='hidden'", map)
        results.screenshot(results_filename)

        # Get the map
        driver.set_window_size(683, 384+24)

        try:
            zoom_button = driver.find_element(By.XPATH, '//button[@title="Zoom to task"]')

            # Button will be off screen - so trigger script directly
            driver.execute_script("arguments[0].click();", zoom_button);
            time.sleep(2)
        except NoSuchElementException:
            pass

        driver.execute_script("arguments[0].style.visibility='visible'", map)
        driver.execute_script("arguments[0].style.visibility='hidden'", navbar)
        driver.execute_script("arguments[0].style.visibility='hidden'", results)
        driver.execute_script("arguments[0].style.visibility='hidden'", sponsor)
        driver.execute_script("arguments[0].style.visibility='hidden'", overlays)

        map.screenshot(map_filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("class_name")
    parser.add_argument("--delay", type=int, default=10)
    args = parser.parse_args()

    get_class(args.class_name, "map.png", "results.png")

    # Map
    image = resize_image("map.png", width=1366)

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("Gidole-Regular.ttf", size=80)
    draw.text((10, 10), args.class_name.title(), font=font, fill=(0, 0, 255))

    image.save("tmp.png")
    shutil.move("tmp.png", "output.png")
    print(f"{args.class_name} - Map")

    time.sleep(args.delay)

    # Results
    image = resize_image("results.png", width=1366)
    bg = Image.new("RGBA", (1366, 768), (0, 0, 0))
    bg.paste(image, (0, (768 - image.height) // 2))
    bg.save("tmp.png")
    shutil.move("tmp.png", "output.png")
    print(f"{args.class_name} - Results")
