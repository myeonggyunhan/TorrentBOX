def filesize(value, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(value) < 1024.0:
            return "%3.1f%s%s" % (value, unit, suffix)
        value /= 1024.0
    return "%.1f%s%s" % (value, 'Yi', suffix)

def get_remain_time(total, downloaded, download_rate):
    if download_rate == 0:
        rtime = "0 sec"
        return rtime

    data = (total - downloaded) / download_rate

    m, s = divmod(data, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)

    if data < 60:
        rtime = "%d sec" % s
    elif data < 3600:
        rtime = "%d min %d sec" % (m, s)
    elif data < 216000:
        rtime = "%d hours %d min" % (h, m)
    else:
        rtime = "%d days %d hours" % (d, h)
    return rtime
