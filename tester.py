import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import seaborn as sns
import time
from fbprophet import Prophet

def retrace(data, i_wait, i_lookback, i_lookahead):
    start = time.clock()
    result = data[:i_wait]

    result['yhat_upper'] = np.NAN
    result['yhat_lower'] = np.NAN

    result.columns = ['ds', 'yhat', 'yhat_upper', 'yhat_lower']
    for i in range(i_wait, len(data) - i_lookahead, i_lookahead):
        i1 = i-i_lookback
        if i_lookback == -1:
            i1 = 0
        print "predicting for [%d:%d>]" % (i1, i)
        prediction = predict(data[i1:i], i_lookahead)
        #result = pd.concat([result, prediction[['ds','yhat']]])
        result = result.append(prediction[['ds', 'yhat', 'yhat_upper', 'yhat_lower']], ignore_index=True)

    seconds = time.clock() - start

    fig, ax = plt.subplots()
    ax.plot_date(data['ds'], data['y'], '-b')
    ax.plot_date(result['ds'], result['yhat'], '--g')
    ax.plot_date(result['ds'], result['yhat_upper'], ':r')
    ax.plot_date(result['ds'], result['yhat_lower'], ':r')
    ax.set_title('retrace wait=%d, back=%d, ahead=%d, exetime=%.2fs' % (i_wait, i_lookback, i_lookahead, seconds))
    ax.set_xlabel('date')
    ax.set_ylabel('value')
    plt.show()

def predict(data, i_lookahead):
    model = Prophet(interval_width=.95)
    model.fit(data)
    future = model.make_future_dataframe(periods=i_lookahead, freq='D')
    forecast = model.predict(future)
    return forecast[-i_lookahead:]

if __name__=="__main__":
    dateparser = lambda x: pd.datetime.strptime(x, '%H:%M:%S %d-%m-%Y')
    data = pd.read_csv('~/programmeren/python/datalab/datalab_alg_prophet_test/data/rd_crest_hh.csv', sep=';', parse_dates=[0], date_parser=dateparser)

    #voor deze test beperken we de data even tot 2013
    df = pd.DataFrame({'ds': data['datetime'], 'y':data['RD_TC_1(Y1)']}, columns=['ds', 'y'])
    df = df[473:812]
    retrace(df, i_wait=100, i_lookback=-1, i_lookahead=5)
