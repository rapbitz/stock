import PyrebaseConfig as pbc

pbc.init()
data = {'DATE': '18/5/2015', 'ITEM': '16-Channel 12-bit PWM/Servo', 'PROJECT': 'Smart Microwave', 'USE': '0', 'PRICE': '10', 'ADD': '1'}
pbc.db.child("stock-57ec5").child("transactions").child("MyTrans").set(data)