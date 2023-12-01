from flask import *
from database import *
import uuid
staff=Blueprint('staff',__name__)
 

@staff.route('/staffhome',methods=['get','post'])
def staffhome():
	sname=session['sname']
	sid=session['sid']

	return render_template('staffhome.html',sname=sname)


# @staff.route('/staff_view_profile',methods=['get','post'])
# def staff_view_profile():
# 	data={}
# 	sid=session['sid']
# 	uname=session['username']
# 	q="SELECT * FROM staff INNER JOIN login USING(username) where username='%s'"%(uname)
# 	print(q)
# 	res=select(q)
# 	data['updater']=res
# 	print(res)

# 	if 'update' in request.form:
# 		fname=request.form['fname']
# 		lname=request.form['lname']
# 		place=request.form['place']
# 		phone=request.form['phone']
# 		email=request.form['email']
# 		designation=request.form['designation']
# 		username=request.form['uname']
# 		pwd=request.form['pwd']
# 		q="update staff set username='%s',firstname='%s',lastname='%s',place='%s',phone='%s',email='%s',designation='%s' where staff_id='%s'"%(username,fname,lname,place,phone,email,designation,sid)
# 		update(q)
# 		q="update login set username='%s',password='%s' where username='%s'"%(username,pwd,uname)
# 		update(q)
# 		session['username']=username
# 		uname=session['username']
# 		print(uname)
# 		flash("updated successfully")
# 		return redirect(url_for('staff.staff_view_profile'))
# 	return render_template('staff_view_profile.html',data=data)



@staff.route('/staff_manage_products',methods=['get','post'])
def staff_manage_products():
	data={}
	q="SELECT * FROM category INNER JOIN subcategory USING(category_id) WHERE category.status='active' AND `subcategory`.`status`='active'"
	res=select(q)
	data['cat']=res

	return render_template('staff_manage_products.html',data=data)

@staff.route('/staff_make_purchase',methods=['get','post'])
def staff_make_purchase():
	data={}
	sid=session['sid']
	rate=request.args['rate']
	data['mrp']=rate
	pname=request.args['pname']
	data['pname']=pname
	# stocks=request.args['stocks']

	product_id=request.args['pid']
	# q="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS st_name FROM `staff`"
	# st=select(q)
	# data['staff']=st
 
	q="SELECT * FROM `vendor`"
	vendor=select(q)
	data['vendor']=vendor
 
	if 'purchase' in request.form:
		# staff=request.form['staff']
		vendors=request.form['vendor']
		pqnty=request.form['pqnty']
		ptotal=request.form['ptotal']
		print(vendors,pqnty,ptotal)
		# mfd=request.form['mfd']
		# expd=request.form['expd']
		# stocks_hand=int(stocks)+int(pqnty)
		# print(stocks_hand)

		q="INSERT INTO `purchasemaster` VALUES(NULL,'%s','%s',CURDATE(),'%s','%s','%s')"%(sid,vendors,product_id,pqnty,ptotal)
		insert(q)
		# q="INSERT INTO `purchase_child` VALUES(NULL,'%s','%s','%s','%s','%s','%s','%s','%s')"%(mp_id,vendors,item_id,pqnty,ptotal)
		# insert(q)
		q="UPDATE `product` SET `quantity`=`quantity`+'%s' WHERE `product_id`='%s'"%(pqnty,product_id)
		update(q)
		flash("STOCK UPDATED")
		return redirect(url_for("staff.staff_manage_stock"))
 
	return render_template('staff_make_purchase.html',data=data)


