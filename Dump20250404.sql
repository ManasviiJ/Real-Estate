-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: re_estate
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `loc`
--

DROP TABLE IF EXISTS `loc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `loc` (
  `STATE` varchar(30) DEFAULT NULL,
  `CITY` varchar(30) DEFAULT NULL,
  KEY `CITY` (`CITY`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loc`
--

LOCK TABLES `loc` WRITE;
/*!40000 ALTER TABLE `loc` DISABLE KEYS */;
INSERT INTO `loc` VALUES ('Karnataka','Bangalore'),('Uttar Pradesh','Noida'),('Maharashtra','Mumbai'),('Andhra Pradesh','Vijaywada'),('Kerala','Trivandrum'),('Uttarakhand','Dehradun'),('Delhi NCR','New Delhi'),('Delhi NCR','Old Delhi'),('Tamil Nadu','Chennai'),('Goa','Panaji'),('Telangana','Hyderabad'),('Bihar','Patna'),('Rajasthan','Jaipur'),('Rajasthan','Jaisalmer'),('Haryana','Gurugram');
/*!40000 ALTER TABLE `loc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `properties`
--

DROP TABLE IF EXISTS `properties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `properties` (
  `property_id` char(10) NOT NULL,
  `owner_username` varchar(60) DEFAULT NULL,
  `property_category` enum('Apartment','Independent House','Villa','Commercial','Land/Plot') DEFAULT NULL,
  `location_city` varchar(30) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `rent_price` decimal(15,2) DEFAULT NULL,
  `bhk` int DEFAULT NULL,
  `partners` int DEFAULT NULL,
  PRIMARY KEY (`property_id`),
  KEY `owner_username` (`owner_username`),
  KEY `location_city` (`location_city`),
  CONSTRAINT `properties_ibfk_1` FOREIGN KEY (`owner_username`) REFERENCES `users` (`username`),
  CONSTRAINT `properties_ibfk_2` FOREIGN KEY (`location_city`) REFERENCES `loc` (`CITY`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `properties`
--

LOCK TABLES `properties` WRITE;
/*!40000 ALTER TABLE `properties` DISABLE KEYS */;
INSERT INTO `properties` VALUES ('SRAAP0003','Deekshi@gmail.com','Apartment','Vijaywada','Palatial Heights','Palatial Heights 45, Krishna Riverside Avenue,Benz Circle, Vijayawada, Andhra Pradesh 520008',350000000.00,10,NULL),('SRIUK0001','Deekshi@gmail.com','Independent House','Dehradun','Himalayan Haveli','Cheel Ghosla Cottage, 45 Pine Ridge Road',170000000.00,10,NULL),('SRVGA0002','dio@gmail.com','Villa','Panaji','Sagarkila Villa','Sagarika Villa\n14 Fisherman\'s Wharf Road\nCalangute, Goa 403516\n',250000000.00,10,NULL);
/*!40000 ALTER TABLE `properties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `res_prop_det`
--

DROP TABLE IF EXISTS `res_prop_det`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `res_prop_det` (
  `sno` int NOT NULL AUTO_INCREMENT,
  `property_id` char(10) DEFAULT NULL,
  `area_sqft` int DEFAULT NULL,
  `furnishing_details` enum('Unfurnished','Semi-furnished','Furnished') DEFAULT NULL,
  `parking_availability` tinyint(1) DEFAULT NULL,
  `age_of_property` int DEFAULT NULL,
  `description` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`sno`),
  KEY `property_id` (`property_id`),
  CONSTRAINT `res_prop_det_ibfk_1` FOREIGN KEY (`property_id`) REFERENCES `properties` (`property_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `res_prop_det`
--

LOCK TABLES `res_prop_det` WRITE;
/*!40000 ALTER TABLE `res_prop_det` DISABLE KEYS */;
INSERT INTO `res_prop_det` VALUES (1,'SRAAP0003',7000,'Furnished',1,12,NULL),(2,'SRIUK0001',5000,'Furnished',1,20,NULL),(3,'SRVGA0002',5000,'Furnished',1,15,NULL);
/*!40000 ALTER TABLE `res_prop_det` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `res_prop_img`
--

DROP TABLE IF EXISTS `res_prop_img`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `res_prop_img` (
  `image_id` int NOT NULL AUTO_INCREMENT,
  `property_id` char(10) DEFAULT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`image_id`),
  KEY `property_id` (`property_id`),
  CONSTRAINT `res_prop_img_ibfk_1` FOREIGN KEY (`property_id`) REFERENCES `properties` (`property_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `res_prop_img`
--

LOCK TABLES `res_prop_img` WRITE;
/*!40000 ALTER TABLE `res_prop_img` DISABLE KEYS */;
INSERT INTO `res_prop_img` VALUES (1,'SRIUK0001','images/prop_res/hh_dehradun(1).png'),(2,'SRIUK0001','images/prop_res/hh_dehradun(2).png'),(3,'SRIUK0001','images/prop_res/hh_dehradun(3).png'),(4,'SRVGA0002','images/prop_res/sv_panaji(1).png'),(5,'SRVGA0002','images/prop_res/sv_panaji(2).png'),(6,'SRVGA0002','images/prop_res/sv_panaji(3).png'),(7,'SRAAP0003','images/prop_res/ph_vijaywada(1).png'),(8,'SRAAP0003','images/prop_res/ph_vijaywada(2).png'),(9,'SRAAP0003','images/prop_res/ph_vijaywada(3).png');
/*!40000 ALTER TABLE `res_prop_img` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `name` varchar(30) NOT NULL,
  `username` varchar(60) NOT NULL,
  `password` varchar(30) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `role` varchar(30) DEFAULT NULL,
  `profile_pic` varchar(60) DEFAULT 'images/pfp/superhero.png',
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('Deekshitha','Deekshi@gmail.com','urdum',NULL,'Owner','images\\pfp\\deekshitha_new.png'),('Dio','dio@gmail.com','dio','5676765437','Owner','images\\pfp\\dio.png'),('Irene','Irene@hotmail.com','blu',NULL,'Tenant','images/pfp/superhero.png'),('Manasvi','manasvi@gmail.com','man','7676767676','Tenant','images\\pfp\\manasvi.png'),('Peezo','peezo@cat.in','cat','4545454545','Owner','images\\pfp\\peezo.png');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-04 12:40:13
