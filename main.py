# Copyright 2019 Oskar Sharipov
# Copyright 2019 Timur Garaev
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.


from selenium import webdriver
from time import sleep


# ----------------------------
# Edit lines below.


FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLScyrlhh0IGxev3S9CKrO8vyX_MkhfLSKCl_2Ux3QZRDo2_DaA/viewform'
driver = webdriver.WebKitGTK
INPUT_FIELD_XPATH_LAYOUT = '/html/body/div/div[2]/form/div/div[2]/div[2]/div[{index}]/div/div[2]/div/div[1]/div/div[1]/input'
SEND_BUTTON_XPATH = '/html/body/div/div[2]/form/div/div[2]/div[3]/div[1]/div/div/span'

# New design xpaths. WIP (have no opportunity to look at new design page).
# INPUT_FIELD_XPATH_LAYOUT = '/html/body/div/div[2]/form/div/div[2]/div[2]/div[{index}]/div/div[2]/div/div[1]/div/div[1]/input'
# SEND_BUTTON_XPATH = '/html/body/div/div[2]/form/div/div[2]/div[3]/div[1]/div/div/span'

# Stop editing lines.
# ----------------------------


def is_command(string):
    return len(string) and string[0] in ('<', '>', '@')


def new_index(string, previous_index):
    # if command is < which means 'decrease index'
    if all(char == '<' for char in string):
        return previous_index - len(string)

    # if command is > which means 'increase index'
    if all(char == '>' for char in string):
        return previous_index + len(string)

    # if command is @N which means 'goto N'
    if string[0] == '@' and string[1:].isdigit():
        return int(string[1:])

    # if command syntax is wrong
    return previous_index


def preload(driver):
    driver.get(FORM_URL)
    problem_set_number = input('Задание: ')
    start_with = input('Начинать с номера: ')
    while 'y' not in input('Вы залогинились в Google [y/n]? '):
        pass

    return problem_set_number, start_with


def fill(driver, fill_with):
    ANSWER_FIELDS = 3
    fill_xpaths = [
        INPUT_FIELD_XPATH_LAYOUT.format(
            index=index+1
        )
        for index in range(ANSWER_FIELDS)
    ]

    for i in range(ANSWER_FIELDS):
        element = driver.find_element_by_xpath(fill_xpaths[i])
        element.send_keys(fill_with[i])
    send_button_element = driver.find_element_by_xpath(SEND_BUTTON_XPATH)
    send_button_element.click()


def rolling(driver, problem_set_number, start_with):
    index = int(start_with)

    while True:
        if driver.current_url != FORM_URL:
            driver.get(FORM_URL)
        answer = input('№{}: '.format(index))
        if is_command(answer):
            index = new_index(answer, index)
            continue

        fill_with = [
            problem_set_number,
            index,
            answer
        ]
        fill(driver, fill_with)
        index += 1


def main():
    global driver
    # execute webdriver
    driver = driver()
    problem_set_number, start_with = preload(driver)
    rolling(driver, problem_set_number, start_with)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        print('Пока <3')
