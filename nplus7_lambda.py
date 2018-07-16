import twitter
import json
import os
import boto3
from boto3.dynamodb.conditions import Key, Attr
import random
from string import punctuation

os.environ['AWS_SHARED_CREDENTIALS_FILE'] = ".aws/credentials"

def get_word_id(search_word):
	table = boto3.resource('dynamodb', region_name='<put region name here>').Table(<'put_table_name_here')
	search_word = search_word.lower()
	response = table.query(
		KeyConditionExpression=Key('word').eq(search_word),
		ProjectionExpression="word, wordid"
	)
	last_wordid = 0
	for i in response['Items']:
		last_wordid = (i['wordid'])
	if last_wordid == 0:
		new_word = search_word
		if search_word[len(search_word) - 1] == 's':
			new_word = search_word[:(len(search_word)-1)]
			print("Second Try: ", new_word)
			response = table.query(
				KeyConditionExpression=Key('word').eq(new_word),
				ProjectionExpression="word, wordid"
			)
			for i in response['Items']:
				last_wordid = i['wordid']
	return last_wordid

def get_new_word(search_wordid):
	table = boto3.resource('dynamodb', region_name='<put region name here>').Table(<'put_table_name_here')
	word = ''
	search_word_id = search_wordid
	while(word == ''): 
		response = table.query(
			KeyConditionExpression=Key('wordid').eq(search_word_id)
		)
		for i in response['Items']:
			if '_' not in i['word']:
				word = i['word']
			else:
				continue
		search_word_id += 1
	return word
		
		
def get_creds():
	with open('credentials.json') as f:
		credentials = json.loads(f.read())
		api = twitter.Api(**credentials)
		return api
	
def get_timeline(user_name, api):	
	t = api.GetUserTimeline(screen_name=user_name, count=100)
	tweets = [i.AsDict() for i in t]
	tweet = tweets[0]
	return tweet['full_text']
	
def search_tweets(search_item, api):
	search = api.GetSearch(
		term=search_item, lang="en")

def send_tweet(api, new_tweet):
	contents = new_tweet
	status = api.PostUpdate(contents)


def build_tweet(api):
	
	#GET USER TIMELINE
	user_name = 'CNN'
	last_tweet = get_timeline(user_name, api)
	print("\nOld Tweet:\n\n", last_tweet)
	words = last_tweet.split()
	new_sentence = ''
	for word in words:
		
		if 'http' in word:
			continue
		sword = word.lower()
		sword = ''.join(c for c in word if c not in punctuation)
		if sword == '':
			continue
		if word[0].isupper():
			new_sentence += word
		elif word[0] == '@' or word[0] == '#':
			new_sentence += word
		elif sword not in ['And','and','On','on','Is','is','The','the','Here','here','Have','have','Will','will','Won\'t','won\'t','Why','why','How','how','What','what','This','this','These','these','Are','are','As','as','At','at','but','do','did','to','the','The','in','for','by','want','of','I','i','a','an','A','An','Who','who','Man','Woman','man','woman']:
				
			old_wordid = get_word_id(sword)
			
			if old_wordid != 0:
				
		
				random_n = random.randint(1,8)
				new_word = get_new_word(old_wordid + random_n)
				print("New Word After: ", new_word)

				
				if sword[0].isupper():
					new_sentence += new_word.capitalize()
				else:
					new_sentence += new_word
				
			
			else:
				if word[0].isupper():
					new_sentence += sword.capitalize()
				else:
					new_sentence += sword
		
		else:
			new_sentence += word
		new_sentence += ' '
	new_sentence = new_sentence.replace('_',' ')
	return new_sentence

def lambda_handler(_event_json, _context):
	api = get_creds()
	new_tweet = build_tweet(api)
	send_tweet(api, new_tweet)