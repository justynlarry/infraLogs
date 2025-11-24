mysqldump: [Warning] Using a password on the command line interface can be insecure.
-- MySQL dump 10.13  Distrib 9.5.0, for Linux (x86_64)
--
-- Host: localhost    Database: infralogDb01
-- ------------------------------------------------------
-- Server version	9.5.0

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
Warning: A partial dump from a server that has GTIDs will by default include the GTIDs of all transactions, even those that changed suppressed parts of the database. If you don't want to restore GTIDs, pass --set-gtid-purged=OFF. To make a complete dump, pass --all-databases --triggers --routines --events. 
Warning: A dump from a server that has GTIDs enabled will by default include the GTIDs of all transactions, even those that were executed during its extraction and might not be represented in the dumped data. This might result in an inconsistent data dump. 
In order to ensure a consistent backup of the database, pass --single-transaction or --lock-all-tables or --source-data. 
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '1eea7703-b11b-11f0-a4bd-3e3775c15193:1-59';

--
-- Table structure for table `critical_logs`
--

DROP TABLE IF EXISTS `critical_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `critical_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `record_time` datetime NOT NULL,
  `message` text,
  `hostname` varchar(255) DEFAULT NULL,
  `command_name` varchar(255) DEFAULT NULL,
  `process_id` int DEFAULT NULL,
  `priority` int DEFAULT NULL,
  `syslog_id` varchar(255) DEFAULT NULL,
  `report_host` varchar(255) NOT NULL,
  `report_date` date NOT NULL,
  `report_uuid` varchar(64) NOT NULL,
  `imported_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `record_time` (`record_time`),
  UNIQUE KEY `uniq_log` (`record_time`,`hostname`,`command_name`,`process_id`,`report_uuid`),
  KEY `idx_logs_host_date` (`report_host`,`report_date`),
  KEY `idx_logs_record_time` (`record_time`),
  KEY `idx_logs_uuid` (`report_uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=1403 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `failed_ssh`
--

DROP TABLE IF EXISTS `failed_ssh`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `failed_ssh` (
  `id` int NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `source_ip` varchar(45) NOT NULL,
  `source_port` smallint unsigned NOT NULL,
  `attempted_user` varchar(255) NOT NULL,
  `log_line` text NOT NULL,
  `failure_type` enum('failed_password','invalid_user','connection_closed') DEFAULT NULL,
  `invalid_user` tinyint(1) DEFAULT '0',
  `report_host` varchar(255) NOT NULL,
  `report_date` date NOT NULL,
  `report_uuid` varchar(36) NOT NULL,
  `imported_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_failed_ssh_host_date` (`report_host`,`report_date`),
  KEY `idx_failed_ssh_uuid` (`report_uuid`),
  KEY `idx_failed_ssh_source_ip` (`source_ip`),
  KEY `idx_failed_ssh_timestamp` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `failed_svcs`
--

DROP TABLE IF EXISTS `failed_svcs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `failed_svcs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `unit` varchar(255) NOT NULL,
  `svc_load` varchar(255) NOT NULL,
  `active` varchar(255) NOT NULL,
  `sub` varchar(255) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `report_host` varchar(255) NOT NULL,
  `report_date` date NOT NULL,
  `report_uuid` varchar(64) NOT NULL,
  `imported_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_storage_host_date` (`report_host`,`report_date`),
  KEY `idx_storage_uuid` (`report_uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=469 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `storage_logs`
--

DROP TABLE IF EXISTS `storage_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `storage_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `filesystem` varchar(255) NOT NULL,
  `size` varchar(64) DEFAULT NULL,
  `used` varchar(64) DEFAULT NULL,
  `avail` varchar(64) DEFAULT NULL,
  `use_percentage` varchar(32) DEFAULT NULL,
  `mounted_on` varchar(255) DEFAULT NULL,
  `report_host` varchar(255) NOT NULL,
  `report_date` date NOT NULL,
  `report_uuid` varchar(64) NOT NULL,
  `imported_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_storage_record` (`filesystem`,`mounted_on`,`report_date`,`report_uuid`),
  KEY `idx_storage_host_date` (`report_host`,`report_date`),
  KEY `idx_storage_uuid` (`report_uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=966 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-24 22:29:37
