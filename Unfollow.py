from Instagram_Bot import InstagramBot
import time
import calendar

if __name__ == "__main__":

    username = input("[*]Username: ")
    password = input("[*]Password: ")

    ig = InstagramBot(username, password)
    print("[*]Logging in")
    ig.login()
    print("[+]Logged in")

    while True:
        try:
            deleteLines = []
            with open('Accounts_Followed.csv') as input_file:
                for i, line in enumerate(input_file):
                    print("[*]Checking " + line)
                    split = line.split(",")
                    split[1] = split[1][:-1]
                    print(split)
                    if int(calendar.timegm(time.time)) - int(split[1]) > 259200:
                        ig.unfollowUser(split[0])
                        deleteLines.append(line)
            for line in deleteLines:
                f = open("Accounts_Followed.csv", "r+")
                d = f.readlines()
                f.seek(0)
                for i in d:
                    if i != line:
                        f.write(i)
                f.truncate()
                f.close()
        except Exception as e:
            print(e)
            ig.closeBrowser()
            time.sleep(60)
            ig = InstagramBot(username, password)
            ig.login()