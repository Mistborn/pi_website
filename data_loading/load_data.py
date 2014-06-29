# # default
# engine = create_engine('postgresql://scott:tiger@localhost/mydatabase')
import psycopg2


# quick temporary solution (more awesome SQLAlchemy-based solution will come later)
def load_latest_temperature():
    connection = psycopg2.connect("dbname='pi_data' user='pi' host='localhost' password='temporarypassword'")
    cursor = connection.cursor()
    cursor.execute("""select log_time, cpu_temperature from system_stats_log order by log_time desc limit 1""")
    (time, cpu_temperature) = cursor.fetchone()
    return (time, cpu_temperature)

# for quick testing
if __name__ == '__main__':
    print(load_latest_temperature())