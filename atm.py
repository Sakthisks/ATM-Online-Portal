import mysql.connector
from flask import Flask,request,render_template
import Tkinter as tk
import tkMessageBox


app=Flask(__name__,static_url_path="")
class sks:
	@app.route('/get_cnum',methods=["GET","POST"])
	def get_cnum():
		sks.cnum=request.form['cnum']
		db= mysql.connector.connect(user='root', password='sakthi',host='127.0.0.1',database='sakthi')
		cursor=db.cursor()
		try:
			cursor.execute("select pin from atm where cnum="+request.form['cnum'])
		except Exception:
			return "<br/>ERROR"
		ans=(i[0] for i in cursor.fetchall())
		x=list(ans)	
		db.close()
		print (request.form['pin'])
		print (x[0])
		if str(request.form['pin'])==str(x[0]):
			print ("success")
			return render_template("action.html")
		else:
			return render_template("atmerror.html")
	@app.route('/balance',methods=["GET","POST"])
	def balance():
		print(sks.cnum)
		db= mysql.connector.connect(user='root', password='sakthi',host='127.0.0.1',database='sakthi')
		cursor=db.cursor()
		try:
			cursor.execute("select balance from atm where cnum="+sks.cnum)
		except Exception:
			return "<br/>ERROR"
		ans=(i[0] for i in cursor.fetchall())
		x=list(ans)	
		db.close()
		return "<br/>BALANCE :"+str(x[0])
	@app.route('/withdraw',methods=["GET","POST"])
	def withdraw():
		db= mysql.connector.connect(user='root', password='sakthi',host='127.0.0.1',database='sakthi')
		cursor=db.cursor()
		try:
			cursor.execute("select balance from atm where cnum="+sks.cnum)
		except Exception as e:
			print(e)
			return "<br/>ERROR"
		ans=(i[0] for i in cursor.fetchall())
		x=list(ans)	
		print (request.form['amount'])
		print (x[0])
		if int(request.form['amount'])>int(x[0]):
			return render_template("withdrawerror.html")
		else:
			s=int(x[0])-int(request.form['amount'])		
			print (s)
			cursor.execute("update atm set balance=%s where cnum='%s'"%(s,sks.cnum))
			db.commit()
		db.close()
		return "<br/>transaction success"
	@app.route('/deposit',methods=["GET","POST"])
	def deposit():
		db= mysql.connector.connect(user='root', password='sakthi',host='127.0.0.1',database='sakthi')
		cursor=db.cursor()
		try:
			cursor.execute("select balance from atm where cnum="+sks.cnum)
		except Exception as e:
			print(e)
			return "<br/>ERROR"
		ans=(i[0] for i in cursor.fetchall())
		x=list(ans)	
		print (request.form['amount'])
		print (x[0])
		if int(request.form['amount'])>0 :
			s=int(x[0])+int(request.form['amount'])		
			print (s)
			cursor.execute("update atm set balance=%s where cnum='%s'"%(s,sks.cnum))
			db.commit()
		else:
			return render_template("depositerror.html")
		db.close()
		return "<br/>transaction success"
	@app.route('/reset',methods=["GET","POST"])
	def reset():
		flag=0
		db= mysql.connector.connect(user='root', password='sakthi',host='127.0.0.1',database='sakthi')
		cursor=db.cursor()
		try:
			if request.form['newpin']==request.form['cpin']:
				cursor.execute("update atm set pin=%s where cnum='%s'"%(request.form['cpin'],sks.cnum))
				#ans=(i[0] for i in cursor.fetchall())
				db.commit()
			else:
				return render_template("reseterror.html")
		except Exception as e:
			print(e)
			db.rollback()
			flag=1	
		db.close()
		if (flag==0):
			return "<br/> SuccessFully Updated"
		else:
			return "<br/> Error in updation"
	@app.route('/addphone',methods=["GET","POST"])
	def addphone():
		flag=0
		db= mysql.connector.connect(user='root', password='sakthi',host='127.0.0.1',database='sakthi')
		cursor=db.cursor()
		try:
			if len(request.form['phone'])==10:		
				cursor.execute("update atm set phone=%s where cnum='%s'"%(request.form['phone'],sks.cnum))
				#ans=(i[0] for i in cursor.fetchall())
				db.commit()
			else:
				return render_template("addphoneerror.html") 
		except Exception as e:
			print(e)
			db.rollback()
			flag=1	
		db.close()
		if (flag==0):
			return "<br/> SuccessFully Updated"
		else:
			return "<br/> Error in updation"
	@app.route('/aadhar',methods=["GET","POST"])
	def aadhar():
		flag=0
		db= mysql.connector.connect(user='root', password='sakthi',host='127.0.0.1',database='sakthi')
		cursor=db.cursor()
		try:
			print (len(request.form['aadhar']))
			if len(request.form['aadhar'])==12:				
				cursor.execute("update atm set aadhar='%s' where cnum='%s'"%(request.form['aadhar'],sks.cnum))
				#ans=(i[0] for i in cursor.fetchall())
				db.commit()
			else:
				return render_template("aadharerror.html")
		except Exception as e:
			print(e)
			db.rollback()
			flag=1	
		db.close()
		if (flag==0):
			return "<br/> SuccessFully Updated"
		else:
			return "<br/> Error in updation"
	@app.route('/blockdisplay',methods=["GET","POST"])
	def blockdisplay():
		flag=0
		db= mysql.connector.connect(user='root', password='sakthi',host='127.0.0.1',database='sakthi')
		cursor=db.cursor()
		try:
			cursor.execute("select cnum from atm where phone="+request.form['phone'])
			ans=(i[0] for i in cursor.fetchall())
			x=list(ans)
			print (x)
			return ",".join(x)
			if len(x)>1:
				return render_template("block.html")
			else:
				blockcard()
		except Exception as e:
			print(e)
			db.rollback()
			flag=1	
			db.close()
			return render_template("blockerror.html")
		return x
	@app.route('/blockcard',methods=["GET","POST"])
	def blockcard():
		flag=0
		db= mysql.connector.connect(user='root', password='sakthi',host='127.0.0.1',database='sakthi')
		cursor=db.cursor()
		try:
			cursor.execute("select phone from atm")
		except Exception as e:
			print(e)
			db.rollback()
			flag=1	
		ans=(i[0] for i in cursor.fetchall())
		x=list(ans)
		for i in range(0,len(x)):
			print (x[i])
			if int(request.form['bcnum  '])==int(x[i]):
				cursor.execute("delete from atm where phone="+request.form['bcnum'])
				db.commit()
				print ("success")
			else:
				return render_template("blockerror.html")
		db.close()
		if flag==0:
			return "<br/> your card is blocked SuccessFully "
		else:
			return "<br/> Error in blocking"					

if __name__=="__main__":
	app.run(host="localhost",debug=True)
