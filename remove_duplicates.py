import sys
import os
import hashlib
import datetime
import shutil

NUMBER_OF_BYTES = 64

def main():
	root_path = sys.argv[1]
	file_paths = []
	dir_paths = []
	for root, dirs, files in os.walk(root_path):
		for file in files:
			file_path = os.path.join(root, file)
			file_paths.append(file_path)
		for dirr in dirs:
			dir_path = os.path.join(root, dirr)
			dir_paths.append(dir_path)
	
	file_hashes_to_paths = {}
	for file_path in file_paths:
		with open(file_path, "rb") as file:
			data = file.read(NUMBER_OF_BYTES)
			h = hashlib.md5()
			h.update(data)
			file_hash = h.hexdigest()
			if file_hash in file_hashes_to_paths:
				file_hashes_to_paths[file_hash].append(file_path)
			else:
				file_hashes_to_paths[file_hash] = []
				file_hashes_to_paths[file_hash].append(file_path)

	out_filename = str(datetime.datetime.now()).replace(":", "-") + ".txt"
	with open(out_filename, "w", encoding="utf-8") as out_file:
		k = 1
		for file_paths in file_hashes_to_paths.values():
			if (len(file_paths) > 1):
				file_hashes = []
				for file_index in range(0, len(file_paths)):
					file_path = file_paths[file_index]
					with open(file_path, "rb") as file:
						data = file.read()
						h = hashlib.sha256()
						h.update(data)
						file_hash = h.hexdigest()
						file_hashes.append(file_hash)

				file_labels = [False] * len(file_hashes)
				for i in range(0, len(file_hashes) - 1):
					file_labels[i] = True
					duplicate_paths = []
					for j in range(i + 1, len(file_hashes)):
						if file_hashes[i] == file_hashes[j] and not(file_labels[j]):
							file_labels[j] = True
							duplicate_paths.append(file_paths[j])
					
					if len(duplicate_paths) > 0:
						out_file.write(str(k) + "] Removing following duplicates of the file " + file_paths[i] + ": ")
						for file_path in duplicate_paths:
							try:
								out_file.write(file_path + " ")
								os.remove(file_path)
							except Exception as e:
								print(str(e))
								out_file.write(str(e) + " ")

						out_file.write("\n")
						k += 1
	
	dir_paths.sort(reverse=True)
	k = 1
	with open(out_filename, "a") as file:
		file.write("\n")
		for dir_path in dir_paths:
			if check_dir(dir_path):
				try:
					file.write(str(k) + "] Removing directory " + dir_path + "\n")
					shutil.rmtree(dir_path)
					k += 1
				except Exception as e:
					print(str(e))
					file.write(str(e) + " ")

def check_dir(path):
	dirs = os.listdir(path)
	for dirr in dirs:
		dir_path = os.path.join(path, dirr)
		if os.path.isfile(dir_path):
			return False
		else:
			return check_dir(dir_path)
	return True

if __name__ == "__main__":
	main()
	