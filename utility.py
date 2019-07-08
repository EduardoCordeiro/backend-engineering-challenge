from datetime import datetime
import json

def process_input_data(f):
    """
    Reads the input file and creates a list of events

    :param f: input file to be read
    :return: array of events (dictionary)
    """

    input_file = open(f, 'r')

    input_events = []

    for event in input_file:
        event_data = json.loads(event)

        # convert string to datetime object for easier manipulation
        try:
            event_data['timestamp'] = datetime.strptime(event_data['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            raise ValueError('Incorrect date time format, should be YYYY-MM-DD HH:MM:SS.mmmmmmm')

        if event_data['duration'] < 0:
            raise Exception(f"Duration is lower than zero ({event_data['duration']})")

        input_events.append(event_data)

    input_file.close()

    return input_events


def log_average_time(input_file, console_log, average_times, output_filename = None):
    """
    Log the average time to the output file
    There is an optional argument that can be given to log to the console as well

    :param input_file: input file name
    :param console_log: console logging toggle
    :param average_times: a list of tuple (time, average)
    :param output_filename: name of the output file
    """

    if output_filename is None:
        output_filename = f"outputs/{input_file.split('/')[-1]}"

    output_file = open(f'{output_filename}', 'a+')

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