
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




#%% 

feed = pd.read_csv(r'data\feed.csv', encoding= "ISO-8859-1")
feed['Time'] = pd.to_datetime(feed['Time'], infer_datetime_format = True)
feed['Time'] = feed['Time'].dt.tz_localize('Etc/GMT+0').dt.tz_convert('Singapore')
feed['hour'] = feed['Time'].dt.hour
feed['activity'] = feed['Likes'] + feed['Reactions'] + feed['Shares']
feed['Time of the day'] = pd.cut(feed['hour'], right = False, bins =[8,20], labels = ['Working hours'])
feed['hour (12 hours)'] = np.where(feed['hour']>12, feed['hour']-12, feed['hour'])
feed['angle'] = feed['hour (12 hours)']/12*360


businessfeed = feed[feed['Time of the day']== 'Working hours']
businessfeed = businessfeed.groupby('angle')['activity'].mean()


offbusinessfeed = feed[feed['Time of the day']!= 'Working hours']
offbusinessfeed = offbusinessfeed.groupby('angle')['activity'].mean()

#%%
members = pd.read_csv(r'data\member.csv', encoding= "ISO-8859-1")

merged= pd.merge(feed, members, on='User ID')
merged = merged[(merged['hour'] <= 5 )&(merged['hour'] >= 0 )]
merged = merged['Name'].value_counts().head()

#%%
fig = plt.figure(figsize = (10,10))

ax = plt.subplot(211,polar = True)
equals = np.linspace(0,360,12, endpoint=False)
ax.bar(np.radians(offbusinessfeed.index.values),offbusinessfeed,width= 0.5, linewidth=0, color = 'orange', label = 'Off-work hours')
ax.bar(np.radians(businessfeed.index.values),businessfeed, width= 0.5, linewidth=0, alpha = 0.4, label = 'Working Hours (8am - 8pm)' )

#remove y labels
plt.setp(ax.get_yticklabels(), visible = False)

#setting the clock hours labels
ax.set_xticks(np.linspace(0, 2*np.pi, 12, endpoint=False))
ax.set_xticklabels([12,1,2,3,4,5,6,7,8,9,10,11])

#reversing order of labels
ax.set_theta_direction(-1)
#setting 12 at 12 oclock position
ax.set_theta_offset(np.pi/2.0)

#cosmetics
ax.legend(bbox_to_anchor = (1.0,1.0))
ax.yaxis.grid(False)
plt.title('When is the best time to get reactions from a post? \n Average reactions by hour of the day \n')

#%%
ax1 = plt.subplot(212)
ax1.bar(range(len(merged.index)), merged, width= 0.5 )
plt.xticks(range(len(merged.index)), merged.index)

ax1.set_ylabel('Number of night owl posts')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_linewidth(0.5)
ax1.spines['left'].set_linewidth(0.5)


rects = ax1.patches

for rect in rects:
    y = rect.get_height()
    x = rect.get_x() + rect.get_width()/2
    label = "{:.0f}".format(y)
    plt.annotate(label,(x,y), xytext = (0,5), textcoords = 'offset points', ha= 'center')
    

plt.title('\n Night owls of WPFB Data Science Community \n (Top 5 community members by number of posts between 12mn to 5am) \n')
plt.tight_layout()
plt.savefig(r'WPFB.png', bbox_inches = 'tight')
plt.show()

