from flask import *
from database import *
import uuid
customer=Blueprint('customer',__name__)
 

@customer.route('/customerhome',methods=['get','post'])
def customerhome():
	cname=session['cname']
	cid=session['cid']
	print(cname)
	return render_template('customerhome.html',cname=cname)




@customer.route('/customer_sendfeedback',methods=['get','post'])
def customer_sendfeedback():
	data={}
	cid=session['cid']
	q="select * from branches"
	res=select(q)
	data['branch']=res
	print(res)
	if 'submit' in request.form:
		fb=request.form['fb']
		bid=request.form['bid']
		q="insert into feedback values(NULL,'%s','%s','%s','pending',NOW())"%(cid,bid,fb)
		res=insert(q)
		return redirect(url_for('customer.customer_sendfeedback'))
	q="select * from feedback inner join branches using(branch_id) where customer_id='%s'"%(cid)	
	res=select(q)
	data['fb']=res
	print(res)
	return render_template('customer_sendfeedback.html',data=data)


@customer.route('/customer_complaints',methods=['get','post'])
def customer_complaints():
	data={}
	cid=session['cid']
	if 'send' in request.form:
		comp=request.form['com']
	
		q="insert into complaint values(NULL,'%s','%s','pending')"%(cid,comp)
		res=insert(q)
		return redirect(url_for('customer.customer_complaints'))
	q="select * from complaint  where customer_id='%s'"%(cid)	
	res=select(q)
	data['comp']=res
	print(res)
	return render_template('customer_complaints.html',data=data)




@customer.route('/customer_review_andrate',methods=['get','post'])
def customer_review_andrate():
	data={}
	cid=session['cid']
	q="select * from branches"
	res=select(q)
	data['branch']=res
	print(res)
	q="select * from review_rating inner join branches using(branch_id) where customer_id='%s'"%(cid)
	res=select(q)
	data['rating']=res
	print(res)
	if 'submit' in request.form:
		bid=request.form['bid']
		rate=request.form['rate']
		review=request.form['review']
		q="select * from review_rating where customer_id='%s' and branch_id='%s'"%(cid,bid)
		res=select(q)
		if res:
			q="update review_rating set rating_point='%s',review_comment='%s',review_date=NOW() where customer_id='%s' and branch_id='%s' "%(rate,review,cid,bid)
			update(q)
			return redirect(url_for('customer.customer_review_andrate'))		
		else:
			print("&&&&&&&&&&&&&&&&&&&&&&&&&")
			q="insert into review_rating values(NULL,'%s','%s','%s','%s',NOW())"%(cid,bid,review,rate)
			res=insert(q)
			return redirect(url_for('customer.customer_review_andrate'))
	# q="select * from feedback inner join branches using(branch_id) where customer_id='%s'"%(cid)	
	# res=select(q)
	# data['fb']=res
	# print(res)
	return render_template('customer_review_andrate.html',data=data)



