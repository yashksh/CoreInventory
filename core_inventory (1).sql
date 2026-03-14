-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 14, 2026 at 12:10 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `core_inventory`
--

-- --------------------------------------------------------

--
-- Table structure for table `contacts`
--

CREATE TABLE `contacts` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `type` enum('vendor','customer','internal') DEFAULT 'vendor',
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contacts`
--

INSERT INTO `contacts` (`id`, `name`, `type`, `email`, `phone`, `created_at`) VALUES
(1, 'Azure Interior', 'vendor', NULL, NULL, '2026-03-14 08:20:09'),
(2, 'Azure Interior', 'vendor', 'sales@azureinterior.com', '+91 79 2345 6789', '2026-03-14 09:37:49'),
(3, 'Steel Craft Supplies', 'vendor', 'orders@steelcraft.in', '+91 22 4567 8901', '2026-03-14 09:37:49'),
(4, 'TimberWorks India', 'vendor', 'info@timberworks.co.in', '+91 80 3456 7890', '2026-03-14 09:37:49'),
(5, 'PackRight Solutions', 'vendor', 'contact@packright.com', '+91 44 5678 9012', '2026-03-14 09:37:49'),
(6, 'Nova Electronics', 'vendor', 'procurement@novaelec.in', '+91 11 6789 0123', '2026-03-14 09:37:49'),
(7, 'Pinnacle Furnishings', 'customer', 'buying@pinnacle.co.in', '+91 79 7890 1234', '2026-03-14 09:37:49'),
(8, 'Metro Office Hub', 'customer', 'orders@metrooffice.com', '+91 22 8901 2345', '2026-03-14 09:37:49'),
(9, 'GreenLeaf Interiors', 'customer', 'design@greenleaf.in', '+91 80 9012 3456', '2026-03-14 09:37:49'),
(10, 'Skyline Commercial', 'customer', 'procurement@skylinecomm.com', '+91 11 0123 4567', '2026-03-14 09:37:49'),
(11, 'Coastal Retail Group', 'customer', 'supply@coastalretail.in', '+91 44 1234 5678', '2026-03-14 09:37:49');

-- --------------------------------------------------------

--
-- Table structure for table `inventory`
--

CREATE TABLE `inventory` (
  `id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `location_id` int(11) NOT NULL,
  `quantity` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inventory`
--

INSERT INTO `inventory` (`id`, `product_id`, `location_id`, `quantity`) VALUES
(1, 1, 1, 50),
(2, 2, 1, 50),
(3, 1, 3, 45),
(4, 1, 7, 20),
(5, 1, 10, 12),
(6, 2, 3, 30),
(7, 2, 4, 15),
(8, 2, 10, 8),
(9, 3, 3, 120),
(10, 3, 7, 60),
(11, 3, 10, 40),
(12, 4, 3, 200),
(13, 4, 7, 80),
(14, 4, 11, 50),
(15, 5, 4, 35),
(16, 5, 8, 25),
(17, 6, 4, 50),
(18, 6, 7, 30),
(19, 6, 10, 20),
(20, 7, 3, 80),
(21, 7, 8, 45),
(22, 8, 3, 150),
(23, 8, 7, 70),
(24, 8, 11, 35),
(25, 9, 4, 60),
(26, 9, 8, 40),
(27, 10, 3, 25),
(28, 10, 10, 10),
(29, 11, 4, 15),
(30, 11, 11, 5),
(31, 12, 3, 200),
(32, 12, 7, 100),
(33, 13, 4, 500),
(34, 13, 8, 300),
(35, 13, 11, 200),
(36, 14, 4, 40),
(37, 14, 8, 20),
(38, 15, 3, 90),
(39, 15, 7, 60),
(40, 15, 10, 30);

-- --------------------------------------------------------

--
-- Table structure for table `locations`
--

CREATE TABLE `locations` (
  `id` int(11) NOT NULL,
  `warehouse_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `short_code` varchar(20) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `locations`
--

