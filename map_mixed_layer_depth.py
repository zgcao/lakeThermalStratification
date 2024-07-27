import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.basemap import Basemap
import proplot as pplt

plt.rcParams['font.family'] = 'Arial'
# plt.rcParams['font.size'] = 11

vmin = -3
vmax = 3
interval = 1
cmap1 = pplt.Colormap('Curl_r', N=(vmax-vmin)/interval*4)
#
df = pd.read_excel('data/stat/trend/eplimnion_trend_v2.xlsx')
df = df.dropna(subset=[f'MLD_Sen'])
lat = df['lat'].values
lon = df['long'].values
data = df['MLD_Sen'].values * 10
#
m = Basemap(projection='robin', lon_0=0)
m.drawcoastlines(linewidth=0.2, color='black')
m.drawlsmask(land_color='0.6')
m.drawparallels(np.arange(-90, 90, 30), labels=[0, 0, 0, 0], linewidth=0.1, **{'rotation': 'vertical'})
m.drawmeridians(np.arange(-180, 180, 30), labels=[0, 0, 0, 0], linewidth=0.1)
m = m.scatter(lon, lat, latlon=True, c=data, s=12, cmap=cmap1)
cb = plt.colorbar(label='Z$_e$ trend (m decade$^{-1}$)', orientation='horizontal',
            ticks=np.arange(vmin, vmax+interval, interval), 
            shrink=0.6, aspect=20)
cb.ax.xaxis.set_ticks([], minor=True)
plt.clim(vmin, vmax)
plt.tight_layout()
plt.savefig(f'figures/Figure1-EP_trend-2.png', dpi=1200)
plt.show()
