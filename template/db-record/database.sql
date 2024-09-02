mysql -u root -p
CREATE DATABASE IF NOT EXISTS `schooldb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE USER 'eben'@'localhost' IDENTIFIED BY '***********';
GRANT ALL PRIVILEGES ON `schooldb`.* TO 'eben'@'localhost';
FLUSH PRIVILEGES;

echo "Database created successfully"
