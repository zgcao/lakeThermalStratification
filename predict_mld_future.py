import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.ensemble import RandomForestRegressor

# link depth and fetch to the model
df = pd.read_csv('data/stat/04_annualSummerMean.csv')
obj = 'Ze'
cols = ['year', 'AT', 'WS', 'TP', 'SR', 'LR', 'SP', obj]
df1 = df[cols]
df1 = df1[df1['Ze']>0]
df1 = df1.dropna()
print(df1.shape)
#
x = df1[cols[:-1]].values
y = df1[obj].values
# scaler the data
x_scaler = StandardScaler()
y_scaler = MinMaxScaler()
x_t1 = x_scaler.fit_transform(x)
y_t1 = y_scaler.fit_transform(np.log(y.reshape(-1, 1)))
# fit a RF model
rf_model = RandomForestRegressor(n_jobs=-1)
rf_model.fit(x_t1, y_t1.ravel())
# predict for different SSP sceniors
pred_mld = []
i = 0
models = ['gfdl-esm4', 'ipsl-cm6a-lr', 'mpi-esm1-2-hr', 'mri-esm2-0', 'ukesm1-0-ll']
variables = ['year', 'tas', 'sfcwind', 'pr', 'rsds', 'rlds', 'huss']
for model in models:
    for ssp in ['ssp126', 'ssp370', 'ssp585']:
        df = pd.read_csv(f'data/future_simulation/future_series_{model}_{ssp}.csv').dropna()
        data = df[variables].values
        # scaler
        data_scl = x_scaler.transform(data)
        # predict
        y_pred = rf_model.predict(data_scl).reshape(-1, 1)
        mld_hat = np.exp(y_scaler.inverse_transform(y_pred))
        output_data = df[['Name', 'year']].copy()
        output_data['MLD'] = mld_hat
        output_data['SSP'] = ssp[:3].upper() + ' ' + ssp[3:]
        output_data['model'] = model
        if i == 0:
            pred_mld = output_data
        else:
            pred_mld = pd.concat((pred_mld, output_data), axis=0)
        i = i + 1
pred_mld.to_csv(f'data/future_simulation/MLD_Projection_climate_concat.csv')
