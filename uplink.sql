-- MariaDB dump 10.19  Distrib 10.6.5-MariaDB, for Linux (x86_64)
--
-- Host: 10.0.0.254    Database: uplink
-- ------------------------------------------------------
-- Server version	10.5.12-MariaDB-0+deb11u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `log`
--

DROP TABLE IF EXISTS `log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` int(11) NOT NULL,
  `date` date DEFAULT NULL,
  `time` time DEFAULT NULL,
  `uptime` int(11) DEFAULT NULL,
  `internal_ip` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `external_ip` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `external_ipv6` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_linked` tinyint(1) DEFAULT NULL,
  `is_connected` tinyint(1) DEFAULT NULL,
  `str_transmission_rate_up` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `str_transmission_rate_down` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `str_max_bit_rate_up` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `str_max_bit_rate_down` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `str_max_linked_bit_rate_up` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `str_max_linked_bit_rate_down` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `modelname` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `system_version` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `provider` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `message` varchar(2048) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `source_host` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=798844 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'uplink'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-12-27  1:40:08
