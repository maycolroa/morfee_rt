-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 24-06-2024 a las 22:55:19
-- Versión del servidor: 10.4.19-MariaDB
-- Versión de PHP: 7.4.20

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `db_morfee_rt`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users_usermorfee`
--

CREATE TABLE `users_usermorfee` (
  `id` bigint(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `cliente_id` bigint(20) DEFAULT NULL,
  `rol_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `users_usermorfee`
--

INSERT INTO `users_usermorfee` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `cliente_id`, `rol_id`) VALUES
(1, 'pbkdf2_sha256$600000$1DSwNivNgJhzg1xOaL9XWV$ALlvn4mtts505wrE94TWN0qDVnWRX0oeMof3QOfNBcI=', '2024-02-06 20:31:40.028251', 1, 'admin', 'DANIEL', 'FRANCO', 'a@gmail.com', 1, 1, '2023-08-28 19:52:00.409678', NULL, NULL),
(2, 'pbkdf2_sha256$600000$LwdqWj7wklYg3YfVCLq8PZ$4p+fpBu0ieEXkbbxncMHS5Utt3+pai2uEHk1j9fKzRo=', '2023-09-27 21:20:21.684207', 1, 'gustavo', '', '', 'a@gmail.com', 1, 1, '2023-09-27 21:18:38.950358', NULL, NULL);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `users_usermorfee`
--
ALTER TABLE `users_usermorfee`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD KEY `users_usermorfee_cliente_id_1fd026b8_fk_auth_cliente_id` (`cliente_id`),
  ADD KEY `users_usermorfee_rol_id_8acd7d58_fk_auth_rol_id` (`rol_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `users_usermorfee`
--
ALTER TABLE `users_usermorfee`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `users_usermorfee`
--
ALTER TABLE `users_usermorfee`
  ADD CONSTRAINT `users_usermorfee_cliente_id_1fd026b8_fk_auth_cliente_id` FOREIGN KEY (`cliente_id`) REFERENCES `auth_cliente` (`id`),
  ADD CONSTRAINT `users_usermorfee_rol_id_8acd7d58_fk_auth_rol_id` FOREIGN KEY (`rol_id`) REFERENCES `auth_rol` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
