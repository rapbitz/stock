import tkinter as tk
import tkinter.filedialog as filedialog
import crud
import csv
import re
import codecs
import config
import PyrebaseConfig as pbc
from tkinter import ttk
from time import sleep
from google.auth.exceptions import TransportError

global fileName, allBalance, allTransaction, balanceVariable, noteVariable, itemList, transactionSize, gui, initBalanceRows, projectVar, itemsByProject

def init():
	global initBalanceRows
	try:
		balanceLoadRef = pbc.db1.reference(str(config.BALANCE_NODE_NAME))
		initBalanceRows = balanceLoadRef.get()
	except TransportError as e:
		print('Cannot connect to Firebase. Please check your internet connection.')

def askToOpenFile():
	global fileName
	#file = filedialog.askopenfile(parent=gui,mode='rb',title='Choose a file')
	fileName = filedialog.askopenfilename(parent=gui,title='Choose a file')
	filePathVar.set(fileName)

def fileImport():
	global transactionSize, gui
	delimiter=';'
	reader = codecs.open(fileName,'r',encoding='utf-8', errors='ignore')
	transactionSize = crud.getMaxRecordNumber(config.TRANSACTION_SIZE_NODE_NAME)
	# print('Transaction Size ===== '+str(transactionSize))
	i=1;
	for line in reader:
		row = line.split(delimiter)
		#print(row)
		splitedRow = str(row[0]).split(',')
		#print("data :")
		#print(splitedRow)
		#print("\n")
		if(transactionSize is not None):
			ref = pbc.db1.reference(str(config.TRANSACTION_NODE_NAME)+str(transactionSize+i))
			j = transactionSize+i
			# print('Update transaction size inside the loop Not None case ', j, '\n')
			crud.updateMaxRecordSize(nodeName=config.TRANSACTION_SIZE_NODE_NAME,size=j)
		else:
			# print('Update transaction size inside the loop None case ', i, '\n')
			ref = pbc.db1.reference(str(config.TRANSACTION_NODE_NAME)+str(i))
			crud.updateMaxRecordSize(nodeName=config.TRANSACTION_SIZE_NODE_NAME,size=i)
		#crud.insertTransactionFromFile(row=splitedRow,toFireBase=False)
		crud.insertTransactionFromFile(row=splitedRow,toFireBase=True,ref=ref)
		i += 1
	# loadProjectList()
	# showAllBalance(gui)
	# gui.mainloop()
	# gui.update()

def setChoosenItemSBalance(value):
	# print("Choosen Item -------------")
	# print(value)
	balanceRecord = next((record for record in allBalance if record['ITEM'] == value), False)
	transactionRecord = next((record for record in allTransaction if record['ITEM'] == value), False)
	#decodedTransactionRecord = str(transactionRecord).decode('Tis-620')
	# print(balanceRecord)
	#print(transactionRecord)
	#print(balanceRecord['BALANCE'])
	#print(record['NOTE'])
	balanceVariable.set(balanceRecord['BALANCE'])
	noteVariable.set(transactionRecord['NOTE'])

def showAllBalance(gui):
	global initBalanceRows

	tree = ttk.Treeview(gui)
	tree.place(x=30, y=95)
	#tree.pack(side='left')
	tree.grid(row=7, column=1)

	scrollBar = ttk.Scrollbar(gui, orient="vertical", command=tree.yview)
	#vsb.pack(side='right', fill='y')
	scrollBar.grid(row=7, column=2, rowspan=2,  sticky=tk.N+tk.S+tk.W)

	tree.configure(yscrollcommand=scrollBar.set)

	tree["columns"] = ("1", "2")
	tree['show'] = 'headings'
	tree.column("1", width=400, anchor='c')
	tree.column("2", width=100, anchor='c')
	tree.heading("1", text="Item")
	tree.heading("2", text="Balance")
	tree.bind("<Double-1>", showDetailWindow)
	# tree.bind("<ButtonRelease-1>", showDetailWindow)
	if(initBalanceRows is not None):
		# n = int(1)
		for key, val in initBalanceRows.items():
			# print(n)
			# n += 1
			if(key != 'size'):
				# print('ITEM ============================= \n')
				# print(val['ITEM'], '\n')
				tree.insert("",'end',text="L1",values=(str(val['ITEM']),str(val['BALANCE'])))

