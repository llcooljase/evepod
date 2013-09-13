import os
from eve import Eve


app = Eve(settings='settings.py')

# Start the application
#if __name__ == '__main__':
app.run(debug=False)
