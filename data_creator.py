#! /usr/bin/python
import json
import nltk
import re

# Filenames of various tables that will be opened.
checkin_file = "yelp_training_set_checkin.json"
review_file = "yelp_training_set_review.json" 
user_file = "yelp_training_set_user.json" 
business_file = "yelp_training_set_business.json"  
attributes_file = "yelp_training_set_attributes.csv"

# Returns the attribute index for the length related scores.
def GetLengthScoreIndex():
  return ["words", "paras", "para1", "sentences"]
  
# Returns scores related to length of the text.
def GetLengthScores(text):
  return [len(text.split(" ")),  # Number of words
          len(text.split("\n")),   # Number of paragraphs
          len(re.split('[.!?]', text)),  # Number of sentences
          len(text.split("\n")[0].split(" "))]  # First paragraph length

# Returns the attribute index for the Parts of Speech related stuff.
def GetPOSScoreIndex(): return []

# Returns scores related to the various parts of speech usages.
def GetPOSScores(text): return []

# Returns the attribute index for the sentiment scores.
def GetSentiScoreIndex(): return[]

# Returns various scores returned from sentiment analysis of the text.
def GetSentiScores(text): return []

############# Read all the tables
# Load all the Check in info.
li = [json.loads(a.strip('\n')) for a in open(checkin_file).readlines()]
checkin_info = {}
for x in li: checkin_info[x["business_id"]] = json.dumps(x["checkin_info"])

# Load all the business details.
li = [json.loads(a.strip('\n')) for a in open(business_file).readlines()]
business = {}
for x in li: business[x["business_id"]] = json.dumps(x)

# Load all the user info.
li = [json.loads(a.strip('\n')) for a in open(user_file).readlines()]
user = {}
for x in li: user[x["user_id"]] = json.dumps(x)

############# Reading tables done

# The file to which we will write our attributes to.
attributes = open(attributes_file, 'w')

# write the index first
index = ["num"]
index += GetLengthScoreIndex()
index += GetPOSScoreIndex()
index += GetSentiScoreIndex()
index += ["stars", "user_name", "user_review_count", \
         "user_avg_stars", "user_useful", "user_funny", "user_cool", \
         "biz_name", "biz_neighb", "biz_address", "biz_city", "biz_state", \
         "biz_lat", "biz_lng", "biz_review_count", "biz_stars", "biz_cats", \
         "biz_open", "funny", "cool", "useful"]
attributes.writelines([", ".join(index) + "\n"])

# Convert reviews to attributes by joining them with the other tables
reviews = open(review_file, 'r')
count = 0
failures = 0
for review in reviews:
  try:
    attrs = []  # A list of attributes that need to be output
    count = count + 1
    attrs.append(count)  # serial number

    li = json.loads(review)

    # Review text scores
    #attrs.append(li["text"].replace("\n", " "))
    review_text = li["text"]
    attrs += [str(attr) for attr in GetLengthScores(review_text)]
    attrs += [str(attr) for attr in GetPOSScores(review_text)]
    attrs += [str(attr) for attr in GetSentiScores(review_text)]

    # Review info    
    attrs.append(li["stars"])
    
    # User info
    ui = json.loads(user[li["user_id"]])
    attrs.append(ui["name"])
    attrs.append(ui["review_count"])
    attrs.append(ui["average_stars"])
    attrs.append(ui["votes"]["useful"])
    attrs.append(ui["votes"]["funny"])
    attrs.append(ui["votes"]["cool"])

    # Business info
    bi = json.loads(business[li["business_id"]])
    attrs.append(bi["name"])
    attrs.append(bi["neighborhoods"])
    attrs.append(bi["full_address"].replace("\n", " "))
    attrs.append(bi["city"])
    attrs.append(bi["state"])
    attrs.append(bi["latitude"])
    attrs.append(bi["longitude"])
    attrs.append(bi["review_count"])
    attrs.append(bi["stars"])
    attrs.append(bi["categories"])
    attrs.append(bi["open"])

    # Checkin info
    #ci = checkin_info[li.["business_id"]]

    # Votes
    attrs.append(li["votes"]["funny"])
    attrs.append(li["votes"]["cool"])
    attrs.append(li["votes"]["useful"])
    
    attributes.writelines([", ".join([str(a) for a in attrs])])
  except BaseException as e:
    #print e
    failures = failures + 1
    continue
print count, "successes", failures, "failures"
