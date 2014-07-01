# ! /usr/bin/python3

from decimal import Decimal
import psycopg2
import os
from collections import namedtuple


class RaspberryPiData:
    def __init__(self):
        self.cpu_temperature = cpu_temperature()
        disk_size, used_space, free_space = disk_usage('/')
        self.disk_size = disk_size
        self.disk_usage = used_space

_ntuple_diskusage = namedtuple('usage', 'total used free')

def disk_usage(path):
    """Return disk usage statistics about the given path.

    Returned valus is a named tuple with attributes 'total', 'used' and
    'free', which are the amount of total, used and free space, in bytes.

    Credit: http://stackoverflow.com/a/7285483
    """
    st = os.statvfs(path)
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    return _ntuple_diskusage(total, used, free)

def cpu_temperature():
    with open('/sys/class/thermal/thermal_zone0/temp') as temperature_file:
        temperature_in_millidegrees = int(temperature_file.readline())
        temperature = Decimal(temperature_in_millidegrees / 1000).quantize(Decimal('.1'))  # show to one decimal place
    return temperature


# persist (save) data to database
def persist_data(data):
    connection = psycopg2.connect("dbname='pi_data' user='pi' host='localhost' password='temporarypassword'")
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO system_stats_log (cpu_temperature, disk_size, disk_usage)
                      VALUES ({cpu_temperature}, {disk_size}, {disk_usage})""".format(
                   cpu_temperature=data.cpu_temperature,
                   disk_size=data.disk_size,
                   disk_usage=data.disk_usage))
    connection.commit()


def main():
    data = RaspberryPiData()
    persist_data(data)


if __name__ == '__main__':
    main()