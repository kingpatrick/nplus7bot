import os
import json
import boto3
import nltk
from nltk.corpus import wordnet as wn


os.environ['AWS_SHARED_CREDENTIALS_FILE'] = "./.aws/credentials"

session = boto3.Session()

table = boto3.resource('dynamodb', region_name='<put region name here>').Table(<'put_table_name_here')

words = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}
word_list = sorted(words)
word_id = 0
with table.batch_writer() as batch:
	for word in word_list:
		print(word)
		batch.put_item(
			Item = {
					'word':word,
					'wordid':word_id					
			}
		)
		word_id += 1
		