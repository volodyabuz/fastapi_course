import time

# CPU task
def process_data():
    x = 2**50
    time.sleep(1)


def generate_report():
    time.sleep(2)


def main():
    start_time = time.perf_counter()
    process_data()
    generate_report()
    end_time = time.perf_counter()
    print("Времени прошло: ", end_time - start_time)


if __name__ == '__main__':
    main()