@customer.route('/staff_view_cart',methods=['get','post'])
def user_view_cart():
	data={}
	cid=session['cid']
	q="SELECT * FROM purchasechild INNER JOIN `purchasemaster` USING(`pmaster_id`) INNER JOIN vendorproduct using(vproduct_id) inner join vendor using(venor_id) inner join products USING(`product_id`) WHERE `purchasemaster`.`staff_id`='%s' AND `purchasemaster`.`status`='pending'"%(cid)
	res=select(q)
	print(q)
	data['cart']=res

	if 'action' in request.args:
		action=request.args['action']
		pid=request.args['pid']
		oid=request.args['oid']
		oquantity=request.args['oquantity']
		data['oquantity']=oquantity
	else:
		action=None
	if action=="update":
		q="SELECT *,`order_details`.`quantity` AS oquantity,`order_details`.`amount` as oamount,products.`quantity`  AS pquantity,products.amount as pamount FROM order_master INNER JOIN `order_details` USING(`omaster_id`) INNER JOIN products USING(`product_id`) WHERE `order_master`.`user_id`='%s' AND `order_master`.`status`='pending' AND `order_details`.product_id='%s'"%(uid,pid)
		res=select(q)
		data['updater']=res
		pamount=res[0]['pamount']
	if 'updatequa'  in request.form:
		upquantity=request.form['upquantity']
		q="update order_master set total=total+('%s'*'%s')-('%s'*'%s') where omaster_id='%s' and status='pending'"%(upquantity,pamount,oquantity,pamount,oid)
		update(q)
		q="update order_details set quantity='%s',amount='%s'*'%s' where product_id='%s' and omaster_id='%s'"%(upquantity,pamount,upquantity,pid,oid)
		update(q)
		return redirect(url_for('staff.staff_view_cart'))
	if action=='delete':
		q="SELECT *,`order_details`.`quantity` AS oquantity,`order_details`.`amount` as oamount,products.`quantity`  AS pquantity,products.amount as pamount FROM order_master INNER JOIN `order_details` USING(`omaster_id`) INNER JOIN products USING(`product_id`) WHERE `order_master`.`user_id`='%s' AND `order_master`.`status`='pending' AND `order_details`.product_id='%s'"%(uid,pid)
		res=select(q)
		pamount=res[0]['pamount']
		q="delete from order_details where product_id='%s' and omaster_id='%s'"%(pid,oid)
		delete(q)
		q="update order_master set total=total-('%s'*'%s') where omaster_id='%s' and status='pending'"%(oquantity,pamount,oid)
		update(q)
		q="SELECT * FROM `order_master` INNER JOIN `order_details` USING(`omaster_id`) WHERE  `order_details`.`omaster_id`='%s'"%(oid)
		res=select(q)
		if res:
			return redirect(url_for("staff.staff_view_cart"))
		else:
			q="delete from `order_master` where omaster_id='%s'"%(oid)
			delete(q)
			return redirect(url_for('staff.user_viewproducts'))	
	if 'action2' in request.args:
		action2=request.args['action2']
		oid=request.args['oid']	
		amt=request.args['amt']
	else:
		action2=None
	if action2=='payment':
		data['oid']=oid
		q="SELECT *,`products`.`quantity` AS pquantity,`order_details`.`quantity` AS oquantity FROM `order_master` INNER JOIN `order_details` USING(omaster_id) INNER JOIN products  USING (product_id) WHERE `order_master`.omaster_id='%s'"%(oid)
		res=select(q)
		print(res)
		for row in res:
			print(row['oquantity'])
			print(row['pquantity'])
			if int(row['pquantity'])>=int(row['oquantity']):
				data['amt']=amt
			else:
				flash(row['product_name']+" "+"IS ONLY"+" "+row['pquantity']+"AVAILABLE")
				return redirect(url_for("staff.staff_view_cart"))
	if 'pay' in request.form:
		amt=request.args['amt']
		q="SELECT *,`products`.`quantity` AS pquantity,`order_details`.`quantity` AS oquantity FROM `order_master` INNER JOIN `order_details` USING(omaster_id) INNER JOIN products  USING (product_id) WHERE `order_master`.omaster_id='%s'"%(oid)
		res=select(q)
		print(res)
		for row in res:
			oqunatity=row['oquantity']
			pid=row['product_id']
			q="update products set quantity=quantity-'%s' where product_id='%s'"%(oqunatity,pid)
			update(q)
		q="insert into payment values(NULL,'%s','%s',NOW())"%(oid,amt)
		insert(q)
		q="update order_master set status='orderd' where omaster_id='%s'"%(oid)
		update(q)
		q="insert into pickups values(NULL,'%s',NULL,NOW(),'waiting')"%(oid)
		insert(q)
		return redirect(url_for('staff.staff_view_cart'))
	return render_template("staff_view_cart.html",data=data)


