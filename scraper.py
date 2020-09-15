from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
from PIL import Image
from os import mkdir, path
from shutil import rmtree
import sys

# location of slide files pre pdf conversion
slides_root = "temp-slides/"

# make sure that the temp dir doesn't already exist
if path.exists(slides_root):
    input("please delete or move temp-slides, then press any key")

# set up the web driver
options = Options()
options.headless = True
driver = webdriver.Firefox(service_log_path='/dev/null', options=options)

# each arg is a url to a particular prof's weird slideshow
# screenshot each slide and combine them into a single pdf,
# then delete the leftover slide pictures and claim victory
arg_counter = 1
while arg_counter < len(sys.argv):
    url = sys.argv[arg_counter]
    driver.get(url)
    next_slide_button = driver.find_element_by_class_name('navigate-right')
    counter = 0
    enabled = True
    mkdir(slides_root)
    while enabled:
        enabled = next_slide_button.is_enabled()
        driver.save_screenshot(slides_root + str(counter) + ".png")
        # sleep to let the slide come into view
        sleep(0.75)
        if enabled:
            next_slide_button.click()
        counter += 1

    images = []
    for i in range(counter):
        images.append(Image.open(slides_root + str(i) + ".png").convert('RGB'))
        images[0].save(url.split("/")[5].split(".")[0] + ".pdf", save_all=True,
                       append_images=images)
    rmtree(slides_root)
    arg_counter += 1

driver.close()
