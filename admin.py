from flask import *
from database import *
import uuid
admin=Blueprint('admin',__name__)
 

@admin.route('/adminhome',methods=['get','post'])
def adminhome():
	return render_template('adminhome.html')



@admin.route('/admin_manage_staff',methods=['get','post'])
def admin_manage_staff():
	data={}
	if 'submit' in request.form:
		fname=request.form['fname']
		lname=request.form['lname']
		place=request.form['place']
		phone=request.form['phone']
		email=request.form['email']
		
		password=request.form['password']
		q="select * from login where username='%s'"%(email)
		res=select(q)
		if res:
			flash('THIS USER NAME ALREADY TAKEN BY ANOTHER USER')
			return redirect(url_for('admin.admin_manage_staff'))
		else:
			q="insert into login values('%s','%s','staff')"%(email,password)
			insert(q)
		q="insert into staff values(NULL,'%s','%s','%s','%s','%s','%s')"%(email,fname,lname,place,phone,email)
		insert(q)
		return redirect(url_for('admin.admin_manage_staff'))
	q="select * from staff inner join login using(username)"
	res=select(q)
	if res:
		data['staff']=res
		print(res)
	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
	else:
		action=None
	if action=='active':
		q="update login set usertype='staff' where username='%s'"%(id)
		update(q)
		return redirect(url_for('admin.admin_manage_staff'))
	if action=='inactive':
		q="update login set usertype='inactive' where username='%s'"%(id)
		update(q)
		return redirect(url_for('admin.admin_manage_staff'))
	if action=='update':
		q="select * from staff where staff_id='%s'"%(id)
		data['updater']=select(q)
	if 'update' in request.form:
		fname=request.form['fname']
		lname=request.form['lname']
		place=request.form['place']
		phone=request.form['phone']
		email=request.form['email']
		
		q="update staff set firstname='%s',lastname='%s',place='%s',phone='%s',email='%s' where staff_id='%s'"%(fname,lname,place,phone,email,id)
		update(q)
		return redirect(url_for('admin.admin_manage_staff'))
	return render_template('admin_manage_staff.html',data=data)


@admin.route('/admin_manage_vendor',methods=['get','post'])
def admin_manage_vendor():
	data={}
	if 'submit' in request.form:
		vname=request.form['vname']
		place=request.form['place']
		phone=request.form['phone']
		email=request.form['email']
		q="insert into vendor values(NULL,'%s','%s','%s','%s','active')"%(vname,place,phone,email)
		insert(q)
		return redirect(url_for('admin.admin_manage_vendor'))
	q="select * from vendor"
	res=select(q)
	if res:
		data['vendor']=res
		print(res)
	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
	else:
		action=None
	if action=='active':
		q="update vendor set status='active' where vendor_id='%s'"%(id)
		update(q)
		return redirect(url_for('admin.admin_manage_vendor'))
	if action=='inactive':
		q="update vendor set status='inactive' where vendor_id='%s'"%(id)
		update(q)
		return redirect(url_for('admin.admin_manage_vendor'))
	if action=='update':
		q="select * from vendor where vendor_id='%s'"%(id)
		data['updater']=select(q)
	if 'update' in request.form:
		vname=request.form['vname']
		place=request.form['place']
		phone=request.form['phone']
		email=request.form['email']	
		q="update vendor set vname='%s',place='%s',phone='%s',email='%s' where vendor_id='%s'"%(vname,place,phone,email,id)
		update(q)
		return redirect(url_for('admin.admin_manage_vendor'))
	return render_template('admin_manage_vendor.html',data=data)


@admin.route('/admin_manage_products',methods=['get','post'])
def admin_manage_products():
	data={}
	q="SELECT * FROM category INNER JOIN subcategory USING(category_id) WHERE category.status='active' AND `subcategory`.`status`='active'"
	res=select(q)
	data['cat']=res

	return render_template('admin_manage_products.html',data=data)



