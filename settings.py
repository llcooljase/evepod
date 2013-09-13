
#------------------------------------------------------------------------------
#
# GLOBAL SETTINGS
#
# Defines: gateway_schema, dataset_schema, pod_schema, user_schema,
#
#------------------------------------------------------------------------------
import os
# FIGURE OUT WHERE WE ARE RUNNING... ON HEROKU, OR LOCALLY?

if os.environ.get('PORT'):
	# We're hosted on Heroku! Use the MongoHQ Sandbox as our backend
	MONGO_HOST = 'paulo.mongohq.com'
	MONGO_PORT = 10086
	MONGO_USERNAME = 'tushivjek'
	MONGO_PASSWORD = 'cych2re7shu5quim'
	MONGO_DBNAME = 'evepod'	
	SERVER_NAME = ''
else:
	# We're running on a local machine. Let's just use the local mongod instance.
	# Note that MONGO_HOST and MONGO_PORT could be left out, because they are 
	# pointing to defaults in a barebone mongod instance!
	MONGO_HOST = 'paulo.mongohq.com'
	MONGO_PORT = 10086
	MONGO_USERNAME = 'tushivjek'
	MONGO_PASSWORD = 'cych2re7shu5quim'
	MONGO_DBNAME = 'evepod'	
	
	# Still need to set the API entry point:

SERVER_NAME = '0.0.0.0:5000'

# Mongo HQ url:
# mongodb://tushivjek:cych2re7shu5quim@paulo.mongohq.com:10046/poddleTest

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH) and deletes of individual items
# (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

# Set the public methods for the read-only API. 
# Only authorized users can write, edit and delete
PUBLIC_METHODS = ['GET'] 
PUBLIC_ITEM_METHODS = ['GET']

#------------------------------------------------------------------------------
#
# RESOURCE SCHEMAS
#
# Defines: 	gateway_schema, dataset_schema, pod_schema, user_schema,
#			allsensorinfo, allpoddata, allfarmerdata, farmers 
#
#------------------------------------------------------------------------------
gateway_schema = {
	# Schema definition, based on Cerberus grammar. Check the Cerberus project
	# (https://github.com/nicolaiarocci/cerberus) for details.
	'urlname' : {
		'type': 'string',
		'minlength': 1,
		'maxlength': 10,
		'required': True,
		'unique': True,
	},
	'pods' : {'type':'list','items':[{'type':'string'}]},
}

dataset_schema = {
	# Schema definition, based on Cerberus grammar. Check the Cerberus project
	# (https://github.com/nicolaiarocci/cerberus) for details.
	'urlname' : {
		'type': 'string',
		'minlength': 1,
		'maxlength': 10,
		'required': True,
		'unique': True,
	},
	'users': {'type':'list','items':[{'type':'string'}]},
	'data': {
		'type':'list','schema':{
			'timestamp':{'type':'datetime','required':True},
			'value':{'type':'float','required':True},
			'pod':{'type':'string','required':True},
			'sensor':{'type':'string','required':True},
		},
	},
}

user_schema = {
	# Schema definition, based on Cerberus grammar. Check the Cerberus project
	# (https://github.com/nicolaiarocci/cerberus) for details.
	'username' : {
		'type' : 'string',
		'required' : True,
		'unique' : True,
	},
	'password' : { # Plaintext. We're awful
		'type':'string',
		'required': True, 	
	},
}

pod_schema = { 
	# Schema definition, based on Cerberus grammar. Check the Cerberus project
	# (https://github.com/nicolaiarocci/cerberus) for details.
	'urlname' : {
		'type': 'string',
		'minlength': 1,
		'maxlength': 10,
		'required': True,
	},
	'id' : {
		'type': 'string',
		'minlength': 7,
		'maxlength': 7,
		'required': True,
		'unique': True,
	},
	'dataset' : {
		'type':'string',
	},
	'gateway' : {
		'type':'string',
	},
	'serialnumber':{
		'type':'string',
	},
}

sensor_schema = { 
	# Schema definition, based on Cerberus grammar. Check the Cerberus project
	# (https://github.com/nicolaiarocci/cerberus) for details.
	'urlname' : {
		'type': 'string',
		'minlength': 1,
		'maxlength': 10,
		'required': True,
	},
	'id' : {
		'type': 'string',
		'minlength': 8,
		'maxlength': 8,
		'required': True,
		'unique': True,
	},
}

