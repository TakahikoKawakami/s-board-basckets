mysql -u root -e "create database basket_analysis"
mysql -u root -e "alter user root@localhost identified by 'root'"
cp src/.env.example src/.env