/*
SQLyog Community v13.1.7 (64 bit)
MySQL - 5.5.20-log : Database - bike_accessories_shop
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`bike_accessories_shop` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `bike_accessories_shop`;

/*Table structure for table `brand` */

DROP TABLE IF EXISTS `brand`;

CREATE TABLE `brand` (
  `brand_id` int(11) NOT NULL AUTO_INCREMENT,
  `brand` varchar(50) DEFAULT NULL,
  `bstatus` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`brand_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `brand` */

insert  into `brand`(`brand_id`,`brand`,`bstatus`) values 
(1,'b1','inactive'),
(2,'b2','active'),
(3,'b3','inactive');

/*Table structure for table `category` */

DROP TABLE IF EXISTS `category`;

CREATE TABLE `category` (
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `category` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `category` */

insert  into `category`(`category_id`,`category`,`status`) values 
(1,'cat1','active'),
(2,'cat2','active');

/*Table structure for table `customer` */

DROP TABLE IF EXISTS `customer`;

CREATE TABLE `customer` (
  `customer_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `firstname` varchar(50) DEFAULT NULL,
  `lastname` varchar(50) DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `gender` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`customer_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `customer` */

insert  into `customer`(`customer_id`,`username`,`firstname`,`lastname`,`place`,`phone`,`email`,`gender`) values 
(1,'sethu','sethu','sethu','ertyu','23456789','buyer@gmail.com','Male');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `username` varchar(50) NOT NULL,
  `password` varchar(50) DEFAULT NULL,
  `usertype` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`username`,`password`,`usertype`) values 
('jifin','jifin','staff'),
('admin','admin','admin'),
('sethu','sethu','customer');

/*Table structure for table `orderchild` */

DROP TABLE IF EXISTS `orderchild`;

CREATE TABLE `orderchild` (
  `ochild_id` int(11) NOT NULL AUTO_INCREMENT,
  `omaster_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `amount` varchar(50) DEFAULT NULL,
  `quantity` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ochild_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `orderchild` */

insert  into `orderchild`(`ochild_id`,`omaster_id`,`product_id`,`amount`,`quantity`) values 
(1,1,1,'500','1'),
(2,2,1,'500','1'),
(3,3,1,'1500','3'),
(4,3,2,'500','1');

/*Table structure for table `ordermaster` */

DROP TABLE IF EXISTS `ordermaster`;

CREATE TABLE `ordermaster` (
  `omaster_id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_id` int(11) DEFAULT NULL,
  `total` varchar(50) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`omaster_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `ordermaster` */

insert  into `ordermaster`(`omaster_id`,`customer_id`,`total`,`date`,`status`) values 
(1,1,'500','2022-02-17','delivered'),
(2,1,'500','2022-03-02','ordered'),
(3,1,'2000','2022-03-21','delivered');

/*Table structure for table `payment` */

DROP TABLE IF EXISTS `payment`;

CREATE TABLE `payment` (
  `payment_id` int(11) NOT NULL AUTO_INCREMENT,
  `omaster_id` int(11) DEFAULT NULL,
  `amount` varchar(50) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`payment_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `payment` */

insert  into `payment`(`payment_id`,`omaster_id`,`amount`,`date`) values 
(1,1,'500','2022-02-17 21:48:10'),
(2,2,'500','2022-03-02 10:35:38'),
(3,3,'2000','2022-03-21 20:52:33');

/*Table structure for table `product` */

DROP TABLE IF EXISTS `product`;

CREATE TABLE `product` (
  `product_id` int(11) NOT NULL AUTO_INCREMENT,
  `subcategory_id` int(11) DEFAULT NULL,
  `brand_id` int(11) DEFAULT NULL,
  `product` varchar(50) DEFAULT NULL,
  `image` varchar(50) DEFAULT NULL,
  `rate` varchar(50) DEFAULT NULL,
  `quantity` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`product_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `product` */

insert  into `product`(`product_id`,`subcategory_id`,`brand_id`,`product`,`image`,`rate`,`quantity`,`status`) values 
(1,2,2,'p1','static/6692a5e3-d5a7-47b9-89da-779d3d3fec27b6.jpg','500','17','active'),
(2,2,2,'p2','static/d35e87c8-fa74-4c9f-83b8-40ef053fd2fbb3.jpg','500','4','active'),
(3,NULL,NULL,NULL,NULL,NULL,NULL,NULL);

/*Table structure for table `purchasechild` */

DROP TABLE IF EXISTS `purchasechild`;

CREATE TABLE `purchasechild` (
  `purchasechild_id` int(11) NOT NULL AUTO_INCREMENT,
  `pmaster_id` int(11) DEFAULT NULL,
  `vproduct_id` int(11) DEFAULT NULL,
  `amount` varchar(50) DEFAULT NULL,
  `quantity` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`purchasechild_id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

/*Data for the table `purchasechild` */

insert  into `purchasechild`(`purchasechild_id`,`pmaster_id`,`vproduct_id`,`amount`,`quantity`) values 
(1,1,1,'1000','2'),
(2,2,1,'500','1'),
(3,3,1,'2500','5'),
(4,4,1,'3000','6'),
(5,5,1,'2000','4'),
(6,6,1,'500','1'),
(7,7,1,'1000','2'),
(8,8,3,'2500','5'),
(9,8,1,'1000','2'),
(10,9,1,'500','1'),
(11,9,3,'500','1');

/*Table structure for table `purchasemaster` */

DROP TABLE IF EXISTS `purchasemaster`;

CREATE TABLE `purchasemaster` (
  `pmaster_id` int(11) NOT NULL AUTO_INCREMENT,
  `staff_id` int(11) DEFAULT NULL,
  `total` varchar(50) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`pmaster_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

/*Data for the table `purchasemaster` */

insert  into `purchasemaster`(`pmaster_id`,`staff_id`,`total`,`date`,`status`) values 
(1,1,'1000','2-2-2102','delivered'),
(2,1,'500','2022-02-17 21:28:08','delivered'),
(3,1,'2500','2022-03-21 12:42:49','delivered'),
(4,1,'3000','2022-03-21 14:19:00','ordered'),
(5,0,'2000','2022-03-21 16:00:04','ordered'),
(6,1,'500','2022-03-21 16:05:09','ordered'),
(7,1,'1000','2022-03-21 16:06:11','ordered'),
(8,0,'3500','2022-03-21 20:48:42','ordered'),
(9,0,'1000','2022-03-21 20:49:49','ordered');

/*Table structure for table `staff` */

DROP TABLE IF EXISTS `staff`;

CREATE TABLE `staff` (
  `staff_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `firstname` varchar(50) DEFAULT NULL,
  `lastname` varchar(50) DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`staff_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `staff` */

insert  into `staff`(`staff_id`,`username`,`firstname`,`lastname`,`place`,`phone`,`email`) values 
(1,'jifin','jifi','staff','wet','23456','joyelroy24@gmail.com');

/*Table structure for table `subcategory` */

DROP TABLE IF EXISTS `subcategory`;

CREATE TABLE `subcategory` (
  `subcategory_id` int(11) NOT NULL AUTO_INCREMENT,
  `category_id` int(11) DEFAULT NULL,
  `subcategory` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`subcategory_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `subcategory` */

insert  into `subcategory`(`subcategory_id`,`category_id`,`subcategory`,`status`) values 
(1,1,'cat1sub1','inactive'),
(2,1,'cat1sub2','active'),
(3,2,'cat2sub','active');

/*Table structure for table `vehicle` */

DROP TABLE IF EXISTS `vehicle`;

CREATE TABLE `vehicle` (
  `vehicle_id` int(11) NOT NULL AUTO_INCREMENT,
  `vehiclename` varchar(100) DEFAULT NULL,
  `image` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`vehicle_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `vehicle` */

/*Table structure for table `vendor` */

DROP TABLE IF EXISTS `vendor`;

CREATE TABLE `vendor` (
  `vendor_id` int(11) NOT NULL AUTO_INCREMENT,
  `vname` varchar(50) DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`vendor_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `vendor` */

insert  into `vendor`(`vendor_id`,`vname`,`place`,`phone`,`email`,`status`) values 
(1,'stervi','ruyru','23456789','ityuj@g','active'),
(2,'ar','ew','fgt','sdf','active');

/*Table structure for table `vendorproduct` */

DROP TABLE IF EXISTS `vendorproduct`;

CREATE TABLE `vendorproduct` (
  `vproduct_id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) DEFAULT NULL,
  `vendor_id` int(11) DEFAULT NULL,
  `vpstatus` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`vproduct_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `vendorproduct` */

insert  into `vendorproduct`(`vproduct_id`,`product_id`,`vendor_id`,`vpstatus`) values 
(1,1,1,'active'),
(2,2,2,'inactive'),
(3,2,1,'active');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
