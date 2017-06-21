# datalab_alg_prophet_test
Test of the prophet library by rectracing known measurements

This project tests the fbprophet library by retracing a given dataset. It takes the following parameters

* data, the data already prepared for fbprophet
* wait, the periods we wait before w start using the predictions (training time)
* lookback, the periods we use for (re)training, -1 means all available periods
* lookahead, the periods we will look ahead

For example; say we have 1000 data points all collected on consecutive days. We want to test the effectiveness of 
fbprophet for this dataset. The retrace function will do just that. We use wait=100, lookback=-1, lookahead=5.

The algorithms will do the following

* initialize an empty result 
* set t = 100 (wait)
* first step; add all (measured) points up until t = wait (we do not predict anything until t=wait)
* make a prediction model based on all measurements until t=100
* predict 5 days ahead
* add the predictions to the result
* t increases with 5 (the amount of lookahead periods)
* make a prediction model based on all measurements until current t (105)
* add the predictions to the result
* .... (repeat until we have handled the entire data)

The script will plot a graph showing the measured and predicted (including upper and lower boundaries) values which can be used to see if fbprophet works ok and to finetune the parameters.

![alt text](http://url/to/img.png)