INSERT INTO `locations` (`id`, `warehouse_id`, `name`, `short_code`, `created_at`) VALUES
(1, 1, 'Stock1', 'WH/Stock1', '2026-03-14 08:20:09'),
(2, 1, 'Stock2', 'WH/Stock2', '2026-03-14 08:20:09'),
(3, 1, 'Stock Zone A', 'WH/Stock-A', '2026-03-14 09:37:49'),
(4, 1, 'Stock Zone B', 'WH/Stock-B', '2026-03-14 09:37:49'),
(5, 1, 'Receiving Dock', 'WH/Recv', '2026-03-14 09:37:49'),
(6, 1, 'Shipping Dock', 'WH/Ship', '2026-03-14 09:37:49'),
(7, 2, 'Shelf 1', 'ND/Shelf-1', '2026-03-14 09:37:49'),
(8, 2, 'Shelf 2', 'ND/Shelf-2', '2026-03-14 09:37:49'),
(9, 2, 'Cold Storage', 'ND/Cold', '2026-03-14 09:37:49'),
(10, 3, 'Bay A', 'SH/Bay-A', '2026-03-14 09:37:49'),
(11, 3, 'Bay B', 'SH/Bay-B', '2026-03-14 09:37:49'),
(12, 3, 'Returns Area', 'SH/Returns', '2026-03-14 09:37:49');

-- --------------------------------------------------------

--
-- Table structure for table `move_history`
--

