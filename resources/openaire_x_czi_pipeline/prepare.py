import zipfile
import sys
import tarfile

# Replace 'your_file.zip' with the actual path to your zip file
zip_file_path = sys.argv[1]

# Replace 'output_folder' with the desired output folder
output_folder = 'input/czi_mentions_data'

# Open the zip file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
	# Extract all the contents into the specified folder
	zip_ref.extractall(output_folder)

print(f"File '{zip_file_path}' successfully extracted to '{output_folder}'.")

for tar_file_path in ["raw.tar.gz", "linked.tar.gz"]:
	# Replace 'your_file.tar' with the actual path to your tar file
	tar_file_path = f"{output_folder}/{tar_file_path}"

	# Replace 'output_folder' with the desired output folder
	#out_folder_name = tar_file_path.split(".")[0]
	#tar_output_folder = f"{output_folder}/{out_folder_name}"

	# Open the tar file
	with tarfile.open(tar_file_path, 'r') as tar_ref:
    		# Extract all the contents into the specified folder
		tar_ref.extractall(output_folder)
		print(f"File '{tar_file_path}' successfully extracted to '{output_folder}'.")
