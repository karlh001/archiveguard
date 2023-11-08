# Script to generate hash files in a directory structure
# My Site: https://karlhunter.co.uk/ag
# On GitHub: https://github.com/karlh001/archiveguardian
# By Karl Hunter 2023

import os, sys, hashlib, json, getopt
from datetime import datetime
from pathlib import Path

# Program information variables
ver_number = 1.2

# If changing the extension, make sure you are not
# running again on a previous directory with this
# current hash, otherwise all the objects and hash files
# will be re-hashed wasting time and resource.
hash_ext = '.aghash0'
# If you change the extension, add the character and
# input the number below. For example, .sha256 would be
# 7 characters, including the dot.
# This is used later to remove last x characters to 
# check if the file is a hash file.
hash_ext_size = 8

print(f'ArchiveGuardian version {ver_number}')

# Create variables for later
# Python doesn't like missing variables
dir_to_run = ''
dir_path = ''
confirm_schedule = ''

# Write hash function
def write_hash_func(file_path_full,save_as_file,checksum):

	# Set the buffer size; prevents large files clogging RAM
	buffer_size = 65536 

	# Set as sha256
	sha256 = hashlib.sha256()

	full_path_with_hash = str(file_path_full) + hash_ext

	# Get file size
	# To prevent error, the file size needs to be
	# greater than 0 bytes. Hash will not work otherwise
	file_size = os.path.getsize(file_path_full)

	# Check file can be opened
	# If not, this may be because permission denied
	file_accessiable = os.access(file_path_full, os.R_OK)


	if file_size > 0 and file_accessiable == True:
		# Opens the file and generates a hash
		with open(file_path_full, 'rb') as f:

			while True:
				data = f.read(buffer_size)	
				if not data:
					break
				sha256.update(data)

				hash_output = format(sha256.hexdigest())
		
		# Should this script save the JSON file?
		# Function will be told with either "write" or "no write"
		# depending that the purpose is.
		if save_as_file == 'write':
			dt = datetime.now()
			ts = datetime.timestamp(dt)

			# Attempt to write the hash file. 
			# If this fails report the error
			try:
				
				json_data = {'Program_Name': 'ArchiveGuard', 'Link': 'https://karlhunter.co.uk/ag', 'Hash_Ver': ver_number, 'File_Path': str(file_path_full), 'File_Size': file_size, 'ts': ts, 'Alg': 'sha256', 'Hash': hash_output}
				json_write = json.dumps(json_data)

				# Write hash to file
				file_hash_write = open(full_path_with_hash, "w")
				file_hash_write.write(json_write)
				file_hash_write.close()
				file_hash_write.close()
				
			except:
				# Error writing the hash file.
				# Report to user
				print('Failed Write Hash:', full_path_with_hash)
			
		elif save_as_file == 'no_write':
			# Just output the hash, do not write to file.
			# Checksum comes from the check_hash.py
			if hash_output != checksum:
				# The hash stored in file and new file hash does not match
				print('Failed Hash:', file_path_full)
		f.close()

# Cycle through folder function
def run_dir_scan_func(dir_path):

	# Make sure directory structure ends in /
	# If user does not specify the ending slash, 
	# then need to add on
	dir_path_check = str(dir_path)[-1:]
	
	if dir_path_check != '/':
		# Add the / end of path
		dir_path = dir_path + '/'

	# Check if path is a directory, otherwise
	# do not run. Could be a file
	if os.path.isdir(dir_path):

		# Loop through the directory tree to find files
		for file_path_full in Path( dir_path ).rglob( '*' ):

			check_if_hash = str(file_path_full)[-hash_ext_size:]

			# Skip if extension exists; this is done to ignore the hash files 
			if check_if_hash != hash_ext:
				
				# This file is not a hash file.
				# Time to check if this file has its own hash file

				full_path_hash_check = str(file_path_full) + hash_ext 

				if os.path.exists(full_path_hash_check): 

					# The hash file exists
					# Moving on to check file hash
					check_hash_func(str(file_path_full))

				else:

					# This file does not have an accociated hash file
					# Create new file
					# Check if actually a file (not a directory)
					if os.path.isfile(file_path_full) == True:
						# Opens the hash writer module
						write_hash_func(file_path_full, 'write', 'none')
						
			else:
				# Although the hash file exists check if orgional time
				# is still present
				remove_hash_extension = str(file_path_full)[:-hash_ext_size]
				if os.path.isfile(remove_hash_extension) == False:
					print(f'File Missing: {remove_hash_extension}')

	else:
		# Not a directory
		print('Not a directory')

# Check Hash function
def check_hash_func(file_path_full):
	
	# Adds extension to find hash file
	full_path_with_hash = str(file_path_full) + hash_ext
	# Resets variable
	checksum = 0
	
	# Tries to read the JSON. If fails reports to user
	# and continues the script
	try:
		# Open the hash file in the JSON format
		json_file = open(full_path_with_hash)
		json_data = json.load(json_file)
		# Get the hash data from the hash file
		checksum = json_data['Hash']
	except: 
		print('Damaged Hash:', full_path_with_hash)
		
	# Closing file
	json_file.close()

	# Hash the file
	write_hash_func(file_path_full, 'no_write', checksum)



# Welcome area. Checks for arguements

# Remove 1st argument from the
# list of command line arguments
argumentList = sys.argv[1:]
 
# Options: need to create variable with blank
# value for later use in the script
options = "d:s:"

try:
	# Parsing argument
	arguments, values = getopt.getopt(argumentList, options)
	 
	# Checking each argument
	for currentArgument, currentValue in arguments:       

		if currentArgument in ("-d"):
			dir_path = currentValue
		if currentArgument in ("-s"):
			confirm_schedule = currentValue

except getopt.error as err:
	# output error, and return with an error code
	print (str(err))


# Do checks on directory
# Has the user given a path?
if dir_path != '':

	# Fist check if on schedule
	# If "-s yes" supplied then run script
	# without prompting user
	if confirm_schedule == 'yes':
		run_dir_scan_func(dir_path)
		print('Scan completed')
	else:

		# No schedule defined
		# So will ask user to confirm happy to run on input dir
		answer = input(f"Run on directory? {dir_path} (y or n): ")

		# Check user answer
		if answer == "y":
			# Run the scan function
			run_dir_scan_func(dir_path)
			print('Scan completed')
		
		elif answer == "n":
			# User selected no, so will stop the script
			print('Aborted')
			
		else:
			
			print(f"Your answer can only be y or n. You answered {answer}")

# Tell users that they have not given a directory to scan
# Then suggest how to do this
else:
	print('Please choose a directory option. -d /path/to/files/')
