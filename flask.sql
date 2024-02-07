/*
 Navicat Premium Data Transfer

 Source Server         : min
 Source Server Type    : MySQL
 Source Server Version : 80026 (8.0.26)
 Source Host           : localhost:3306
 Source Schema         : flask

 Target Server Type    : MySQL
 Target Server Version : 80026 (8.0.26)
 File Encoding         : 65001

 Date: 24/06/2023 11:14:21
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student`  (
  `id` int NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `sex` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `age` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of student
-- ----------------------------
INSERT INTO `student` VALUES (110, '沐翎', '女', 11);
INSERT INTO `student` VALUES (1001, '张三', '女', 20);
INSERT INTO `student` VALUES (1002, '李四', '女', 11);
INSERT INTO `student` VALUES (1003, '王五', '男', 12);
INSERT INTO `student` VALUES (1004, '孙六', '男', 23);
INSERT INTO `student` VALUES (1005, '一', '男', 2);
INSERT INTO `student` VALUES (1006, '二', '女', 50);
INSERT INTO `student` VALUES (1007, '啊啊啊', '女', 50);
INSERT INTO `student` VALUES (1008, '二', '女', 30);
INSERT INTO `student` VALUES (1009, '呜呜呜', '男', 55);
INSERT INTO `student` VALUES (1111, '啊啊啊', '女', 55);
INSERT INTO `student` VALUES (10000, '啊啊啊', '男', 55);
INSERT INTO `student` VALUES (10017, '啊啊啊', '男', 20);

SET FOREIGN_KEY_CHECKS = 1;