@customer.route('/customer_view_products',methods=['get','post'])
def customer_view_products():
	data={}
	cid=session['cid']
	q="select * from product inner join subcategory using(subcategory_id) inner join category using(category_id) inner join brand using(brand_id) where product.status='active'"
	res=select(q)
	data['products']=res
	print(res)

	if 'search' in request.form:
		name=request.form['rad']
		find="%"+request.form['find']+"%"
		if name=='product':
			q="select * from product inner join subcategory using(subcategory_id) inner join category using(category_id) inner join brand using(brand_id) where product like '%s' and product.status='active'"%(find)
			print(q)
			res=select(q)
			print(res)
			if res:
				data['products']=res
			else:
				flash("NO MATCHED ITEMS FIND ON YOUR SEARCH")
				return redirect(url_for('customer.customer_view_products'))
		if name=='category':
			q="select * from product inner join subcategory using(subcategory_id) inner join category using(category_id) inner join brand using(brand_id) where category like '%s' product.status='active'"%(find)
			print(q)
			res=select(q)
			print(res)
			if res:
				data['products']=res
			else:
				flash("NO MATCHED ITEMS FIND ON YOUR SEARCH")
				return redirect(url_for('customer.customer_view_products'))
		if name=='subcategory':
			q="select * from product inner join subcategory using(subcategory_id) inner join category using(category_id) inner join brand using(brand_id) where subcategory like '%s' product.status='active'"%(find)
			print(q)
			res=select(q)
			print(res)
			if res:
				data['products']=res
			else:
				flash("NO MATCHED ITEMS FIND ON YOUR SEARCH")
				return redirect(url_for('customer.customer_view_products'))
		if name=='brand':
			q="select * from product inner join subcategory using(subcategory_id) inner join category using(category_id) inner join brand using(brand_id) where brand like '%s'"%(find)
			print(q)
			res=select(q)
			print(res)
			if res:
				data['products']=res
			else:
				flash("NO MATCHED ITEMS FIND ON YOUR SEARCH")
				return redirect(url_for('customer.customer_view_products'))

	if 'action' in request.args:
		action=request.args['action']
		pid=request.args['pid']
		rate=request.args['rate']
	else:
		action=None
	if action=='book':

		q="SELECT * FROM `ordermaster` WHERE `customer_id`='%s' AND STATUS='pending'"%(cid)
		res=select(q)
		print(res)
		if res:
			if res:
				oid=res[0]['omaster_id']
				q="update ordermaster set date=curdate(),total=total+'%s'  WHERE omaster_id='%s'"%(rate,oid)
				res=update(q)
				q="select * from orderchild where product_id='%s' and omaster_id='%s'"%(pid,oid)
				res=select(q)
				if res:
					q="update orderchild set quantity=quantity+1,amount=amount+'%s' where product_id='%s' and omaster_id='%s'"%(rate,pid,oid)
					update(q)
					flash("Your CART Updated")
					return redirect(url_for("customer.customer_view_cart"))
		
				else:
					q="insert into orderchild values(NULL,'%s','%s','%s','1')"%(oid,pid,rate)
					insert(q)
					flash("Your CART Updated")
					return redirect(url_for("customer.customer_view_cart"))			
			
		else:
			q="insert into ordermaster values(NULL,'%s','%s',curdate(),'pending')"%(cid,rate)
			res=insert(q)
			q="insert into orderchild values(NULL,'%s','%s','%s','1')"%(res,pid,rate)
			insert(q)
			flash("Your CART Updated")
			return redirect(url_for("customer.customer_view_cart"))
	return render_template('customer_view_products.html',data=data)

