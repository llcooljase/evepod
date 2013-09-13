# Unused schema.
# These schema define tables that will always be read-only from the API. 
# All writes to these tables will execute via a separate 
allfarmerdata_schema = {
	'farmerid':{'type':'string','required':True,'unique':True},
	'data':{
		'type':'list', 'schema': {
			'type':'dict','schema':{
				'value':{'type':'float'},
				'timestamp':{'type','datetime'},
				'tod048':{'type','integer'},
				'tod192':{'type','integer'},
			},
		},
	},
}

allpoddata_schema = {
	'podid':{'type':'string','required':True,'unique':True},
	'data':{
		'type':'list', 'schema': {
			'type':'dict','schema':{
				'value':{'type':'float'},
				'timestamp':{'type','datetime'},
				'tod048':{'type','integer'},
				'tod192':{'type','integer'},
			},
		},
	},
}

allsensorinfo_schema = {
	'id':{'type':'string','required':True,'unique':True},
	'nbytesvalue':{'type':'integer'},
	'urlname':{
		'type':'string',
		'maxlength':10,
		'required':True,
		'unique':True,
	},
	'vendor':{'type':'string'},
	'model':{'type':'string'},
	'type':{'type':'string'},
	'firmware':{'type':'string'},
	'y_axis_string': {'type':'string'},
	'units': {'type':'string'},				
}