CREATE DATABASE IF NOT EXISTS ldev_sprinkler;

USE ldev_sprinkler;


CREATE TABLE `teams` (
    `id` VARCHAR(12) NOT NULL PRIMARY KEY,
    `name` VARCHAR(45) NOT NULL UNIQUE,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE `users` (
    `id` VARCHAR(12) NOT NULL PRIMARY KEY,
    `email` VARCHAR(45) NOT NULL UNIQUE,
    `password` VARCHAR(255) NOT NULL,
    `role` ENUM('superuser', 'commonuser') NOT NULL DEFAULT 'commonuser',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `team_id` VARCHAR(12),
    CONSTRAINT `fk_users_team_id`
        FOREIGN KEY (`team_id`)
        REFERENCES `teams`(`id`)
        ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE `user_activity_logs` (
    `id` VARCHAR(12) NOT NULL PRIMARY KEY,
    `action` VARCHAR(255) NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `users_id` VARCHAR(12) NOT NULL,
    CONSTRAINT `fk_user_activity_logs_users_id`
        FOREIGN KEY (`users_id`)
        REFERENCES `users`(`id`)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `locales` (
    `id` VARCHAR(12) NOT NULL PRIMARY KEY,
    `name` VARCHAR(45) NOT NULL,
    `latitude` DECIMAL(10, 8) NOT NULL,
    `longitude` DECIMAL(10, 8) NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `team_id` VARCHAR(12) NOT NULL,
    CONSTRAINT `fk_locales_team_id`
        FOREIGN KEY (`team_id`)
        REFERENCES `teams`(`id`)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `ldevs` (
    `id` VARCHAR(12) NOT NULL PRIMARY KEY,
    `name` VARCHAR(45) NOT NULL,
    `locales_id` VARCHAR(12) NOT NULL,
    CONSTRAINT `fk_ldevs_locales_id`
        FOREIGN KEY (`locales_id`)
        REFERENCES `locales`(`id`)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `logs` (
    `id` VARCHAR(12) NOT NULL PRIMARY KEY,
    `humidity` FLOAT NOT NULL,
    `temperature` FLOAT NOT NULL,
    `is_irrigating` TINYINT(1) NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `ldev_id` VARCHAR(12) NOT NULL,
    CONSTRAINT `fk_logs_ldev_id`
        FOREIGN KEY (`ldev_id`)
        REFERENCES `ldevs`(`id`)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `errors` (
    `id` VARCHAR(12) NOT NULL PRIMARY KEY,
    `message` VARCHAR(255) NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `ldev_id` VARCHAR(12) NOT NULL,
    CONSTRAINT `fk_errors_ldev_id`
        FOREIGN KEY (`ldev_id`)
        REFERENCES `ldevs`(`id`)
        ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE `routines` (
    `id` VARCHAR(12) NOT NULL PRIMARY KEY,
    `humidity` FLOAT,
    `temperature` FLOAT, 
    `begin_time` TIME,
    `end_time` TIME,
    `liters_of_water` INT,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `locales_id` VARCHAR(12) NOT NULL,
    CONSTRAINT `fk_routines_locales_id`
        FOREIGN KEY (`locales_id`)
        REFERENCES `locales`(`id`)
        ON DELETE CASCADE ON UPDATE CASCADE
);


