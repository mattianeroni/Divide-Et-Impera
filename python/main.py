import utils


if __name__ == "__main__":
    for filename in utils.benchmarks:
        nodes = tuple(i for i in utils.read_file(filename))
