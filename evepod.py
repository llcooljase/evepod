import os
from eve import Eve


app = Eve()

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
    app.run(host=host, port=port)
