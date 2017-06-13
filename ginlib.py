import zipfile
import os.path
import ntpath, pdb
import re
from subprocess import call
from time import gmtime, strftime
from unrar import rarfile
import tarfile
import platform
import subprocess
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def sin(rom):
	print 'Please wait...\nGetting system.sin from ROM...'
	foldersin = 'system.sin' + rom.replace('/','.')
	foldersin = re.sub( '\s+', '', foldersin ).strip()
	if os.path.exists(foldersin):
		os.system('rm -rf ' + foldersin)
	with zipfile.ZipFile(rom,"r") as zip_ref:
		zip_ref.extract('system.sin', foldersin)
	print 'GET system.sin SUCCESSFULLY.\nGetting system.ext4 from system.sin...'
	call(["java","-jar","sin2ext4.jar",foldersin,"/system.sin"])
	filename = os.path.splitext(rom)[0]

	print 'GET system.ext4 SUCCESSFULLY.'
	print 'Mounting system.ext4...'
	tmp = 'system' + rom.replace('/','.')
	if os.path.exists(tmp):
		os.system('rm -rf ' + tmp)
	tmp = re.sub( '\s+', '', tmp ).strip()
	os.makedirs(tmp)
	call(["sudo","mount","-t","ext4",foldersin + '/system.ext4 ./',tmp])
	print 'MOUNT system.ext4 SUCCESSFULLY.\nGetting /system/framework...'
	output = 'framework_' + path_leaf(rom)  + '_' +  strftime('%Y-%m-%d_%H-%M-%S', gmtime())
	output = re.sub( '\s+', '', output ).strip()
	os.makedirs(output)
	sdk, version = get_sdk_version_android(tmp)
	if sdk == 21 or sdk == 22 :
    		os.system('java -jar oat2dex_v0.86.jar -o '+ tmp + '/framework/ devfw '+ tmp + '/framework/')
	elif sdk >= 23:
    		os.system('java -jar oat2dex.jar -o '+ tmp + '/framework/ devfw '+ tmp + '/framework/')		
	checkFile = os.path.isfile(tmp + '/framework/boot-jar-result/framework.jar')
	if checkFile:
    		call('cp -r '+tmp + '/framework/boot-jar-result/framework.jar ' +output+'/framework.jar', shell=True)
	else:
    		call('cp -r '+tmp + '/framework/framework.jar ' +output+'/framework.jar', shell=True)
	print 'GET /system/framework SUCCESSFULLY.'
	call(["sudo", "umount", tmp])
	os.system('rm -rf ' + tmp)
	os.system('rm -rf ' + foldersin)
	size = 0
	checkFile = os.path.isfile(output + '/framework.jar')
	if checkFile:
		size = os.path.getsize(output + '/framework.jar')
	return size,output,sdk,version


def dat(rom):
	print 'Please wait...\nGetting system.transfer.list and system.new.dat from ROM...'
	folderdat = 'system.dat' + rom.replace('/','.')
	folderdat = re.sub( '\s+', '', folderdat ).strip()
	if os.path.exists(folderdat):
		os.system('rm -rf ' + folderdat)
	with zipfile.ZipFile(rom,"r") as zip_ref:
		zip_ref.extract('system.new.dat', folderdat)
		zip_ref.extract('system.transfer.list', folderdat)
	print 'GET system.transfer.list AND system.new.dat SUCCESSFULLY.\nGetting system.img...'
	call(["python", "./sdat2img.py", folderdat + "/system.transfer.list", folderdat + "/system.new.dat", folderdat + "/system.img"])
	print 'GET system.img SUCCESSFULLY.'
	print 'Mounting system.img...'
	tmp = 'system' + rom.replace('/','.')
	tmp = re.sub( '\s+', '', tmp ).strip()	
	#pdb.set_trace()
	os.makedirs(tmp)
	linkMount = folderdat + '/system.img'
	call(["sudo","mount",linkMount,tmp])
	print 'MOUNT system.img SUCCESSFULLY.\nGetting /system/framework...'
	print 'Deodex .jar ....'
	sdk, version = get_sdk_version_android(tmp)
	if sdk == '21' or sdk == '22' :
		os.system('java -jar oat2dex_v0.86.jar -o '+ tmp + '/framework/ devfw '+ tmp + '/framework/')
	elif int(sdk) >= 23:
		os.system('java -jar oat2dex.jar -o '+ tmp + '/framework/ devfw '+ tmp + '/framework/')			
	output = 'framework_' + path_leaf(rom)  + '_' +  strftime('%Y-%m-%d_%H-%M-%S', gmtime())
	output = re.sub( '\s+', '', output ).strip()
	os.makedirs(output)
	checkFile = os.path.isfile(tmp+ '/framework/boot-jar-result/framework.jar')
	if checkFile:
    		tmp1 = tmp + '/framework/boot-jar-result/framework.jar'
	else:
    		tmp1 = tmp + '/framework/framework.jar'
	call('cp -r '+tmp1+' ./' +output+'/framework.jar', shell=True)
	print 'GET /system/framework SUCCESSFULLY.'

	call(["sudo", "umount",tmp])
	
	os.system('rm -rf ' + folderdat)
	os.system('rm -rf ' + tmp)
	size = 0
	checkFile = os.path.isfile(output + '/framework.jar')
	if checkFile:
		size = os.path.getsize(output + '/framework.jar')
	return size,output,sdk,version

