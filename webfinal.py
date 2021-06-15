#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import os

from instagramy import *
import re
import numpy as np
from flask import Flask, request, render_template
import pickle
from instabot import Bot
from difflib import SequenceMatcher

def count_digits_in_string(string):
    count = 0
    for i in string:
        if(i.isdigit()):
            count = count+1
    return count
    

def count_words_in_string(string):
    count = len(re.findall(r'\w+', string))
    return(count)
    
def trimuptoseq(x):
    return re.match("(.*?).jpg",x).group()


def is_propic_present(x):
    if(str(x)=="True"):
        return 0
    else:
        return 1

def is_private_account(x):
    if (str(x)=="True"):
        return 1
    else:
        return 0

def is_exturl_present(x):
    if str(x)=="":
        return 0
    else:
        return 1

def is_unameeqname(x1,x2):
    if(similar(x1,x2)>=5):
            return 1
    else:
            return 0

def similar(a, b):
    return float(SequenceMatcher(None, a, b).ratio())

def myfunc():
    uname=input("Username : ")
    if os.path.exists("config/" + uname + "_uuid_and_cookie.json"):
        os.remove("config/" + uname + "_uuid_and_cookie.json")
    pwd=input("Password : ")
    bot = Bot()
    bot.login(username=uname,password=pwd)
    ch=input("1: self 0:other")
    if(ch=="0"):
        uname=input("Enter Username")
    ch=input("Followers 1 ,Following 0")
    if(float(ch)==1):
        my_followers = bot.get_user_followers(uname)
    else:
        my_followers = bot.get_user_following(uname)

    print("pic\tn/lu\twrds\tn/ln\tu=n\tbio\txurl\tpri\tmcount\tfs\tfg")
    verified_users_list = []
    for follower in my_followers:
        #print(follower)
        #print()
        try:
            #user = InstagramUser(bot.get_user_info(follower)['username'])
            user = bot.get_user_info(follower)


            if(user["is_verified"]=="True"):
                verified_users_list.append(user["username"])
            following_count=user["following_count"]
            follower_count=user["follower_count"]
            npluname=count_digits_in_string(user["username"])/len(user["username"])
            wplname=count_words_in_string(user["full_name"])
            nplname=count_digits_in_string(user["full_name"])/len(user["full_name"])
            biolen=len(str(user["biography"]))
            propic=is_propic_present(user["has_anonymous_profile_picture"])

            exturl = is_exturl_present(user["external_url"])
            privacy = is_private_account(user["is_private"])
            post_count = user["media_count"]
            unameeqname = is_unameeqname(str(user['username']), str(user["full_name"]))
            #print(int(propic),"\t", round(float(npluname),2),"\t", int(wplname), "\t",round(float(nplname),2), "\t",int(unameeqname),"\t",
            #                 int(biolen),"\t", int(exturl), "\t",int(privacy), "\t",int(post_count), "\t",int(follower_count),"\t",
            #                 int(following_count))
            init_features = [int(propic), round(float(npluname),2), int(wplname), round(float(nplname),2), int(unameeqname),
                             int(biolen), int(exturl), int(privacy), int(post_count), int(follower_count),
                            int(following_count)]
            # init_features = [float(x) for x in request.form.values()]

            final_features = [np.array(init_features)]
            #print(final_features)
            # Std Scaling
            from sklearn.preprocessing import StandardScaler

            #sc = StandardScaler()
            #final_features = sc.fit_transform(final_features)


            model = pickle.load(open('model.pkl', 'rb'))
            prediction = model.predict(final_features)



            #print(user['username'],"\t\tLR : ",prediction1,"\tGN : ",prediction2,"\tDT : ", prediction3, "\tKN : ", prediction4,"\tSV : ", prediction5, "\tRF : ", prediction6)
            #print(user['username'],"\t\tLR : ",prediction)

            print(user['username'])
            if (prediction == 1):
                print("Fake")
                # return render_template('spam.html', predict=' :This Instagram account is Fake')
            else:
                print("Not Fake")
                # return render_template('spam.html', predict=' :This Instagram account is Not Fake')


        except Exception as e:
            print(e)
    #print("Verified Follower/Following ", verified_users_list)



    #return render_template('spam.html',follow_count=user.user_data["edge_follow"]['count'],
    


#app = Flask(__name__)

#@app.route('/')
#@app.route('/home')
#def home():


#    return render_template('contact.html',predict="ffjfhj",var="hjgj")

#@app.route('/contact')
#def contact():
#    return render_template('contact.html')

#@app.route('/report')
#def report():
#    return render_template('report.html')

#@app.route('/spam')
#def quality():

    
       
#@app.route('/predict',methods=['POST'])
#def predict():
#    return render_template('spam.html')


if __name__ == "__main__":
#    app.run
     myfunc()