@customer.route('/customer_view_cart',methods=['get','post'])
def customer_view_cart():
	data={}
	cid=session['cid']
	q="SELECT *,orderchild.quantity AS orqua,product.`quantity` AS proqua FROM orderchild INNER JOIN `ordermaster` USING(`omaster_id`)  INNER JOIN product  USING (product_id)  WHERE `ordermaster`.`customer_id`='%s' AND `ordermaster`.`status`='pending'"%(cid)
	print(q)
	res=select(q)
	print(res)
	data['cart']=res
	if res:
		total=res[0]['total']	
		omid=res[0]['omaster_id']

	if 'action' in request.args:
			action=request.args['action']
			proid=request.args['proid']
			ochild_id=request.args['ochild_id']
			prorate=request.args['prorate']
			data['prorate']=prorate
			purqua=request.args['purqua']
			puramt=int(purqua)*int(prorate)
			print(puramt)
			
	else:
		action=None
	if action=="update":
		data['proqua']=request.args['proqua']
		q="select * from product where product_id='%s'"%(proid)
		res=select(q)
		data['pname']=res[0]['product']
		
	if 'updatequa'  in request.form:
		upquantity=request.form['upqua']
		newamt=int(prorate)*int(upquantity)
		q="update ordermaster set total=total+'%s'-'%s' where omaster_id='%s'"%(newamt,puramt,omid)
		update(q)
		q="update orderchild set quantity='%s',amount='%s' where ochild_id='%s'"%(upquantity,newamt,ochild_id)
		update(q)
		return redirect(url_for('customer.customer_view_cart'))
	if action=='delete':
		q="delete from orderchild where ochild_id='%s' "%(ochild_id)
		delete(q)
		q="update ordermaster set total=total-'%s' where omaster_id='%s'"%(puramt,omid)
		update(q)
		q="SELECT * FROM `orderchild`  WHERE  `orderchild`.`omaster_id`='%s'"%(omid)
		print(q)
		res=select(q)
		if res:
			return redirect(url_for("customer.customer_view_cart"))
		else:
			q="delete from `ordermaster` where omaster_id='%s'"%(omid)
			delete(q)
			return redirect(url_for('customer.customer_view_cart'))	

	if 'action2' in request.args:
		action2=request.args['action2']	
		amt=request.args['amt']
	else:
		action2=None
	if action2=='payment':
		print("++++++++++++++++++++++++++++")
		q="SELECT *,orderchild.quantity AS orqua,product.`quantity` AS proqua FROM orderchild INNER JOIN `ordermaster` USING(`omaster_id`)  INNER JOIN product  USING (product_id)  WHERE `ordermaster`.omaster_id='%s'"%(omid)
		print(q)
		res=select(q)
		print(res)
		for row in res:
			orqua=row['orqua']
			product=row['product']
			proqua=row['proqua']
			if int(proqua)<int(orqua):
				flash(product+" Only Left"+proqua +"Update It On Your Quantity To Purchase")
				return redirect(url_for("customer.customer_view_cart"))
			else:
				data['pay']=amt
	if 'pay' in request.form:	
		q="SELECT *,orderchild.quantity AS orqua,product.`quantity` AS proqua FROM orderchild INNER JOIN `ordermaster` USING(`omaster_id`)  INNER JOIN product  USING (product_id)  WHERE `ordermaster`.omaster_id='%s'"%(omid)
		res=select(q)
		for row in res:
			orqua=row['orqua']
			proqua=row['proqua']
			upqua=int(proqua)-int(orqua)
			product_id=row['product_id']
			q="update product set quantity='%s' where product_id='%s'"%(upqua,product_id)
			update(q)
		q="update ordermaster set status='ordered' where omaster_id='%s'"%(omid)	
		update(q)
		q="insert into payment values(NULL,'%s','%s',NOW())"%(omid,data['pay'])
		insert(q)
		flash("BOOKED SUCESSFULLY")
		return redirect(url_for("customer.customer_view_cart"))
			
	return render_template("customer_view_cart.html",data=data)

@customer.route('/customer_view_orders',methods=['get','post'])
def customer_view_orders():
	cid=session['cid']
	data={}
	q="select * from ordermaster where customer_id='%s' and status='ordered'"%(cid)
	res=select(q)
	data['orders']=res
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
	
	return render_template('customer_view_orders.html',data=data)



@customer.route('/customer_view_profile',methods=['get','post'])
def customer_view_profile():
	data={}
	username=session['username'] 
	print(username)
	q="select * from customer inner join login using(username) where username='%s'"%(username)
	res=select(q)
	print(res)
	data['customer']=res
	if 'submit' in request.form:
		place=request.form['place']
		ph=request.form['ph']
		email=request.form['email']
		gender=request.form['gen']
		
		
		password=request.form['password']
		q="update login set username='%s',password='%s' where username='%s'"%(email,password,username)
		update(q)
		q="update customer set place='%s',phone='%s',email='%s',gender='%s',username='%s' where username='%s' "%(place,ph,email,gender,email,username)
		update(q)
		session['username']=email
		flash("PROFILE UPDATED")
		return redirect(url_for('customer.customer_view_profile'))
	# if 'action' in request.args:
	# 	q="update login set usertype='deleted' where username='%s'"%(username)
	# 	update(q)
	# 	flash("ACCOUNT DELETED SUCESSFULLY")
	# 	return redirect(url_for('public.home'))
	return render_template('customer_view_profile.html',data=data)