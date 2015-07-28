#!/usr/bin/env python

##############################################
#
#  AAAI Twitterbot
#  Written for the AAAI-15 Scavenger Hunt
#
#  By Timothy Ferrell
#  December 2014
#
##############################################


from twython import Twython
from textwrap import wrap
import sys
import time

#function for returning an incorrect answer
def incorrect_answer(keyword, solution_attempt):
	return "I'm sorry, your response '" + solution_attempt + "' for the keyword '"+keyword+"' was incorrect. Please try again."

#function for returning a correct answer
def correct_answer(next_keyword, next_clue):
	return  "Congratulations, you have correctly found the solution! The next keyword is '"+next_keyword+"' and the next clue is '"+next_clue+"'. Good luck!"

#function for sending dm with character restrictions
def send_dm(sender_id,send_text):
	print "Sending dm: " + send_text
	split_text = wrap(send_text,140)
	for text_pc in split_text:
		twitter.send_direct_message(user_id=sender_id,text=text_pc)
	return
#function for finishing hunt
def solved_hunt():
	return "Congratulations, you have finished the AAAI-15 Scavenger Hunt! Random winners will be selected to win prizes at the end of each day. You will be informed if you have won!"

#necessary definitions for authenticating
#Should keep these private
app_key = "XXX"
app_secret = "XXX"
oauth_token = "XXX"
oauth_secret = "XXX"
twitter = Twython (app_key,app_secret,oauth_token,oauth_secret)

#Clues dictionaries for each day
tuesday_clues=['Paper ID of the paper whose first word of its title is the following anagram: "Cafes"','Paper ID of the paper whose first word of its title is a 10-letter word answer to the following clue: "Elucidating; Clarifying"','Paper ID of the paper whose first word of its title is the following anagram: "Maths First"','Paper ID of the paper whose first word of its title is a 5-letter word answer to the following clue: "Begone!"','Paper ID of the paper whose first word of its title is a 7-letter word answer to the following clue: "AAAI, for example"']
tuesday_answers=['1884','21','450','2251','2576']
tuesday_keywords=['tue1','tue2','tue3','tue4','tue5']

wednesday_clues=['Paper ID of the paper whose first word of its title is the following anagram: "Drawer"','Paper ID of the paper whose first word of its title is a 10-letter word answer to the following clue: "Seeing; Sensing"',' Paper ID of the paper whose first word of its title is the following anagram: "Messy Vial"','Paper ID of the paper whose third word of its title is an 11-letter word answer to the following clue: "Wyoming\'s Shape"','Paper ID of the paper whose first two words of its title is the following anagram: "Opting Virtually"']
wednesday_answers=['1568','205','1301','2580','20']
wednesday_keywords=['wed1','wed2','wed3','wed4','wed5']

thursday_clues=['Paper ID of the paper whose last word of its title is a 7-letter word answer to the following clue: "Ebay sales"','Paper ID of the paper whose first word of its title is the following anagram: "Occurred Words"','Paper ID of the paper whose first word of its title is a 10-letter word answer to the following clue: "Gathering Tightly"','Paper ID of the paper whose last word of its title is a 6-letter word answer to the following clue: "A, B, or C, for example"','Paper ID of the paper whose first three word of its title is the following anagram: "Morning Hostel Obligations"']
thursday_answers=['2071','190','2013','109','2039']
thursday_keywords=['thurs1','thurs2','thurs3','thurs4','thurs5']

#get day of the week
day_of_week = time.strftime("%A")
print day_of_week
if day_of_week=="Monday" or day_of_week=="Tuesday":
	clues = tuesday_clues
	answers = tuesday_answers
	keywords = tuesday_keywords
elif day_of_week=="Wednesday":
	clues = wednesday_clues
	answers = wednesday_answers
	keywords = wednesday_keywords
elif day_of_week=="Thursday":
	clues = thursday_clues
	answers = thursday_answers
	keywords= thursday_keywords
else:
	print "No clues for this day"
	sys.exit()
			

