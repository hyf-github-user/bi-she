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

 Date: 22/03/2022 14:32:28
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
INSERT INTO `alembic_version` VALUES ('44c2c4612b49');
COMMIT;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of auth_group
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
BEGIN;
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add content type', 4, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (14, 'Can change content type', 4, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (15, 'Can delete content type', 4, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (16, 'Can view content type', 4, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (17, 'Can add session', 5, 'add_session');
INSERT INTO `auth_permission` VALUES (18, 'Can change session', 5, 'change_session');
INSERT INTO `auth_permission` VALUES (19, 'Can delete session', 5, 'delete_session');
INSERT INTO `auth_permission` VALUES (20, 'Can view session', 5, 'view_session');
INSERT INTO `auth_permission` VALUES (21, 'Can add IP黑名单', 6, 'add_ipblacklist');
INSERT INTO `auth_permission` VALUES (22, 'Can change IP黑名单', 6, 'change_ipblacklist');
INSERT INTO `auth_permission` VALUES (23, 'Can delete IP黑名单', 6, 'delete_ipblacklist');
INSERT INTO `auth_permission` VALUES (24, 'Can view IP黑名单', 6, 'view_ipblacklist');
INSERT INTO `auth_permission` VALUES (25, 'Can add 在线用户', 7, 'add_onlineusers');
INSERT INTO `auth_permission` VALUES (26, 'Can change 在线用户', 7, 'change_onlineusers');
INSERT INTO `auth_permission` VALUES (27, 'Can delete 在线用户', 7, 'delete_onlineusers');
INSERT INTO `auth_permission` VALUES (28, 'Can view 在线用户', 7, 'view_onlineusers');
INSERT INTO `auth_permission` VALUES (29, 'Can add 权限', 8, 'add_permissions');
INSERT INTO `auth_permission` VALUES (30, 'Can change 权限', 8, 'change_permissions');
INSERT INTO `auth_permission` VALUES (31, 'Can delete 权限', 8, 'delete_permissions');
INSERT INTO `auth_permission` VALUES (32, 'Can view 权限', 8, 'view_permissions');
INSERT INTO `auth_permission` VALUES (33, 'Can add 角色', 9, 'add_roles');
INSERT INTO `auth_permission` VALUES (34, 'Can change 角色', 9, 'change_roles');
INSERT INTO `auth_permission` VALUES (35, 'Can delete 角色', 9, 'delete_roles');
INSERT INTO `auth_permission` VALUES (36, 'Can view 角色', 9, 'view_roles');
INSERT INTO `auth_permission` VALUES (37, 'Can add 用户', 10, 'add_users');
INSERT INTO `auth_permission` VALUES (38, 'Can change 用户', 10, 'change_users');
INSERT INTO `auth_permission` VALUES (39, 'Can delete 用户', 10, 'delete_users');
INSERT INTO `auth_permission` VALUES (40, 'Can view 用户', 10, 'view_users');
COMMIT;