@staff.route('/staff_manage_productssub',methods=['get','post'])
def staff_manage_productssub():
	data={}
	cat=request.args['cat']
	data['cat']=cat
	subcat=request.args['subcat']
	data['subcat']=subcat
	q="select * from brand where bstatus='active'"
	data['brand']=select(q)
	q="select * from product inner join brand using(brand_id) where subcategory_id='%s'"%(subcat)
	res=select(q)
	data['pro']=res
	print("++++++")
	print(res)
	if 'submit' in request.form:
		brand=request.form['brand']
		rate=request.form['rate']
		pro=request.form['pro']
		img=request.files['img']
		path='static/'+str(uuid.uuid4())+img.filename
		img.save(path)
		q="select * from product where subcategory_id='%s' and brand_id='%s' and product='%s'"%(subcat,brand,pro)
		res=select(q)
		if res:
			pid=res[0]['product_id']
			q="update product set rate='%s' where product_id='%s'"%(rate,pid)
			update(q)
			flash('THIS PRODUCT IS ALREADY ADDED UPDATE DETAILS SUCCESFULLY')
			return redirect(url_for('staff.staff_manage_products',cat=cat,subcat=subcat))
		else:
			q="insert into product values(NULL,'%s','%s','%s','%s','%s',0,'active')"%(subcat,brand,pro,path,rate)
			lid=insert(q)
			return redirect(url_for('staff.staff_manage_productssub',cat=cat,subcat=subcat))

	if 'action' in request.args:
		action=request.args['action']
		id=request.args['pid']
	else:
		action=None
	
	if action=='active':
		q="update product set status='active' where product_id='%s'"%(id)
		update(q)
		return redirect(url_for('staff.staff_manage_productssub',cat=cat,subcat=subcat))
	if action=='inactive':
		q="update product set status='inactive' where product_id='%s'"%(id)
		update(q)
		return redirect(url_for('staff.staff_manage_productssub',cat=cat,subcat=subcat))



	if action=='update':
		q="select * from product where product_id='%s'"%(id)
		data['updater']=select(q)
	if 'update' in request.form:
		brand=request.form['brand']
		rate=request.form['rate']
		pro=request.form['pro']
		pro=request.form['pro']
		img=request.files['img']
		path='static/'+str(uuid.uuid4())+img.filename
		img.save(path)
		q="update product set image='%s',brand_id='%s',rate='%s',product='%s' where product_id='%s'"%(path,brand,rate,pro,id)
		update(q)
		return redirect(url_for('staff.staff_manage_productssub',cat=cat,subcat=subcat))
	return render_template('staff_manage_productssub.html',data=data)





@staff.route('/staff_manage_stock',methods=['get','post'])
def staff_manage_stock():
	data={}
	q="select * from product inner join brand using(brand_id) inner join subcategory using(subcategory_id) inner join category using(category_id)"
	res=select(q)
	data['pro']=res
	print(res)
	return render_template('staff_manage_stock.html',data=data)


@staff.route('/staff_view_provendor',methods=['get','post'])
def staff_view_provendor():
	data={}
	sid=session['sid']
	pid=request.args['pid']
	q="select rate from product where product_id='%s'"%(pid)
	res=select(q)
	pamt=res[0]['rate']
	data['pid']=pid
	pname=request.args['pname']
	data['pname']=pname
	q="select * from vendorproduct inner join vendor using(vendor_id) where product_id='%s' and vpstatus='active'"%(pid) 
	res=select(q)
	data['vendor']=res
	print(res)
	if 'action' in request.args:
		vpid=request.args['vpid']
		vid=request.args['vid']
		q="select * from purchasemaster where staff_id='%s' and status='pending'"%(sid)
		res=select(q)
		if res:
			pmaster_id=res[0]['pmaster_id']
			total=res[0]['total']
			q="select vendor_id from purchasechild inner join vendorproduct using(vproduct_id) inner join vendor using(vendor_id) where pmaster_id='%s'"%(pmaster_id)
			print(q)
			res=select(q)
			bkvenid=res[0]['vendor_id']
			print(q)
			print(res)
			if int(bkvenid)==int(vid):
				q="select * from purchasechild where vproduct_id='%s' and pmaster_id='%s'"%(vpid,pmaster_id)
				res=select(q)
				if res:
					preamt=int(res[0]['amount'])
					newamt=preamt+int(pamt)
					q="update purchasechild set quantity=quantity+1,amount='%s' where vproduct_id='%s' and pmaster_id='%s'"%(newamt,vpid,pmaster_id)
					print(q)
					update(q)

					q="update purchasemaster set total=total+'%s' where  pmaster_id='%s'"%(pamt,pmaster_id)
					update(q)
					flash("ALREADY THIS ITEM ON CART !CART UPDATED SUCESSFULLY")
					return redirect(url_for('staff.staff_view_provendor',pid=pid,pname=pname))
				else:
					q="insert into purchasechild values(NULL,'%s','%s','%s','1')"%(pmaster_id,vpid,pamt)
					insert(q)
					q="update purchasemaster set total=total+'%s' where  pmaster_id='%s'"%(pamt,pmaster_id)
					update(q)
					flash("ADDED TO CART")
					return redirect(url_for('staff.staff_view_provendor',pid=pid,pname=pname))
			else:
				flash("YOU CAN PURCHASE FROM A SINGLE VENDOR AT TIME IF YOU WANT TO PURCHASE PLEASE CLEAR CART")
				return redirect(url_for('staff.staff_view_provendor',pid=pid,pname=pname))
		else:
			q="insert into purchasemaster values(NULL,'%s','%s',NOW(),'pending')"%(sid,pamt)
			pmaster_id=insert(q)
			q="insert into purchasechild values(NULL,'%s','%s','%s','1')"%(pmaster_id,vpid,pamt)
			insert(q)
			flash("ADDED TO CART")
			return redirect(url_for('staff.staff_view_provendor',pid=pid,pname=pname))
	return render_template('staff_view_provendor.html',data=data)


