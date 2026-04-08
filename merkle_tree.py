import hashlib
import os
import sys


def get_hasher(algorithm="sha1"):
    algorithm = algorithm.lower()
    if algorithm == "sha1":
        return hashlib.sha1()
    elif algorithm == "md5":
        return hashlib.md5()
    else:
        raise ValueError("Only sha1 or md5 are supported.")


def hash_file(filepath, algorithm="sha1", chunk_size=8192):
    hasher = get_hasher(algorithm)
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def hash_string(data, algorithm="sha1"):
    hasher = get_hasher(algorithm)
    hasher.update(data.encode("utf-8"))
    return hasher.hexdigest()


def build_merkle_tree(filepaths, algorithm="sha1"):
    if not filepaths:
        raise ValueError("No input files provided.")

    filepaths = sorted(filepaths)

    print("Input Files:")
    for path in filepaths:
        print(path)

    print("\nLeaf Hashes:")
    leaf_hashes = []
    for path in filepaths:
        file_hash = hash_file(path, algorithm)
        leaf_hashes.append(file_hash)
        print(f"{os.path.basename(path)}: {file_hash}")

    levels = [leaf_hashes]
    current_level = leaf_hashes[:]
    level_number = 1

    while len(current_level) > 1:
        if len(current_level) % 2 == 1:
            current_level.append(current_level[-1])

        next_level = []
        print(f"\nBuilding Level {level_number}:")
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i + 1]
            parent_hash = hash_string(left + right, algorithm)
            next_level.append(parent_hash)
            print(f"Hash({left} + {right}) = {parent_hash}")

        levels.append(next_level)
        current_level = next_level
        level_number += 1

    return levels


def print_tree(levels):
    print("\nMerkle Tree:")
    for i, level in enumerate(levels):
        print(f"Level {i}:")
        for item in level:
            print(f"  {item}")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("python merkle_tree.py <file1> <file2> <file3> ... [--algo sha1|md5]")
        sys.exit(1)

    args = sys.argv[1:]
    algorithm = "sha1"

    if "--algo" in args:
        index = args.index("--algo")
        if index + 1 >= len(args):
            print("Error: missing value after --algo")
            sys.exit(1)
        algorithm = args[index + 1]
        del args[index:index + 2]

    filepaths = args

    for path in filepaths:
        if not os.path.isfile(path):
            print(f"Error: file not found -> {path}")
            sys.exit(1)

    levels = build_merkle_tree(filepaths, algorithm)
    print_tree(levels)

    top_hash = levels[-1][0]
    print(f"\nTop Hash ({algorithm.upper()}): {top_hash}")


if __name__ == "__main__":
    main()
