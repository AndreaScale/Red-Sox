import pandas as pd
import plotly.express as px
import numpy as np
import statistics
import matplotlib.pyplot as plt

#As a first step I will compute the distribution of prices along the days until game without any restriction. I will the compare the results over the years. 

#I will first procede with 2009, the procedure will be the same for the other years.

file09 = pd.read_csv('red_sox_2009.csv')

fig1 = px.histogram(file09, x="days_from_transaction_until_game", y="price_per_ticket", histfunc='avg', title='Distribution 2009')
fig1.show()

#We start to see a fuzzy and expected pattern: prices grow as game date approches

#I want to construct a more clear plot, with a moving average for the price. I group togheter prices per days

file09_group = file09.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()

file09_group['moving_average_5'] = file09_group['price_per_ticket'].rolling(window=5).mean()
file09_group['moving_average_15'] = file09_group['price_per_ticket'].rolling(window=15).mean()

ax = file09_group.plot(kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
file09_group.plot(ax = ax, kind='line', x="days_from_transaction_until_game", y="moving_average_5")
ax.set_title("2009")



#This plot is way more clear than the histogram. We start to see a pattern. The price grows in the first 50 days, then stabilizes untill the very laast few days (5-10), when it drops.

file10 = pd.read_csv('red_sox_2010.csv')
file11 = pd.read_csv('red_sox_2011.csv')
file12 = pd.read_csv('red_sox_2012.csv')

#In order to have a better representation of this dataset I'm going to merge the four datasets with a 'year' variable

file09['year'] = [2009 for k in range(0,np.size(file09,0))]
file10['year'] = [2010 for k in range(0,np.size(file10,0))]
file11['year'] = [2011 for k in range(0,np.size(file11,0))]
file12['year'] = [2012 for k in range(0,np.size(file12,0))]

file = file09._append(file10._append(file11._append(file12)))

histo_all = px.histogram(file, x="days_from_transaction_until_game", y="price_per_ticket", color='year', histfunc='avg', title='Subdivision in years')

histo_all.show()

#Instrogram gives us an idea. Let us see plots and moving averages

file10_group = file10.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()
file10_group['moving_average_5'] = file10_group['price_per_ticket'].rolling(window=5).mean()
file10_group['moving_average_15'] = file10_group['price_per_ticket'].rolling(window=15).mean()

file11_group = file11.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()
file11_group['moving_average_5'] = file11_group['price_per_ticket'].rolling(window=5).mean()
file11_group['moving_average_15'] = file11_group['price_per_ticket'].rolling(window=15).mean()

file12_group = file12.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()
file12_group['moving_average_5'] = file12_group['price_per_ticket'].rolling(window=5).mean()
file12_group['moving_average_15'] = file12_group['price_per_ticket'].rolling(window=15).mean()

#I now plot them all

fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(nrows=2, ncols=2)

plt.subplot(2, 2, 1)
file09_group.plot(ax = ax0, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
file09_group.plot(ax = ax0, kind='line', x="days_from_transaction_until_game", y="moving_average_5")
ax0.set_title("2009") 

plt.subplot(2, 2, 2)  
file10_group.plot(ax = ax1, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
file10_group.plot(ax = ax1, kind='line', x="days_from_transaction_until_game", y="moving_average_5")
ax1.set_title("2010") 

plt.subplot(2, 2, 3)
file11_group.plot(ax = ax2, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
file11_group.plot(ax = ax2, kind='line', x="days_from_transaction_until_game", y="moving_average_5")
ax2.set_title("2011") 

plt.subplot(2, 2, 4)
file12_group.plot(ax = ax3, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
file12_group.plot(ax = ax3, kind='line', x="days_from_transaction_until_game", y="moving_average_5")
ax3.set_title("2012") 

axm = file09_group.plot(kind='line', x="days_from_transaction_until_game", y="moving_average_15")
file10_group.plot(ax = axm, kind='line', x="days_from_transaction_until_game", y="moving_average_15", )
file11_group.plot(ax = axm, kind='line', x="days_from_transaction_until_game", y="moving_average_15")
file12_group.plot(ax = axm, kind='line', x="days_from_transaction_until_game", y="moving_average_15")
axm.set_title("Moving averages (window = 15)")
axm.legend(['2009','2010','2011','2012'])


#These graphs have a lot to say:

#1) My first idea has been confutated by data. It is clear that shorter time to game-day does not imply higher price of the ticket. On the contrary
#   we can clearly see that prices usually decrease in the last days before the game. 

#2) Nevertheless prices grow fast in the first 50 days on the market, before stabilizing, a part from 2010. In 2010 the initial trend is inverted: in the first
#   50 days the prices decrease with high rate

#3) Although the question is not about how prices change over the year, but about how the distribution evolves, it is interesting noticing 
#   an tremendous increase of almost 100% per year   


#We are now going to delve more into data.

#As a second step I want to better study differences betwen sections. Let us study 2009 at first and then the others


histo_09_sec = px.histogram(file09, x="days_from_transaction_until_game", y="price_per_ticket", color='sectiontype', histfunc='avg', title='Subdivision in sections 2009')

histo_09_sec.show()

#The graphical representation is not so clear now. Let us use some statistcs instead. We are going to evaluate mean, median, max and min
#for 3 time slots, [0:50], [51:150] and more than 150.


print(file09.loc[(file09['sectiontype'] == "SRO") & (file09['days_from_transaction_until_game'] <= 50)]['price_per_ticket']) 

sections = list(set(file09['sectiontype'].tolist()))

sec_stat_09 = []
sec_stat_09_less50 = []
sec_stat_09_less150 = []
sec_stat_09_more150 = []

for sec in sections:
    sec_50 = file09.loc[(file09['sectiontype'] == sec) & (file09['days_from_transaction_until_game'] <= 50)]['price_per_ticket']
    sec_150 = file09.loc[(file09['sectiontype'] == sec) & (50 < file09['days_from_transaction_until_game']) & ((file09['days_from_transaction_until_game']) <= 150)]['price_per_ticket']
    sec_stat_09 += [[sec + " less 50 days", min(sec_50), max(sec_50), statistics.mean(sec_50), statistics.median(sec_50)]] 
    sec_stat_09_less50 += [[sec + " less 50 days", min(sec_50), max(sec_50), statistics.mean(sec_50), statistics.median(sec_50)]]
    sec_stat_09 += [[sec + " more 50 less 150 days", min(sec_150), max(sec_150), statistics.mean(sec_150), statistics.median(sec_150)]]
    sec_stat_09_less150 += [[sec + " more 50 less 150 days", min(sec_150), max(sec_150), statistics.mean(sec_150), statistics.median(sec_150)]]
    if len(file09.loc[(file09['sectiontype'] == sec) & (150 < file09['days_from_transaction_until_game'])]['price_per_ticket']) != 0:
        sec_250 = file09.loc[(file09['sectiontype'] == sec) & (150 < file09['days_from_transaction_until_game'])]['price_per_ticket']
        sec_stat_09 += [[sec + " more 150 days", min(sec_250), max(sec_250), statistics.mean(sec_250), statistics.median(sec_250)]]
        sec_stat_09_more150 += [[sec + " more 150 days", min(sec_250), max(sec_250), statistics.mean(sec_250), statistics.median(sec_250)]]

table_sec_90 = pd.DataFrame(sec_stat_09,columns=['Section and time interval','Min','Max','Mean','Median'])

print(table_sec_90)

Section_90 = open("Statistics_2009_section.html","w")
Section_90.write(pd.DataFrame.to_html(table_sec_90))
Section_90.close()

#Closely looking at this statistics the first impression given by the first histogram seems wrong, as the second histogram showed.
#In almost all sectors the trend, given this subdivision of time, is characterized by a relatively small increase over the first two periods
#followed by a bigger fall in the last one. 
# 
# I now wan to group the sectors in 3 price range, and compare the evolution of prices of this 3 groups
#because from this statistics the more expensive sector seem to have the biggest change over time. In order to do so I want to see the minimus values 
#at start date for each section, for a better understanding of the categories

min_start_90 = []

for sec in sections:
    sec_min = min(file09.loc[(file09['sectiontype'] == sec) & (file09['days_from_transaction_until_game'] > 100)]['price_per_ticket'])
    min_start_90 += [[sec, sec_min]]

table_sec_90_min = pd.DataFrame(min_start_90,columns=['Section','Min'])

print(table_sec_90_min)

#Then i divide [0$:30$], [30$:100$] and more than 100$

less_50 = ['RFGS','SRO','RFROOFBOX','UpperBleachers','FamilyGS','IFGS']
less_150 = ['PAVBOX','FieldBox','LogeBox','PAVSRO','RFFieldBox']
more_150 = ['EMCCLUB','PAVCLUB','PAVCLB_HP','LFPAV','DUGOUTBOX','MONSTR_SRO']

#I update the dataset with a variable 'price range' with values '0', '1', '2' which states in which group the section is

def price_range_valutator(string):
    if string in less_50: return 0
    if string in less_150: return 1
    if string in more_150: return 2


file09['price_range'] = file09['sectiontype'].map(price_range_valutator)


fig_sec_09 = px.histogram(file09, x="days_from_transaction_until_game", y="price_per_ticket", color='price_range', histfunc='avg', title='Subdivision in price range 2009')

fig_sec_09.show()

#The graph corroborate my hypotesis. We can clearly see that the cheaper section, i.e. price_range = 0,1, are much more stable than the most expensive.

#I now conduct the same anlysis for each year, fixing the 3 price ranges.

file10['price_range'] = file10['sectiontype'].map(price_range_valutator)
file11['price_range'] = file11['sectiontype'].map(price_range_valutator)
file12['price_range'] = file12['sectiontype'].map(price_range_valutator)

file09_range0 = file09.loc[file09['price_range'] == 0][['days_from_transaction_until_game','price_per_ticket']]
file09_range1 = file09.loc[file09['price_range'] == 1][['days_from_transaction_until_game','price_per_ticket']]
file09_range2 = file09.loc[file09['price_range'] == 2][['days_from_transaction_until_game','price_per_ticket']]
file09_group_range0 = file09_range0.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()
file09_group_range1 = file09_range1.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()
file09_group_range2 = file09_range2.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()
file10_range0 = file10.loc[file10['price_range'] == 0][['days_from_transaction_until_game','price_per_ticket']]
file10_range1 = file10.loc[file10['price_range'] == 1][['days_from_transaction_until_game','price_per_ticket']]
file10_range2 = file10.loc[file10['price_range'] == 2][['days_from_transaction_until_game','price_per_ticket']]
file10_group_range0 = file10_range0.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()
file10_group_range1 = file10_range1.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()
file10_group_range2 = file10_range2.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()
file11_range0 = file11.loc[file11['price_range'] == 0][['days_from_transaction_until_game','price_per_ticket']]
file11_range1 = file11.loc[file11['price_range'] == 1][['days_from_transaction_until_game','price_per_ticket']]
file11_range2 = file11.loc[file11['price_range'] == 2][['days_from_transaction_until_game','price_per_ticket']]
file11_group_range0 = file11_range0.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()
file11_group_range1 = file11_range1.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()
file11_group_range2 = file11_range2.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()
file12_range0 = file12.loc[file12['price_range'] == 0][['days_from_transaction_until_game','price_per_ticket']]
file12_range1 = file12.loc[file12['price_range'] == 1][['days_from_transaction_until_game','price_per_ticket']]
file12_range2 = file12.loc[file12['price_range'] == 2][['days_from_transaction_until_game','price_per_ticket']]
file12_group_range0 = file12_range0.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()
file12_group_range1 = file12_range1.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()
file12_group_range2 = file12_range2.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()

fig2, ((ax0, ax1), (ax2, ax3)) = plt.subplots(nrows=2, ncols=2)

plt.subplot(2, 2, 1)
file09_group_range0.plot(ax = ax0, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
file09_group_range1.plot(ax = ax0, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
file09_group_range2.plot(ax = ax0, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
ax0.set_title("2009") 
ax0.legend(['range 0','range 1','range 2'])

plt.subplot(2, 2, 2)  
file10_group_range0.plot(ax = ax1, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
file10_group_range1.plot(ax = ax1, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
file10_group_range2.plot(ax = ax1, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
ax1.set_title("2010") 
ax1.legend(['range 0','range 1','range 2'])

plt.subplot(2, 2, 3)
file11_group_range0.plot(ax = ax2, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
file11_group_range1.plot(ax = ax2, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
file11_group_range2.plot(ax = ax2, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
ax2.set_title("2011")
ax2.legend(['range 0','range 1','range 2']) 

plt.subplot(2, 2, 4)
file12_group_range0.plot(ax = ax3, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
file12_group_range1.plot(ax = ax3, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
file12_group_range2.plot(ax = ax3, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
ax3.legend(['range 0','range 1','range 2'])
ax3.set_title("2012") 


#The trend continue untill 2012, when all sections behave extremely similarly. 

fig12 = px.histogram(file12, x="days_from_transaction_until_game", y="price_per_ticket", histfunc='avg', title='2012')
fig12.show()

#2012 shows a less predictable behavior with respect to previous years.

#I will now study the rapid increase durign the first 50/80 days in the market.

#Let us study the first 50 days of 2009

first50_09 = file09.loc[file09['days_from_transaction_until_game'] > 200]
first50_09_list = [min(first50_09['price_per_ticket']),max(first50_09['price_per_ticket']),statistics.mean(first50_09['price_per_ticket']),statistics.median(first50_09['price_per_ticket']),statistics.stdev(first50_09['price_per_ticket'])]
first50_09_stats = pd.DataFrame([first50_09_list],columns=['Min','Max','Mean','Median','SD'])

print(first50_09_stats)

#The variance is very large in this first period, let us compare it with future periods

after50_09 = file09.loc[file09['days_from_transaction_until_game'] <= 200]
after50_09_list = [min(after50_09['price_per_ticket']),max(after50_09['price_per_ticket']),statistics.mean(after50_09['price_per_ticket']),statistics.median(after50_09['price_per_ticket']),statistics.stdev(after50_09['price_per_ticket'])]
after50_09_stats = pd.DataFrame([after50_09_list],columns=['Min','Max','Mean','Median','SD'])

print(after50_09_stats)

#Although we are taking in consideration a 4 time bigger time intervall the standard deviation decreased of almost 25%. This statistic is confirms the high volatility of prices in the first 50 years.

#Let us study if the behaviour does or not change thorugh the years

before50_10 = file10.loc[file10['days_from_transaction_until_game'] > 200]
after50_10 = file10.loc[file10['days_from_transaction_until_game'] <= 200]
after50_10_stats = [min(after50_10['price_per_ticket']),max(after50_10['price_per_ticket']),statistics.mean(after50_10['price_per_ticket']),statistics.median(after50_10['price_per_ticket']),statistics.stdev(after50_10['price_per_ticket'])]
before50_10_stats = [min(before50_10['price_per_ticket']),max(before50_10['price_per_ticket']),statistics.mean(before50_10['price_per_ticket']),statistics.median(before50_10['price_per_ticket']),statistics.stdev(before50_10['price_per_ticket'])]

before50_11 = file11.loc[file11['days_from_transaction_until_game'] > 200]
after50_11 = file11.loc[file11['days_from_transaction_until_game'] <= 200]
after50_11_stats = [min(after50_11['price_per_ticket']),max(after50_11['price_per_ticket']),statistics.mean(after50_11['price_per_ticket']),statistics.median(after50_11['price_per_ticket']),statistics.stdev(after50_11['price_per_ticket'])]
before50_11_stats = [min(before50_10['price_per_ticket']),max(before50_11['price_per_ticket']),statistics.mean(before50_11['price_per_ticket']),statistics.median(before50_11['price_per_ticket']),statistics.stdev(before50_11['price_per_ticket'])]


before50_12 = file12.loc[file12['days_from_transaction_until_game'] > 200]
after50_12 = file12.loc[file12['days_from_transaction_until_game'] <= 200]
after50_12_stats = [min(after50_12['price_per_ticket']),max(after50_12['price_per_ticket']),statistics.mean(after50_12['price_per_ticket']),statistics.median(after50_12['price_per_ticket']),statistics.stdev(after50_12['price_per_ticket'])]
before50_12_stats = [min(before50_12['price_per_ticket']),max(before50_12['price_per_ticket']),statistics.mean(before50_12['price_per_ticket']),statistics.median(before50_12['price_per_ticket']),statistics.stdev(before50_12['price_per_ticket'])]

before_50_stats_all = pd.DataFrame([[2009]+first50_09_list,[2010]+before50_10_stats,[2011]+before50_11_stats,[2012]+before50_12_stats],columns=['Year','Min','Max','Mean','Median','SD'])
after_50_stats_all = pd.DataFrame([[2009]+after50_09_list,[2010]+after50_10_stats,[2011]+after50_11_stats,[2012]+after50_12_stats],columns=['Year','Min','Max','Mean','Median','SD'])

Before50 = open("Statistics_before_50_days.html","w")
Before50.write(pd.DataFrame.to_html(before_50_stats_all))
Before50.close()

After50 = open("Statistics_after_50_days.html","w")
After50.write(pd.DataFrame.to_html(after_50_stats_all))
After50.close()

#This analysis clearly shows that in every year the firrst 50 days of the market are the most unstable. 
#Nevertheless this stabilization after the first 50 days gets less strong as years passes.

#I do not expect the other variables do not seem to have any influence on the evolution of the prices over time. They surely influence the prices, but not their evolution.
#Let us test this hypothesis.

file09_group_day = file09.groupby(['day_game'])['price_per_ticket'].mean().reset_index()

After503 = open("Statisticsdays.html","w")
After503.write(pd.DataFrame.to_html(file09_group_day))
After503.close()

print(file09_group_day)

#The mean price is 20% higher, as expected. The trend:

file09_day = file09.loc[file09['day_game'] == 1][['days_from_transaction_until_game','price_per_ticket']]
file09_group_day = file09_day.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()
file09_nday = file09.loc[file09['day_game'] == 0][['days_from_transaction_until_game','price_per_ticket']]
file09_group_nday = file09_nday.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()

axd = file09_group_day.plot(kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
file09_group_nday.plot(ax = axd, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
axd.set_title("2009 day_game Y/N")
axd.legend(['Day game','Non day game'])

#We see a little less stability for day game, but a small difference between the two. Therefore variable day_game does not seem to affect the evolution of prices
# 
# For what concerns weekend_game:

file09_group_weekend = file09.groupby(['weekend_game'])['price_per_ticket'].mean().reset_index()

print(file09_group_weekend)

#The mean price is almost 30% higher. The trend:

file09_weekend = file09.loc[file09['weekend_game'] == 1][['days_from_transaction_until_game','price_per_ticket']]
file09_group_weekend = file09_weekend.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()
file09_nweekend = file09.loc[file09['weekend_game'] == 0][['days_from_transaction_until_game','price_per_ticket']]
file09_group_nweekend = file09_nweekend.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()

axw = file09_group_weekend.plot(kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
file09_group_nweekend.plot(ax = axw, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
axw.set_title("2009 weekend_game Y/N")
axw.legend(['Weekend game','Non weekend game'])

#As shown before unstability problem arise in the first 50-80 days of market. In this categorization both variables look extremely instable in that period
#I conduct a fast statistical analysis

first50_09_weekend = file09_weekend.loc[file09_weekend['days_from_transaction_until_game'] > 200]
stat_weekend_list = [min(first50_09_weekend['price_per_ticket']),max(first50_09_weekend['price_per_ticket']),statistics.mean(first50_09_weekend['price_per_ticket']),statistics.median(first50_09_weekend['price_per_ticket']),statistics.stdev(first50_09_weekend['price_per_ticket'])]
stat_weekend = pd.DataFrame([stat_weekend_list],columns=['Min','Max','Mean','Median','SD'])

print(stat_weekend)

weeke = open("Statisticsweek.html","w")
weeke.write(pd.DataFrame.to_html(stat_weekend))
weeke.close()


first50_09_nweekend = file09_nweekend.loc[file09_nweekend['days_from_transaction_until_game'] > 200]
stat_nweekend_list = [min(first50_09_nweekend['price_per_ticket']),max(first50_09_nweekend['price_per_ticket']),statistics.mean(first50_09_nweekend['price_per_ticket']),statistics.median(first50_09_nweekend['price_per_ticket']),statistics.stdev(first50_09_nweekend['price_per_ticket'])]
stat_nweekend = pd.DataFrame([stat_nweekend_list],columns=['Min','Max','Mean','Median','SD'])

weeken = open("Statisticsnweek.html","w")
weeken.write(pd.DataFrame.to_html(stat_nweekend))
weeken.close()

print(stat_nweekend)

#What was not clear from the graph is enlighted by the SD. Weekend games are much less stable than non weekend games, in fact the latter's sd is half the first's one.
#Therefore weekend_game seem to heavely influence the variance of the initial distribution.

#Let us conduct the same analysis over the years.

file10_day = file10.loc[file10['day_game'] == 1][['days_from_transaction_until_game','price_per_ticket']]
file10_group_day = file10_day.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()
file10_nday = file10.loc[file10['day_game'] == 0][['days_from_transaction_until_game','price_per_ticket']]
file10_group_nday = file10_nday.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()
file11_day = file11.loc[file11['day_game'] == 1][['days_from_transaction_until_game','price_per_ticket']]
file11_group_day = file11_day.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()
file11_nday = file11.loc[file11['day_game'] == 0][['days_from_transaction_until_game','price_per_ticket']]
file11_group_nday = file11_nday.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()
file12_day = file12.loc[file12['day_game'] == 1][['days_from_transaction_until_game','price_per_ticket']]
file12_group_day = file12_day.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()
file12_nday = file12.loc[file12['day_game'] == 0][['days_from_transaction_until_game','price_per_ticket']]
file12_group_nday = file12_nday.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()


axd = file09_group_day.plot(kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
file09_group_nday.plot(ax = axd, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
axd.set_title("2009 day_game Y/N")
axd.legend(['Day game','Non day game'])

fig1, ((ax0, ax1), (ax2, ax3)) = plt.subplots(nrows=2, ncols=2)

plt.subplot(2, 2, 1)
file09_group_day.plot(ax = ax0, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
file09_group_nday.plot(ax = ax0, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
ax0.set_title("2009") 
ax0.legend(['Day game','Non day game'])

plt.subplot(2, 2, 2)  
file10_group_day.plot(ax = ax1, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
file10_group_nday.plot(ax = ax1, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
ax1.set_title("2010")
ax1.legend(['Day game','Non day game']) 

plt.subplot(2, 2, 3)
file11_group_day.plot(ax = ax2, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
file11_group_nday.plot(ax = ax2, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
ax2.set_title("2011") 
ax2.legend(['Day game','Non day game'])

plt.subplot(2, 2, 4)
file12_group_day.plot(ax = ax3, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
file12_group_nday.plot(ax = ax3, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
ax3.set_title("2012")
ax3.legend(['Day game','Non day game']) 

fig1.suptitle("Day/No Day")

#We conclude that the day_game categorization does not give any additional information. The loss of stability of 2012 is a behavior that characterizes the year, and it is not due to the 
#day_game variable

file10_weekend = file10.loc[file10['weekend_game'] == 1][['days_from_transaction_until_game','price_per_ticket']]
file10_group_weekend = file10_weekend.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()
file10_nweekend = file10.loc[file10['weekend_game'] == 0][['days_from_transaction_until_game','price_per_ticket']]
file10_group_nweekend = file10_nweekend.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()
file11_weekend = file11.loc[file11['weekend_game'] == 1][['days_from_transaction_until_game','price_per_ticket']]
file11_group_weekend = file11_weekend.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()
file11_nweekend = file11.loc[file11['weekend_game'] == 0][['days_from_transaction_until_game','price_per_ticket']]
file11_group_nweekend = file11_nweekend.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()
file12_weekend = file12.loc[file12['weekend_game'] == 1][['days_from_transaction_until_game','price_per_ticket']]
file12_group_weekend = file12_weekend.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()
file12_nweekend = file12.loc[file12['weekend_game'] == 0][['days_from_transaction_until_game','price_per_ticket']]
file12_group_nweekend = file12_nweekend.groupby(['days_from_transaction_until_game'])['price_per_ticket'].mean().reset_index()


axd = file09_group_weekend.plot(kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
file09_group_nweekend.plot(ax = axd, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
axd.set_title("2009 weekend_game Y/N")
axd.legend(['weekend game','Non weekend game'])

fig1, ((ax0, ax1), (ax2, ax3)) = plt.subplots(nrows=2, ncols=2)

plt.subplot(2, 2, 1)
file09_group_weekend.plot(ax = ax0, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
file09_group_nweekend.plot(ax = ax0, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
ax0.set_title("2009") 
ax0.legend(['Weekend game','Non weekend game'])

plt.subplot(2, 2, 2)  
file10_group_weekend.plot(ax = ax1, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
file10_group_nweekend.plot(ax = ax1, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
ax1.set_title("2010") 
ax1.legend(['Weekend game','Non weekend game'])

plt.subplot(2, 2, 3)
file11_group_weekend.plot(ax = ax2, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
file11_group_nweekend.plot(ax = ax2, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
ax2.set_title("2011") 
ax2.legend(['Weekend game','Non weekend game'])

plt.subplot(2, 2, 4)
file12_group_weekend.plot(ax = ax3, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
file12_group_nweekend.plot(ax = ax3, kind='line', x="days_from_transaction_until_game", y="price_per_ticket")
ax3.set_title("2012") 
ax3.legend(['Weekend game','Non weekend game'])

fig1.suptitle("weekend/No weekend")

#While weekend games tend to unstable in the first 50 days, non weekend games increas their instability over the years, with unexpected peacks 
#with the exeption of 2010

plt.show()