def raw(rom):
	print 'Please wait...\nExtracting ROM...'
	folderraw = 'system.raw' + rom.replace('/','.')
	folderraw = re.sub( '\s+', '', folderraw ).strip()
	if os.path.exists(folderraw):
		os.system('rm -rf ' + folderraw)
	tmp = 'ROM' + rom.replace('/','.')
	tmp = re.sub( '\s+', '', tmp ).strip()
	with zipfile.ZipFile(rom,"r") as zip_ref:
		zip_ref.extractall("./" + tmp)
	print 'EXTRACT ROM SUCCESSFULLY.\nGetting /system/framework...'
	output = 'framework_' + path_leaf(rom)  + '_' +  strftime('%Y-%m-%d_%H-%M-%S',gmtime())
	output = re.sub( '\s+', '', output ).strip()
	os.makedirs(output)
	sdk, version = get_sdk_version_android(tmp)
	if sdk == 21 or sdk == 22 :
    		os.system('java -jar oat2dex_v0.86.jar -o '+ tmp + '/framework/ devfw '+ tmp + '/framework/')
	elif sdk >= 23:
    		os.system('java -jar oat2dex.jar -o '+ tmp + '/framework/ devfw '+ tmp + '/framework/')		

	checkFile = os.path.isfile(tmp + '/system/framework/boot-jar-result/framework.jar')
	if checkFile:
		tmp1 = 'cp -r ' + tmp + '/system/framework/boot-jar-result/framework.jar ' + output +'/framework.jar'
	else:
		tmp1 = 'cp -r ' + tmp + '/system/framework/framework.jar ' + output  +'/framework.jar'

	os.system(tmp1)
	print 'GET /system/framework SUCCESSFULLY.'
	os.system('rm -rf ' + tmp)
	size = 0
	checkFile = os.path.isfile(output + '/framework.jar')
	if checkFile:
		size = os.path.getsize(output + '/framework.jar')
	return size,output,sdk,version