-- ----------------------------
-- Table structure for category
-- ----------------------------
DROP TABLE IF EXISTS `category`;
CREATE TABLE `category` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '分类主键',
  `name` varchar(64) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_category_name` (`name`),
  KEY `ix_category_timestamp` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of category
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for collect
-- ----------------------------
DROP TABLE IF EXISTS `collect`;
CREATE TABLE `collect` (
  `collector_id` int NOT NULL,
  `collected_id` int NOT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`collector_id`,`collected_id`),
  KEY `collected_id` (`collected_id`),
  CONSTRAINT `collect_ibfk_1` FOREIGN KEY (`collector_id`) REFERENCES `user` (`id`),
  CONSTRAINT `collect_ibfk_2` FOREIGN KEY (`collected_id`) REFERENCES `post` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of collect
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '评论主键',
  `body` text,
  `timestamp` datetime DEFAULT NULL,
  `flag` int DEFAULT NULL COMMENT '评论被举报次数',
  `author_id` int DEFAULT NULL,
  `post_id` int DEFAULT NULL,
  `reviewed` tinyint(1) DEFAULT NULL COMMENT '是否通过审核',
  `replied_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `author_id` (`author_id`),
  KEY `post_id` (`post_id`),
  KEY `replied_id` (`replied_id`),
  KEY `ix_comment_timestamp` (`timestamp`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `user` (`id`),
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`),
  CONSTRAINT `comment_ibfk_3` FOREIGN KEY (`replied_id`) REFERENCES `comment` (`id`),
  CONSTRAINT `comment_chk_1` CHECK ((`reviewed` in (0,1)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of comment
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_oauth_users_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_oauth_users_id` FOREIGN KEY (`user_id`) REFERENCES `oauth_users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
BEGIN;
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (6, 'monitor', 'ipblacklist');
INSERT INTO `django_content_type` VALUES (7, 'monitor', 'onlineusers');
INSERT INTO `django_content_type` VALUES (8, 'oauth', 'permissions');
INSERT INTO `django_content_type` VALUES (9, 'oauth', 'roles');
INSERT INTO `django_content_type` VALUES (10, 'oauth', 'users');
INSERT INTO `django_content_type` VALUES (5, 'sessions', 'session');
COMMIT;

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
BEGIN;
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2022-03-18 17:53:04.451370');
INSERT INTO `django_migrations` VALUES (2, 'contenttypes', '0002_remove_content_type_name', '2022-03-18 17:53:04.469028');
INSERT INTO `django_migrations` VALUES (3, 'auth', '0001_initial', '2022-03-18 17:53:04.493482');
INSERT INTO `django_migrations` VALUES (4, 'auth', '0002_alter_permission_name_max_length', '2022-03-18 17:53:04.538409');
INSERT INTO `django_migrations` VALUES (5, 'auth', '0003_alter_user_email_max_length', '2022-03-18 17:53:04.541105');
INSERT INTO `django_migrations` VALUES (6, 'auth', '0004_alter_user_username_opts', '2022-03-18 17:53:04.543487');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0005_alter_user_last_login_null', '2022-03-18 17:53:04.545848');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0006_require_contenttypes_0002', '2022-03-18 17:53:04.546765');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0007_alter_validators_add_error_messages', '2022-03-18 17:53:04.549223');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0008_alter_user_username_max_length', '2022-03-18 17:53:04.552317');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0009_alter_user_last_name_max_length', '2022-03-18 17:53:04.555719');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0010_alter_group_name_max_length', '2022-03-18 17:53:04.562155');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0011_update_proxy_permissions', '2022-03-18 17:53:04.565081');
INSERT INTO `django_migrations` VALUES (14, 'oauth', '0001_initial', '2022-03-18 17:53:04.612633');
INSERT INTO `django_migrations` VALUES (15, 'admin', '0001_initial', '2022-03-18 17:53:04.704307');
INSERT INTO `django_migrations` VALUES (16, 'admin', '0002_logentry_remove_auto_add', '2022-03-18 17:53:04.724350');
INSERT INTO `django_migrations` VALUES (17, 'admin', '0003_logentry_add_action_flag_choices', '2022-03-18 17:53:04.729220');
INSERT INTO `django_migrations` VALUES (18, 'monitor', '0001_initial', '2022-03-18 17:53:04.741094');
INSERT INTO `django_migrations` VALUES (19, 'monitor', '0002_onlineusers_user', '2022-03-18 17:53:04.749156');
INSERT INTO `django_migrations` VALUES (20, 'sessions', '0001_initial', '2022-03-18 17:53:04.762662');
COMMIT;

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of django_session
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for follow
-- ----------------------------
DROP TABLE IF EXISTS `follow`;
CREATE TABLE `follow` (
  `follower_id` int NOT NULL,
  `followed_id` int NOT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`follower_id`,`followed_id`),
  KEY `followed_id` (`followed_id`),
  CONSTRAINT `follow_ibfk_1` FOREIGN KEY (`follower_id`) REFERENCES `user` (`id`),
  CONSTRAINT `follow_ibfk_2` FOREIGN KEY (`followed_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of follow
-- ----------------------------
BEGIN;
INSERT INTO `follow` VALUES (1, 1, '2022-03-22 14:09:53');
INSERT INTO `follow` VALUES (2, 2, '2022-03-22 14:13:11');
INSERT INTO `follow` VALUES (3, 3, '2022-03-22 14:16:53');
INSERT INTO `follow` VALUES (4, 4, '2022-03-22 14:17:05');
INSERT INTO `follow` VALUES (5, 5, '2022-03-22 14:17:21');
INSERT INTO `follow` VALUES (6, 6, '2022-03-22 14:17:33');
INSERT INTO `follow` VALUES (7, 7, '2022-03-22 14:17:41');
INSERT INTO `follow` VALUES (8, 8, '2022-03-22 14:18:12');
COMMIT;

-- ----------------------------
-- Table structure for link
-- ----------------------------
DROP TABLE IF EXISTS `link`;
CREATE TABLE `link` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of link
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for monitor_ipblacklist
-- ----------------------------
DROP TABLE IF EXISTS `monitor_ipblacklist`;
CREATE TABLE `monitor_ipblacklist` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `ip` char(39) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ip` (`ip`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of monitor_ipblacklist
-- ----------------------------
BEGIN;
INSERT INTO `monitor_ipblacklist` VALUES (5, '2022-03-20 14:36:42.982323', '2022-03-20 14:36:42.982386', '127.0.0.2');
INSERT INTO `monitor_ipblacklist` VALUES (6, '2022-03-20 14:48:27.648719', '2022-03-20 14:48:27.648734', '1.1.1.1');
INSERT INTO `monitor_ipblacklist` VALUES (7, '2022-03-20 14:48:45.626203', '2022-03-20 14:48:45.626250', '127.1.2.1');
COMMIT;

-- ----------------------------
-- Table structure for monitor_onlineusers
-- ----------------------------
DROP TABLE IF EXISTS `monitor_onlineusers`;
CREATE TABLE `monitor_onlineusers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `ip` char(39) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `monitor_onlineusers_user_id_248dbc65_fk_oauth_users_id` (`user_id`),
  CONSTRAINT `monitor_onlineusers_user_id_248dbc65_fk_oauth_users_id` FOREIGN KEY (`user_id`) REFERENCES `oauth_users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of monitor_onlineusers
-- ----------------------------
BEGIN;
INSERT INTO `monitor_onlineusers` VALUES (1, '2022-03-18 17:58:25.256184', '2022-03-18 17:58:25.256195', '127.0.0.1', 1);
COMMIT;

-- ----------------------------
-- Table structure for notification
-- ----------------------------
DROP TABLE IF EXISTS `notification`;
CREATE TABLE `notification` (
  `id` int NOT NULL AUTO_INCREMENT,
  `message` text NOT NULL,
  `is_read` tinyint(1) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `receiver_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `receiver_id` (`receiver_id`),
  KEY `ix_notification_timestamp` (`timestamp`),
  CONSTRAINT `notification_ibfk_1` FOREIGN KEY (`receiver_id`) REFERENCES `user` (`id`),
  CONSTRAINT `notification_chk_1` CHECK ((`is_read` in (0,1)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of notification
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for oauth_permissions
-- ----------------------------
DROP TABLE IF EXISTS `oauth_permissions`;
CREATE TABLE `oauth_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `name` varchar(30) NOT NULL,
  `sign` varchar(30) NOT NULL,
  `menu` tinyint(1) NOT NULL,
  `method` varchar(8) NOT NULL,
  `path` varchar(200) NOT NULL,
  `desc` varchar(30) NOT NULL,
  `pid_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sign` (`sign`),
  KEY `oauth_permissions_pid_id_efc19a81_fk_oauth_permissions_id` (`pid_id`),
  CONSTRAINT `oauth_permissions_pid_id_efc19a81_fk_oauth_permissions_id` FOREIGN KEY (`pid_id`) REFERENCES `oauth_permissions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of oauth_permissions
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for oauth_roles
-- ----------------------------
DROP TABLE IF EXISTS `oauth_roles`;
CREATE TABLE `oauth_roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `name` varchar(32) NOT NULL,
  `desc` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of oauth_roles
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for oauth_roles_to_oauth_permissions
-- ----------------------------
DROP TABLE IF EXISTS `oauth_roles_to_oauth_permissions`;
CREATE TABLE `oauth_roles_to_oauth_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `roles_id` int NOT NULL,
  `permissions_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `oauth_roles_to_oauth_per_roles_id_permissions_id_3a4ca737_uniq` (`roles_id`,`permissions_id`),
  KEY `oauth_roles_to_oauth_permissions_id_953b1995_fk_oauth_per` (`permissions_id`),
  CONSTRAINT `oauth_roles_to_oauth_permissions_id_953b1995_fk_oauth_per` FOREIGN KEY (`permissions_id`) REFERENCES `oauth_permissions` (`id`),
  CONSTRAINT `oauth_roles_to_oauth_roles_id_46f34d12_fk_oauth_rol` FOREIGN KEY (`roles_id`) REFERENCES `oauth_roles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of oauth_roles_to_oauth_permissions
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for oauth_users
-- ----------------------------
DROP TABLE IF EXISTS `oauth_users`;
CREATE TABLE `oauth_users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `name` varchar(20) NOT NULL,
  `mobile` varchar(11) DEFAULT NULL,
  `image` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `mobile` (`mobile`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of oauth_users
-- ----------------------------
BEGIN;
INSERT INTO `oauth_users` VALUES (1, 'pbkdf2_sha256$150000$dr0gpxYZWX3j$2cX+Hg16n1YUwdkgerJVHKojylCavBg3cWt4HWdtKuw=', '2022-03-21 21:33:15.512149', 1, 'admin', '', '', '1348977728@qq.com', 1, 1, '2022-03-18 17:54:14.272297', '胡印福', '15879093053', 'avatar/2022/03/image.png');
COMMIT;

-- ----------------------------
-- Table structure for oauth_users_groups
-- ----------------------------
DROP TABLE IF EXISTS `oauth_users_groups`;
CREATE TABLE `oauth_users_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `users_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `oauth_users_groups_users_id_group_id_a6d5dd23_uniq` (`users_id`,`group_id`),
  KEY `oauth_users_groups_group_id_234502cc_fk_auth_group_id` (`group_id`),
  CONSTRAINT `oauth_users_groups_group_id_234502cc_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `oauth_users_groups_users_id_84419b9f_fk_oauth_users_id` FOREIGN KEY (`users_id`) REFERENCES `oauth_users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of oauth_users_groups
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for oauth_users_to_oauth_roles
-- ----------------------------
DROP TABLE IF EXISTS `oauth_users_to_oauth_roles`;
CREATE TABLE `oauth_users_to_oauth_roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `users_id` int NOT NULL,
  `roles_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `oauth_users_to_oauth_roles_users_id_roles_id_e75d7440_uniq` (`users_id`,`roles_id`),
  KEY `oauth_users_to_oauth_roles_roles_id_bd989b73_fk_oauth_roles_id` (`roles_id`),
  CONSTRAINT `oauth_users_to_oauth_roles_roles_id_bd989b73_fk_oauth_roles_id` FOREIGN KEY (`roles_id`) REFERENCES `oauth_roles` (`id`),
  CONSTRAINT `oauth_users_to_oauth_roles_users_id_0a28e3e5_fk_oauth_users_id` FOREIGN KEY (`users_id`) REFERENCES `oauth_users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of oauth_users_to_oauth_roles
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for oauth_users_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `oauth_users_user_permissions`;
CREATE TABLE `oauth_users_user_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `users_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `oauth_users_user_permiss_users_id_permission_id_c70cd3b8_uniq` (`users_id`,`permission_id`),
  KEY `oauth_users_user_per_permission_id_74d25bb2_fk_auth_perm` (`permission_id`),
  CONSTRAINT `oauth_users_user_per_permission_id_74d25bb2_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `oauth_users_user_permissions_users_id_bb814e73_fk_oauth_users_id` FOREIGN KEY (`users_id`) REFERENCES `oauth_users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of oauth_users_user_permissions
-- ----------------------------
BEGIN;
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
-- Table structure for post
-- ----------------------------
DROP TABLE IF EXISTS `post`;
CREATE TABLE `post` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '文章主键',
  `title` varchar(255) DEFAULT NULL,
  `body` text,
  `timestamp` datetime DEFAULT NULL,
  `can_comment` tinyint(1) DEFAULT NULL,
  `auth` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `flag` int DEFAULT NULL COMMENT '文章被举报次数',
  `category_id` int DEFAULT NULL,
  `author_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  KEY `author_id` (`author_id`),
  KEY `ix_post_timestamp` (`timestamp`),
  CONSTRAINT `post_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`),
  CONSTRAINT `post_ibfk_2` FOREIGN KEY (`author_id`) REFERENCES `user` (`id`),
  CONSTRAINT `post_chk_1` CHECK ((`can_comment` in (0,1)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of post
-- ----------------------------
BEGIN;
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of role
-- ----------------------------
BEGIN;
INSERT INTO `role` VALUES (1, 'locked', NULL);
INSERT INTO `role` VALUES (2, 'user', NULL);
INSERT INTO `role` VALUES (3, 'admin', NULL);
COMMIT;

-- ----------------------------
-- Table structure for roles_permissions
-- ----------------------------
DROP TABLE IF EXISTS `roles_permissions`;
CREATE TABLE `roles_permissions` (
  `role_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`role_id`,`permission_id`),
  KEY `permission_id` (`permission_id`),
  CONSTRAINT `roles_permissions_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`),
  CONSTRAINT `roles_permissions_ibfk_2` FOREIGN KEY (`permission_id`) REFERENCES `permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of roles_permissions
-- ----------------------------
BEGIN;
INSERT INTO `roles_permissions` VALUES (1, 1);
INSERT INTO `roles_permissions` VALUES (2, 1);
INSERT INTO `roles_permissions` VALUES (3, 1);
INSERT INTO `roles_permissions` VALUES (1, 2);
INSERT INTO `roles_permissions` VALUES (2, 2);
INSERT INTO `roles_permissions` VALUES (3, 2);
INSERT INTO `roles_permissions` VALUES (2, 3);
INSERT INTO `roles_permissions` VALUES (3, 3);
INSERT INTO `roles_permissions` VALUES (2, 4);
INSERT INTO `roles_permissions` VALUES (3, 4);
INSERT INTO `roles_permissions` VALUES (3, 5);
INSERT INTO `roles_permissions` VALUES (3, 6);
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
  `avatar_raw` varchar(64) DEFAULT NULL,
  `private_key` text COMMENT '加密密码的私钥',
  `rsa_password` text COMMENT '对密码进行加密之后的密文',
  `active` tinyint(1) DEFAULT NULL,
  `confirmed` tinyint(1) DEFAULT NULL,
  `locked` tinyint(1) DEFAULT NULL,
  `role_id` int DEFAULT NULL,
  `receive_comment_notification` tinyint(1) DEFAULT NULL,
  `receive_follow_notification` tinyint(1) DEFAULT NULL,
  `receive_collect_notification` tinyint(1) DEFAULT NULL,
  `public_collections` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_user_email` (`email`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`),
  CONSTRAINT `user_chk_1` CHECK ((`active` in (0,1))),
  CONSTRAINT `user_chk_2` CHECK ((`confirmed` in (0,1))),
  CONSTRAINT `user_chk_3` CHECK ((`locked` in (0,1))),
  CONSTRAINT `user_chk_4` CHECK ((`receive_comment_notification` in (0,1))),
  CONSTRAINT `user_chk_5` CHECK ((`receive_follow_notification` in (0,1))),
  CONSTRAINT `user_chk_6` CHECK ((`receive_collect_notification` in (0,1))),
  CONSTRAINT `user_chk_7` CHECK ((`public_collections` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of user
-- ----------------------------
BEGIN;
INSERT INTO `user` VALUES (1, 'admin', 'pbkdf2:sha256:150000$BGzNbXZu$fbc22aa1d95bac61c420156a2c6a097a2d85fc04942b5b09d5020c7380125bce', 3, 'admin', '1348977728@qq.com', NULL, '2022-03-22 14:09:53', 'admin_s.png', 'admin_m.png', 'admin_l.png', NULL, '2d2d2d2d2d424547494e205253412050524956415445204b45592d2d2d2d2d0a4d4949435941494241414b42675144414b554a307458632b674449647a75612f346161686e7564455857464c4c732b666e6c774268514d4774335559316a5a310a4f3543744b4b79506d6f416a73476933476e78344c426a5a4a33785859584d78306170596b4c47514561683030546b426c50786448746c6f327049744b6873520a325537496166354e44486a672b51422b386a5965754b6f5a6d76594d52532f77696a664e4a5551684e683139635344733352734f7873686f58514944415141420a416f47414954472f61687643796f676f6f422b536d736a6e47506f7a4a7773656548645170466b6475614635675671466e744736504977616c4e373232434f760a53507237533834476646665a7677466b4b46414d43563965797965705739447841563657444269434c74714479304f5957567559454832544e5a734c634141680a52705a35306f416a7a6157654238692b792f6853676370506c706c386779636b666a49532f75706873764e6f7856304352514461786546667259372f345266640a6366705962574550766d5134373433636c4f68537a7170555264493068484c65427666316d6563774f5570566174694a6f64415976634e38625473576c6158390a4951794f5954504b4a63686148774939414f4463483951303659466e415152553238366943526f6b50674442566662364c413042574858544c543868544a49410a786467707846735273512f483133627974644a43383473687946667775356c6d41774a4548527238612b30385043436e4f79666878596676784e64776e2f36470a346854526638724d384639466f7755482f792f774a7a577467305872394d6339506270515a43704336726668683553724f367a3837616853366f377951384d430a505143466769316a306762537a6c584d504a5a474765394e6c6a63364f354450453773542f626949504e71676f53545669352f73754e2f644d71507575726b7a0a3575674e37374b713657514b307553514d41454352443671474450427869394e45464a704d3754634f6a527a312f487955325951476c68417438533977796b7a0a6b33336869516e6679375279734263584d2b66625a5a544c4f7834526c4972307166644530524e4933673258656f6f6a0a2d2d2d2d2d454e44205253412050524956415445204b45592d2d2d2d2d0a', '9ebbf889f59a681048a98fd2b5845e8c6dd4f7eed5f91ea0259b0e098cb4326f25c08c65c22cbc52c5958d88e01877360e9b5b7c1114f6126cb464633fa4cf1212cf31e5310534e94cd38d9af3f62482139bcd59b1774c8e42dbe68093b53c1f17191cad890fd48fe5e98e5f573264d0a9f08fbb95ad53d76fdbe58522e5e357', 1, 1, 0, 3, 1, 1, 1, 0);
INSERT INTO `user` VALUES (2, 'hyf', 'pbkdf2:sha256:150000$1La6Aqvm$fd24ec0e54204dcbaf0146dec6db593951276be4459f4072b703591159caa440', 2, 'hyf', '1841671754@qq.com', NULL, '2022-03-22 14:13:10', 'hyf_s.png', 'hyf_m.png', 'hyf_l.png', NULL, '2d2d2d2d2d424547494e205253412050524956415445204b45592d2d2d2d2d0a4d4949435967494241414b426751436c62354a79705a6a4e6d3634574e747046666837437950345449336f56576554384e5064704d6e702b477446794663434a0a6b585765587158553767566b2b792f516d33465275386e5059476544744d54773765314c5144656677746d326f4d4b564249722b4667664754335a2b534638490a5775534f2f5536477a3261634b2f70765a4f774c365353574f79394558357830464e67676c784f6558327a523352374135475973584f354731774944415141420a416f47424149656d49585843464c586168666350435242634a6f72653158344a342b756e35787470727368694c4a424547794b7064564d586f314b3146744b750a5446774e6e706f314b73697936766f5165544245513238754d767044566147714273752f726455665839736c65724c6b6e62315a6a2b3961304c67624e4275590a636363625a64337a54717075663965484c50516a37316c687050472f42526d51677547785654425774664c7a314d4268416b55417674797a493264627642686d0a50716b79633833505446567773546c5a2f342f704a6275776d7148364f30364255777346733035426757762b305255594a48552b4951464641484e78466b33730a344d4b553575726e74526d4e454a45435051446435577650576c78765a48357372416151524c79326e514d6f336f4f79716a4c5368774c79737568583670694a0a3965454c55572f746b79526144546a45757154734d53464b49444952754a424a464f6343525143693548397248754a334653666d494d647a6546714d336e72510a646f38754179664c30585533644469356478582b78764231694c743164724e43784d7358436f3063354256382f676d744c4a4b58664e7053666e6545343671320a55514939414a796c44664f6d6261537867394a427171794436646a63684e4f414b65616834686a652b4d544f61646c4f6f6e7161476c463848784450464257430a53665950634d66516378693647373649315572534e774a4544646d4c326859366c7a5658653642776336416746676a3567534c4f78582b6a2f6a5843514c566f0a6c464671717a6a312b4f646c445068486d373372726c7857412f4c314f754e2f787a3862324d6e2f424e4270316276715434453d0a2d2d2d2d2d454e44205253412050524956415445204b45592d2d2d2d2d0a', 'a124e35c63ac2516e45bb9c664c67dad1475c1ce0d8b93158bfcf25296a070bf3a4eb532d436abb7fb87326bbfcdea536f91c1c69169fb939f2c1350a3c94cc8adc7c33101bb620c98abbdda76ff5ba4b3a282591a057f4d87a6920a28508642aa2d4943bd206ca9f42aabe7d2398093a74a8adddf0044a90671a4000c05023d', 1, 1, 0, 2, 1, 1, 1, 0);
INSERT INTO `user` VALUES (3, 'haha', 'pbkdf2:sha256:150000$pBizMLEI$a57e44e609157be8dcb97bbe242a365bebbc5e2c04609845e547ead01f61ed97', 2, 'haha', '414124@qq.com', NULL, '2022-03-22 14:16:53', 'haha_s.png', 'haha_m.png', 'haha_l.png', NULL, '2d2d2d2d2d424547494e205253412050524956415445204b45592d2d2d2d2d0a4d4949435877494241414b426751445434554a516f503175444f5953645147494a3254725931624d704863426c7a7334546d3263456155784d443167464f434e0a3868516155383234494c755a3562676533333364555846693156534674555365766779766a5a6e334b6c4978672f527651353670586d764b544c4d54344942520a687370762f6c30615439707032305530495053325841653141554877342b7955467076617357704634746b48657945417a4a62453941322b6c514944415141420a416f474158524d463434396b354a514c2b53326d3935312b6970782f77374f336831356371465a6a646679575757343864396d543779625a5239747163696b470a344172326637466a672f5a4433637569726e3237414e44704f3070357252456b4d47364f304a6f37655a4d374d7663306b504e726f4e366d786f67543172465a0a6462356c704e3871416939684a5a5a6c54666d3056445857796b6e676d565053434a7942384d352f79744e5347563043525144593350567550653146774d33580a477a6a6c2b2b725561415a49364b576f334655547035533534773633485573506a6930327252436a6d58767641773039396678344679646269345a4a742f69550a5974664e54343042597777345477493941506f6545384f3778326d734243445231664c7664347a5162465669554f4e494c6c70426a69446852413930704979690a3461555252494b7779446458346652616d59354b4f4a712f336656753633563932774a4555387774326b64376f2f52346c61496a506c7331787058627439694f0a437333343466746a634f445945744879367a505a4c4d4e374a6e787363314d4f6a743636692f30476245316875714b6f483036436251644d53546a6f772b6b430a50424d4d50566358737430535535496f534e4869654d6c4a6969614b6754783933384852346b4151783730686c664a3736524649476c36566c666e5a414955360a625231502b37575654524d47366e6d644a774a455238634d3131324e6b63515630794766397361644c47686c6d6c4d4b77664e386d52776a78554f66307738320a4d3741444b4b76455368496f75756a564c67654d58494571717851454a51565935705052633770667575716230596b3d0a2d2d2d2d2d454e44205253412050524956415445204b45592d2d2d2d2d0a', '92a2edf98242f45f06bd71f3e444c3fddbec6ab922468d700ed8999f926bd5b9592eaf3f61bb84c9f3906a2f779ff3f05f71dd56f34427423091c7d3d4348b4127cc78cd9b3e05d4003eee8f06539ae9dc48d611c99a2e361ca604b8e6468e6f47b2cb705a21de9aa92c5aabb75f58d26eb6c7bea1e4ea441a5cec4c14fcbac8', 1, 1, 0, 2, 1, 1, 1, 0);
INSERT INTO `user` VALUES (4, 'ddd', 'pbkdf2:sha256:150000$EJgB4vIB$1e31196595c0833d5301a97a86afe60f2a9e827e44070f229f15f649f4f6bb2b', 2, 'ddd', '21341@qq.com', NULL, '2022-03-22 14:17:04', 'ddd_s.png', 'ddd_m.png', 'ddd_l.png', NULL, '2d2d2d2d2d424547494e205253412050524956415445204b45592d2d2d2d2d0a4d4949435941494241414b426751434c6a44644f3644702f556e38696f666c7834462f394d5961366b394d5953773548487a71434f726d78347867333134316c0a4a30776a4539544a4a686d646f49634d7662475478564e715a4c594f71514942424651356a7879354d495a2f42746e2f3536362b4f7a4f33496c6832424953340a50675458446574766b62543752734562564c5079545041537053766f646578376e71393639467552656b6d556d436f33587045754f75392f34774944415141420a416f4741482b2f3054497662723334612b4c736e557365755545314162333062682b6a4e6d4c7474385a5974483668417836372b666c4d54477367554941456e0a526173536e586a67706c6733386861676b4252663779434a494e6553686e43366b6c747a6177767371456370316a37366d4b5a2b32555947587a4657766d65540a2b4b66307048455042496e5047447245542f4b2b51586f4a31467a3045664356687872706a4637707634783652584543525143507a464d2b3275764f6a4f476f0a35646142546137747631625355304c4e4b447957356262362b61623668704c7070397675746b4b7631564648776f355a2f34614d6730596d71525362473857730a7542797336593743436a304b3677493941506875336b796e335a77696a4954696e4434494177306865382b73647758572f586a776f54375866575173376a39760a485337545543565077637a636f7167757375685769517752644a316f5439327736514a4555656176647a7062576b3531624b78547131766969546b557130434f0a364b6a464d6244757369326c52455748775a7441736371505776536c6b62696e4f5731485a68715378777841563050504a39764a5156625a58333154585463430a5051445655735936426f3770716c55464b6c314665725738436274352b54722b336277727046796854494b55695778504e6764574651656c386c5755707752590a374469642f75695258302f47646a4c57527a6b43524478642b71594d5138366538356b4e672b6e745a42574b415342643673572b6e6a3870656c69476a5078430a454a68584d396e4e69686a396e6c6671664b79466c5462384f5a334d72616d5843666d6d4876576e766b77484f3965760a2d2d2d2d2d454e44205253412050524956415445204b45592d2d2d2d2d0a', '1a8a65f870805a71efa9251ef921b686d8e36fcbce72c64a264180336a0f095357e9da8eb3bb0a2ee49112c1d88b07f4e6e21fc35d7ef3fed7709fdd9bebd0810237c4161af396d31ec481503a5dbb7ae433ebd3057121d533b9ab0db68e995a753748ff839851a7f1757e4addbed34b7478aa3608a537399c96cf07150e53ab', 1, 1, 0, 2, 1, 1, 1, 0);
INSERT INTO `user` VALUES (5, 'qwer', 'pbkdf2:sha256:150000$mQkueyAx$ef8ec5b03687625220b42e489b174232677daf87beccf0614079974f7e82ae76', 2, 'qwer', '13124123@qq.com', NULL, '2022-03-22 14:17:21', 'qwer_s.png', 'qwer_m.png', 'qwer_l.png', NULL, '2d2d2d2d2d424547494e205253412050524956415445204b45592d2d2d2d2d0a4d4949435941494241414b426751434c64506b397a4e2f715a4c563778724e7336574a7367353875564e61694a596d78386c67455933794c4f50417232367a740a363453697367534e4b6675594f3641464d747a2f3257776b64754a6d2b6a4734776f71745737634f4f304863685756763366305a484c577a65303435456766700a566b564454794b307674426d7652594548454543504f43434d6935316b782f3147597a47716d664a58335831747a73625352327a6d53474e73774944415141420a416f4741616d3647766679374d36645376726d4350472f4e3979566f2b6a497a634b4b586553434d7669537a61346d7a2b725434514d684c664f5043423335770a44746f4b6f5930564434702f4e30456f50784659345068424c6230707934464a326b516147764a504134744d54355741542b54543465332f59666f514d51746d0a5132496c65635370415161506d5633434b794d6f5732616e4254696754434c6e715572372b32466d50444e714775454352514430444a5935574a5848516b39710a64464a6773535639702b7a354c34532f6e597a5348576a74744a484f4d73513975713542364b48413659416f4e5936554336564a6e4468456c6553666e6331690a3857454f4e784e697945596f59774939414a4a4a4e6f585a387346616b31587950415833456c31723450564653334a30354b437468333843354144735a5542530a596d58394a70703033324469665535617038474b4346344574647a4768474e2b63514a46414d766e2f466762714d45637155667a75715270506a3758344970750a356f5a4739394c536d636f4b46637a6e34386b44776662316a4c696e48396e34725a454b6a65614c37514e354464564450736a4e6a74385771303763734b6d720a416a7745567465664d4d2f616e4730795a335551574476624f592f36746f742b59616c47657439434454766d4b787a317733765875714b69676b542b41726e6b0a305275597968646c636f3553646a4548496f454352462b766f446a3548646933512b75627a72555977306d52626c4a366977796d4157424d42715a694e4c44330a674e52634959754952327132534b6452424244754b43635a7a44313033737353454239665050346c48707a697a3356360a2d2d2d2d2d454e44205253412050524956415445204b45592d2d2d2d2d0a', '49e0079b64937374c3030546e3f7e5e217553c21214d3da812bb545e8d52b9b2620e148fccd17ab5fd3d2c6c62049a0c037c953e9f2ad01f69ac48df978d78b2aed24d3642f3ac540ec6e86a870725de9e15f1032e749c6868bdaafe19d618b87d328b73909d9067c5c759149b8a37abb52922759e82eab98d8b1c8c5ade7a82', 1, 1, 0, 2, 1, 1, 1, 0);
INSERT INTO `user` VALUES (6, 'lll', 'pbkdf2:sha256:150000$F6FYCnX5$c2245c7a56a6e6f2b3c206bc0037bd8530b12ff364eeeb0b582530c2c0415aef', 2, 'lll', '21524314@qq.com', NULL, '2022-03-22 14:17:33', 'lll_s.png', 'lll_m.png', 'lll_l.png', NULL, '2d2d2d2d2d424547494e205253412050524956415445204b45592d2d2d2d2d0a4d4949435941494241414b426751434a65634a6d68356746584f43706862416855443955435a306c523875577156565343752f75336a586f6f6a785047472f540a57566354394d3367786d4e62514d6a5155536f582b6f366d394f714a394961336146616745667279506c695750386c79443656346f4a354269374b59775639500a497832336a696756666f5a66512f342b6b694a4e4853546c773871723149444153526b6e516e61667a467a546a492f4b4b793174784647596e774944415141420a416f4741524a786b44552b3236315a444f6466693433317458622b2b6b68435735775a7a38704a4b314f684a39325367764d6a785a6f57384539576c756e7a490a7359355071736758506768716b61444350542b775663414a4f4c57745575626a51393744424c3143574e596445656936493342492f56514b6f344f4a4631612f0a4451765772765054724a64366c53436657667a3955746565356d3764686f4766746f6c50654763434d694166344545435251447430526e4b4439336a646d72530a412b4b7534444678616e456c6261553853704e777163766d4f786c7a6c6e4e454f654c5977752b2b593730336c6c533974317a786645374a47615a39676e6b730a764a505942636e4238575a4647514939414a50386f6b6a364f4c49774b484c63784d4e706541755a487239746c2f573465767377506b526a63524575506439740a47497371324f30316978415375657738742f72525765435234302b414763694b64774a46414b5378724a52387a494f6348486e343675474572586b48352f65740a71554c4a7572584a51555865493941696e777a657362532f753177306f6e4e2b6a6f3063455366446d4b51344f5536754c744447662f5359665a4c735a4a44780a416a7759614531337a645532426c31566648587a614e7a45784f39655554774436665a576f5946546c4463637830797249666f76556454505973705a7a307a630a32724c5a616c667867763544715851584d4563435243506b45372b3839316e3377587947595959747073665337526d754733516a58314f6a713147575a6232420a37414f59616c3134315154666f2f476f2f6a464c466d70713979307734522f6e4171734b6f6143797a32397a6e5a54350a2d2d2d2d2d454e44205253412050524956415445204b45592d2d2d2d2d0a', '4c5104c40bfa3e9d30d39aeea0fe4f49f699f89a88fc93db9257bce64723c651ee6eccd3c2ee95ba1e90de7565d1e8de457cef787190fdc13fc2b3011f5d45b2111f7530ace953a34e1b412596e78b95637f66c4b86159358db57269889ee05667ec5733654a4198a620e5121a4364c91a223c97be8d2f85f55a34144ed99eeb', 1, 1, 0, 2, 1, 1, 1, 0);
INSERT INTO `user` VALUES (7, 'ppp', 'pbkdf2:sha256:150000$wJ115MYl$e5849b3c31aebf45b5b0aaae9887c0a4a79c3cc25af2e93308f99f93553b95ee', 2, 'ppp', 'ppp', NULL, '2022-03-22 14:17:41', 'ppp_s.png', 'ppp_m.png', 'ppp_l.png', NULL, '2d2d2d2d2d424547494e205253412050524956415445204b45592d2d2d2d2d0a4d4949435941494241414b4267514352332b432b6170646571694d5337516e51474f6734557744594845626d30656c4571376c62416956467938466b5a6138580a53456444527065656b5749446b326d7432774346554a4d7233317876485241473272644b4e4f4a6349732b523159614b6e4c5056504365674f647447755a31340a4f574c7a4e6c5a4f524b7341622f512b396645475643463958656967387746374d572f4d76675432637744626a4a4534524c7268455a485835514944415141420a416f47414467516432773377313261766b677a3269576b7250755979795a45462b76326d5654504f7a6f444a5267694b33334f7076436e3074764563646c37760a745070414344566e756d65416a4a47636c77794b756a52583164366536777a363058796e443143724474314c3939565552706539792b4d6c6850727441614f550a782b4e64694e6f6a446b7577336f54746f38632f74716b387563794554376434496d6a2b6c434a736935312f593845435251442b7548764461306e4d4f4d51550a445249615853627448565a412f384b39385364654a7834576250346232473132544a50553633686741764a6b4d647937467a31526452616d66726b51423243590a65316263487856586a684d7539514939414a4b6263516168384663347273674f6a6f6645674f546239445639627949616b315575616f754b4957647663624e670a2b637155455174465966564370357869314e6870457555764768306a39522b504d514a45482f484d2b36344a334558474f576d474f713479416f79715534352f0a777368716b6f452f5962716268367831316438327276343034333262486e757558667846495745597a52715a5a4f773337676552316874443175346e633730430a50484949746b47536448396a64342f6b7772695941436f446246437534474b4769564d595a34646953646c4b7467587779467271454e6654662f356c656a6f4b0a4a63537539694f4f4836484b396a383241514a46414d314b667076626775336351686446734a714a2b79616656375846555a65463473465276763455704854620a434e396e59394c68636a575a38677a7a6f7751316f4c4d46733656596462366a415934346e6573486c4c7a70752f54360a2d2d2d2d2d454e44205253412050524956415445204b45592d2d2d2d2d0a', '4ecf852c5b6bf3c3950bb3f02b6c0e0b980735740e546479df1372db82fb548f510b6c426265a17cebbaa4717a1a3e97c91d6d3a4dd492ed8839fb25f9a20d36912036d707ba1cfb422aec0c6d321d4c6013be277209d8d878495d9c08b6b13b5e082775e91dea3da486cc10af0c078258d078ee58f8cf8dfcc24960c5fd85ef', 1, 1, 0, 2, 1, 1, 1, 0);
INSERT INTO `user` VALUES (8, 'sss', 'pbkdf2:sha256:150000$hgsihW1i$568b658c7a27a0aa5965aeb12631f5e3b18663ec723064f2ff2eb783fa7e5f0b', 2, 'sss', '2151341532@qq.com', NULL, '2022-03-22 14:18:12', 'sss_s.png', 'sss_m.png', 'sss_l.png', NULL, '2d2d2d2d2d424547494e205253412050524956415445204b45592d2d2d2d2d0a4d4949435941494241414b426751444947646263336e3332374563394e4e74727054444f6f6e71473961546a6c55346d755677394874666356646739715751630a565445757a3777736a394d6e3232654638643275324b496868494e306e705a6233705873483678676a705038396f59506142424a43454830616d7751304c46660a5572612b2b4b78367431585971585a477479492f6a634d3830474e4835522b41665a4f417552574a4a674b37344a30624d50344273712f456c774944415141420a416f4741442b4c56527857323547716677554534426c544943692b6d454a37683531754d4a394468664d79394548595551396a31354c5879774b656e5a645a4a0a536b6e463730466a65795568776731324c6b55453036635638566c4e2f4a3238594a66565469496c306d32595547586349504f58334c71456f3474315333386e0a794c614c456e6b793558626b6b445a355379767a6931514652445a733851566771656477487366387743636c2f326b435251445a567744334967532f6f4547580a69567455497a47697455782f437a456c77746f6a4c7871483251334c746252444951553779694e6d416463485a634f52365a545639366763416a47454c6966470a4a384363525961543577436e34774939414f757830383766542b537357763353762b4d4e554162794259654d463179625a744f68494f347033466a4f376549640a3866526e316b383351327232746f6e6f616b51776e4d5037636874326464474776514a464149494435794c763664464d7142426a3767754f4a6a4a45724b64500a5a6135474f304a532b6c634d424a4735654557304b6a4a5451517654792f4f7a372b4f497a5332577771314772714a354466676662627a4f5a717878773157720a416a78683559485a656b322f3649722b784975704c6a31674e535277305a4a6568376d6c433163584e5648746e54325858754c42706d4f516b5a367944666c780a764a52753846596333524c664c3076756c47304352417676513979686949784c4a6a52325573512f366a716d6f3068376b716e497935475542665836483477330a4e627948636d624750774451486f68416547596b35724650384e636143344e4e4b476d4c723678593169416b2f7343300a2d2d2d2d2d454e44205253412050524956415445204b45592d2d2d2d2d0a', 'abaef3ea92ebeeae36f788217899195204834ee95972b7c5dae5c907023a1ee636e00c0a0e2cba09143d047f4efbb7a501052fd57a8c6f736168e54733ced19e54921008767e360859078458d259756951618bb8efc62fee090b888557f8e7aa04f5846843c2ececa98b08ef7f8079879fe93a1397114c34e106374f14ed4f37', 1, 1, 0, 2, 1, 1, 1, 0);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