def testBind(event):
	print("Double click !!!")

def showDetailWindow(a):
	# print("Detail ...")
	# print(gui.attributes.get('tree').focus()) # Dont work
	detailGui = tk.Tk()
	detailGui.geometry("640x640")
	detailGui.title(" R&D Stock ")
	detailGui.mainloop()
	# for item in self.tree.selection():
	# 	print(self.tree.item(item,"text"))

def showSearchBalance(itemList):
	tree = ttk.Treeview(gui)
	tree.place(x=30, y=95)
	#tree.pack(side='left')
	tree.grid(row=7, column=1)

	scrollBar = ttk.Scrollbar(gui, orient="vertical", command=tree.yview)
	#vsb.pack(side='right', fill='y')
	scrollBar.grid(row=7, column=2, rowspan=2,  sticky=tk.N+tk.S+tk.W)

	tree.configure(yscrollcommand=scrollBar.set)

	tree["columns"] = ("1", "2")
	tree['show'] = 'headings'
	tree.column("1", width=400, anchor='c')
	tree.column("2", width=100, anchor='c')
	tree.heading("1", text="Item")
	tree.heading("2", text="Balance")
	tree.bind("<Double-1>", showDetailWindow)
	# tree.bind("<<TreeviewSelect>>", showDetailWindow)
	if(itemList is not None):
		for val in itemList:
			tree.insert("",'end',text="L1",values=(str(val['ITEM']),str(val['BALANCE'])))

def searchItem():
	# showProgressBar()
	# print("Searching ...")
	keyword = searchItemVar
	balanceRows = dict({})
	if(projectVar != 'All' and 'itemsByProject' in globals()):
		# print(" Dont search all !! ")
		key = int(1)
		for value in itemsByProject:
			balanceRows.update({str(key):value})
			key += int(1)
	else:
		itemSearchRef = pbc.db1.reference(str(config.BALANCE_NODE_NAME))
		balanceRows = itemSearchRef.order_by_key().get()

	if(balanceRows is not None):
		balanceRows.pop('size', None)
		itemList = []

		for key, val in balanceRows.items():
			# print('Key = '+str(key)+' , value = '+str(val))
			itemName = val['ITEM']
			if(str(itemName).find(str(keyword.get())) != -1):
				# print('Found '+str(keyword.get())+' in '+str(itemName))
				itemList.append(val)
			# print(keyword.get() ,str(keyword.get()).find('*'))
			if(str(keyword.get()).find('*') != -1):
				keywordList = str(keyword.get()).split('*')
				# print('keyword list =',keywordList)
				foundFlg = False
				lastIndex = 0
				for keywordVal in keywordList:
					index = str(itemName).find(str(keywordVal))
					if(index != -1):
						if(lastIndex <= index):
							foundFlg = True
							lastIndex = index
						else:
							foundFlg = False
							lastIndex = index
					else:
						foundFlg = False
				if(foundFlg):
					itemList.append(val)

		showSearchBalance(itemList)


def showItemByProject(project):
	showSearchBalance(searchItemByProject(project))

