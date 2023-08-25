import mysql.connector
from main import get_mysql_config

mysql_ip, mysql_username, mysql_password, mysql_database, mysql_table = get_mysql_config("config.yaml")

conn = mysql.connector.connect(
    host=mysql_ip,
    user=mysql_username,
    password=mysql_password,
    database=mysql_database
)

cursor = conn.cursor()
delete_query = "DELETE FROM {}".format(mysql_table)
cursor.execute(delete_query)
conn.commit()

cursor.close()
conn.close()

print("Deleted all data from the table.")
