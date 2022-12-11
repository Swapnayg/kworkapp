import psycopg2

conn = psycopg2.connect(database="kworkDB", user='postgres', password='swapna234', host='127.0.0.1', port= '5432')
cursor = conn.cursor()
sql = "DELETE FROM public.channels_postgres_groupchannel;"
cursor.execute(sql)
conn.commit()
cursor.close()
conn.close()
