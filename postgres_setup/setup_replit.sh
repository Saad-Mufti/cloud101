rm -rf postgres
initdb -D postgres
echo "unix_socket_directories = ''" >> postgres/postgresql.conf
pg_ctl -D postgres -l logfile start
psql -h localhost -U runner -d postgres -a -f init.sql