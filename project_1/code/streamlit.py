# Your Name
# si649f20 altair transforms 2

# imports we will use
import altair as alt
import pandas as pd
import streamlit as st

#Title
st.title("Why does Norway perform so well?")

#Import data
df_m=pd.read_csv('medals.csv')
df3=pd.read_csv('rinks.csv',encoding='ISO-8859-1')
df3_p=df3.groupby('NOC')['place'].count().reset_index().sort_values(by=['place'],ascending=False)

#Sidebar


###### Making of all the charts
df_top=df_m.groupby(["NOC"]).count().reset_index().sort_values(by=['Medal'],ascending=False)['NOC'].head(9)

top=df_top.tolist()
df_top=df_m[df_m['NOC'].isin(df_top.tolist())]
########Vis 1

selection = alt.selection_single(on="mouseover",empty='none')
condition = alt.condition(selection, alt.value(1),alt.value(0.3))


c_line=alt.Chart(df_top[df_top['NOC']=='NOR']).mark_line().encode(
    x=alt.X('Year'),
    y=alt.Y('count(Medal):Q'),
    color = 'NOC:N'
).properties(width=700,height=500).add_selection(
    selection
)


c1=alt.Chart(df_top[df_top['NOC']=='NOR']).mark_area(opacity=1).encode(
    x=alt.X('Year'),
    y=alt.Y('count(Medal):Q'),
    color = 'NOC:N',
    opacity = condition
).properties(width=700,height=500,title="Medal Count of top 5 countries over time")


c2=alt.Chart(df_top[df_top['NOC']=='GER']).mark_area(opacity=0.3).encode(
    x=alt.X('Year'),
    y=alt.Y('count(Medal):Q'),
    color = 'NOC:N',
    opacity = condition
).properties(width=400,height=300)
c3=alt.Chart(df_top[df_top['NOC']=='AUT']).mark_area(opacity=0.2).encode(
    x=alt.X('Year'),
    y=alt.Y('count(Medal):Q'),
    color = 'NOC:N',
    opacity = condition
).properties(width=400,height=300)
c4=alt.Chart(df_top[df_top['NOC']=='URS']).mark_area(opacity=0.2).encode(
    x=alt.X('Year'),
    y=alt.Y('count(Medal):Q'),
    color = 'NOC:N',
    opacity = condition
).properties(width=400,height=300)
c5=alt.Chart(df_top[df_top['NOC']=='USA']).mark_area(opacity=0.2).encode(
    x=alt.X('Year'),
    y=alt.Y('count(Medal):Q'),
    color = 'NOC:N',
    opacity = condition
).properties(width=400,height=300)


Vis1=(c1+c2+c3+c4+c5+c_line).configure_title(fontSize=20)


########################vis2############################################

c_line=alt.Chart(df_top[df_top['NOC']=='NOR']).mark_line(color='red').encode(
    x=alt.X('Year'),
    y=alt.Y('count(Medal):Q')
).properties(width=300,height=200)


c1=alt.Chart(df_top[df_top['NOC']=='NOR']).mark_area(opacity=0.3,color='red').encode(
    x=alt.X('Year'),
    y=alt.Y('count(Medal):Q',axis=alt.Axis(title="Count of Medals")),
    color=alt.Color('count(Medal):Q',scale=alt.Scale(scheme='reds'),legend=alt.Legend(title='Count of Medals'))
).properties(width=300,height=200,title="Norway count of medals over time")
c1=c1+c_line


c2=alt.Chart(df_m[df_m['NOC']=='NOR']).mark_area().encode(
    x=alt.X('Year'),
    y=alt.Y('count(Medal):Q',axis=alt.Axis(title="Count of Medals")),
    color = 'Sport:N'
).properties(width=300,height=200,title="Norway count of medals of cetain sport over time")

text_annotation=c2.mark_text(
    align='left',
    dx=7,
    color='black'
).encode(
    text=alt.Text('count(Medal):Q'),
    x=alt.X('Year',axis=None,scale=alt.Scale(domain=[1920, 2010]))
)

c3=alt.Chart(df_m[df_m['NOC']=='NOR']).mark_area().encode(
    x=alt.X('Year'),
    y=alt.Y('count(Medal):Q',axis=alt.Axis(title="Count of Medals")),
    color = 'Discipline:N'
).properties(width=300,height=200,title='Norway count of medals of certain discipline varies over time'
)

c4=alt.Chart(df_m[df_m['NOC']=='NOR']).mark_area().encode(
    x=alt.X('Year'),
    y=alt.Y('count(Medal):Q',axis=alt.Axis(title="Count of Medals")),
    color = 'Event gender:N'
).properties(width=300,height=200,title='Norway count of medals of event gender varies over time'
)

Vis2=(c1|c2)&(c3|c4).resolve_scale(color='independent', x='shared',y='shared')


















#vis Medal Count distribtuion of top 9 countries varies over time

selection =alt.selection_single(
    fields=['Sport'],on="click",bind='legend'
    
)
condition = alt.condition(selection,alt.value(1),alt.value(0.3))

vis_facet=alt.Chart(df_top).mark_area().encode(
    x=alt.X('Year'),
    y=alt.Y('count(Medal):Q'),
    color = 'Sport:N',
    opacity=condition
).properties(
    width=150,
    height=150,
    title="Medal Count of top 9 countries over time"
).facet(
    facet=alt.Facet('NOC:N',sort=alt.EncodingSortField('Medal', op='count', order='ascending')),
    columns=3
).add_selection(
    selection
).configure_legend(
    strokeColor='gray',
    fillColor='#EEEEEE',
    padding=10,
    cornerRadius=10,
    orient='right',
    symbolSize=200,
    symbolType='square'
).configure_axis(
    labelFontSize=12,
    titleFontSize=15
)








