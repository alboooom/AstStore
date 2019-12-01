import psycopg2
conn = psycopg2.connect(dbname='albertastaduran', user='albertastaduran',
                        password='mypassword', host='localhost')

cursor = conn.cursor()
def select(sql_request):
    list_with_dict = []
    cursor.execute(sql_request)
    data = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]
    for line in data:
        key_val = {}
        for n in range(len(colnames)):
            key_val[colnames[n]] = line[n]
        list_with_dict.append(key_val)
    return list_with_dict