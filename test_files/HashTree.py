import hashlib
import os


def hash_file(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
        return hashlib.sha1(data).hexdigest()


def build_merkle_tree(hashes):

    # Keep looping until one hash remains
    while len(hashes) > 1:
        new_level = []

        # Process pairs of hashes
        for i in range(0, len(hashes), 2):

            left = hashes[i]

            # Check if there is a right node
            if i + 1 < len(hashes):
                right = hashes[i + 1]
            else:
                # If odd number, duplicate last hash
                right = left

            # Combine and hash
            combined_string = left + right
            combined_hash = hashlib.sha1(combined_string.encode()).hexdigest()

            new_level.append(combined_hash)

        # Move up one level
        hashes = new_level

    return hashes[0]


def get_files_from_folder(folder_path):
    files = []

    # Loop through everything in the folder
    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)

        # Only include files (skip subfolders)
        if os.path.isfile(full_path):
            files.append(full_path)

    return files


# ===== MAIN PROGRAM =====

folder_path = "test_files"   # <-- change this if needed

files = get_files_from_folder(folder_path)

if len(files) == 0:
    print("No files found in folder.")
else:
    print("Files being processed:")
    for f in files:
        print(f)

    leaf_hashes = []

    # Hash each file
    for f in files:
        file_hash = hash_file(f)
        leaf_hashes.append(file_hash)

    # Build Merkle Tree
    top_hash = build_merkle_tree(leaf_hashes)

    print("\nTop Hash:", top_hash)
