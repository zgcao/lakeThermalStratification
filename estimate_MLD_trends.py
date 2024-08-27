import pandas as pd
from pathlib import Path
from scipy import stats
import numpy as np


def mk_estimate_trend(year, data, key):
    # stat the trend using M-K and linear regression
    from numpy import argsort, nan
    # sort following year
    year = year[data>0]
    data = data[data>0]
    # print(data)
    # lsq regression cofficients
    l_slope, intercept_, l_rValue, l_pValue, std_err = stats.linregress(year, data)
    # Theil-Sen estimator Slope,  (Kendall)
    result = stats.mstats.theilslopes(data, year, alpha=0.95, method='separate')
    sen_slope = result.slope
    # Siegel estimator Slope, https://extremelearning.com.au/the-siegel-and-theil-sen-non-parametric-estimators-for-linear-regression/
    # result = stats.mstats.siegelslopes(data, year)
    # sigel_slope = result.slope
    stat = {f'{key}_Sen':np.round(sen_slope,4), f'{key}_Slope':np.round(l_slope,4), f'{key}_P':np.round(l_pValue,4)}
    return stat

"""Main"""
df = pd.read_excel('data/stat/02_Anual_mean_thermocline_params_check.xlsx')
# grouby using lake_name
trend_list1 = []
df_g = df.groupby('id')
for lake_name, data in df_g:
    trend1 = mk_estimate_trend(data['year'].values, data['epilimnion'].values, 'MLD')
    trend2 = mk_estimate_trend(data['year'].values, data['MT'].values, 'MT')
    # merge dict
    meta_data = df[df['id']==lake_name].iloc[0]
    trend = {**trend1, **trend2}
    trend['lake_id'] = meta_data.get('lake_id')
    trend['name'] = meta_data.get('name')
    trend['country'] = meta_data.get('country')
    trend['lat'] = meta_data.get('lat')
    trend['long'] = meta_data.get('long')
    trend['max_depth'] = meta_data.get('max_depth')
    trend['continent'] = meta_data.get('continent')
    trend['Source'] = meta_data.get('Source')
    trend_list1.append(trend)
pd.DataFrame(trend_list1).to_excel('data/stat/trend/eplimnion_trend_v2.xlsx')
