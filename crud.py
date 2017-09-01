from tinydb import TinyDB, Query, where
import config
import re
import PyrebaseConfig as pbc
import json
#db.insert({'type': 'strawberry', 'count': 39})
#db.insert({'type': 'raspberry', 'count': 21})

def init():
	global transactionDB, balanceDB, transactionData, balanceSizeRef
	transactionData = {}
	transactionDB = TinyDB('transaction.json')
	#transactionDB.all()
	balanceDB = TinyDB('balance.json')
	for columnName in config.TRANSACTION_COLUMNS:
		transactionData.update({columnName:''})
	# print(transactionData)
	#pbc.init()# Initial Pyrebase for Firebase Realtime Database ..............
	pbc.initSDK()
	balanceSizeRef = pbc.db1.reference(str(config.BALANCE_SIZE_NODE_NAME))
	# print('BALANCE_NODE_NAME ===== '+str(config.BALANCE_NODE_NAME))

#def commitDataToFireBase():
#	pbc.db

#def setDataToFirbase(ref,nodeName):
#	ref.set()

def getMaxRecordNumber(nodeName):
	ref = pbc.db1.reference(nodeName)
	maxRecord = ref.get()
	#print('Max ------------------------ '+str(maxRecord))
	return maxRecord

def updateMaxRecordSize(nodeName, size):
	# print('Set ', nodeName, ' to ', size, '\n')
	maxRecordRef = pbc.db1.reference(nodeName)
	maxRecordRef.set(size)

def insertTransactionFromFile(row, toFireBase, ref):
	global transactionDB, balanceDB, transactionData
	i=0
	for columnName in config.TRANSACTION_COLUMNS:
		data = str(row[i]).replace("\r\n","")
		if('"' in data):
			data = data.replace('"', ' ')
		transactionData.update({columnName:data})
		i += 1
	if(toFireBase):
		ref.set(transactionData)
		updateBalance(transactionData=transactionData,toFireBase=True)
	else:
		transactionDB.insert(transactionData)
		updateBalance(transactionData=transactionData,toFireBase=False)

def updateBalance(transactionData,toFireBase):
	global balanceSizeRef
	if(toFireBase):
		balanceSize = getMaxRecordNumber(config.BALANCE_SIZE_NODE_NAME)
		if(balanceSize is not None):
			updateBalanceRef = pbc.db1.reference(str(config.BALANCE_NODE_NAME)+str(int(balanceSize)+1))
		#	updateMaxRecordSize(nodeName=config.BALANCE_SIZE_NODE_NAME, size=str(int(balanceSize)+1))
		else:
			updateBalanceRef = pbc.db1.reference(str(config.BALANCE_NODE_NAME)+str(1))
		#	updateMaxRecordSize(nodeName=config.BALANCE_SIZE_NODE_NAME, size=str(1))
		updateBalanceToFireBase(transactionData=transactionData, updateRef=updateBalanceRef)
	else:
		balanceRow = balanceDB.search(where('ITEM') == transactionData['ITEM'])
		#print("Update Balance ---------------------------------------------------")
		#print(balanceRow)
		if(len(balanceRow) == 0):
			# print("No Item Balance ---------------------------------------------------")
			#print(balanceRow)
			#print(transactionData['ITEM'])
			#print(transactionData)
			if(int(transactionData['ADD']) > 0):
				newBalance = {'ITEM':transactionData['ITEM'],'BALANCE':transactionData['ADD']}
				balanceDB.insert(newBalance)
		else:
			# print("Item of Transaction alrready have balance --------------------------")
			#print(balanceRow)
			transactionQty = int(transactionData['ADD'])
			if(transactionQty > 0):#ADD TRANSACTION
				#print(balanceRow[0]['BALANCE'])
				transactionQty += int(balanceRow[0]['BALANCE'])
				balanceDB.update({'BALANCE':transactionQty}, where('ITEM') == transactionData['ITEM'])
			else:#USE TRANSACTION
				transactionQty = int(transactionData['USE'])
				transactionQty = int(balanceRow[0]['BALANCE']) - transactionQty
				balanceDB.update({'BALANCE':transactionQty}, where('ITEM') == transactionData['ITEM'])

def updateBalanceToFireBase(transactionData, updateRef):

	balanceSize = getMaxRecordNumber(config.BALANCE_SIZE_NODE_NAME)
	#if(balanceRows is not None):
	#	for key, val in balanceRows.items():
	#		print('balance key :'+str(key)+'|'+'balance value :'+str(val))

	#print(str(balanceSize))
	if(balanceSize is None): # Balance is empty
		#print('No Balance Row --------------------------------')
		addQty = int(transactionData['ADD'])
		#print('Add QTY = '+str(addQty))
		if(addQty > 0):
			#print('Setting new balance ------------------------')
			newBalance = {'ITEM':transactionData['ITEM'],'BALANCE':addQty}
			updateRef.set(newBalance) # Add new balance record
			updateMaxRecordSize(nodeName=config.BALANCE_SIZE_NODE_NAME, size=str(1)) # Increase size of balance
	else:                    # Balance is not empty
		allBalanceRef = pbc.db1.reference(str(config.BALANCE_NODE_NAME))
		balanceRows = allBalanceRef.get()
		#print('Have Balance Row ----------------------------')
		addQty = int(transactionData['ADD'])
		useQty = int(transactionData['USE'])
		# print('Add QTY = ', addQty, '\n')
		# print('Use QTY = ', useQty, '\n')
		isNotMatch = True
		for key, val in balanceRows.items():
			#print('transactionData[ITEM] == '+str(transactionData['ITEM']))
			#print('key == '+str(key))
			#print('val == '+str(val))
			if(key != 'size'):
				if(transactionData['ITEM'] == val['ITEM']): # Already have item in balance
					balance = val['BALANCE']
					newBalance = 0
					if(addQty > 0):
						newBalance = balance+addQty
					if(useQty > 0):
						newBalance = balance-useQty
						# print('Substract balance !!!')
						# print(balance, ' - ', useQty, ' = ', newBalance)
					updateRef = pbc.db1.reference(str(config.BALANCE_NODE_NAME)+str(key))
					updateRef.set( {'ITEM':transactionData['ITEM'],'BALANCE':newBalance} )
					isNotMatch = False
		if(isNotMatch): # No matched item
			newBalance = 0
			if(addQty > 0):
				newBalance = newBalance+addQty
			if(useQty > 0):
				newBalance = newBalance-useQty
			updateRef.set({'ITEM':transactionData['ITEM'],'BALANCE':newBalance})
			updateMaxRecordSize(nodeName=config.BALANCE_SIZE_NODE_NAME, size=str(int(balanceSize)+1))

				

def getAllBalance():
	allBalance = balanceDB.all()
	return allBalance

def getAllTransaction():
	allTransaction = transactionDB.all()
	return allTransaction

def addNewItemFromTransation(transactionData):
	print("Add New Item from Transaction -----------------------------------------")

def add():
	global transactionDB, balanceDB
	# print("Do add item ...")
	stock = Query()
	#db.search(stock.name == name)
	#db.insert({name:qty})

def delete():
	print("Do delete item ...")