#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time

keyword = '美食'
width = 1280

options = webdriver.ChromeOptions()
options.add_argument('user-data-dir=chrome')

with webdriver.Chrome(options=options) as driver:
    driver.get(f'https://www.pexels.com/zh-cn/search/{keyword}/')

    WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'photo-item')))

    baseHandle = driver.current_window_handle

    photoDict = {}
    for i in range(100):
        elements = driver.find_elements_by_class_name('photo-item')
        elementCount = len(elements)

        print(f'found photo elements: {elementCount}')

        for element in elements:
            photoId = element.get_attribute('data-photo-modal-medium-id')
            if photoId is None:
                print(f'    invalid {element.tag_name}')
            else:
                if photoId in photoDict:
                    continue

                photoDict[photoId] = True
                downloadUrl = f'https://images.pexels.com/photos/{photoId}/pexels-photo-{photoId}.jpeg?w={width}&q=92&fit=scale-down&dl={photoId}.jpg&fm=jpg'
                print(f'    new image: {downloadUrl}')
                driver.execute_script(f'''window.open("{downloadUrl}","_blank");''')
                time.sleep(0.5)

        driver.switch_to.window(baseHandle)
        time.sleep(0.5)

        scrollHeight = driver.execute_script('return window.document.body.scrollHeight')
        driver.execute_script(f'window.scroll(0, {scrollHeight})')
        print(f'scroll to {scrollHeight}')

        time.sleep(3)

    print('exiting')