#------------------------------------------------------------------------------
#
# RESOURCE DEFINITIONS
#
# Defines: pods,
#
#------------------------------------------------------------------------------
pods = {
	# 'title' tag used in item links. Defaults to the resource title minus
	# the final, plural 's' (works fine in most cases but not for 'people')
	# 'item_title': 'p',
	# by default the standard item entry point is defined as
	# '/<item_title>/<ObjectId>/'. We leave it untouched, and we also enable an
	# additional read-only entry point. This way consumers can also perform
	# GET requests at '/<item_title>/<urlname>/'.
	'additional_lookup': {
		'url': '[\w]+',
		'field': 'urlname'
	},
	# We choose to override global cache-control directives for this resource.
	'cache_control': 'max-age=10,must-revalidate',
	'cache_expires': 10,
	
	# most global settings can be overridden at resource level
	'resource_methods': ['GET', 'POST', 'DELETE'],
	'schema': pod_schema
}

datasets = {
	# 'title' tag used in item links. Defaults to the resource title minus
	# the final, plural 's' (works fine in most cases but not for 'people')
	# 'item_title': 'f',
	# by default the standard item entry point is defined as
	# '/<item_title>/<ObjectId>/'. We leave it untouched, and we also enable an
	# additional read-only entry point. This way consumers can also perform
	# GET requests at '/<item_title>/<urlname>/'.
	'additional_lookup': {
		'url': '[\w]+',
		'field': 'urlname'
	},
	# We choose to override global cache-control directives for this resource.
	'cache_control': 'max-age=10,must-revalidate',
	'cache_expires': 10,
	
	# most global settings can be overridden at resource level
	'resource_methods': ['GET', 'POST', 'DELETE'],
	'schema': dataset_schema
}

users = {
	# 'title' tag used in item links. Defaults to the resource title minus
	# the final, plural 's' (works fine in most cases but not for 'people')
	# 'item_title': 'f',
	# by default the standard item entry point is defined as
	# '/<item_title>/<ObjectId>/'. We leave it untouched, and we also enable an
	# additional read-only entry point. This way consumers can also perform
	# GET requests at '/<item_title>/<lastname>/'.
	'additional_lookup': {
		'url': '[\w]+',
		'field': 'username'
	},
	# We choose to override global cache-control directives for this resource.
	'cache_control': '',
	'cache_expires': 0,
	
	# Only allow superusers and admin
	# 'allowed_roles': ['superuser', 'admin'],
	
	# Allow 'token' to be returned with POST responses (MUST USE SSL!)
	# 'extra_response_fields': ['token'],
	# most global settings can be overridden at resource level
	'resource_methods': ['GET', 'POST', 'DELETE'],	
	'schema': user_schema
}

gateways = {
	# 'title' tag used in item links. Defaults to the resource title minus
	# the final, plural 's' (works fine in most cases but not for 'people')
	# 'item_title': 'f',
	# by default the standard item entry point is defined as
	# '/<item_title>/<ObjectId>/'. We leave it untouched, and we also enable an
	# additional read-only entry point. This way consumers can also perform
	# GET requests at '/<item_title>/<lastname>/'.
	'additional_lookup': {
		'url': '[\w]+',
		'field': 'urlname'
	},
	# We choose to override global cache-control directives for this resource.
	'cache_control': 'max-age=10,must-revalidate',
	'cache_expires': 10,
	
	# most global settings can be overridden at resource level
	'resource_methods': ['GET', 'POST', 'DELETE'],
	'schema': gateway_schema
}

sensors = {
	# 'title' tag used in item links. Defaults to the resource title minus
	# the final, plural 's' (works fine in most cases but not for 'people')
	# 'item_title': 'f',
	# by default the standard item entry point is defined as
	# '/<item_title>/<ObjectId>/'. We leave it untouched, and we also enable an
	# additional read-only entry point. This way consumers can also perform
	# GET requests at '/<item_title>/<lastname>/'.
	'additional_lookup': {
		'url': '[\w]+',
		'field': 'urlname'
	},
	# We choose to override global cache-control directives for this resource.
	'cache_control': 'max-age=10,must-revalidate',
	'cache_expires': 10,
	
	# most global settings can be overridden at resource level
	'resource_methods': ['GET', 'POST', 'DELETE'],
	'schema': sensor_schema
}
#------------------------------------------------------------------------------
#
# DOMAINS
#
# Uses: pods, users, farmers, gateways, sensors, datasets
#
#------------------------------------------------------------------------------

DOMAIN = {
        'gateways':gateways,
		'pods': pods,
		'users':users,
		'datasets':datasets,
		'sensors':sensors,
}

