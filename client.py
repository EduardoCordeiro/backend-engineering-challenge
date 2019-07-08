import argparse

import MovingAverage
import Testing
import utility

def parse_arguments():
    """
    Argument parser.

    -f, --file 'path/to/input/file': path to the input file (default 'inputs/example.json')
    -w, --window 'int': window size to analyse (default 10)
    -p, --print: enable console output
    -o, --output_file 'path/to/output/file': path to the output file, where to save the results (default is outputs/input_name.json)
    -t, --test: run tests

    :return: Namespace object with the arguments received
    """

    # handle arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--input_file', help = 'Path to the input file', default = 'inputs/example.json')
    parser.add_argument('-w', '--window', type = int, help = 'Window size to analyse', default = 10)
    parser.add_argument('-p', '--print', default = False, action = 'store_true',
                        help = 'enables console output logging (default is file only)')
    parser.add_argument('-o', '--output_file',
                        help = 'output file to save the results to, default saved to outputs/input_name.json')
    parser.add_argument('-t', '--test', default = False, action = 'store_true', help = 'run tests')

    args =  parser.parse_args()

    # check for argument correctness
    if args.window <= 0:
        raise Exception(f'Window size needs to be an Integer higher than zero ({args.window})')

    if type(args.window) is not int:
        raise Exception(f'Window size needs to be an Integer ({type(args.window)})')

    return args


def main():
    arguments = parse_arguments()

    if arguments.test:
        Testing.Testing().run_tests()
    else:

        # process input file and store the events read
        events = utility.process_input_data(arguments.input_file)

        # create moving average class with event and window size
        moving_average = MovingAverage.MovingAverage(events, arguments.window)

        # perform moving average time calculation
        average_times = moving_average.moving_average()

        # for output in average_times:
        utility.log_average_time(arguments.input_file, arguments.print, average_times, arguments.output_file)


if __name__ == "__main__":
    main()