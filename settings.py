
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
	# Set API entry point (for heroku):
	MONGO_HOST = 'paulo.mongohq.com'
	MONGO_PORT = 10086
	MONGO_USERNAME = 'tushivjek'
	MONGO_PASSWORD = 'cych2re7shu5quim'
	MONGO_DBNAME = 'evepod'	
	SERVER_NAME = 'app.pulsepod.io'
else:
	# Run locally, because my internet at home stinks
	MONGO_HOST = 'localhost'
	MONGO_PORT = 27017
	MONGO_DBNAME = 'evepod'
	SERVER_NAME = '0.0.0.0:5000'


# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH) and deletes of individual items
# (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

# Set the public methods for the read-only API. 
# Only authorized users can write, edit and delete
# PUBLIC_METHODS = ['GET'] 
# PUBLIC_ITEM_METHODS = ['GET']

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
	'urlid' : {
		'type': 'string',
		'minlength': 1,
		'maxlength': 10,
		'required': True,
		'unique': True,
	},
	'pods' : {'type':'list','items':[{
											'type':'objectid',
											'data_relation': {
												'collection':'pods',
												'field':'_id',
												'embeddable':True
												}
											},
											]
				},
}

dataset_schema = {
	# Schema definition, based on Cerberus grammar. Check the Cerberus project
	# (https://github.com/nicolaiarocci/cerberus) for details.
	'urlid' : { # Dataset url name
		'type': 'string',
		'minlength': 1,
		'maxlength': 10,
		'required': True,
		'unique': True,
	},
	'users': {'type':'list','items':[{'type':'string'}]}, # Should be embeddable
	'pods': {'type':'list','items':[{'type':'string'}]},  # Should be embeddable
}

data_schema = {
	# Schema definition, based on Cerberus grammar. Check the Cerberus project
	# (https://github.com/nicolaiarocci/cerberus) for details.
	# Note: using short variable names to save space in MongoDB.
	't':{'type':'datetime','required':True},   # datetime
	'v':{'type':'float','required':True},      # value
	'p':{'type':'string','required':True},     # pod
	's':{'type':'string','required':True},     # sensor
}

user_schema = {
	# Schema definition, based on Cerberus grammar. Check the Cerberus project
	# (https://github.com/nicolaiarocci/cerberus) for details.
	'u' : { # username
		'type' : 'string',
		'required' : True,
		'unique' : True,
	},
	'p' : { # Plaintext. We're awful
		'type':'string',
		'required': True, 	
	},
}

pod_schema = { 
	# Schema definition, based on Cerberus grammar. Check the Cerberus project
	# (https://github.com/nicolaiarocci/cerberus) for details.
	'urlid' : { # Pod URL name
		'type': 'string',
		'minlength': 1,
		'maxlength': 10,
		'required': True,
	},
	'id' : { # Pod ID
		'type': 'string',
		'minlength': 7,
		'maxlength': 7,
		'required': True,
		'unique': True,
	},
	'ds' : { # dataset (should be embeddable?)
		'type':'string',
	},
	'g' : { # Gateway (should be embeddable?)
		'type':'string',
	},
	'sn':{ # Serial Number (does not need to be unique, since one SN can be many pods!
		'type':'string',
	},
}

sensor_schema = { 
	# Schema definition, based on Cerberus grammar. Check the Cerberus project
	# (https://github.com/nicolaiarocci/cerberus) for details.
	'urlid' : {
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
	'nbytes' : {
		'type':'integer',
		'required':True
	}
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
		'field': 'urlid'
	},
	# We choose to override global cache-control directives for this resource.
	'cache_control': 'max-age=10,must-revalidate',
	'cache_expires': 10,
	# most global settings can be overridden at resource level
	'resource_methods': ['GET', 'POST', 'DELETE'],
	'item_methods': ['GET','PATCH'],
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
		'field': 'urlid'
	},
	# We choose to override global cache-control directives for this resource.
	'cache_control': 'max-age=10,must-revalidate',
	'cache_expires': 10,
	
	# most global settings can be overridden at resource level
	'resource_methods': ['GET', 'POST', 'DELETE'],
	'schema': dataset_schema
}

data = {

	# most global settings can be overridden at resource level
	'resource_methods': ['GET', 'POST', 'DELETE'],
	'schema': data_schema	
}

users = {
	# 'title' tag used in item links. Defaults to the resource title minus
	# the final, plural 's' (works fine in most cases but not for 'people')
	# 'item_title': 'f',
	# by default the standard item entry point is defined as
	# '/<item_title>/<ObjectId>/'. We leave it untouched, and we also enable an
	# additional read-only entry point. This way consumers can also perform
	# GET requests at '/<item_title>/<username>/'.
	'additional_lookup': {
		'url': '[\w]+',
		'field': 'u'
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
		'field': 'urlid'
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
		'field': 'urlid'
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
		'data':data,
}

