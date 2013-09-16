import os
import calendar, datetime
import re
from eve import Eve

app = Eve()

def before_insert_data(documents):
	print "A POST to data was just performed!"
	for d in documents:
		print "Posting " + d["s"] + " data from " + d["p"] + " to the database"
		
def pods_request_callback(request, payload):
	print "A GET on pods was just performed!"

# Heroku defines a $PORT environment variable that we use to determine
# if we're running locally or not.
port = os.environ.get('PORT')
if port:
    host = '0.0.0.0'
    port = int(port)
else:
    host = '127.0.0.1'
    port = 5000

# Start the application
if __name__ == '__main__':
	app.on_insert_data += before_insert_data
	app.on_GET_pods += pods_request_callback
	app.run(host=host, port=port)
