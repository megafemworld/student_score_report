mysql -u root -p
CREATE DATABASE IF NOT EXISTS `schooldb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE USER 'don'@'localhost' IDENTIFIED BY '08033191820Ee';
GRANT ALL PRIVILEGES ON `schooldb`.* TO 'eben'@'localhost';
FLUSH PRIVILEGES;

echo "Database created successfully"
