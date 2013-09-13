# -*- coding: utf-8 -*-

"""
    evepod-demo-client
    ~~~~~~~~~~~~~~~

    Simple and quickly hacked togheter, this script is used to reset the
    eve-demo API to its initial state. It will use standard API calls to:

        1) delete all items in the 'people' and 'works' collections
        2) post multiple items in both collection

    I guess it can also serve as a basic example of how to programmatically
    manage a remot e API using the phenomenal Requests library by Kenneth Reitz
    (a very basic 'get' function is included even if not used).

    :copyright: (c) 2012 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""
import requests
import json
import random

#ENTRY_POINT = 'http://eve-demo.herokuapp.com'
ENTRY_POINT = 'http://0.0.0.0:5000'

DATASET = 'zambia2013'

def post_pods():
    pods = [
		{ 	
			'urlname' : 'zari01',
		  	'id' : 'p000101',
		   	'dataset' : DATASET,
			'gateway' : 'g0001',
			'serialnumber': '0001'
		 },
		{ 
			'urlname' : 'zari02',
			'id' : 'p000201',
			'dataset' : DATASET,
			'gateway' : 'g0001',
			'serialnumber': '0002'
		},
		{ 
			'urlname' : 'zari03',
			'id' : 'p000301',
			'dataset' : DATASET,
			'gateway' : 'g0001',
			'serialnumber': '0003'
		},
    ] #END OF POD LIST

    payload = {}
    for pod in pods:
        payload[pod['id']] = json.dumps(pod)

    r = perform_post('pods', payload)
    print "'pods' posted"
    print r.status_code
    print r.json

    valids = []
    if r.status_code == 200:
        response = r.json()
        print response
        for pod in payload:
            result = response[pod]
            if result['status'] == "OK":
                valids.append(result['_id'])

    return valids


def post_users(ids):
	users = []
	users.append({
		'username': 'kkc9q',
		'password' : 'badpassword'
	})
	payload = {}
	for i in range(len(users)):
		payload['users' + str(i + 1)] = json.dumps(users[i])
	r = perform_post('users', payload)
	print "'users' posted"
	print r.status_code
	print r.json

def post_gateways():
	gateway = {
		'urlname':'g0001',
		'pods':['p000201','p000101'],
	}
	payload = {}
	payload[gateway['urlname']] = json.dumps(gateway)
	r = perform_post('gateways', payload)
	print "'gateways' posted"
	print r.status_code
	print r.json
	

def post_datasets():
	dataset = {
		'urlname' : DATASET,
		'users' : [ 'kkc9q' ]
	}
	payload = {}
	payload[dataset['urlname']] = json.dumps(dataset)
	r = perform_post('datasets', payload)
	print "'datasets' posted"
	print r.status_code
	print r.json

	
	
def perform_post(resource, data):
    return requests.post(endpoint(resource), data)


def delete():
	r = perform_delete('pods')
	print "'pods' deleted"
	print r.status_code
	r = perform_delete('users')
	print "'users' deleted"
	print r.status_code
	r = perform_delete('datasets')
	print "'datasets' deleted"
	print r.status_code
	r = perform_delete('gateways')
	print "'gateways' deleted"
	print r.status_code
	


def perform_delete(resource):
    return requests.delete(endpoint(resource))


def endpoint(resource):
    return '%s/%s/' % (ENTRY_POINT, resource)


def get():
    r = requests.get(ENTRY_POINT)
    print r.json

if __name__ == '__main__':
	delete()
	ids = post_pods()
	post_users(ids)
	post_datasets()
	post_gateways()
	get()
	