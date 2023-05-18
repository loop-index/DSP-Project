-- MySQL dump 10.13  Distrib 8.0.33, for Linux (x86_64)
--
-- Host: localhost    Database: test
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `test`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `test` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `test`;

--
-- Table structure for table `advertiser`
--

DROP TABLE IF EXISTS `advertiser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `advertiser` (
  `advertiser_id` int NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`advertiser_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `advertiser`
--

LOCK TABLES `advertiser` WRITE;
/*!40000 ALTER TABLE `advertiser` DISABLE KEYS */;
INSERT INTO `advertiser` VALUES (1458,'Dazzling Mart','Chinese vertical e-commerce'),(2259,'NutriBlend','Milk powder'),(2261,'CommuniCall','Telecom'),(2821,'SoleMates','Footwear'),(2997,'Appify','Mobile e-commerce app install'),(3358,'InnovaTech','Software'),(3386,'Global Connections','International e-commerce'),(3427,'PetroPrime','Oil'),(3476,'WheelWorks','Tire');
/*!40000 ALTER TABLE `advertiser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `campaign`
--

DROP TABLE IF EXISTS `campaign`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `campaign` (
  `campaign_id` int NOT NULL,
  `advertiser_id` int DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `budget` decimal(10,2) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`campaign_id`),
  KEY `advertiser_id` (`advertiser_id`),
  CONSTRAINT `campaign_ibfk_1` FOREIGN KEY (`advertiser_id`) REFERENCES `advertiser` (`advertiser_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `campaign`
--

LOCK TABLES `campaign` WRITE;
/*!40000 ALTER TABLE `campaign` DISABLE KEYS */;
INSERT INTO `campaign` VALUES (1,1458,'Summer Sale','2023-01-01','2023-06-30',10000.00,'Active','2023-05-18 19:57:33'),(2,1458,'Holiday Special','2023-01-01','2023-12-31',15000.00,'Active','2023-05-18 19:57:33'),(3,3358,'Product Launch','2023-01-01','2023-08-15',5000.00,'Active','2023-05-18 19:57:40'),(4,3386,'International Expansion','2023-01-01','2024-02-29',25000.00,'Active','2023-05-18 19:57:45'),(5,3386,'Black Friday Sale','2023-01-01','2023-11-30',10000.00,'Active','2023-05-18 19:57:45'),(6,3427,'New Product Launch','2023-01-01','2023-09-30',8000.00,'Active','2023-05-18 19:57:53'),(7,3476,'Seasonal Tire Sale','2023-01-01','2023-05-31',5000.00,'Active','2023-05-18 19:57:58'),(8,3476,'Winter Tire Promotion','2023-01-01','2023-11-15',6000.00,'Active','2023-05-18 19:57:58'),(9,2259,'Healthy Growth','2023-01-01','2023-12-31',12000.00,'Active','2023-05-18 19:58:03'),(10,2261,'Unlimited Data Plan','2023-01-01','2023-12-31',20000.00,'Active','2023-05-18 19:58:09'),(11,2821,'Summer Collection','2023-01-01','2023-08-31',6000.00,'Active','2023-05-18 19:58:44'),(12,2821,'Year-End Clearance','2023-01-01','2023-12-31',8000.00,'Active','2023-05-18 19:58:48'),(13,2997,'App Launch Promotion','2023-01-01','2023-10-15',5000.00,'Active','2023-05-18 19:58:53'),(14,2997,'Holiday Install Special','2023-01-01','2023-12-31',6000.00,'Active','2023-05-18 19:58:53');
/*!40000 ALTER TABLE `campaign` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interest_groups`
--

DROP TABLE IF EXISTS `interest_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interest_groups` (
  `main_key` varchar(255) NOT NULL,
  `interests` text,
  `users` text,
  PRIMARY KEY (`main_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interest_groups`
--

LOCK TABLES `interest_groups` WRITE;
/*!40000 ALTER TABLE `interest_groups` DISABLE KEYS */;
INSERT INTO `interest_groups` VALUES ('art','art,photography','2,4,7,12,15,19,22'),('basketball','basketball,soccer,football','4,5,8,12,14,16,18,20,23'),('books','books','10'),('cars','cars','8'),('cooking','cooking','5,9,15,21'),('dancing','dancing','7,11,19'),('fashion','fashion','9'),('fitness','fitness,yoga','8,13,16,20'),('gaming','gaming','3,6,12,14,18'),('hiking','hiking','1,5,10,17,22'),('movies','movies,anime','3,6,9,13,17,21'),('music','music,guitar','2,4,10,11,14,16,18,22,23'),('programming','programming','1'),('reading','reading','1,6,13,17,21'),('traveling','traveling,travel','3,7,11,15,20,23');
/*!40000 ALTER TABLE `interest_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `gender` enum('Male','Female','Other') DEFAULT NULL,
  `interests` text,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'John',22,'Male','[\"Programming\", \"Hiking\", \"Reading\"]'),(2,'Jane',19,'Female','[\"Art\", \"Music\", \"Photography\"]'),(3,'David',25,'Male','[\"Gaming\", \"Movies\", \"Traveling\"]'),(4,'John Doe',20,'Male','[\"Basketball\", \"Music\", \"Photography\"]'),(5,'Jane Smith',23,'Female','[\"Soccer\", \"Cooking\", \"Hiking\"]'),(6,'Alex Rodriguez',21,'Male','[\"Gaming\", \"Anime\", \"Reading\"]'),(7,'Maria Garcia',19,'Female','[\"Dancing\", \"Travel\", \"Art\"]'),(8,'James Brown',25,'Male','[\"Fitness\", \"Football\", \"Cars\"]'),(9,'Olivia Wilson',22,'Female','[\"Fashion\", \"Movies\", \"Cooking\"]'),(10,'David Lee',24,'Male','[\"Guitar\", \"Books\", \"Hiking\"]'),(11,'Samantha Kim',20,'Female','[\"Music\", \"Travel\", \"Dancing\"]'),(12,'Daniel Chen',21,'Male','[\"Soccer\", \"Gaming\", \"Photography\"]'),(13,'Emily Davis',23,'Female','[\"Yoga\", \"Reading\", \"Movies\"]'),(14,'Michael Jones',22,'Male','[\"Basketball\", \"Music\", \"Gaming\"]'),(15,'Sophia Martinez',21,'Female','[\"Cooking\", \"Travel\", \"Photography\"]'),(16,'William Nguyen',20,'Male','[\"Soccer\", \"Music\", \"Fitness\"]'),(17,'Isabella Perez',22,'Female','[\"Hiking\", \"Reading\", \"Movies\"]'),(18,'Andrew Kim',21,'Male','[\"Basketball\", \"Gaming\", \"Music\"]'),(19,'Mia Johnson',20,'Female','[\"Dancing\", \"Art\", \"Photography\"]'),(20,'Jonathan Davis',24,'Male','[\"Football\", \"Fitness\", \"Travel\"]'),(21,'Avery Taylor',22,'Female','[\"Movies\", \"Cooking\", \"Reading\"]'),(22,'Kevin Lee',21,'Male','[\"Guitar\", \"Hiking\", \"Photography\"]'),(23,'Chloe Brown',23,'Female','[\"Soccer\", \"Music\", \"Travel\"]');
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

-- Dump completed on 2023-05-18 16:59:20
