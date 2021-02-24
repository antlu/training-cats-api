import psycopg2

conn = psycopg2.connect('dbname=wg_forge_db user=wg_forge host=localhost port=5433')
with conn:
    with conn.cursor() as cur:
        query = '''
        INSERT INTO cats_stat
        SELECT
            round(avg(tail_length), 1),
            percentile_cont(0.5) WITHIN GROUP (ORDER BY tail_length),
            mode() within group (order by tail_length),
            round(avg(whiskers_length), 1),
            percentile_cont(0.5) WITHIN GROUP (ORDER BY whiskers_length),
            mode() within group (order by whiskers_length)
        FROM cats;
        '''
        cur.execute(query)
conn.close()
