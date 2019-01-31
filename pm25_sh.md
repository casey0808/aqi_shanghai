

```python
# import libs and datasets
import numpy as np
import pandas as pd
import datetime

from bokeh.io import show, output_notebook
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, RangeTool, HoverTool
from bokeh.plotting import figure, output_file, show

pm25 = pd.read_csv('datasets/Shanghai_2017_HourlyPM25_created20170803.csv', encoding = 'gbk', parse_dates = ['Date (LST)'])
```


```python
# drop unnecessary columns and handle invalid values
pm25 = pm25.drop(['Site', 'Parameter', 'Unit', 'Duration', 'QC Name'], axis = 1)
pm25.loc[pm25['Value'] < 0] = np.nan
```


```python
pm25 = pm25.rename(columns = {'Date (LST)': 'Date'})
pm25.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 4344 entries, 0 to 4343
    Data columns (total 6 columns):
    Date     4266 non-null datetime64[ns]
    Year     4266 non-null float64
    Month    4266 non-null float64
    Day      4266 non-null float64
    Hour     4266 non-null float64
    Value    4266 non-null float64
    dtypes: datetime64[ns](1), float64(5)
    memory usage: 203.7 KB
    


```python
# create source
hours = np.array(pm25['Date'], dtype = np.datetime64)
source = ColumnDataSource(data = dict(hours = hours, value = pm25['Value'],
                                      year = pm25['Year'], month = pm25['Month'],
                                      day = pm25['Day'], time = pm25['Hour']))
```


```python
# display bokeh plot in the notebook output
output_notebook()
```



    <div class="bk-root">
        <a href="https://bokeh.pydata.org" target="_blank" class="bk-logo bk-logo-small bk-logo-notebook"></a>
        <span id="1002">Loading BokehJS ...</span>
    </div>





```python
# create the main plot
Tools = 'save, reset, box_zoom, hover, wheel_zoom'
p = figure(title = 'Hourly PM2.5 of Shanghai', plot_height = 400, plot_width = 800, tools = Tools, toolbar_location = 'right',
          x_axis_type = 'datetime', x_axis_location = 'above',
          background_fill_color = '#efefef', x_range = (hours[0], hours[500]),
          y_range = (0, np.max(pm25['Value']) + 20))

p.line('hours', 'value', source = source)
p.yaxis.axis_label = 'PM2.5 μg/m3'
```


```python
# create the select plot below
select = figure(title = 'Drag the selection box to change the range above', 
               plot_height = 130, plot_width = 800, y_range = p.y_range,
               x_axis_type = 'datetime', y_axis_type = 'linear',
               tools = '', toolbar_location = None, background_fill_color = '#efefef')

# set hovertool 
p.select_one(HoverTool).tooltips = [
    ('Date', '@year/@month/@day'),
    ('Time', '@time'),
    ('PM2.5', '@value'),
]
```


```python
# set range_tool
range_tool = RangeTool(x_range = p.x_range)
range_tool.overlay.fill_color = 'navy'
range_tool.overlay.fill_alpha = 0.2
```


```python
select.line('hours', 'value', source = source)
select.ygrid.grid_line_color = None
select.add_tools(range_tool)
select.toolbar.active_multi = range_tool

output_file("pm25_sh.html")
show(column(p, select))
```








  <div class="bk-root" id="6b5eec4b-4bf9-43be-b627-46a2c1da1e53" data-root-id="1095"></div>