@admin.route('/admin_manage_productssub',methods=['get','post'])
def admin_manage_productssub():
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
			return redirect(url_for('admin.staff_manage_products',cat=cat,subcat=subcat))
		else:
			q="insert into product values(NULL,'%s','%s','%s','%s','%s',0,'active')"%(subcat,brand,pro,path,rate)
			lid=insert(q)
			return redirect(url_for('admin.admin_manage_productssub',cat=cat,subcat=subcat))

	if 'action' in request.args:
		action=request.args['action']
		id=request.args['pid']
	else:
		action=None
	
	if action=='active':
		q="update product set status='active' where product_id='%s'"%(id)
		update(q)
		return redirect(url_for('admin.admin_manage_productssub',cat=cat,subcat=subcat))
	if action=='inactive':
		q="update product set status='inactive' where product_id='%s'"%(id)
		update(q)
		return redirect(url_for('admin.admin_manage_productssub',cat=cat,subcat=subcat))



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
		return redirect(url_for('admin.admin_manage_productssub',cat=cat,subcat=subcat))
	return render_template('admin_manage_productssub.html',data=data)



@admin.route('/admin_view_user',methods=['get','post'])
def admin_view_user():
	data={}
	q="select * from customer"
	res=select(q)
	data['users']=res
	print(res)
	return render_template('admin_view_user.html',data=data)


@admin.route('/admin_manage_category',methods=['get','post'])
def admin_manage_category():
	data={}
	if 'submit' in request.form:
		cat=request.form['cat']
		q="select * from category where category='%s'"%(cat)
		res=select(q)
		if res:
			flash('THIS CATEGORY IS ALREADY ADDED')
			return redirect(url_for('admin.admin_manage_category'))
		else:
			q="insert into category values(NULL,'%s','active')"%(cat)
			lid=insert(q)
			return redirect(url_for('admin.admin_manage_category'))

	q="select * from category"
	res=select(q)
	if res:
		data['category']=res
		print(res)
	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
	else:
		action=None
	if action=='active':
		q="update category set status='active' where category_id='%s'"%(id)
		update(q)
		return redirect(url_for('admin.admin_manage_category'))
	if action=='inactive':
		q="update category set status='inactive' where category_id='%s'"%(id)
		update(q)
		return redirect(url_for('admin.admin_manage_category'))
	if action=='update':
		q="select * from category where category_id='%s'"%(id)
		data['updater']=select(q)
	if 'update' in request.form:
		cat=request.form['cat']
		q="update category set category='%s' where category_id='%s'"%(cat,id)
		update(q)
		return redirect(url_for('admin.admin_manage_category'))
	return render_template('admin_manage_category.html',data=data)

@admin.route('/admin_manage_subcat',methods=['get','post'])
def admin_manage_subcat():
	data={}
	id=request.args['id']
	data['id']=id
	cat=request.args['cat']
	data['cat']=cat
	
	if 'submit' in request.form:
		subcat=request.form['subcat']
		q="select * from subcategory where subcategory='%s' and category_id='%s'"%(subcat,id)
		res=select(q)
		if res:
			flash('THIS SUBCATEGORY IS ALREADY ADDED')
			return redirect(url_for('admin.admin_manage_subcat',id=id,cat=cat))
		else:
			q="insert into subcategory values(NULL,'%s','%s','active')"%(id,subcat)
			lid=insert(q)
			return redirect(url_for('admin.admin_manage_subcat',id=id,cat=cat))

	q="select * from subcategory where category_id='%s'"%(id)
	res=select(q)
	if res:
		data['subcategory']=res
		print(res)
	if 'action' in request.args:
		action=request.args['action']
		subid=request.args['subid']
	else:
		action=None

	if action=='update':
		q="select * from subcategory where subcategory_id='%s'"%(subid)
		data['updater']=select(q)
	if action=='active':
		q="update subcategory set status='active' where subcategory_id='%s'"%(subid)
		update(q)
		return redirect(url_for('admin.admin_manage_subcat',cat=cat,id=id))
	if action=='inactive':
		q="update subcategory set status='inactive' where subcategory_id='%s'"%(subid)
		update(q)
		return redirect(url_for('admin.admin_manage_subcat',cat=cat,id=id))
	if 'update' in request.form:
		subcat=request.form['subcat']
		q="update subcategory set subcategory='%s' where subcategory_id='%s'"%(subcat,subid)
		update(q)
		return redirect(url_for('admin.admin_manage_subcat',cat=cat,id=id))
	return render_template('admin_manage_subcat.html',data=data)




