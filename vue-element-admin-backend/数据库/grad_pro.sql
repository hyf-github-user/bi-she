/*
 Navicat Premium Data Transfer

 Source Server         : 本地MySQL
 Source Server Type    : MySQL
 Source Server Version : 80025
 Source Host           : localhost:3306
 Source Schema         : grad_pro

 Target Server Type    : MySQL
 Target Server Version : 80025
 File Encoding         : 65001

 Date: 02/12/2021 20:32:10
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
BEGIN;
INSERT INTO `alembic_version` VALUES ('79c9c77eb5f9');
COMMIT;

-- ----------------------------
-- Table structure for permission
-- ----------------------------
DROP TABLE IF EXISTS `permission`;
CREATE TABLE `permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of permission
-- ----------------------------
BEGIN;
INSERT INTO `permission` VALUES (6, 'ADMINISTER');
INSERT INTO `permission` VALUES (2, 'COLLECT');
INSERT INTO `permission` VALUES (3, 'COMMENT');
INSERT INTO `permission` VALUES (1, 'FOLLOW');
INSERT INTO `permission` VALUES (5, 'MODERATE');
INSERT INTO `permission` VALUES (4, 'UPLOAD');
COMMIT;

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of role
-- ----------------------------
BEGIN;
INSERT INTO `role` VALUES (1, 'locked', NULL);
INSERT INTO `role` VALUES (2, 'user', NULL);
INSERT INTO `role` VALUES (3, 'editor', NULL);
INSERT INTO `role` VALUES (4, 'admin', NULL);
COMMIT;

-- ----------------------------
-- Table structure for roles_permissions
-- ----------------------------
DROP TABLE IF EXISTS `roles_permissions`;
CREATE TABLE `roles_permissions` (
  `role_id` int DEFAULT NULL,
  `permission_id` int DEFAULT NULL,
  KEY `role_id` (`role_id`),
  KEY `permission_id` (`permission_id`),
  CONSTRAINT `roles_permissions_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`),
  CONSTRAINT `roles_permissions_ibfk_2` FOREIGN KEY (`permission_id`) REFERENCES `permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of roles_permissions
-- ----------------------------
BEGIN;
INSERT INTO `roles_permissions` VALUES (1, 1);
INSERT INTO `roles_permissions` VALUES (1, 2);
INSERT INTO `roles_permissions` VALUES (2, 1);
INSERT INTO `roles_permissions` VALUES (2, 2);
INSERT INTO `roles_permissions` VALUES (2, 3);
INSERT INTO `roles_permissions` VALUES (2, 4);
INSERT INTO `roles_permissions` VALUES (3, 1);
INSERT INTO `roles_permissions` VALUES (3, 2);
INSERT INTO `roles_permissions` VALUES (3, 3);
INSERT INTO `roles_permissions` VALUES (3, 4);
INSERT INTO `roles_permissions` VALUES (3, 5);
INSERT INTO `roles_permissions` VALUES (4, 1);
INSERT INTO `roles_permissions` VALUES (4, 2);
INSERT INTO `roles_permissions` VALUES (4, 3);
INSERT INTO `roles_permissions` VALUES (4, 4);
INSERT INTO `roles_permissions` VALUES (4, 5);
INSERT INTO `roles_permissions` VALUES (4, 6);
COMMIT;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(120) NOT NULL,
  `password_hash` varchar(120) DEFAULT NULL,
  `auth` smallint DEFAULT NULL,
  `name` varchar(20) NOT NULL,
  `email` varchar(254) NOT NULL,
  `website` varchar(255) DEFAULT NULL,
  `register_time` datetime DEFAULT NULL,
  `avatar_s` varchar(64) DEFAULT NULL,
  `avatar_m` varchar(64) DEFAULT NULL,
  `avatar_l` varchar(64) DEFAULT NULL,
  `confirmed` tinyint(1) DEFAULT NULL,
  `locked` tinyint(1) DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `role_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_user_email` (`email`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`),
  CONSTRAINT `user_chk_1` CHECK ((`confirmed` in (0,1))),
  CONSTRAINT `user_chk_2` CHECK ((`locked` in (0,1))),
  CONSTRAINT `user_chk_3` CHECK ((`active` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of user
-- ----------------------------
BEGIN;
INSERT INTO `user` VALUES (1, 'admin', 'pbkdf2:sha256:150000$B7C6xecJ$a2de2a4f020aaf7762c72741ee5bc92a446e1068a15f0f158783e3e7223b1f09', 3, 'hyf', '1348977728@qq.com', NULL, '2021-12-01 15:35:46', NULL, NULL, NULL, 1, 0, 1, 4);
INSERT INTO `user` VALUES (2, '1', 'pbkdf2:sha256:150000$SlEx0Nzy$d283a1db1b5e3a5d0a792075271319411231d2524fbf937d9054a609c3d03e5a', 1, '1', '12@qq.com', NULL, '2021-12-01 15:36:11', NULL, NULL, NULL, 1, 0, 1, 2);
INSERT INTO `user` VALUES (3, '2', 'pbkdf2:sha256:150000$Olvw1qLi$e02f548fce244528e0df6b85426bd36e2e4a4fa9e13fe59cc70b1de97967e756', 1, '2', '12456@qq.com', NULL, '2021-12-01 15:36:32', NULL, NULL, NULL, 1, 0, 1, 2);
INSERT INTO `user` VALUES (4, '3', 'pbkdf2:sha256:150000$bTKtYBWR$c3c7c31125c25b2ccd0d40dd9dce579a82552c7c787ffeeea9a237bb2f6ed5d2', 1, '3', '124125@qq.com', NULL, '2021-12-01 15:39:20', NULL, NULL, NULL, 1, 0, 1, 2);
INSERT INTO `user` VALUES (5, '4', 'pbkdf2:sha256:150000$uauuHgd0$09f6d207e91185ee7f574db6668c8a0e3c4cbc5dfaa7bd5d4e5bf188532dac28', 1, '4', '2412412@qq.com', NULL, '2021-12-01 15:39:33', NULL, NULL, NULL, 1, 0, 1, 2);
INSERT INTO `user` VALUES (6, '5', 'pbkdf2:sha256:150000$b1nV3e2d$476a64bfc58b9cba3b35ba6e0f4c3678012f7b438708fc5fefb6cb1965a91af4', 1, '5', '2152356326@qq.com', NULL, '2021-12-01 15:40:00', NULL, NULL, NULL, 1, 0, 1, 2);
INSERT INTO `user` VALUES (7, '6', 'pbkdf2:sha256:150000$Ess1dhoD$2e2a18b5fdc155987456cd42c120942c29a881cd3acc7cc41f46358265d41c0b', 1, '6', '43626@qq.com', NULL, '2021-12-01 15:40:19', NULL, NULL, NULL, 1, 0, 1, 2);
INSERT INTO `user` VALUES (8, '7', 'pbkdf2:sha256:150000$UQeTYtsZ$b570777573887c31d41fa03bed47aa0170975560fcc274e53d15b4315e41f25a', 1, '7', '24231523@qq.com', NULL, '2021-12-01 15:40:32', NULL, NULL, NULL, 1, 0, 1, 2);
INSERT INTO `user` VALUES (9, '8', 'pbkdf2:sha256:150000$Azvkv2q1$d63d112df3eb3beb42517bb114353c29ccb1daf46eac138ba7219eb39b5f4d0f', 1, '8', '4135312535@qq.com', NULL, '2021-12-01 15:40:45', NULL, NULL, NULL, 1, 0, 1, 2);
INSERT INTO `user` VALUES (10, '9', 'pbkdf2:sha256:150000$C7Kj3UWi$6ccccf70a681a65acffc7b39b3cafe91fd93a6788d507b8a78a3fdafa5e5a73a', 1, '9', '242351@qq.com', NULL, '2021-12-01 15:41:01', NULL, NULL, NULL, 1, 0, 1, 2);
INSERT INTO `user` VALUES (11, '10', 'pbkdf2:sha256:150000$MdBw1JMw$750e0a1710af776a516ef0e9efdca9be18d525487c62f777937068a4fafc5346', 1, '10', '21423515@qq.com', NULL, '2021-12-01 15:41:18', NULL, NULL, NULL, 1, 0, 1, 2);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
