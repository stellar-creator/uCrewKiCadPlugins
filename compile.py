import os, sys, json, hashlib, shutil, time, datetime, dateutil.parser, zipfile
from os.path import basename
from shutil import make_archive

pluginDirSize = 0

def main():
	print("uCrew KiCad Repository Builder v0.1")
	buildZip('uCrewProjectUploader/latests.zip', 'uCrewProjectUploader/')
	packageBuilder()
	repositoryBuilder()
	print("Done!")

def getDirSize(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += getDirSize(entry.path)
    return total

def sha256(filename):
	sha256_hash = hashlib.sha256()
	with open(filename,"rb") as f:
		for byte_block in iter(lambda: f.read(4096),b""):
			sha256_hash.update(byte_block)
		return sha256_hash.hexdigest()

def buildZip(file, directory):
	print("Buld zip airchive of " + file + " in directory " + directory)
	if os.path.exists(file):
		os.remove(file)
	"""
	zipf = zipfile.ZipFile('.zip', 'w', zipfile.ZIP_DEFLATED)
	# Create zip
	for root, dirs, files in os.walk(directory):
		for zfile in files:
			zipf.write(os.path.join(root, zfile))
	zipf.close()
	"""
	shutil.make_archive(".tmp", "zip", directory)
	global pluginDirSize 
	pluginDirSize = getDirSize(directory)
	print("Directory size " + str(pluginDirSize))
	print("Copy .tmp.zip to " + file)
	shutil.copyfile('.tmp.zip', file)
	if os.path.exists('.tmp.zip'):
		os.remove('.tmp.zip')
	print("Zip airchive ready")

def fileSize(file):
	return os.path.getsize(file)

def getFileTimestamp(file):
	ti_m = os.path.getmtime(file)
	m_ti = time.ctime(ti_m)
	t_obj = time.strptime(m_ti)
	T_stamp = time.strftime("%Y-%m-%d %H:%M:%S", t_obj)
	return T_stamp

def packageBuilder():
	print("Read packages.json")
	# Read file
	packageFile = open('packages.json')
	# Load json
	packageData = json.load(packageFile)
	print("Current hash is " + packageData['packages'][0]['versions'][0]['download_sha256'])
	print("Current size is " + str(packageData['packages'][0]['versions'][0]['download_size']))
	# Change hash
	global pluginDirSize
	packageData['packages'][0]['versions'][0]['download_sha256'] = sha256('uCrewProjectUploader/latests.zip')
	packageData['packages'][0]['versions'][0]['download_size'] = int(fileSize('uCrewProjectUploader/latests.zip'))
	packageData['packages'][0]['versions'][0]['install_size'] = pluginDirSize

	print("New hash is " + packageData['packages'][0]['versions'][0]['download_sha256'])
	print("File size is " + str(packageData['packages'][0]['versions'][0]['download_size']))
	print("Save packages.json")
	with open('packages.json', 'w') as f:
		json.dump(packageData, f, indent=4)
	with open('uCrewProjectUploader/metadata.json', 'w') as f:
		json.dump(packageData['packages'][0], f, indent=4)

def repositoryBuilder():
	print("Read repository.json")
	repositoryFile = open('repository.json')
	repositoryData = json.load(repositoryFile)
	print("Work with packages")
	print("Current hash is " + repositoryData['packages']['sha256'])
	repositoryData['packages']['sha256'] = sha256('packages.json')
	print("New hash is " + repositoryData['packages']['sha256'])

	print("Current UTC timestamp is " + repositoryData['packages']['update_time_utc'])
	repositoryData['packages']['update_time_utc'] = getFileTimestamp('packages.json')
	print("New UTC timestamp is " + repositoryData['packages']['update_time_utc'])

	utcTimestamp = int(dateutil.parser.parse(repositoryData['packages']['update_time_utc'], dayfirst=True).timestamp())

	print("Current timestamp is " + str(repositoryData['packages']['update_timestamp']))
	repositoryData['packages']['update_timestamp'] = utcTimestamp
	print("New timestamp is " + str(repositoryData['packages']['update_timestamp']))

	print("Work with resources")
	print("Current hash is " + repositoryData['resources']['sha256'])
	repositoryData['resources']['sha256'] = sha256('resources.zip')
	print("New hash is " + repositoryData['resources']['sha256'])

	print("Current UTC timestamp is " + repositoryData['resources']['update_time_utc'])
	repositoryData['resources']['update_time_utc'] = getFileTimestamp('resources.zip')
	print("New UTC timestamp is " + repositoryData['resources']['update_time_utc'])

	utcTimestamp = int(dateutil.parser.parse(repositoryData['resources']['update_time_utc'], dayfirst=True).timestamp())

	print("Current timestamp is " + str(repositoryData['resources']['update_timestamp']))
	repositoryData['resources']['update_timestamp'] = utcTimestamp
	print("New timestamp is " + str(repositoryData['resources']['update_timestamp']))
	print("Save repository.json")
	with open('repository.json', 'w') as f:
		json.dump(repositoryData, f, indent=4)

if __name__ == "__main__":
    main()