import argparse
import time

from PIL import Image

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

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

    with webdriver.Chrome(options=options) as driver:
        driver.implicitly_wait(10)
        driver.set_window_size(1920, 1080)

        driver.get(f"https://wwgc.onglide.com/?className={class_name}")

        navbar = driver.find_element(By.CLASS_NAME, "navbar")
        results = driver.find_element(By.CLASS_NAME, "resultsOverlay")
        sponsor = driver.find_element(By.CLASS_NAME, "sponsor")
        overlays = driver.find_element(By.CLASS_NAME, "overlays")
        map = driver.find_element(By.CLASS_NAME, "resizingMap")
        time.sleep(1)

        driver.execute_script("arguments[0].style.visibility='hidden'", map)
        results.screenshot(results_filename)

        driver.set_window_size(683, 384+24)
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

    image = resize_image("map.png", width=1366)
    image.save("output.png")
    print(f"{args.class_name} - Map")

    time.sleep(args.delay)
    image = resize_image("results.png", width=1366)
    image.save("output.png")
    print(f"{args.class_name} - Results")
