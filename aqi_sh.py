# import libs and datasets
import numpy as np
import pandas as pd
import datetime

from bokeh.io import show, output_notebook
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, RangeTool, HoverTool
from bokeh.plotting import figure, output_file, show

aqi = pd.read_excel('datasets/sh_daily_aqi.xls', parse_dates = ['date'])


aqi.sort_values(by = 'date', inplace = True)
print(aqi.head())
#print(aqi.date.dt.year)



date = np.array(aqi['date'], dtype = np.datetime64)

source = ColumnDataSource(data = dict(date = date, value = aqi['aqi'],
                                      value2 = aqi['pm2.5'],
                                     year = aqi['date'].dt.year, month = aqi['date'].dt.month,
                                     day = aqi['date'].dt.day))


# display bokeh plot in the notebook output
output_notebook()


# create the main plot
Tools = 'save, reset, box_zoom, hover, wheel_zoom'
p = figure(title = 'Daily AQI of Shanghai', plot_height = 400, plot_width = 800, tools = Tools, toolbar_location = 'right',
          x_axis_type = 'datetime', x_axis_location = 'above',
          background_fill_color = '#efefef', x_range = (date[100], date[200]),
          y_range = (0, max(np.max(aqi['aqi']), np.max(aqi['pm2.5'])) + 20))

p.line('date', 'value', source = source)
#p.line('date', 'value2', source = source, legend = 'PM2.5', color = 'red')
p.yaxis.axis_label = 'AQI'


# create the select plot below
select = figure(title = 'Drag the selection box to change the range above', 
               plot_height = 130, plot_width = 800, y_range = p.y_range,
               x_axis_type = 'datetime', y_axis_type = 'linear',
               tools = '', toolbar_location = None, background_fill_color = '#efefef')

# set hovertool 
p.select_one(HoverTool).tooltips = [
    ('Date', '@year/@month/@day'),
    ('AQI', '@value'),
]


# set range_tool
range_tool = RangeTool(x_range = p.x_range)
range_tool.overlay.fill_color = 'navy'
range_tool.overlay.fill_alpha = 0.2


select.line('date', 'value', source = source)
select.ygrid.grid_line_color = None
select.add_tools(range_tool)
select.toolbar.active_multi = range_tool

output_file("aqi_sh.html")
show(column(p, select))