def image(rom):
	print 'Please wait...\nExtracting ROM...'
	folderimage = 'system.img' + rom.replace('/','.')
	folderimage = re.sub( '\s+', '', folderimage ).strip()
	if os.path.exists(folderimage):
    		os.system('rm -rf ' + folderimage)
	tmp = 'ROM' + rom.replace('/','.')
	tmp = re.sub( '\s+', '', tmp ).strip()
	file_name, file_extension = os.path.splitext(rom)
	if file_extension == '.zip':
		with zipfile.ZipFile(rom,'r') as zip_ref:
			file_data = find_data_zip(zip_ref,'system.img')
			zip_ref.extract(file_data, folderimage)
	elif file_extension == '.rar':
			rar = rarfile.RarFile(rom,'r')
			file_data = find_data_rar(rar,'system.img')
			rar.extract(file_data, folderimage)
	elif file_extension == '.gz':
		with tarfile.TarFile(rom,'r') as tar_ref:
			tar_ref.extract(find_data_tar(tar_ref,'system.img'), folderimage)
	print 'GET system.img SUCCESSFULLY.\nGetting system.img...'
	#Convert img format android to ext4
	call(["simg2img",folderimage+'/'+file_data,folderimage+'/system.raw.img'])
	print 'CONVERTED system.img SUCCESSFULLY.\nGetting system.raw.img...'
	print 'Mounting system.raw.img...'
	tmp = 'system' + rom.replace('/','.')
	tmp = re.sub( '\s+', '', tmp ).strip()	
	os.makedirs(tmp)
	linkMount = folderimage + '/system.raw.img'
	call(["sudo","mount",linkMount,tmp])
	print 'MOUNT system.raw.img SUCCESSFULLY.\nGetting /system/framework...'
	print 'Deodex .jar ....'
	sdk, version = get_sdk_version_android(tmp)
	if sdk == 21 or sdk == 22 :
    		os.system('java -jar oat2dex_v0.86.jar -o '+ tmp + '/framework/ devfw '+ tmp + '/framework/')
	elif sdk >= 23:
    		os.system('java -jar oat2dex.jar -o '+ tmp + '/framework/ devfw '+ tmp + '/framework/')	
	output = 'framework_' + path_leaf(rom)  + '_' +  strftime('%Y-%m-%d_%H-%M-%S', gmtime())
	output = re.sub( '\s+', '', output ).strip()
	os.makedirs(output)
	checkFile = os.path.isfile(tmp+ '/framework/boot-jar-result/framework.jar')
	if checkFile:
    		tmp1 = tmp + '/framework/boot-jar-result/framework.jar'
	else:
    		tmp1 = tmp + '/framework/framework.jar'
	call('cp -r '+tmp1+' ./' +output+'/framework.jar', shell=True)
	print 'GET /system/framework SUCCESSFULLY.'

	call(["sudo", "umount",tmp])
	
	os.system('rm -rf ' + folderimage)
	os.system('rm -rf ' + tmp)
	size = 0
	checkFile = os.path.isfile(output + '/framework.jar')
	if checkFile:
		size = os.path.getsize(output + '/framework.jar')
	return size,output,sdk,version

def get_sdk_version_android(members):
    checkfile = 'build.prop'
    for dirname, dirnames, filenames in os.walk(members):
        for filename in filenames:
            if(checkfile == filename):
                path = os.path.join(dirname, filename)
                command = "cat " + path
                all_info = subprocess.check_output(command, shell=True).strip()
                for line1 in all_info.split("\n"):
                    if "ro.build.version.sdk" in line1:
                        sdk = re.sub("ro.build.version.sdk=", "",line1,1)
                        for line2 in all_info.split("\n"):
                            if "ro.build.version.release" in line2:
                                version = re.sub("ro.build.version.release=", "",line2,1)
                                return sdk,version
    return None,None

def get_sdk_version_brand_android(members):
    checkfile = 'build.prop'
    for dirname, dirnames, filenames in os.walk(members):
        for filename in filenames:
            if(checkfile == filename):
                path = os.path.join(dirname, filename)
                command = "cat " + path
                all_info = subprocess.check_output(command, shell=True).strip()
                for line1 in all_info.split("\n"):
                    if "ro.build.version.sdk" in line1:
                        sdk = re.sub("ro.build.version.sdk=", "",line1,1)
                        for line2 in all_info.split("\n"):
                            if "ro.build.version.release" in line2:
                                version = re.sub("ro.build.version.release=", "",line2,1)
                                for line3 in all_info.split("\n"):
									if "ro.product.brand" in line3:
										brand = re.sub("ro.product.brand=", "",line3,1)
										return sdk,version,brand
    return None,None,None


def find_data_tar(members,path):
    for member in members.getnames():
    	if(path_leaf(str(member)) == path):
			return str(member)
    return None
	
def find_data_zip(members,path):
    for member in members.namelist():
        	if(path_leaf(str(member)) == path):
				return str(member)
    return None

def find_data_rar(members,path):
    for member in members.namelist():
        	if(path_leaf(str(member)) == path):
				return str(member)
    return None
	