@admin.route('/adminmanage_venpro',methods=['get','post'])
def adminmanage_venpro():
	data={}
	id=request.args['id']
	q="select * from vendor where vendor_id='%s'"%(id)
	res=select(q)
	data['vname']=res[0]['vname']
	data['id']=id
	q="select * from product inner join brand using(brand_id) inner join subcategory using(subcategory_id) inner join category using(category_id) where product.status='active'"
	res=select(q)
	data['pro']=res

	q="select * from vendorproduct inner join product using(product_id) inner join brand using(brand_id) inner join subcategory using(subcategory_id) inner join category using(category_id)  where vendor_id='%s'"%(id)
	print(q)
	res=select(q)
	data['assignedpro']=res
	
	if 'action' in request.args:
		action=request.args['action']
		pid=request.args['pid']
	else:
		action=None
	
	if action=='assign':
		q="select * from vendorproduct where product_id='%s' and vendor_id='%s'"%(pid,id)
		res=select(q)
		if res:
			flash("ALREADY ASSIGNED")
			return redirect(url_for('admin.adminmanage_venpro',id=id))
		else:
			q="insert into vendorproduct values(NULL,'%s','%s','active')"%(pid,id)
			insert(q)
			return redirect(url_for('admin.adminmanage_venpro',id=id))
	if 'action2' in request.args:
		action2=request.args['action2']
		vpid=request.args['vpid']
		
		if action2=='active':
			q="update vendorproduct set vpstatus='active' where vproduct_id='%s'"%(vpid)
			update(q)
			return redirect(url_for('admin.adminmanage_venpro',id=id))
		if action2=='inactive':
			q="update vendorproduct set vpstatus='inactive' where vproduct_id='%s'"%(vpid)
			update(q)
			return redirect(url_for('admin.adminmanage_venpro',id=id))

		if action2=='remove':	
			q="delete from vendorproduct where vproduct_id='%s'"%(vpid)
			delete(q)
			flash("REMOVED SUCESSFULLY")
			return redirect(url_for('admin.adminmanage_venpro',id=id))

	return render_template('adminmanage_venpro.html',data=data)


@admin.route('/admin_view_products',methods=['get','post'])
def admin_view_products():
	data={}
	q="select * from product inner join brand using(brand_id) inner join subcategory using(subcategory_id) inner join category using(category_id)"
	res=select(q)
	data['pro']=res
	if 'submit' in request.form:
		search=request.form['search']+'%'
		q="select * from product inner join brand using(brand_id) inner join subcategory using(subcategory_id) inner join category using(category_id) where  product like '%s'"%(search)
		res=select(q)
		if res:
			data['pro']=res
		else:
			flash("NO RESULTS FOUND")
			return redirect(url_for('admin.admin_view_products'))
	return render_template('admin_view_products.html',data=data)





# @admin.route('/admin_view_orders',methods=['get','post'])
# def admin_view_orders():
	
# 	data={}
# 	q="select *,purchasemaster.status as pmstatus from purchasemaster inner join staff using(staff_id) inner join purchasechild using(pmaster_id) inner join vendorproduct using(vproduct_id) inner join vendor using(vendor_id) where purchasemaster.status in ('ordered','delivered')"
# 	res=select(q)
# 	data['orders']=res
# 	print(res)
# 	if 'action' in request.args:
# 		action=request.args['action']
# 		pmaster_id=request.args['pmaster_id'] 
# 	else:
# 		action=None
# 	if action=='products':
# 		q="SELECT *,purchasechild.quantity AS orqua FROM purchasechild INNER JOIN `purchasemaster` USING(`pmaster_id`)  INNER JOIN vendorproduct  USING (vproduct_id) inner join product using(product_id) inner join subcategory using(subcategory_id) inner join category using(category_id) inner join brand using(brand_id)  WHERE `purchasemaster`.pmaster_id='%s'"%(pmaster_id)
# 		res=select(q)
# 		data['products']=res
# 		print(res)
# 	if action=='delivered':
# 		q="update purchasemaster set status='delivered' where pmaster_id='%s'"%(pmaster_id)
# 		update(q)
# 		return redirect(url_for('admin.admin_view_orders'))
	
