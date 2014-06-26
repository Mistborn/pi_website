# ! /usr/bin/python3

from decimal import Decimal
import psycopg2


class RaspberryPiData:
    def __init__(self):
        self.cpu_temperature = cpu_temperature()


def cpu_temperature():
    with open('/sys/class/thermal/thermal_zone0/temp') as temperature_file:
        temperature_in_millidegrees = int(temperature_file.readline())
        temperature = Decimal(temperature_in_millidegrees / 1000).quantize(Decimal('.1'))  # show to one decimal place
    return temperature


# persist (save) data to database
def persist_data(data):
    connection = psycopg2.connect("dbname='pi_data' user='pi' host='localhost' password='temporarypassword'")
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO system_stats_log (cpu_temperature) VALUES ({cpu_temperature})""".format(
                   cpu_temperature=data.cpu_temperature))
    connection.commit()


def main():
    data = RaspberryPiData()
    persist_data(data)


if __name__ == '__main__':
    main()