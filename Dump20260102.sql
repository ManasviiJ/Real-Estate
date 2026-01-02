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
-- Table structure for table `interested_users`
--

DROP TABLE IF EXISTS `interested_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interested_users` (
  `tenant_username` varchar(100) NOT NULL,
  `property_id` varchar(100) NOT NULL,
  `transaction_type` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`tenant_username`,`property_id`),
  KEY `property_id` (`property_id`),
  CONSTRAINT `interested_users_ibfk_1` FOREIGN KEY (`tenant_username`) REFERENCES `users` (`username`),
  CONSTRAINT `interested_users_ibfk_2` FOREIGN KEY (`property_id`) REFERENCES `properties` (`property_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interested_users`
--

LOCK TABLES `interested_users` WRITE;
/*!40000 ALTER TABLE `interested_users` DISABLE KEYS */;
/*!40000 ALTER TABLE `interested_users` ENABLE KEYS */;
UNLOCK TABLES;

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
INSERT INTO `properties` VALUES ('LRVGA0001','manasvi@gmail.com','Villa','Panaji','Sagarkila VIlla','4th Cross Main Road',10000.00,4),('SRIKA0001','manasvi@gmail.com','Independent House','Bangalore','Serenity Haven','Avenue Street 15, Whitefield',110000000.00,3);
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
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `res_prop_det`
--

LOCK TABLES `res_prop_det` WRITE;
/*!40000 ALTER TABLE `res_prop_det` DISABLE KEYS */;
INSERT INTO `res_prop_det` VALUES (24,'SRIKA0001',2500,'Furnished',1,12,'Luxury house in whitefield.'),(26,'LRVGA0001',2100,'Semi-furnished',1,3,'Ready to move house for rent');
/*!40000 ALTER TABLE `res_prop_det` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `res_prop_img`
--

DROP TABLE IF EXISTS `res_prop_img`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `res_prop_img` (
  `sno` int NOT NULL AUTO_INCREMENT,
  `property_id` char(10) DEFAULT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`sno`),
  KEY `property_id` (`property_id`),
  CONSTRAINT `res_prop_img_ibfk_1` FOREIGN KEY (`property_id`) REFERENCES `properties` (`property_id`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `res_prop_img`
--

LOCK TABLES `res_prop_img` WRITE;
/*!40000 ALTER TABLE `res_prop_img` DISABLE KEYS */;
INSERT INTO `res_prop_img` VALUES (50,'SRIKA0001','images\\prop_res\\sh_bangalore (1).jpg'),(51,'SRIKA0001','images\\prop_res\\sh_bangalore (2).jpg'),(52,'SRIKA0001','images\\prop_res\\sh_bangalore (3).jpg'),(56,'LRVGA0001','images\\prop_res\\sv_panaji (2).png'),(57,'LRVGA0001','images\\prop_res\\sv_panaji(1).png'),(58,'LRVGA0001','images\\prop_res\\sv_panaji(3).png');
/*!40000 ALTER TABLE `res_prop_img` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tenant_favorites`
--

DROP TABLE IF EXISTS `tenant_favorites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tenant_favorites` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tenant_username` varchar(60) DEFAULT NULL,
  `property_id` char(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_favorite` (`tenant_username`,`property_id`),
  KEY `property_id` (`property_id`),
  CONSTRAINT `tenant_favorites_ibfk_1` FOREIGN KEY (`tenant_username`) REFERENCES `users` (`username`),
  CONSTRAINT `tenant_favorites_ibfk_2` FOREIGN KEY (`property_id`) REFERENCES `properties` (`property_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tenant_favorites`
--

LOCK TABLES `tenant_favorites` WRITE;
/*!40000 ALTER TABLE `tenant_favorites` DISABLE KEYS */;
/*!40000 ALTER TABLE `tenant_favorites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tenant_properties`
--

DROP TABLE IF EXISTS `tenant_properties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tenant_properties` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tenant_username` varchar(60) DEFAULT NULL,
  `property_id` char(10) DEFAULT NULL,
  `transaction_type` enum('rented','bought') DEFAULT NULL,
  `transaction_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `tenant_username` (`tenant_username`),
  KEY `property_id` (`property_id`),
  CONSTRAINT `tenant_properties_ibfk_1` FOREIGN KEY (`tenant_username`) REFERENCES `users` (`username`),
  CONSTRAINT `tenant_properties_ibfk_2` FOREIGN KEY (`property_id`) REFERENCES `properties` (`property_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tenant_properties`
--

LOCK TABLES `tenant_properties` WRITE;
/*!40000 ALTER TABLE `tenant_properties` DISABLE KEYS */;
/*!40000 ALTER TABLE `tenant_properties` ENABLE KEYS */;
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
INSERT INTO `users` VALUES ('Deekshitha','duck@gmail.com','duck','6767676767','Tenant','images\\pfp\\deekshitha_new.png'),('Manasvi','manasvi@gmail.com','man','7676663548','Owner','images\\pfp\\superhero.png');
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

-- Dump completed on 2026-01-02 23:07:23