CREATE TABLE `move_history` (
  `id` int(11) NOT NULL,
  `move_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `from_location_id` int(11) DEFAULT NULL,
  `to_location_id` int(11) DEFAULT NULL,
  `quantity` int(11) NOT NULL,
  `move_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `move_history`
--

INSERT INTO `move_history` (`id`, `move_id`, `product_id`, `from_location_id`, `to_location_id`, `quantity`, `move_date`) VALUES
(1, 1, 1, 1, 1, 5, '2026-03-14 09:10:23'),
(2, 4, 1, 1, NULL, 5, '2026-03-14 09:12:57'),
(3, 10, 1, NULL, 3, 25, '2026-03-14 11:07:41'),
(4, 10, 3, NULL, 3, 50, '2026-03-14 11:07:41'),
(5, 10, 9, NULL, 3, 20, '2026-03-14 11:07:41'),
(6, 11, 5, NULL, 4, 15, '2026-03-14 11:07:41'),
(7, 11, 6, NULL, 4, 25, '2026-03-14 11:07:41'),
(8, 11, 15, NULL, 4, 40, '2026-03-14 11:07:41'),
(9, 12, 7, NULL, 7, 30, '2026-03-14 11:07:41'),
(10, 12, 8, NULL, 7, 45, '2026-03-14 11:07:41'),
(11, 12, 12, NULL, 7, 80, '2026-03-14 11:07:41'),
(12, 17, 1, 3, NULL, 10, '2026-03-14 11:07:41'),
(13, 17, 3, 3, NULL, 30, '2026-03-14 11:07:41'),
(14, 18, 7, 3, NULL, 15, '2026-03-14 11:07:41'),
(15, 18, 8, 3, NULL, 40, '2026-03-14 11:07:41'),
(16, 18, 9, 3, NULL, 10, '2026-03-14 11:07:41'),
(17, 19, 2, 7, NULL, 5, '2026-03-14 11:07:41'),
(18, 19, 6, 7, NULL, 12, '2026-03-14 11:07:41'),
(19, 24, 3, 3, 7, 25, '2026-03-14 11:07:41'),
(20, 24, 8, 3, 7, 20, '2026-03-14 11:07:41'),
(21, 28, 2, NULL, 3, 20, '2026-03-14 11:07:41'),
(22, 28, 4, NULL, 3, 80, '2026-03-14 11:07:41'),
(23, 29, 13, NULL, 8, 400, '2026-03-14 11:07:41'),
(24, 29, 14, NULL, 8, 30, '2026-03-14 11:07:41'),
(25, 29, 15, NULL, 8, 50, '2026-03-14 11:07:41'),
(26, 30, 1, NULL, 10, 15, '2026-03-14 11:07:41'),
(27, 30, 3, NULL, 10, 40, '2026-03-14 11:07:41'),
(28, 30, 10, NULL, 10, 12, '2026-03-14 11:07:41'),
(29, 35, 1, 3, NULL, 8, '2026-03-14 11:07:41'),
(30, 35, 3, 3, NULL, 20, '2026-03-14 11:07:41'),
(31, 35, 9, 3, NULL, 15, '2026-03-14 11:07:41'),
(32, 36, 8, 7, NULL, 35, '2026-03-14 11:07:41'),
(33, 36, 6, 7, NULL, 10, '2026-03-14 11:07:41'),
(34, 37, 4, 10, NULL, 30, '2026-03-14 11:07:41'),
(35, 37, 15, 10, NULL, 18, '2026-03-14 11:07:41'),
(36, 37, 10, 10, NULL, 6, '2026-03-14 11:07:41'),
(37, 42, 1, 3, 10, 10, '2026-03-14 11:07:41'),
(38, 42, 4, 3, 10, 25, '2026-03-14 11:07:41'),
(39, 43, 8, 7, 4, 15, '2026-03-14 11:07:41'),
(40, 43, 6, 7, 4, 8, '2026-03-14 11:07:41');

-- --------------------------------------------------------

--
-- Table structure for table `password_reset_tokens`
--

CREATE TABLE `password_reset_tokens` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `otp` varchar(6) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `expires_at` datetime NOT NULL,
  `used` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `password_reset_tokens`
--

INSERT INTO `password_reset_tokens` (`id`, `user_id`, `otp`, `created_at`, `expires_at`, `used`) VALUES
(1, 4, '504482', '2026-03-14 10:58:36', '2026-03-14 11:08:36', 1),
(2, 4, '833845', '2026-03-14 10:59:13', '2026-03-14 11:09:13', 1);

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `product_code` varchar(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `unit_cost` decimal(10,2) DEFAULT 0.00,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `product_code`, `name`, `unit_cost`, `created_at`) VALUES
(1, 'DESK001', 'Desk', 3000.00, '2026-03-14 08:20:09'),
(2, 'TABLE001', 'Table', 3000.00, '2026-03-14 08:20:09'),
(3, 'CHAIR001', 'Ergonomic Mesh Chair', 8750.00, '2026-03-14 09:37:49'),
(4, 'CHAIR002', 'Visitor Stacking Chair', 2200.00, '2026-03-14 09:37:49'),
(5, 'CAB001', 'Filing Cabinet 4-Drawer', 6800.00, '2026-03-14 09:37:49'),
(6, 'SHELF001', 'Industrial Metal Shelving', 4500.00, '2026-03-14 09:37:49'),
(7, 'MON001', '27\" 4K Monitor', 22000.00, '2026-03-14 09:37:49'),
(8, 'KEY001', 'Wireless Keyboard + Mouse', 1800.00, '2026-03-14 09:37:49'),
(9, 'LAMP001', 'LED Desk Lamp Adjustable', 1200.00, '2026-03-14 09:37:49'),
(10, 'WHTBRD01', 'Magnetic Whiteboard 6x4', 3500.00, '2026-03-14 09:37:49'),
(11, 'PROJ001', 'HD Projector 4000 Lumens', 35000.00, '2026-03-14 09:37:49'),
(12, 'CABLE01', 'CAT6 Ethernet Cable 50m', 850.00, '2026-03-14 09:37:49'),
(13, 'PAPER01', 'A4 Copier Paper (5 Reams)', 750.00, '2026-03-14 09:37:49'),
(14, 'TONER01', 'Laser Printer Toner Black', 2800.00, '2026-03-14 09:37:49'),
(15, 'LOCK001', 'Combination Padlock Heavy', 650.00, '2026-03-14 09:37:49');

-- --------------------------------------------------------

--
-- Table structure for table `stock_moves`
--

CREATE TABLE `stock_moves` (
  `id` int(11) NOT NULL,
  `reference` varchar(30) NOT NULL,
  `operation_type` enum('receipt','delivery','internal') NOT NULL,
  `contact_id` int(11) DEFAULT NULL,
  `from_location_id` int(11) DEFAULT NULL,
  `to_location_id` int(11) DEFAULT NULL,
  `schedule_date` date DEFAULT NULL,
  `status` enum('draft','waiting','ready','done') DEFAULT 'draft',
  `created_by` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `stock_moves`
--

INSERT INTO `stock_moves` (`id`, `reference`, `operation_type`, `contact_id`, `from_location_id`, `to_location_id`, `schedule_date`, `status`, `created_by`, `created_at`) VALUES
(1, 'WH/IN/00001', 'receipt', 1, 1, 1, '2003-10-18', 'done', 2, '2026-03-14 08:37:01'),
(3, 'WH/IN/00002', 'receipt', NULL, NULL, NULL, '2026-03-14', 'draft', 2, '2026-03-14 09:11:02'),
(4, 'WH/OUT/00001', 'delivery', 1, 1, NULL, '2026-03-14', 'done', 2, '2026-03-14 09:11:45'),
(5, 'WH/INT/00001', 'internal', NULL, NULL, NULL, '2026-03-14', 'draft', 2, '2026-03-14 09:15:32'),
(6, 'WH/IN/00003', 'receipt', 1, NULL, 1, '2026-03-03', 'ready', 2, '2026-03-14 09:21:10'),
(7, 'WH/OUT/00002', 'delivery', 1, 2, NULL, '2026-03-09', 'waiting', 2, '2026-03-14 09:22:05'),
(9, 'WH/INT/00002', 'internal', NULL, NULL, NULL, '2026-03-14', 'draft', 2, '2026-03-14 09:23:19'),
(10, 'M/IN/00001', 'receipt', 2, NULL, 3, '2026-02-08', 'done', 4, '2026-03-14 11:07:41'),
(11, 'M/IN/00002', 'receipt', 3, NULL, 4, '2026-02-14', 'done', 4, '2026-03-14 11:07:41'),
(12, 'M/IN/00003', 'receipt', 6, NULL, 7, '2026-02-22', 'done', 4, '2026-03-14 11:07:41'),
(13, 'M/IN/00004', 'receipt', 4, NULL, 3, '2026-03-16', 'ready', 4, '2026-03-14 11:07:41'),
(14, 'M/IN/00005', 'receipt', 5, NULL, 10, '2026-03-18', 'ready', 4, '2026-03-14 11:07:41'),
(15, 'M/IN/00006', 'receipt', 2, NULL, 8, '2026-03-20', 'waiting', 4, '2026-03-14 11:07:41'),
(16, 'M/IN/00007', 'receipt', 6, NULL, 3, '2026-03-25', 'draft', 4, '2026-03-14 11:07:41'),
(17, 'M/OUT/00001', 'delivery', 7, 3, NULL, '2026-02-10', 'done', 4, '2026-03-14 11:07:41'),
(18, 'M/OUT/00002', 'delivery', 8, 3, NULL, '2026-02-20', 'done', 4, '2026-03-14 11:07:41'),
(19, 'M/OUT/00003', 'delivery', 9, 7, NULL, '2026-03-01', 'done', 4, '2026-03-14 11:07:41'),
(20, 'M/OUT/00004', 'delivery', 10, 10, NULL, '2026-03-17', 'ready', 4, '2026-03-14 11:07:41'),
(21, 'M/OUT/00005', 'delivery', 11, 4, NULL, '2026-03-19', 'ready', 4, '2026-03-14 11:07:41'),
(22, 'M/OUT/00006', 'delivery', 7, 3, NULL, '2026-03-22', 'waiting', 4, '2026-03-14 11:07:41'),
(23, 'M/OUT/00007', 'delivery', 8, 8, NULL, '2026-03-28', 'draft', 4, '2026-03-14 11:07:41'),
(24, 'M/INT/00001', 'internal', NULL, 3, 7, '2026-03-02', 'done', 4, '2026-03-14 11:07:41'),
(25, 'M/INT/00002', 'internal', NULL, 7, 10, '2026-03-16', 'ready', 4, '2026-03-14 11:07:41'),
(26, 'M/INT/00003', 'internal', NULL, 4, 11, '2026-03-21', 'waiting', 4, '2026-03-14 11:07:41'),
(27, 'M/INT/00004', 'internal', NULL, 3, 4, '2026-03-26', 'draft', 4, '2026-03-14 11:07:41'),
(28, 'Y/IN/00001', 'receipt', 4, NULL, 3, '2026-02-05', 'done', 5, '2026-03-14 11:07:41'),
(29, 'Y/IN/00002', 'receipt', 5, NULL, 8, '2026-02-18', 'done', 5, '2026-03-14 11:07:41'),
(30, 'Y/IN/00003', 'receipt', 2, NULL, 10, '2026-03-03', 'done', 5, '2026-03-14 11:07:41'),
(31, 'Y/IN/00004', 'receipt', 3, NULL, 4, '2026-03-15', 'ready', 5, '2026-03-14 11:07:41'),
(32, 'Y/IN/00005', 'receipt', 6, NULL, 7, '2026-03-18', 'ready', 5, '2026-03-14 11:07:41'),
(33, 'Y/IN/00006', 'receipt', 4, NULL, 3, '2026-03-22', 'waiting', 5, '2026-03-14 11:07:41'),
(34, 'Y/IN/00007', 'receipt', 5, NULL, 11, '2026-03-27', 'draft', 5, '2026-03-14 11:07:41'),
(35, 'Y/OUT/00001', 'delivery', 9, 3, NULL, '2026-02-12', 'done', 5, '2026-03-14 11:07:41'),
(36, 'Y/OUT/00002', 'delivery', 10, 7, NULL, '2026-02-25', 'done', 5, '2026-03-14 11:07:41'),
(37, 'Y/OUT/00003', 'delivery', 11, 10, NULL, '2026-03-05', 'done', 5, '2026-03-14 11:07:41'),
(38, 'Y/OUT/00004', 'delivery', 7, 3, NULL, '2026-03-17', 'ready', 5, '2026-03-14 11:07:41'),
(39, 'Y/OUT/00005', 'delivery', 8, 4, NULL, '2026-03-20', 'ready', 5, '2026-03-14 11:07:41'),
(40, 'Y/OUT/00006', 'delivery', 9, 8, NULL, '2026-03-24', 'waiting', 5, '2026-03-14 11:07:41'),
(41, 'Y/OUT/00007', 'delivery', 10, 3, NULL, '2026-03-30', 'draft', 5, '2026-03-14 11:07:41'),
(42, 'Y/INT/00001', 'internal', NULL, 3, 10, '2026-02-28', 'done', 5, '2026-03-14 11:07:41'),
(43, 'Y/INT/00002', 'internal', NULL, 7, 4, '2026-03-08', 'done', 5, '2026-03-14 11:07:41'),
(44, 'Y/INT/00003', 'internal', NULL, 4, 8, '2026-03-18', 'ready', 5, '2026-03-14 11:07:41'),
(45, 'Y/INT/00004', 'internal', NULL, 10, 3, '2026-03-23', 'waiting', 5, '2026-03-14 11:07:41'),
(46, 'Y/INT/00005', 'internal', NULL, 3, 7, '2026-03-29', 'draft', 5, '2026-03-14 11:07:41'),
(47, 'WH/OUT/00003', 'delivery', NULL, NULL, NULL, '2026-03-14', 'draft', 5, '2026-03-14 11:08:26'),
(48, 'WH/INT/00003', 'internal', NULL, NULL, NULL, '2026-03-14', 'draft', 5, '2026-03-14 11:08:31');

-- --------------------------------------------------------

--
-- Table structure for table `stock_move_lines`
--

CREATE TABLE `stock_move_lines` (
  `id` int(11) NOT NULL,
  `move_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `stock_move_lines`
--

INSERT INTO `stock_move_lines` (`id`, `move_id`, `product_id`, `quantity`) VALUES
(1, 1, 1, 5),
(2, 4, 1, 5),
(3, 6, 1, 50),
(6, 7, 1, 20),
(7, 10, 1, 25),
(8, 10, 3, 50),
(9, 10, 9, 20),
(10, 11, 5, 15),
(11, 11, 6, 25),
(12, 11, 15, 40),
(13, 12, 7, 30),
(14, 12, 8, 45),
(15, 12, 12, 80),
(16, 13, 2, 12),
(17, 13, 4, 60),
(18, 14, 13, 300),
(19, 14, 14, 25),
(20, 15, 1, 18),
(21, 15, 10, 10),
(22, 16, 11, 8),
(23, 16, 7, 20),
(24, 16, 12, 50),
(25, 17, 1, 10),
(26, 17, 3, 30),
(27, 18, 7, 15),
(28, 18, 8, 40),
(29, 18, 9, 10),
(30, 19, 2, 5),
(31, 19, 6, 12),
(32, 20, 4, 35),
(33, 20, 15, 20),
(34, 21, 5, 10),
(35, 21, 14, 15),
(36, 22, 1, 20),
(37, 22, 11, 3),
(38, 23, 13, 200),
(39, 23, 6, 8),
(40, 24, 3, 25),
(41, 24, 8, 20),
(42, 25, 4, 40),
(43, 25, 12, 30),
(44, 26, 9, 15),
(45, 26, 14, 10),
(46, 27, 7, 10),
(47, 27, 10, 5),
(48, 28, 2, 20),
(49, 28, 4, 80),
(50, 29, 13, 400),
(51, 29, 14, 30),
(52, 29, 15, 50),
(53, 30, 1, 15),
(54, 30, 3, 40),
(55, 30, 10, 12),
(56, 31, 6, 35),
(57, 31, 5, 20),
(58, 32, 7, 25),
(59, 32, 8, 60),
(60, 32, 12, 100),
(61, 33, 2, 15),
(62, 33, 3, 30),
(63, 34, 13, 250),
(64, 34, 9, 30),
(65, 34, 11, 5),
(66, 35, 1, 8),
(67, 35, 3, 20),
(68, 35, 9, 15),
(69, 36, 8, 35),
(70, 36, 6, 10),
(71, 37, 4, 30),
(72, 37, 15, 18),
(73, 37, 10, 6),
(74, 38, 2, 8),
(75, 38, 1, 12),
(76, 39, 5, 12),
(77, 39, 14, 18),
(78, 40, 13, 150),
(79, 40, 7, 10),
(80, 41, 3, 45),
(81, 41, 11, 4),
(82, 41, 12, 60),
(83, 42, 1, 10),
(84, 42, 4, 25),
(85, 43, 8, 15),
(86, 43, 6, 8),
(87, 44, 9, 20),
(88, 44, 14, 12),
(89, 45, 3, 15),
(90, 45, 15, 10),
(91, 46, 7, 12),
(92, 46, 12, 40),
(93, 46, 10, 8);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `login_id` varchar(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `login_id`, `email`, `password_hash`, `created_at`) VALUES
(1, 'admin', 'admin@coreinventory.com', 'scrypt:32768:8:1$placeholder$changeme', '2026-03-14 08:20:09'),
(2, 'gfdhfgzdv', 'maithil@gmail.com', 'scrypt:32768:8:1$hpwZVRx3RYha1Ag8$73eef0134f6f4f0af41b4d4d1be0a6e0a1c13eba7062c96558fea814654f240202e89453f7691f5af4feeb5e10a37d86f26d400ae1245f9c79a035d15216c7a4', '2026-03-14 08:33:54'),
(3, 'maithil@18', 'jsdfnkj@gmail.com', 'scrypt:32768:8:1$SQhIhLxnhsfdBz9w$138a81244ac64cf4bb0ec892ed69d471fd991b648a87dcdca337941cff475cf716732e5e35c072bf0b65737c9cf4cc59a6f96c1120208930470b85a20918ba56', '2026-03-14 10:18:47'),
(4, 'Maithil', 'maithilkorat2006@gmail.com', 'scrypt:32768:8:1$oW2tvP4xjfSNWBCY$d89a090774ccd87b5fc590361979005849b78f787b47b81e870bf6209c4cdb3bde4dd842f4954d61fb8e9cf7cd8ebf3d4f5931c756745f72042bbaf8716cfefc', '2026-03-14 10:56:50'),
(5, 'Myth12', 'maithilkorat@gmail.com', 'scrypt:32768:8:1$lKIB8YEfr4k6OD7U$8a0e593b804a340edf0d09d8d0ced13810ded853f2c8156e7508e2cb8e6912c7537ae003e9f464623de9914ac61d2fbc6ad91f17742da8b070849e0ca5114e61', '2026-03-14 11:01:21');

-- --------------------------------------------------------

--
-- Table structure for table `warehouses`
--

CREATE TABLE `warehouses` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `short_code` varchar(10) NOT NULL,
  `address` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `warehouses`
--

INSERT INTO `warehouses` (`id`, `name`, `short_code`, `address`, `created_at`) VALUES
(1, 'Main Warehouse', 'WH', 'Ahmedabad', '2026-03-14 08:20:09'),
(2, 'North Distribution', 'ND', '45 Logistics Park, Delhi', '2026-03-14 09:37:49'),
(3, 'South Hub', 'SH', '78 Trade Centre, Chennai', '2026-03-14 09:37:49');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `contacts`
--
ALTER TABLE `contacts`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `inventory`
--
ALTER TABLE `inventory`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `product_id` (`product_id`,`location_id`),
  ADD KEY `location_id` (`location_id`);

--
-- Indexes for table `locations`
--
ALTER TABLE `locations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `warehouse_id` (`warehouse_id`);

--
-- Indexes for table `move_history`
--
ALTER TABLE `move_history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `move_id` (`move_id`),
  ADD KEY `product_id` (`product_id`),
  ADD KEY `from_location_id` (`from_location_id`),
  ADD KEY `to_location_id` (`to_location_id`);

--
-- Indexes for table `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_user_id` (`user_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `product_code` (`product_code`);

--
-- Indexes for table `stock_moves`
--
ALTER TABLE `stock_moves`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `reference` (`reference`),
  ADD KEY `contact_id` (`contact_id`),
  ADD KEY `from_location_id` (`from_location_id`),
  ADD KEY `to_location_id` (`to_location_id`),
  ADD KEY `created_by` (`created_by`);

--
-- Indexes for table `stock_move_lines`
--
ALTER TABLE `stock_move_lines`
  ADD PRIMARY KEY (`id`),
  ADD KEY `move_id` (`move_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `login_id` (`login_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `warehouses`
--
ALTER TABLE `warehouses`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `short_code` (`short_code`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `contacts`
--
ALTER TABLE `contacts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `inventory`
--
ALTER TABLE `inventory`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `locations`
--
ALTER TABLE `locations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `move_history`
--
ALTER TABLE `move_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `stock_moves`
--
ALTER TABLE `stock_moves`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT for table `stock_move_lines`
--
ALTER TABLE `stock_move_lines`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=94;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `warehouses`
--
ALTER TABLE `warehouses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `inventory`
--
ALTER TABLE `inventory`
  ADD CONSTRAINT `inventory_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `inventory_ibfk_2` FOREIGN KEY (`location_id`) REFERENCES `locations` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `locations`
--
ALTER TABLE `locations`
  ADD CONSTRAINT `locations_ibfk_1` FOREIGN KEY (`warehouse_id`) REFERENCES `warehouses` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `move_history`
--
ALTER TABLE `move_history`
  ADD CONSTRAINT `move_history_ibfk_1` FOREIGN KEY (`move_id`) REFERENCES `stock_moves` (`id`),
  ADD CONSTRAINT `move_history_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  ADD CONSTRAINT `move_history_ibfk_3` FOREIGN KEY (`from_location_id`) REFERENCES `locations` (`id`),
  ADD CONSTRAINT `move_history_ibfk_4` FOREIGN KEY (`to_location_id`) REFERENCES `locations` (`id`);

--
-- Constraints for table `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  ADD CONSTRAINT `fk_password_reset_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `stock_moves`
--
ALTER TABLE `stock_moves`
  ADD CONSTRAINT `stock_moves_ibfk_1` FOREIGN KEY (`contact_id`) REFERENCES `contacts` (`id`),
  ADD CONSTRAINT `stock_moves_ibfk_2` FOREIGN KEY (`from_location_id`) REFERENCES `locations` (`id`),
  ADD CONSTRAINT `stock_moves_ibfk_3` FOREIGN KEY (`to_location_id`) REFERENCES `locations` (`id`),
  ADD CONSTRAINT `stock_moves_ibfk_4` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`);

--
-- Constraints for table `stock_move_lines`
--
ALTER TABLE `stock_move_lines`
  ADD CONSTRAINT `stock_move_lines_ibfk_1` FOREIGN KEY (`move_id`) REFERENCES `stock_moves` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `stock_move_lines_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
