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


import threading
import queue
from selenium import webdriver


# ----------------------------
# Edit lines below.


FORM_URL = (
    'https://docs.google.com/forms/d/e/'
    '1FAIpQLScyrlhh0IGxev3S9CKrO8vyX_MkhfLSKCl_2Ux3QZRDo2_DaA/viewform'
)
DRIVER = webdriver.WebKitGTK

# New design xpaths.
INPUT_FIELD_XPATH_LAYOUT = (
    '/html/body/div/div[2]/form/div/div/div[2]/'
    'div[{index}]/div/div[2]/div/div[1]/div/div[1]/input'
)
SEND_BUTTON_XPATH = '/html/body/div/div[2]/form/div/div/div[3]/div[1]/div/div/span/span'

# Old design xpaths.
# INPUT_FIELD_XPATH_LAYOUT = (
#   '/html/body/div/div[2]/form/div/div[2]/'
#   'div[2]/div[{index}]/div/div[2]/div/div[1]/div/div[1]/input'
# )
# SEND_BUTTON_XPATH = '/html/body/div/div[2]/form/div/div[2]/div[3]/div[1]/div/div/span'

# Stop editing lines.
# ----------------------------

solutions_queue = queue.Queue()
filling_thread = None


def is_command(string):
    return len(string) and string[0] in ('<', '>', '@', '$')


def process_command(string, previous_index, previous_problem_set):
    # if command is < which means 'decrease index'
    if all(char == '<' for char in string):
        return previous_index - len(string), previous_problem_set

    # if command is > which means 'increase index'
    if all(char == '>' for char in string):
        return previous_index + len(string), previous_problem_set

    # if command is @N which means 'goto N'
    if string[0] == '@' and string[1:].isdigit():
        return int(string[1:]), previous_problem_set

    # if command is $N which means 'goto N problem set and reset index'
    if string[0] == '$' and len(string[1:]):
        return 1, string[1:]

    # if command syntax is wrong
    return previous_index, previous_problem_set


def preload(driver):
    driver.get(FORM_URL)
    problem_set_number = input('Задание: ')
    while 'y' not in input('Вы залогинились в Google [y/n]? '):
        pass

    return problem_set_number


def fill(driver):
    while True:
        solution = solutions_queue.get()
        if solution is None:
            break

        ANSWER_FIELDS = 3
        fill_xpaths = [
            INPUT_FIELD_XPATH_LAYOUT.format(
                index=index+1
            )
            for index in range(ANSWER_FIELDS)
        ]

        if driver.current_url != FORM_URL:
            driver.get(FORM_URL)
        for i in range(ANSWER_FIELDS):
            element = driver.find_element_by_xpath(fill_xpaths[i])
            element.send_keys(solution[i])
        send_button_element = driver.find_element_by_xpath(SEND_BUTTON_XPATH)
        send_button_element.click()


def rolling(problem_set_number, start_with=0):
    index = start_with

    while True:
        answer = input('№{}: '.format(index))
        if is_command(answer):
            index, problem_set_number = process_command(
                answer,
                index,
                problem_set_number
            )
            continue

        solution = [
            problem_set_number,
            index,
            answer
        ]
        solutions_queue.put(solution)
        index += 1


def main():
    global filling_thread
    # execute webdriver
    driver = DRIVER()
    problem_set_number = preload(driver)
    filling_thread = threading.Thread(target=fill, args=(driver,))
    filling_thread.start()
    rolling(problem_set_number)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        print('Завершение работы...')
        solutions_queue.put(None)
        filling_thread.join()
        print('Пока <3')