#list of keywords to prove you got to the correct point
while(1):
	day_of_week = time.strftime("%A")
	print day_of_week
	if day_of_week=="Monday" or day_of_week=="Tuesday":
		clues = tuesday_clues
		answers = tuesday_answers
		keywords = tuesday_keywords
	elif day_of_week=="Wednesday":
		clues = wednesday_clues
		answers = wednesday_answers
		keywords = wednesday_keywords
	elif day_of_week=="Thursday":
		clues = thursday_clues
		answers = thursday_answers
		keywords= thursday_keywords
	else:
		print "No clues for this day"
		sys.exit()
			
	#check all followers, follow back any new ones
	followers = twitter.get_followers_list(screen_name="AAAIConference",count="200");
	for follower in followers['users']:
		follower_sn = follower['screen_name']
		if((not(follower['following'])) and (not(follower['follow_request_sent'] or follower['protected']))):
			print "Requesting to follow " + follower_sn
			twitter.create_friendship(screen_name=follower_sn);	
	
	#sleep 2 minutes between grabbing messages
	time.sleep(90)
	#now grab all new messages
	dms = twitter.get_direct_messages(count="100")
	solved = 0
	for dm in dms:
		#parse retrieved message
		direct_message_id = dm['id']
		sender_id = dm['sender']['id']
		sender_name = dm['sender_screen_name']
		direct_message = dm['text'].lower()
		
		#ensure user is currently following, otherwise break...	
		following = False
		
		for follower in followers['users']:
			if follower['id']==sender_id:
				following=True
				break
		#if could not find id in followers, don't bother trying to send a dm
		if (not(following)):
			break
			
		#make sure time frame is right
		hour = int(time.strftime("%H"))
		print hour
		if (hour < 4 or hour > 19):
			print "Not a valid time"	
			send_text = "Sorry, the Scavenger Hunt is not open right now. Please try again between 6am and 9pm."
			send_dm(sender_id,send_text)
			twitter.destroy_direct_message(id=direct_message_id);
			break
		
		print "Direct message received from " + sender_name + ": " + direct_message
		#initial getting started message
		if direct_message == "begin":
			next_clue = clues[0]
			next_keyword = keywords[0]
			send_text = "Congratulations on starting the AAAI-15 Scavenger Hunt! There will be a sequence of five keywords and clues. Your first keyword is '"+next_keyword+"' and your first clue is '"+next_clue+"'."
		
		else:
			#now parse for key word
			split_message = direct_message.split(None,1)
			keyword = split_message[0].lower()
			if len(split_message) > 1:
				solution_attempt = split_message[1].lower()
			else:
				solution_attempt = "invalid"
			#now check answer against keyword
			print "Attempted solution for " + keyword + ": " + solution_attempt
			if keyword == keywords[0]:
				next_clue = clues[1]
				next_keyword = keywords[1]
				if solution_attempt == answers[0]:
					send_text = correct_answer(next_keyword,next_clue)
				else:
					send_text = incorrect_answer(keyword,solution_attempt)
			elif keyword == keywords[1]:
				next_clue = clues[2]
				next_keyword = keywords[2]
				if solution_attempt == answers[1]:
					send_text = correct_answer(next_keyword,next_clue)
				else:
					send_text = incorrect_answer(keyword,solution_attempt)
		
			elif keyword == keywords[2]:
				next_clue = clues[3]
				next_keyword = keywords[3]
				if solution_attempt == answers[2]:
					send_text = correct_answer(next_keyword,next_clue)
				else:
					send_text = incorrect_answer(keyword,solution_attempt)
			
			elif keyword == keywords[3]:
				next_clue = clues[4]
				next_keyword = keywords[4]
				if solution_attempt == answers[3]:
					send_text = correct_answer(next_keyword,next_clue)
				else:
					send_text = incorrect_answer(keyword,solution_attempt)
		
			elif keyword == keywords[4]:
				if solution_attempt == answers[4]:
					solved = 1
					send_text = solved_hunt()
				else:
					send_text = incorrect_answer(keyword,solution_attempt)
		
		 #and so on as scavenger hunt continues
			else:
				send_text = "Sorry, the keyword '"+keyword+"' did not match any designated keyword."

		#destroy direct message, and send appropriate response
		print send_text
		send_dm(sender_id,send_text)
		twitter.destroy_direct_message(id=direct_message_id);
		
		#Write the name of winner to a text file log
		if(solved):
			filename = "winners"+day_of_week+".txt" 
			writetext = sender_name+"\n"
			with open(filename,"a") as myfile:
				myfile.write(writetext)
			#optional choice to have account tweet out updates (currently commented out)
			#twitter.update_status(status="Congratulations, @"+ sender_name+" has finished the "+day_of_week+" AAAI-15 Scavenger Hunt!")
			solved=0
	
	