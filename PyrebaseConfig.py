
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db as db1

def initSDK():
	# Fetch the service account key JSON file contents
	cred = credentials.Certificate('stock-57ec5-firebase-adminsdk-5ej7c-8727cbbc28.json')

	# Initialize the app with a service account, granting admin privileges
	firebase_admin.initialize_app(cred, 
		{	'databaseURL': 'https://stock-57ec5.firebaseio.com/'
		})

	# As an admin, the app has access to read and write all data, regradless of Security Rules
	#ref = db.reference('Transaction/')