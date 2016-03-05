import argparse



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python implementation of SHA-512 hashing")
    parser.add_argument('input_file', type=argparse.FileType('r'))
    args = parser.parse_args()