@staff.route('/staff_view_cart',methods=['get','post'])
def staff_view_cart():
	data={}
	sid=session['sid']
	print(sid)
	q="SELECT *,purchasechild.quantity as purqua FROM purchasechild INNER JOIN `purchasemaster` USING(`pmaster_id`) INNER JOIN vendorproduct using(vproduct_id) inner join vendor using(vendor_id) inner join product USING(`product_id`) WHERE `purchasemaster`.`staff_id`='%s' AND `purchasemaster`.`status`='pending'"%(sid)
	res=select(q)
	print(res)
	print(q)
	data['cart']=res	

	if 'action' in request.args:
			action=request.args['action']
			vpid=request.args['vpid']
			pmastid=request.args['pmastid']
			purqua=request.args['purqua']
			prorate=request.args['prorate']
			data['prorate']=prorate
			puramt=int(purqua)*int(prorate)
			print(puramt)
			data['purqua']=purqua
	else:
		action=None
	if action=="update":
		q="SELECT * from purchasechild inner join vendorproduct using(vproduct_id) inner join product using (product_id) where pmaster_id='%s' and vproduct_id='%s'"%(pmastid,vpid)
		res=select(q)
		print(res)
		data['updater']=res[0]['product']
		
	if 'updatequa'  in request.form:
		upquantity=request.form['upqua']
		newamt=int(prorate)*int(upquantity)
		q="update purchasemaster set total=total+'%s'-'%s' where pmaster_id='%s' and status='pending'"%(newamt,puramt,pmastid)
		update(q)
		q="update purchasechild set quantity='%s',amount='%s' where vproduct_id='%s' and pmaster_id='%s'"%(upquantity,newamt,vpid,pmastid)
		update(q)
		return redirect(url_for('staff.staff_view_cart'))
	if action=='delete':
		q="delete from purchasechild where vproduct_id='%s' and pmaster_id='%s' "%(vpid,pmastid)
		delete(q)
		q="update purchasemaster set total=total-'%s' where pmaster_id='%s'"%(puramt,pmastid)
		update(q)
		q="SELECT * FROM `purchasemaster` INNER JOIN `purchasechild` USING(`pmaster_id`) WHERE  `purchasechild`.`pmaster_id`='%s'"%(pmastid)
		print(q)
		res=select(q)
		if res:
			return redirect(url_for("staff.staff_view_cart"))
		else:
			q="delete from `purchasemaster` where pmaster_id='%s'"%(pmastid)
			delete(q)
			return redirect(url_for('staff.staff_view_cart'))	

	if 'action2' in request.args:
		action2=request.args['action2']
		pmastid=request.args['pid']	
		amt=request.args['amt']
	else:
		action2=None
	if action2=='payment':
		print("++++++++++++++++++++++++++++")
		q="SELECT *,purchasechild.quantity as purqua from purchasechild inner join vendorproduct using(vproduct_id) inner join product using (product_id) where pmaster_id='%s'"%(pmastid)
		print(q)
		res=select(q)
		print(res)
		for row in res:
			proqua=row['purqua']
			print(row['quantity'])
			proid=row['product_id']
			q="update product set quantity=quantity+'%s' where product_id='%s'"%(proqua,proid)
			print(q)
			update(q)
			
			q="update purchasemaster set status='ordered' where pmaster_id='%s'"%(pmastid)	
			update(q)
			flash("BOOKED SUCESSFULLY")
			return redirect(url_for("staff.staff_view_cart"))
			
	return render_template("staff_view_cart.html",data=data)



