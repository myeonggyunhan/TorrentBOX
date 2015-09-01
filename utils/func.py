import os
import zipfile
def compress_data(path, target):
        # change current working dir
        os.chdir(path)

        ziph = zipfile.ZipFile(target+".zip", 'w', allowZip64=True)
        for root, dirs, files in os.walk(target):
                for file in files:
                        ziph.write(os.path.join(root, file))
        ziph.close()

def unitConversion(data, data_type):
        if data_type is "download_rate":

		if data == 0:
			download_rate = "0 Kb/s"
		elif data<1000 and data>0:
			download_rate = float(data)
			download_rate = "%.2f Kb/s" % download_rate

		elif data<1000000 and data>1000:
			download_rate = float(data) /1000.0
			download_rate = "%.2f Kb/s" % download_rate

                elif data > 1000000:
			download_rate = float(data) /1000000.0
                        download_rate = "%.2f Mb/s" % download_rate
		else:
			print "ERROR"
 
		return download_rate

        elif data_type is "file":
                if data < 1000:
                        file_size = str(data) + "b"
                elif data < 1000000:
                        file_size = str(data/1000) + "Kb"
                elif data < 1000000000:
                        file_size = str(data/1000000) + "Mb"
                else:
                        file_size = str(data/1000000000) + "Gb"
                return file_size

        elif data_type is "time":
                m, s = divmod(data, 60)
                h, m = divmod(m, 60)
                d, h = divmod(h, 24)

                if data < 60:
                        time = "%d sec" % s
                elif data < 3600:
                        time = "%d min %d sec" % (m, s)
                elif data < 216000:
                        time = "%d hr %d min" % (h, m)
                else:
                        time = "%d days %d hr" % (d, h)
                return time
        else:
                return "Not Supported"
