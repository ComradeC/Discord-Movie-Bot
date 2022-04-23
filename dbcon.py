import psycopg2

conn = psycopg2.connect(dbname='moviebotdb', user='postgres', password='admin')     #local test connection
#conn = psycopg2.connect(dbname='postgres', user='root', password='root')          #public server connection