# ########Vis4
df_medal_noc=df_m[~df_m['Medal'].isna()][['NOC','Medal']].groupby('NOC').count().reset_index()
df_medal_rinks=pd.merge(df3_p,df_medal_noc, on='NOC').rename(columns={'place':'Rink count', 'Medal':'Medal count'})
df_medal_rinks.head()
selection=alt.selection_single();
colorCondition=alt.condition(selection,"NOC",alt.value("gray"))

#########################
c1_1=alt.Chart(df_medal_rinks).mark_bar(color='grey').encode(
    y=alt.X('NOC:N',
    sort='-x'),
    x=alt.Y('Rink count'),
    tooltip=['NOC','Medal count:Q','Rink count:Q']
).encode(
    color=colorCondition,   
).add_selection(
    selection
)
c1_2=alt.Chart(df_medal_rinks[df_medal_rinks['NOC']=='NOR']).mark_bar(color='red').encode(
    y=alt.X('NOC:N',
    sort='-x'),
    x=alt.Y('Rink count')

)

vis_rink=c1_1+c1_2

##########################
c2_1=alt.Chart(df_medal_rinks).mark_circle(color='grey').encode(
    x=alt.X('Rink count:Q',
    sort='-y'),
    y=alt.Y('Medal count:Q'),
    size='Rink count:Q',
    tooltip=['NOC','Medal count:Q','Rink count:Q']
).encode(
    color=colorCondition,   
).add_selection(
    selection
).properties(height=300,width=400,title="Total tink count vs medal count in all the year for each countries")

c2_2=alt.Chart(df_medal_rinks[df_medal_rinks['NOC']=='NOR']).mark_circle(color='red').encode(
    x=alt.X('Rink count:Q',
    sort='-y'),
    y=alt.Y('Medal count:Q'),
    size='Rink count:Q'
)
text_annotation=alt.Chart(df_medal_rinks[df_medal_rinks['NOC'].isin(top)]).mark_circle().encode(
    x=alt.X('Rink count:Q',
    sort='-y'),
    y=alt.Y('Medal count:Q'),
).mark_text(
    align='left',
    dx=7,

).encode(
    text=alt.Text('NOC:N')
)
vis_rink_medal=c2_1+c2_2+text_annotation

##############################
vis4=(vis_rink_medal & vis_rink).resolve_scale(x='shared')




# ########Vis4 BONUS OPTIONAL

# #Altair version

# #Streamlit widget version


# ##### Display graphs

options_vis=['Top 5 countires','Sport, Discipline, Event Gender in Norway',"Sports in all countries",'Rinks']

select=st.sidebar.selectbox(label='Select a visualization to display',
options=options_vis)

if select=="Top 5 countires":
    st.header("Norway did perform well in Winter Olympics!")
    Vis1
    """
    To explore the reason why Norway performs so well, the first step is to prove it did perform well in the Winter Olympics. So the number of medals of each country are calculated and ranked. The top 5 countries are visualized to see how the number of medals vary over time. From 1924 to 2006, the number of medals of Norway in each year always took a high rank, and it was never lower than top 5. 

The transparency design is to avoid the hidden information because of overlapping. The red line is used to emphasize the info of Norway. So users can detect Norway without the need for focused attention. It fits into the Preattentive Processing.

    """
elif select =='Sport, Discipline, Event Gender in Norway':
    st.header("Norway did well in skating and skiing!")
    Vis2
    """
    What directly impact Norway’s medal count in the Olympics? In this step, I explored the field sport, discipline, event gender. All those elements are in the same x-axis, the year from 1924 to 2006, as well as the y-axis, the number of medals of Norway each year in Winter Olympics.
To be consistent, the first chart is part of the first visualization. The only difference is that it gets rid of the other 4 countries except Norway. So, we can see the number of medals of Norway in each year varies over time. The rest graphics encode the three fields into color.
In terms of sports, skiing and skating took the highest percentage of the total medals. This means that Norway performed well in skating and skiing! As for discipline, speed skating and cross country took the highest percentage. In event gender part, man won more medals than women in Norway. 
    """


elif select=="Sports in all countries":
    st.header("Top 9 countires most did well in Skiing and Skating!")
    vis_facet
    """
    In the previous step, the one of the result is that Norway did best in skating and skiing. So how about other countries’ best sports?
Different from Norway only won medals in four sports, other countries won medals in seven sports. But skiing and skating are still the sports they performed best in.

The interaction is added in this part. Users can click the area in the chart, so all the facets and legend will have the same color (sport) highlighted. Click the sport in legend, the corresponding part in the chart will also be highlighted
    """
elif select =='Rinks':
    st.header("Norway has the most rinks and medals in the world!")
    vis4
    """
    Since Norway performed well in skating and skiing, so as other top 9 countries, the certain sport is worth exploring. The number of sportsground in one country can matters. Look at the number of rinks in each country, which affects the skating performance.
How many rinks does Norway have? What’s the relationship between number of rinks and the medals in total? The bar chart is used to see the number of rinks Norway and other countries have, sorted to see the ranking. The scatterplot is used to see the relationship between rinks and medals, also the medal count is double-encoded in the circle size. The NOC is encode into color, for the interactive design. The two charts share the same attributes: color stands for NOC; x-axis represents rink count.
By click the circle, the same NOC in the scatterplot and bar chart will be both highlighted. It is easy to see the association. The same rule works when clicking the bar in the barchart. The information of Norway will always be highlighted. Tooltip is to show the NOC, medal count and rink count for each bar or circle.

    """