@staff.route('/staff_view_orders',methods=['get','post'])
def staff_view_orders():
	sid=session['sid']
	data={}
	q="select *,ordermaster.status as omstatus from ordermaster inner join customer using(customer_id) where status in('ordered','delivered') order by omaster_id desc"
	res=select(q)
	session['mains']=q
	data['orders']=res
	q="select *,ordermaster.status as omstatus,sum(total) as sum from ordermaster inner join customer using(customer_id) where status in('ordered','delivered')"
	print(q)
	res=select(q)
	data['total']=res[0]['sum']
	session['sum']=data['total']
	print(res)
	if 'action' in request.args:
		action=request.args['action']
		omaster_id=request.args['omaster_id'] 
	else:
		action=None
	if action=='products':
		q="SELECT *,orderchild.quantity AS orqua,product.`quantity` AS proqua FROM orderchild INNER JOIN `ordermaster` USING(`omaster_id`)  INNER JOIN product  USING (product_id) inner join subcategory using(subcategory_id) inner join category using(category_id) inner join brand using(brand_id)  WHERE `ordermaster`.omaster_id='%s'"%(omaster_id)
		res=select(q)
		data['products']=res
		print(res)
	if action=='delivered':
		q="update ordermaster set status='delivered' where omaster_id='%s'"%(omaster_id)
		update(q)
		return redirect(url_for('staff.staff_view_orders'))

	if 'submit' in request.form:
		from_date=request.form['from_date']
		to_date=request.form['to_date']
		q="select *,ordermaster.status as omstatus from ordermaster inner join customer using(customer_id) where status in('ordered','delivered') and( date between '%s' and '%s')"%(from_date,to_date)
		print(q)
		res=select(q)
		session['mains']=q
		data['orders']=res
		print(res)
		q="select *,ordermaster.status as omstatus,sum(total) as sum from ordermaster inner join customer using(customer_id) where status in('ordered','delivered') and( date between '%s' and '%s')"%(from_date,to_date)
		print(q)
		res=select(q)
		data['total']=res[0]['sum']
		session['sum']=data['total']
	return render_template('staff_view_orders.html',data=data)


@staff.route('/staff_print',methods=['get','post'])
def staff_print():
	data={}


	res=select(session['mains'])
	data['booking']=res
	data['total']=session['sum']
	
	return render_template('admin_print.html',data=data)


@staff.route('/staff_print_purchase',methods=['get','post'])
def staff_print_purchase():
	data={}
	sid=session['sid']
	q="SELECT * FROM  `purchasemaster`  INNER JOIN product USING(product_id) INNER JOIN vendor USING(vendor_id) where staff_id='%s'"%(sid)
	data['purchase']=select(q)
	print(data['purchase'])

	if 'submit' in request.form:
		from_date=request.form['from_date']
		to_date=request.form['to_date']
		print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

		q="SELECT * FROM  `purchasemaster`  INNER JOIN product USING(product_id) INNER JOIN vendor USING(vendor_id) where( date between '%s' and '%s') and staff_id='%s'"%(from_date,to_date,sid)
		print(q)
		res=select(q)
		data['purchase']=res
		print(res)

	return render_template('staff_print_purchase.html',data=data)



@staff.route('/staff_view_profile',methods=['get','post'])
def staff_view_profile():
	data={}
	username=session['username']
	print(username)
	q="select * from staff inner join login using(username) where username='%s'"%(username)
	res=select(q)
	print(res)
	data['updater']=res
	if 'update' in request.form:
		place=request.form['place']
		ph=request.form['phone']
		email=request.form['email']
		
		
		
		password=request.form['pwd']
		q="update login set username='%s',password='%s' where username='%s'"%(email,password,username)
		update(q)
		q="update staff set place='%s',phone='%s',email='%s',username='%s' where username='%s' "%(place,ph,email,email,username)
		update(q)
		session['username']=email
		flash("PROFILE UPDATED")
		return redirect(url_for('staff.staff_view_profile'))
	# if 'action' in request.args:
	# 	q="update login set usertype='deleted' where username='%s'"%(username)
	# 	update(q)
	# 	flash("ACCOUNT DELETED SUCESSFULLY")
	# 	return redirect(url_for('public.home'))
	return render_template('staff_view_profile.html',data=data)