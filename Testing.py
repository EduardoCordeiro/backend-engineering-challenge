import json
import utility

import MovingAverage

class Testing:
    """
    Testing class

    We use the same approach for reading the input files and then obtaining the moving averages with the Moving Average
    class.
    We then compare these values against the ground truth, on the tests/output folder.
    """

    @staticmethod
    def run_test(f, w):
        """
        Runs the test passed as argument, and compares with the ground truth

        :param f: file to read
        :param w: window size
        """

        # process input file and store the events read
        events = utility.process_input_data(f'tests/input/{f}')

        # create moving average class with event and window size
        moving_average = MovingAverage.MovingAverage(events, w)

        # perform moving average time calculation
        average_times = moving_average.moving_average()

        with open(f"tests/output/{f}") as out_file:
            for i, line in enumerate(out_file):
                data = json.loads(line)
                read_average = data['average_delivery_time']

                assert(round(float(average_times[i][1]), 1) == read_average)

    def run_tests(self):
        """
        Function to call from the client, runs all tests

        """

        print("Running Test 1 - tests/input/test_1.json")
        self.run_test('test_1.json', 50)

        print("Running Test 2 - tests/input/test_1.json")
        self.run_test('test_2.json', 20)

        print("Running Test 3 - tests/input/test_1.json")
        self.run_test('test_3.json', 30)

        print("Running Test 4 - tests/input/test_1.json")
        self.run_test('test_4.json', 5)

        print("All tests passed")