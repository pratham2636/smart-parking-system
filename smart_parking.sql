-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: smart_parking
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
-- Table structure for table `bookings`
--

DROP TABLE IF EXISTS `bookings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bookings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `parking_id` int DEFAULT NULL,
  `slot_no` int DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `amount_paid` int DEFAULT NULL,
  `payment_method` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookings`
--

LOCK TABLES `bookings` WRITE;
/*!40000 ALTER TABLE `bookings` DISABLE KEYS */;
INSERT INTO `bookings` VALUES (1,1,1,1,'2026-04-14 17:30:00','2026-04-14 18:00:00','expired',10,NULL),(2,1,1,2,'2026-04-14 17:30:00','2026-04-14 18:00:00','expired',10,NULL),(3,1,1,3,'2026-04-14 17:30:00','2026-04-14 17:35:00','expired',1,NULL),(4,1,1,4,'2026-04-14 17:30:00','2026-04-14 17:35:00','expired',1,NULL),(5,1,1,5,'2026-04-14 17:30:00','2026-04-14 17:35:00','expired',1,NULL),(6,1,1,6,'2026-04-14 17:30:00','2026-04-14 17:35:00','expired',1,NULL),(7,1,1,7,'2026-04-14 17:30:00','2026-04-14 17:35:00','expired',1,NULL),(8,1,1,8,'2026-04-14 17:30:00','2026-04-14 17:35:00','expired',1,NULL),(9,1,1,9,'2026-04-14 16:36:00','2026-04-14 17:35:00','expired',19,NULL),(10,1,1,10,'2026-04-14 16:36:00','2026-04-14 16:38:00','expired',0,NULL),(11,1,2,1,'2026-04-14 16:39:00','2026-04-14 16:41:00','expired',0,NULL),(12,1,1,11,'2026-04-17 15:43:00','2026-04-17 15:44:00','expired',0,NULL),(13,1,1,12,'2026-04-17 15:44:00','2026-04-17 15:45:00','expired',0,NULL),(14,1,1,1,'2026-04-17 15:53:00','2026-04-17 15:55:00','expired',0,NULL),(15,1,3,1,'2026-04-23 17:15:00','2026-04-23 17:16:00','expired',10,'UPI');
/*!40000 ALTER TABLE `bookings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parking`
--

DROP TABLE IF EXISTS `parking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parking` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `location` varchar(200) DEFAULT NULL,
  `total_slots` int DEFAULT NULL,
  `reserved_slots` int DEFAULT NULL,
  `available_slots` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parking`
--

LOCK TABLES `parking` WRITE;
/*!40000 ALTER TABLE `parking` DISABLE KEYS */;
INSERT INTO `parking` VALUES (1,'Mall Parking','Delhi',20,5,15),(2,'Metro Parking','Noida',20,3,17),(3,'Pacific Mall','Subhash Nagar, Delhi',50,10,40);
/*!40000 ALTER TABLE `parking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `role` varchar(20) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Pratham','pratham@gmail.com','12345','user','7428570268','2026-04-17 19:05:51'),(2,'Admin','admin@gmail.com','1234','admin',NULL,'2026-04-17 19:05:51'),(8,'Devanshi','devanshi@gmail.com','1234','user',NULL,'2026-04-17 19:05:51'),(9,'Kunal','kunal@gmail.com','1234','user',NULL,'2026-04-17 19:05:51');
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

-- Dump completed on 2026-04-23 17:27:32
