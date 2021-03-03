import psycopg2

conn = psycopg2.connect('dbname=wg_forge_db user=wg_forge host=localhost port=5433')
cur = conn.cursor()
cur.execute('INSERT INTO cat_colors_info SELECT color, count(*) FROM cats GROUP BY color;')
conn.commit()
cur.close()
conn.close()
