import calendar
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import sys

def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()

def writeFollow(name):
    if os.path.exists("Accounts_Followed.csv"):  # optional check if file exists
        with open("Accounts_Followed.csv", 'a') as file:
            file.write(name +"," + calendar.timegm(time.time()) + "\n")  # could be any text, appended @ the end of file

class InstagramBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()

    def closeBrowser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(2)
        login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        login_button.click()
        time.sleep(2)
        user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)
        password_elem = driver.find_element_by_xpath("//input[@name='password']")
        password_elem.clear()
        password_elem.send_keys(self.password)
        password_elem.send_keys(Keys.RETURN)
        time.sleep(2)

    def unfollowUser(self, user):
        driver = self.driver
        driver.get("https://www.instagram.com/" + user + "/")
        time.sleep(2)
        try:
            driver.find_element_by_xpath("//button[@class='_5f5mN    -fzfL     _6VtSN     yZn4P   ']").click()
        except Exception as e:
            print("[!}]Already unfollowed")


    def like_photo(self, hashtag):
        comments = ['Dope!', 'Awesome!', 'Amazing!', 'Pure fire!', 'Hot', 'Nice!', 'Sweet!', 'Noice', 'Thaz hot',
                    'Looking good!', 'Very nice!', 'Very dope!', 'Absolute fire!', 'Looken good!', 'Wow!']

        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(2)

        # gathering photos
        pic_hrefs = []
        for i in range(1, 7):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                # get tags
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                # finding relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                # building list of unique photos
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
                print("Check: pic href length " + str(len(pic_hrefs)))
            except Exception:
                continue

        # Liking photos
        unique_photos = len(pic_hrefs)
        for pic_href in pic_hrefs:
            driver.get(pic_href)
            time.sleep(.5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            if(random.randint(0,1) == 0):
                try:
                    time.sleep(random.randint(2, 4))
                    try:
                        # Check to see if unlike button exists, should throw error if doesn't
                        driver.find_element_by_xpath('//span[@aria-label="Unlike"]')
                        print("\n[*]Already liked, skipping to next")
                    except Exception as ex:
                        try:
                            print("\n[*]Liking")
                            driver.find_element_by_xpath('//span[@aria-label="Like"]').click()
                            print("[+]Liked")
                            time.sleep(.5)
                            print("[*]Commenting")
                            driver.find_element_by_xpath("//textarea[@aria-label='Add a comment…']").click()
                            driver.find_element_by_xpath("//textarea[@aria-label='Add a comment…']").send_keys(random.choice(comments))
                            driver.find_element_by_xpath("//textarea[@aria-label='Add a comment…']").send_keys(Keys.RETURN)
                            print('[+]Commented')
                            #print("[*]Following")
                            # try:
                            #     driver.find_element_by_xpath("//button[@type='button']").click()
                            #     writeFollow(driver.find_element_by_xpath("//a[@class='FPmhX notranslate nJAzx']").text)
                            # except Exception as e:
                            #     print("[!]Already following")
                        except Exception as e:
                            print("[!]Error")
                            print(e)
                            time.sleep(.5)
                    for second in reversed(range(0, random.randint(18, 28))):
                        print_same_line("[*]#" + hashtag + ': unique photos left: ' + str(unique_photos) + " | Sleeping " + str(second))
                        time.sleep(1)
                except Exception as e:
                    time.sleep(2)
            else:
                print("\n[*]Skipping photo to avoid bot detection")
                time.sleep(random.randint(5,10))
            unique_photos -= 1

if __name__ == "__main__":

    username = input("[*]Username: ")
    password = input("[*]Password: ")

    ig = InstagramBot(username, password)
    print("[*]Logging in")
    ig.login()
    print("[+]Logged in")

    hashtags = ['car', 'honda', 'civic', 'civicsi', 'honda_scene',
                'hondacivicsi', 'hondatuning', 'hondacivic', 'civictyper', 'civichatchback', 'civiccoupe', 'civicnation',
                'civicturbo', 'civicsedan', 'civicclub', 'civic10thgen', 'civic9thgen', 'civic8thgen', 'jdm',
                'slammed', 'tuner', 'vtec', 'ivtec', 'stanced', 'acura', 'stancenation',
                'civictuners', 'civics', 'hondas', 'carculture', 'vtectuning', '1320', 'kseriesonly']

    while True:
        try:
            # Choose a random tag from the list of tags
            tag = random.choice(hashtags)
            ig.like_photo(tag)
            # Wait an hour before moving to next hashtag
            for second in reversed(range(0, random.randint(18000,19000))):
                print_same_line("[*] Seconds till next Hashtag: " + str(second))
                time.sleep(1)
        except Exception:
            ig.closeBrowser()
            time.sleep(60)
            ig = InstagramBot(username, password)
            ig.login()