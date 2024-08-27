import pandas
import pathlib
import seaborn
import matplotlib.pyplot as plt

seaborn.set_style(style='ticks')

all_files = pathlib.Path(r'W:\MLD_Projection\LakeEnsemble\Flake_output').glob('*.txt')
rslt = []
# Flake did not simulate the 2100-12-30
meta_lake = pandas.read_csv(r'data/location.csv')
south_lakes = meta_lake[meta_lake['Latitude']<0]
south_lakes = south_lakes['Name'].to_list()
for txt_file in all_files:
    # txt_file = pathlib.Path('output/Jane_10_GFDL-ESM4_ssp126.txt')
    infos = txt_file.stem.split('_')
    year = int(infos[-1])
    lake_name = '_'.join(infos[:2])
    dt_arr = pandas.date_range(start=f'{year}-01-01', end=f'{year}-12-30')
    f = open(txt_file, 'r')
    lines = f.readlines()[2:]
    h_ml = []
    for line in lines:
        data = line.strip().split()
        h_ml.append(float(data[14]))
        # h_ml.append(float(data[2]))
    out_data = []
    for i, dt in enumerate(dt_arr):
        out_data.append({'date':dt, 'MLD':h_ml[i]})
    out_data = pandas.DataFrame(out_data)
    # filter summer data
    months = [12, 1, 2] if lake_name in south_lakes else [6, 7,8]
    out_data = out_data.loc[out_data['date'].dt.month.isin(months)]
    # annual summer mean
    out_data['year'] = year
    # out_data.groupby('year').mean().to_csv('test.csv')
    # appending info
    out_data['name'] = lake_name
    out_data['model'] = infos[2]
    out_data['ssp']  = infos[3].upper()
    out_data = out_data[['name', 'year', 'MLD', 'model', 'ssp']]
    rslt.append(out_data)
rslt = pandas.concat(rslt, axis=0)
rslt.to_csv('data/Flake_simulation_hML_2021_2100_varyingSDD.csv', index=False)
#
# rslt = pandas.read_csv('Flake_simulation_Tw_2021_2100.csv')
fig, axes = plt.subplots(2, 3, figsize=(9, 6))
#
colormaps = ['xkcd:sky blue', 'xkcd:tangerine', 'xkcd:reddish']
#
df_all = rslt
climate_models = df_all['model'].unique()
#
for i, climate_model in enumerate(climate_models):
    r, c = int(i/3), int(i%3)
    ax = axes[r, c]
    legend = True if r+c == 0 else False
    data = df_all[df_all['model']==climate_model].copy()
    data = data[data['MLD'].between(0, 1000)]
    # data = data[data['value']>0]
    g = seaborn.lineplot(data=data, x='year', y='MLD', hue='ssp', palette=colormaps,
                    legend=legend, linewidth=2.0, alpha=0.8, err_kws={'alpha':0.1},
                    ax=ax)
    ax.set_xlabel('Year')
    ax.set_ylabel('$Z_e$ (m)')
    ax.set_title(climate_model)
    if legend:
        seaborn.move_legend(g, title=None, loc='upper right', frameon=False)
ax = axes[1, 2]
g = seaborn.lineplot(data=df_all, x='year', y='MLD', hue='ssp', palette=colormaps,
                legend=False, linewidth=2.0, alpha=0.8, err_kws={'alpha':0.1},
                ax=ax)
ax.set_xlabel('Year')
ax.set_ylabel('$Z_e$ (m)')
ax.set_title('ALL')
if legend:
    seaborn.move_legend(g, title=None, loc='upper right', frameon=False)
plt.tight_layout()
plt.savefig('figures/FigureS-FLAKE_SSP_prediction.png', dpi=600)
plt.show()
