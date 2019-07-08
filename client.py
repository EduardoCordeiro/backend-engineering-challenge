from datetime import datetime
import argparse
import json
import time

import MovingAverage

def process_input_data(f):
    """
    Reads the input file and creates a list of events

    :param f: input file to be read
    :return: list of events (dictionary)
    """

    input_file = open(f, 'r')

    # storing this in a list for now, check if it makes sense to use dics/sets/tree(no)
    input_events = []

    for event in input_file:
        event_data = json.loads(event)

        # convert string to datetime object for easier manipulation
        try:
            event_data['timestamp'] = datetime.strptime(event_data['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            raise ValueError('Incorrect date time format, should be YYYY-MM-DD HH:MM:SS.mmmmmmm')

        input_events.append(event_data)

    input_file.close()

    return input_events


def log_average_time(input_file, console_log, average_times):
    """
    Log the average time to the output file
    There is an optional argument that can be given to log to the console as well

    :param input_file:
    :param console_log:
    :param average_times:
    :return: None
    """

    output_file_name = input_file.split('/')[-1]

    output_file = open(f'outputs/{output_file_name}', 'a+')

    for at in average_times:

        # create dictionary for the output structure
        moving_average_obj = {
            "date": str(at[0]),
            "average_delivery_time": round(float(at[1]), 1)
        }

        json_obj = json.dumps(moving_average_obj)

        output_file.write(json_obj + '\n')

        # print to console if the argument has been specified
        if console_log:
            print(json_obj)

    output_file.close()


def parse_arguments():
    """
    Argument parser

    :return: Namespace object with the arguments received
    """

    # handle arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--input_file', required = True, help = 'Path to the input file')
    parser.add_argument('-w', '--window', required = True, type = int, help = 'Window size to analyse')
    parser.add_argument('-p', '--print', default = False, action = 'store_true', help = 'enables console output logging (default is file only)')
    parser.add_argument('-o', '--output_file', help = 'define an output file to save the results to, default is saved to outputs/input_name.json')

    args =  parser.parse_args()

    # check for argument correctness
    if args.window <= 0:
        raise Exception(f'Window size needs to be an Integer higher than zero ({args.window})')

    if type(args.window) is not int:
        raise Exception(f'Window size needs to be an Integer ({type(args.window)})')

    return args


def main():
    arguments = parse_arguments()

    # process input file and store the events read
    events = process_input_data(arguments.input_file)

    # create moving average class with event and window size
    moving_average = MovingAverage.MovingAverage(events, arguments.window)

    start = time.time()

    # perform moving average time calculation
    average_times = moving_average.moving_average()

    end = time.time()

    print(end - start)

    # for output in average_times:
    log_average_time(arguments.input_file, arguments.print, average_times)


if __name__ == "__main__":
    main()