# Backend Engineering Challenge


Welcome to our Engineering Challenge repository 🖖

If you found this repository it probably means that you are participating in our recruitment process. Thank you for your time and energy. If that's not the case please take a look at our [openings](https://unbabel.com/careers/) and apply!

Please fork this repo before you start working on the challenge, read it careful and take your time and think about the solution. Also, please fork this repository because we will evaluate the code on the fork.

This is an opportunity for us both to work together and get to know each other in a more technical way. If have some doubt please open and issue and we'll reach out to help.

Good luck!

## Challenge Scenario

At Unbabel we deal with a lot of translation data. One of the metrics we use for our clients' SLAs is the delivery time of a translation. 

In the context of this problem, and to keep things simple, our translation flow is going to be modeled as only one event.

### *translation_delivered*

Example:

```json
{
	"timestamp": "2018-12-26 18:12:19.903159",
	"translation_id": "5aa5b2f39f7254a75aa4",
	"source_language": "en",
	"target_language": "fr",
	"client_name": "easyjet",
	"event_name": "translation_delivered",
	"duration": 20,
	"nr_words": 100
}
```

## Challenge Objective

Your mission is to build a simple command line application that parses a stream of events and produces an aggregated output. In this case, we're interested in calculating, for every minute, a moving average of the translation delivery time for the last X minutes.

If we want to count, for each minute, the moving average delivery time of all translations for the past 10 minutes we would call your application like (feel free to name it anything you like!).

	unbabel_cli --input_file events.json --window_size 10
	
The input file format would be something like:

	{"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "easyjet","event_name": "translation_delivered","nr_words": 30, "duration": 20}
	{"timestamp": "2018-12-26 18:15:19.903159","translation_id": "5aa5b2f39f7254a75aa4","source_language": "en","target_language": "fr","client_name": "easyjet","event_name": "translation_delivered","nr_words": 30, "duration": 31}
	{"timestamp": "2018-12-26 18:23:19.903159","translation_id": "5aa5b2f39f7254a75bb33","source_language": "en","target_language": "fr","client_name": "booking","event_name": "translation_delivered","nr_words": 100, "duration": 54}


The output file would be something in the following format.

```
{"date": "2018-12-26 18:11:00", "average_delivery_time": 0}
{"date": "2018-12-26 18:12:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:13:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:14:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:15:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:16:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:17:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:18:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:19:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:20:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:21:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:22:00", "average_delivery_time": 31}
{"date": "2018-12-26 18:23:00", "average_delivery_time": 31}
{"date": "2018-12-26 18:24:00", "average_delivery_time": 42.5}
```

#### Notes

Before jumping right into implementation we advise you to think about the solution first. We will evaluate, not only if your solution works but also the following aspects:

+ Simple and easy to read code. Remember that [simple is not easy](https://www.infoq.com/presentations/Simple-Made-Easy)
+ Include a README.md that briefly describes how to build and run your code
+ Be consistent in your code. 

Feel free to, in your solution, include some your considerations while doing this challenge. We want you to solve this challenge in the language you feel most confortable with. Our machines run Python, Ruby, Scala, Java, Clojure, Elixir and Nodejs. If you are thinking of using any other programming language please reach out to us first 🙏.

Also if you have any problem please **open an issue**. 

Good luck and may the force be with you

#### Extra points

If you feeling creative feel free to consider any additional cases you might find interesting. Remember this is a bonus, focus on delivering the solution first.

### Solution

The following pseudo-code shows the main algorithm used.
My approach involves a modified version of the bisect_right implementation, that compares
the timestamps of the events.

During the main loop the index of the right-most event, which has a timestamp lower than the current_time is returned.
This means that we have all events in a range from 0 to 'i'. Since we are only interested in events during a certain window,
we remove all events that have already been calculated and are now outside the window.
Afterwards, all that is left is to calculate that average of the current events and saving them in a list for output.
The loop finishes after adding one minute to the current time.

````
MovingAverage()
    average_times = []
    current_time = start_time
    end_time = end_time
    
    while current_time < end_time
    
        i = binarySearch(current_time)
        
        current_events = events[0:i]
        
        removeOldEvents()
        
        average_time = calculateAverage(current_events)
        
        average_times.add(average_time)
        
        current_time += 1 minute
````

####Time Complexity

- n = number of events
- t = number of minutes between end_time and current_time
- c = number of events currently being processed

Outer loop is `O(t)` in all scenarios, as we need to iterate over all the minutes

Binary search during each loop is `O(log n)`, for the worst and average case

Event removal during each loop is `O(c)`, where c is <= n.

Average case: `O(t c)`

Best case: `O(t log n)`

####Benchmarks

Benchmark on the examples generated locally (files were too big to upload to git)
window size = 10

number of events -> time to completion
- 1000 -> 0.02 seconds
- 10000 -> 0.2 seconds
- 100000 -> 3.3 seconds
- 500000 -> 4 minutes 20 seconds
- 1000000 -> 12 minutes

####Tests

I created four tests to demonstrate the correctness of the solution.

The same approach was used for reading the input files and then obtaining the moving 
averages with the Moving Average class.
We then compare these values against the ground truth, on the tests/output folder.

Besides testing for correctness, it was also important to consider the two edge cases
where the starting time could output wrong values. These cases are shown in test 2 and 3,
which test the lower and upper bound for the time interval.

- Test 1
    - 5 events
    - window 50
    
- Test 2
    - 5 events
    - window 20
    - start time 12:59:59.999999

- Test 3
    - 7 events
    - window 30
    - start time 00:00:00.000000

- Test 4
    - 7 events
    - window 5


### Considerations

There are a couple of points that can be considered to speed up the application, depending on requirements.

For instance, we are reading several values from the input file, but only using two fields.
We could save space by only storing those two values.

In the example given the different events are spaced only minutes apart. It would also be important to consider
what happens when the event space is more sparse.

Besides the current input correctness checks that I made, some assumptions had to be made to obtain a correct result.

One of this assumptions was the window size, as it was not given what it could be. 
Does it always refer to minutes? Or on sparser datasets it can refer to hours or even days.

####Client

The client has two python files.

- client.py - main, argument parsing and input/output logic

- MovingAverage.py - implements the algorithm and additional utility functions

Argument options:

    -f, --file 'path/to/input/file': path to the input file (default 'inputs/example.json')
    -w, --window 'int': window size to analyse (default 10)
    -p, --print: enable console output
    -o, --output_file 'path/to/output/file': path to the output file, where to save the results (default is outputs/input_name.json)
    -t, --test: run tests

    example:
    python client.py -f inputs/1000.json -w 25 -p -o outputs/1000_out.json
    
    run tests:
    python client.py -t


####Generator

I created a very simple generator for input files to this challenge, with a command line interface.

    -t, --time 'YYYY-MM-DD HH:MM:SS.ssssss': start time
    -bd, --min_duration 'int': minimum duration (default = 25)
    -td, --max_duration 'int': maximum duration (default = 70)
    -e, --events 'int': number of events to generate (default = 1000)    
    
    example:
    python generator.py -t "2018-12-26 18:11:08.509654" -bd 10 -td 100 -e 4000
    
Developed on Python 3.7, using only standard libraries.
No build required, run example shown below.