# 	return render_template('admin_view_orders.html',data=data)


@admin.route('/admin_view_bookings',methods=['get','post'])
def admin_view_bookings():
	
	data={}
	q="select *,ordermaster.status as omstatus from ordermaster inner join customer using(customer_id) where status in('ordered','delivered')"
	res=select(q)
	data['orders']=res
	session['mains']=q
	q="select *,ordermaster.status as omstatus,sum(total) as sum from ordermaster inner join customer using(customer_id) where status in('ordered','delivered')"
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
		return redirect(url_for('admin.admin_view_bookings'))
	if 'submit' in request.form:
		from_date=request.form['from_date']
		to_date=request.form['to_date']
		q="select *,ordermaster.status as omstatus from ordermaster inner join customer using(customer_id) where status in('ordered','delivered') and( date between '%s' and '%s')"%(from_date,to_date)
		print(q)
		session['mains']=q
		res=select(q)
		data['orders']=res
		print(res)
		q="select *,ordermaster.status as omstatus,sum(total) as sum from ordermaster inner join customer using(customer_id) where status in('ordered','delivered') and( date between '%s' and '%s')"%(from_date,to_date)
		print(q)
		res=select(q)
		data['total']=res[0]['sum']
		session['sum']=data['total']
		

	return render_template('admin_view_bookings.html',data=data)


@admin.route('/admin_print',methods=['get','post'])
def admin_print():
	data={}


	res=select(session['mains'])
	data['booking']=res
	data['total']=session['sum']
	
	return render_template('admin_print.html',data=data)



@admin.route('/admin_print_purchase',methods=['get','post'])
def admin_print_purchase():
	data={}
	q="SELECT * FROM  `purchasemaster`  INNER JOIN product USING(product_id) INNER JOIN vendor USING(vendor_id)"
	data['purchase']=select(q)
	print(data['purchase'])

	if 'submit' in request.form:
		from_date=request.form['from_date']
		to_date=request.form['to_date']
		print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

		q="SELECT * FROM  `purchasemaster`  INNER JOIN product USING(product_id) INNER JOIN vendor USING(vendor_id) where( date between '%s' and '%s')"%(from_date,to_date)
		print(q)
		res=select(q)
		data['purchase']=res
		print(res)

	return render_template('admin_print_purchase.html',data=data)


@admin.route('/admin_manage_brand',methods=['get','post'])
def admin_manage_brand():
	data={}
	if 'submit' in request.form:
		brand=request.form['brand']
		q="select * from brand where brand='%s'"%(brand)
		res=select(q)
		if res:
			flash('THIS BRAND IS ALREADY ADDED')
			return redirect(url_for('admin.admin_manage_brand'))
		else:
			q="insert into brand values(NULL,'%s','active')"%(brand)
			lid=insert(q)
			return redirect(url_for('admin.admin_manage_brand'))

	q="select * from brand"
	res=select(q)
	if res:
		data['brand']=res
		print(res)
	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
	else:
		action=None

	if action=='active':
		q="update brand set bstatus='active' where brand_id='%s'"%(id)
		update(q)
		return redirect(url_for('admin.admin_manage_brand'))
	if action=='inactive':
		q="update brand set bstatus='inactive' where brand_id='%s'"%(id)
		update(q)
		return redirect(url_for('admin.admin_manage_brand'))

	if action=='update':
		q="select * from brand where brand_id='%s'"%(id)
		data['updater']=select(q)
	if 'update' in request.form:
		brand=request.form['brand']
		q="update brand set brand='%s' where brand_id='%s'"%(brand,id)
		update(q)
		return redirect(url_for('admin.admin_manage_brand'))
	return render_template('admin_manage_brand.html',data=data)



