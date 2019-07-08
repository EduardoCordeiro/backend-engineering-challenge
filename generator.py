import argparse
import datetime
import random

def main():
    """
    Simple file generator for the json dictionary required for the challenge.
    Only generating different date/time and duration, all other parameters remain the same

    time is increased between 00:00:01 and 00:59:59
    duration is a range between 25 and 70

    """
    # handle arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--time', help =  'start time', default = "2018-12-26 18:11:08.509654")
    parser.add_argument('-bd', '--min_duration', type = int, help = 'minimum duration', default = 25)
    parser.add_argument('-td', '--max_duration', type = int, help = 'maximum duration', default = 70)
    parser.add_argument('-e', '--events', type = int, help = 'how many events to generate', default = 1000)

    args = parser.parse_args()

    f = open(f"inputs/{args.events}.json", "a+")

    string_time = "2018-12-26 18:11:08.509654"

    current_time = datetime.datetime.strptime(string_time, '%Y-%m-%d %H:%M:%S.%f')

    for i in range(0, args.events):

        duration = random.randint(args.min_duration, args.max_duration)

        json = "{\"timestamp\": \"" \
               + str(current_time) \
               + "\", \"translation_id\": \"5aa5b2f39f7254a75aa5\", " \
                 "\"source_language\": \"en\",\"target_language\":" \
                 " \"fr\",\"client_name\": \"easyjet\",\"event_name\":" \
                 "\"translation_delivered\",\"nr_words\": 30, \"duration\": "\
               + str(duration) + "}\n"

        f.write(json)

        minutes = random.randint(0, 59)
        seconds = random.randint(0, 59)

        current_time += datetime.timedelta(minutes=minutes, seconds=seconds)

    print(f"New file is located at inputs/{args.events}.json")

if __name__ == "__main__":
    main()