def searchItemByProject(project):
	global itemsByProject
	transactionSearchRef = pbc.db1.reference(str(config.TRANSACTION_NODE_NAME))
	transactionRows = transactionSearchRef.order_by_key().get()
	itemByProjectList = []
	itemsByProject = []
	if(project != 'All'):
		if(transactionRows is not None):
			transactionRows.pop('size', None)
			transactionOfProjectList = list(value for (key,value) in transactionRows.items() if transactionRows[key]['PROJECT'] == project)
			itemsOfProjectSet = set(value['ITEM'] for value in transactionOfProjectList)
			# print("Transaction of project ", project, " \n ", transactionOfProjectList, " \n ")
			# print("Items of project ", project, " \n ", itemsOfProjectSet, " \n ")
			transactionOfItemOfProjectList = list(value for value in transactionOfProjectList if value['ITEM'] in itemsOfProjectSet)
			# print("transactionOfItemOfProjectList of project ", project, " \n ", transactionOfItemOfProjectList, " \n ")
			for itemSetValue in itemsOfProjectSet:
		 		itemByProjectList.append({'ITEM':itemSetValue,'BALANCE':'0'})
			for itemListValue in itemByProjectList:
				for transactionValue in transactionOfItemOfProjectList:
		 			if(transactionValue['ITEM'] == itemListValue['ITEM']):
		 				if(int(transactionValue['ADD']) > 0):
		 					itemListValue['BALANCE'] = int(itemListValue['BALANCE']) + int(transactionValue['ADD'])
		 				if(int(transactionValue['USE']) > 0):
		 					itemListValue['BALANCE'] = int(itemListValue['BALANCE']) - int(transactionValue['USE'])
			# print("Final Item List of project ", project, " \n ", itemByProjectList, " \n ")
			itemsByProject = itemByProjectList
			# print('Item ================================================================\n')
			# print(itemByProjectList)
			# print('Item ================================================================\n')
			return itemByProjectList
	else:
		balanceSearchRef = pbc.db1.reference(str(config.BALANCE_NODE_NAME))
		balanceRows = balanceSearchRef.order_by_key().get()		
		if(balanceRows is not None):
			balanceRows.pop('size', None)
			itemByProjectList = list(value for (key,value) in balanceRows.items())
			# print(itemByProjectList)
			itemsByProject = itemByProjectList
			return itemByProjectList

def loadProjectList():
	transactionRef = pbc.db1.reference(str(config.TRANSACTION_NODE_NAME))
	transactionRows = transactionRef.order_by_key().get()
	projectList = []
	if(transactionRows is not None):
		transactionRows.pop('size', None)
		for key, val in transactionRows.items():
			projectList.append(val['PROJECT'])
		projectSet = set(projectList)
		# print('Project Set = ', projectSet)
		projectList = list(projectSet)
	return projectList

def showProgressBar(): # Not use yet
	teams = range(100)
	popup = tk.Toplevel()
	tk.Label(popup, text="In progress").grid(row=0,column=0)
	progress = 0
	progress_var = tk.DoubleVar()
	progress_bar = ttk.Progressbar(popup, variable=progress_var, maximum=100)
	progress_bar.grid(row=1, column=0)#.pack(fill=tk.X, expand=1, side=tk.BOTTOM)
	popup.pack_slaves()
	progress_step = float(100.0/len(teams))
	for team in teams:
		popup.update()
		sleep(0.5) # lauch task
		progress += progress_step
		progress_var.set(progress)

# print(tk.TkVersion)
#print("นี่ไทยนะ".decode('Tis-620')+"\n")
gui = tk.Tk()
gui.geometry("640x640")
gui.title(" R&D Stock ")
crud.init()
# newItemEntry = tk.Entry()
filePathVar = tk.StringVar(None)
filePath = tk.Entry(textvariable=filePathVar)
searchItemVar = tk.StringVar(None)
searchItemText = tk.Entry(textvariable=searchItemVar)
# addButton = tk.Button(text="Add Item",command=crud.add)
browseButton = tk.Button(text="Browse",command=askToOpenFile)
importButton = tk.Button(text="Import",command=fileImport)
searchButton = tk.Button(text="Search",command=searchItem)
# newItemEntry.grid(row=1,column=1)
# addButton.grid(row=1,column=2)
filePath.grid(row=2,column=1)
browseButton.grid(row=2,column=2)
importButton.grid(row=2,column=3)
searchItemText.grid(row=4,column=1)
searchButton.grid(row=4,column=2)
menu = tk.Menu(gui)
file = tk.Menu(menu)
file.add_command(label="New")
menu.add_cascade(label="File",menu=file)
balanceVariable = tk.StringVar(None)
noteVariable = tk.StringVar(None)
balanceVariable.set(0)
noteVariable.set('')

init()
projectVar = tk.StringVar()
projectVar.set('Choose Project')
projectList = loadProjectList()
projectList.append('All')
drop = tk.OptionMenu(gui, projectVar, *projectList, command=showItemByProject)
drop.grid(row=3, column=1)

showAllBalance(gui)

gui.config(menu=menu)
gui.mainloop()