@admin.route('/admin_manage_stock',methods=['get','post'])
def admin_manage_stock():
	data={}
	q="select * from product inner join brand using(brand_id) inner join subcategory using(subcategory_id) inner join category using(category_id)"
	res=select(q)
	data['pro']=res
	print(res)
	return render_template('admin_manage_stock.html',data=data)


@admin.route('/admin_view_provendor',methods=['get','post'])
def admin_view_provendor():
	data={}
	
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
		q="select * from purchasemaster where staff_id='0' and status='pending'"
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
					return redirect(url_for('admin.admin_view_provendor',pid=pid,pname=pname))
				else:
					q="insert into purchasechild values(NULL,'%s','%s','%s','1')"%(pmaster_id,vpid,pamt)
					insert(q)
					q="update purchasemaster set total=total+'%s' where  pmaster_id='%s'"%(pamt,pmaster_id)
					update(q)
					flash("ADDED TO CART")
					return redirect(url_for('admin.admin_view_provendor',pid=pid,pname=pname))
			else:
				flash("YOU CAN PURCHASE FROM A SINGLE VENDOR AT TIME IF YOU WANT TO PURCHASE PLEASE CLEAR CART")
				return redirect(url_for('admin.admin_view_provendor',pid=pid,pname=pname))
		else:
			q="insert into purchasemaster values(NULL,'%s','%s',NOW(),'pending')"%(0,pamt)
			pmaster_id=insert(q)
			q="insert into purchasechild values(NULL,'%s','%s','%s','1')"%(pmaster_id,vpid,pamt)
			insert(q)
			flash("ADDED TO CART")
			return redirect(url_for('admin.admin_view_provendor',pid=pid,pname=pname))
	return render_template('admin_view_provendor.html',data=data)



@admin.route('/admin_make_purchase',methods=['get','post'])
def admin_make_purchase():
	data={}
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

		q="INSERT INTO `purchasemaster` VALUES(NULL,'0','%s',CURDATE(),'%s','%s','%s')"%(vendors,product_id,pqnty,ptotal)
		insert(q)
		# q="INSERT INTO `purchase_child` VALUES(NULL,'%s','%s','%s','%s','%s','%s','%s','%s')"%(mp_id,vendors,item_id,pqnty,ptotal)
		# insert(q)
		q="UPDATE `product` SET `quantity`=`quantity`+'%s' WHERE `product_id`='%s'"%(pqnty,product_id)
		update(q)
		flash("STOCK UPDATED")
		return redirect(url_for("admin.admin_manage_stock"))
 
	return render_template('admin_make_purchase.html',data=data)



@admin.route('/admin_view_cart',methods=['get','post'])
def admin_view_cart():
	data={}


	q="SELECT *,purchasechild.quantity as purqua FROM purchasechild INNER JOIN `purchasemaster` USING(`pmaster_id`) INNER JOIN vendorproduct using(vproduct_id) inner join vendor using(vendor_id) inner join product USING(`product_id`) WHERE `purchasemaster`.`staff_id`='%s' AND `purchasemaster`.`status`='pending'"%(0)
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
		return redirect(url_for('admin.admin_view_cart'))
	if action=='delete':
		q="delete from purchasechild where vproduct_id='%s' and pmaster_id='%s' "%(vpid,pmastid)
		delete(q)
		q="update purchasemaster set total=total-'%s' where pmaster_id='%s'"%(puramt,pmastid)
		update(q)
		q="SELECT * FROM `purchasemaster` INNER JOIN `purchasechild` USING(`pmaster_id`) WHERE  `purchasechild`.`pmaster_id`='%s'"%(pmastid)
		print(q)
		res=select(q)
		if res:
			return redirect(url_for("admin.admin_view_cart"))
		else:
			q="delete from `purchasemaster` where pmaster_id='%s'"%(pmastid)
			delete(q)
			return redirect(url_for('admin.admin_view_cart'))	

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
			return redirect(url_for("admin.admin_view_cart"))
			
	return render_template("admin_view_cart.html",data=data)


