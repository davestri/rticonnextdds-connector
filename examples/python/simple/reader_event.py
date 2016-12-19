##############################################################################
# Copyright (c) 2005-2016 Real-Time Innovations, Inc. All rights reserved.
# Permission to modify and use for internal purposes granted.
# This software is provided "as is", without warranty, express or implied.
##############################################################################

import sys
import os
filepath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(filepath + "/../../../");
import time
import concurrent.futures
import rticonnextdds_connector as rti


connector = rti.Connector(
    "MyParticipantLibrary::Zero",
    filepath + "/../ShapeExample.xml");
input = connector.getInput("MySubscriber::MySquareReader");

def on_data_available(input):
    print('on_data_available taking data ...')
    input.take();
    numOfSamples = input.samples.getLength();
    print('on_data_available ' + repr(numOfSamples) + ' samples taken')
    for j in range (1, numOfSamples+1):
        if input.infos.isValid(j):
            sample = input.samples.getDictionary(j); #this gives you a dictionary
            x = sample['x']; #you can access the dictionary...
            y = sample['y'];
            size = input.samples.getNumber(j, "shapesize"); #or, if you need a single field, you can just access the field directly
            color = input.samples.getString(j, "color");
            print("Received:", repr(sample));

def application_main():
    for i in range(1, 300, 1):
        if True:
            print("application sleeping ...")
            time.sleep(1)
        else:
            #to demonstrate its not necessary to yield for the callback thread to run
            print("application working ...")
            for j in range(1, 25, 1):
                for k in range(1, 1000000, 1):
                    x = 1 + 1
    #stop the callback thread cleanly
    connector.removeListener(on_data_available);
    return True

connector.addListener(on_data_available, input);
try:
    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as my_executor:
        futures.append(
            my_executor.submit(connector.onDataAvailable, 2000));
            #wait timeout, in milliseconds, for infinite wait use default ...
            #my_executor.submit(connector.onDataAvailable));
        futures.append(
            my_executor.submit(application_main))
        print('futures created')
        #check for futures completed or exceptions
        for f in concurrent.futures.as_completed(futures, timeout=None):
            if f.exception():
                print("Future raised exception:")
        #the 'with' syntax implicitly calls executor.shutdown(wait=True)
finally:
    print('all futures completed exiting ... ')
