#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import os
import re
from instabot import Bot
from difflib import SequenceMatcher


def count_digits_in_string(string):
    count = 0
    for i in string:
        if (i.isdigit()):
            count = count + 1
    return count


def count_words_in_string(string):
    count = len(re.findall(r'\w+', string))
    return (count)


def trimuptoseq(x):
    return re.match("(.*?).jpg", x).group()


def is_propic_present(x):
    if (str(x) == "True"):
        return 0
    else:
        return 1


def is_private_account(x):
    if (str(x) == "True"):
        return 1
    else:
        return 0


def is_exturl_present(x):
    if str(x) == "":
        return 0
    else:
        return 1


def is_unameeqname(x1, x2):
    if (similar(x1, x2) >= 5):
        return 1
    else:
        return 0


def similar(a, b):
    return float(SequenceMatcher(None, a, b).ratio())


def myfunc():
    uname = input("Login Username : ")
    if os.path.exists("config/" + uname + "_uuid_and_cookie.json"):
        os.remove("config/" + uname + "_uuid_and_cookie.json")
    pwd = input("Login Password : ")
    bot = Bot()
    bot.login(username=uname, password=pwd)
    print("pic\tn/lu\twrds\tn/ln\tu=n\tbio\txurl\tpri\tmcount\tfs\tfg")
    uname = input("Enter username or e for exit:")
    while (uname != "e"):
        try:
            user = bot.get_user_info(uname)
            following_count = user["following_count"]
            follower_count = user["follower_count"]
            npluname = count_digits_in_string(user["username"]) / len(user["username"])
            wplname = count_words_in_string(user["full_name"])
            nplname = count_digits_in_string(user["full_name"]) / len(user["full_name"])
            biolen = len(str(user["biography"]))
            propic = is_propic_present(user["has_anonymous_profile_picture"])

            exturl = is_exturl_present(user["external_url"])
            privacy = is_private_account(user["is_private"])
            post_count = user["media_count"]
            unameeqname = is_unameeqname(str(user['username']), str(user["full_name"]))
            print(float(propic), "\t", round(float(npluname),2), "\t", float(wplname), "\t", round(float(nplname),2), "\t",
                  float(unameeqname), "\t",
                  float(biolen), "\t", float(exturl), "\t", float(privacy), "\t", float(post_count), "\t",
                  float(follower_count), "\t",
                  float(following_count))
            x = input("1-Fake 0-Not Fake? : ")
            init_features = [float(propic), round(float(npluname), 2), float(wplname), round(float(nplname), 2),
                             float(unameeqname),
                             float(biolen), float(exturl), float(privacy), float(post_count), float(follower_count),
                             float(following_count), float(x)]
            from csv import writer
            with open('dataset.csv', 'a') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(init_features)
                f_object.close()
            unamelist=[uname,x]
            with open('usernames.csv', 'a') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(unamelist)
                f_object.close()

            uname = input("Enter username or e for exit:")

        except Exception as e:
            print(e)

myfunc()