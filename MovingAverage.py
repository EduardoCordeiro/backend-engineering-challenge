from datetime import timedelta

class MovingAverage:
    """
    Implements the moving average algorithm

    Has only two attributes
    - events: array of events
    - window_size: size of the window to analyse
    """

    def __init__(self, events, window_size):
        self.events = events
        self.window_size = window_size

    @staticmethod
    def calculate_average(current_events):
        """
        Calculates the average delivery time for the events being processed

        :return: average of the duration times for the events
        """

        average = 0

        # division by zero case, might work around it on the main function
        if len(current_events) > 0:
            for event in current_events:
                average += int(event['duration'])

            average /= len(current_events)

        return average

    def moving_average(self):
        """
        Moving average algorithm

        We start by obtaining the start and end times, from the first and last event, respectively.
        Then, the main loop iterates until the last minute.
        A binary search is performed to determine which index of the array contains the events are in the current window
        of calculation.
        We then remove the events that have been processed and are not outside the window
        The next steps are calculating the moving average for the current events, followed by adding that the output
        tuple to the list and increasing the current time by one minute

        :return: a list of tuple (time, average) for each minute of the cycle
        """

        # list of tuple (time, average) for each minute of the cycle
        average_times = []

        # first event defines the starting time, rounded down to the minutes
        # which is also the variable used to hold the current time (Explain
        current_time = self.events[0]['timestamp'].replace(microsecond = 0, second = 0)

        # end event defines the ending time, rounded up to the next minute
        end_time = self.events[-1]['timestamp'].replace(microsecond = 0, second = 0) + timedelta(minutes = 1)

        while current_time <= end_time:

            i = self.binary_search(current_time)

            current_events = self.events[0:i]

            # remove events that have been calculated and are now below the window size
            for c in current_events:
                if c['timestamp'] < current_time - timedelta(minutes = self.window_size):
                    current_events.remove(c)
                    self.events.remove(c)

            average = self.calculate_average(current_events)

            average_times.append((current_time, average))

            current_time += timedelta(minutes = 1) # increase minutes by one

        return average_times

    def binary_search(self, t):
        """
        Simple binary search algorithm
        Makes use of a modified bisect_right, as we are interested in finding the element
        closest to the current timestamp and not the actual values of the elements

        :param t: current timestamp
        :return: index of the last element where the timestamp < t
        """

        low = 0
        high = len(self.events)

        while low < high:

            mid = (low + high) // 2

            if t == self.events[mid]['timestamp']:
                return mid + 1 # check for correctness, edge case when the event starts on the exact minute
            elif t < self.events[mid]['timestamp']:
                high = mid
            else:
                low = mid + 1

        return low