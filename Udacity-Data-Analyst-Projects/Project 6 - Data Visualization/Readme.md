# Summary


The goal of this visualization is to illustrate one of the beneficial effect of the great recession of 2008 - reducing airport delays. This graph shows that after 2008 financial crisis, airport congestion was reduced significantly and have not recovered since. This graph was drastically changed twice based on user feedbacks, and the final draft is draft3.html. The first two drafts were trying to convery relationships between airport delays and the great recession, but during the third draft the relationship has changed to the one described in the beginning. 

## Draft 1

### Design

This visualization uses a map to display the delay percentage of all major airports in the United States. A map was used because I want to display the relationship between economy and airport delay in different regions of the United States to show of regional differences. 

The change in delay level across years were illustrated by an animation that ran from 2003 to 2015. Animation is the best way of illustrating change in time in this visualization because it preserves the geographic features. 

The overall delay percentage of airports are double encoded through both the radius of the circle and the color of the circle (with green being less congested and red being more congested). 

I have also placed a circle illustrating the condition of U.S. economy (growth rate) next to the map to provide references to the reader and further demonstrate relationships between economic conditions and airport delays. The growth rate was also double encoded through radius and color to provide a easy connection for readers between airport delays and U.S. economic conditions. 

Overall, this visualization was designed to be a cocktail glass visualization, with a narrative in the beginning and plenty of rooms for users to explore after the narrative. Buttons were provided for users to go to any steps of the visualization. There is also a tooltip box associated with each visualization element (both GDP circles and airport circles) for reader to explore more detailed information about an airport in a specific year. 

### Feedback 

One of the biggest user feedback for this graph is that it is trying to convey too much information (User 1). Even though it is cool to have the map and mouse over function, it distract users from obtaining the actual objective of the visualization (User 2). Therefore, I have decided to remove the maps and instead only illustrate airport information, delay percentage, and those two factor's connection with GDP over year. 

##Draft 2

###Design

This visualization is a dynamic dual-y axis graph. The x axis represent airport overall graphic growth change; the first y axis represent delay percentage change, it is placed in the left becuase it is key information that I want to display; The second y axis represent GDP growth of the US economy. There is a horizontal red line accross the graph, representing the GDP growth of that year. 

Bubbles on this graph represent datapoint of each airport in each year. The color of the bubble represent a double-coded delay-percentage change. The size of the bubble is also double coded, representing the overall traffic in this certain airport. 

Change in time is represented by the animation, which have a transition in place to make visualizing the change much easier. 

Overall, the entire visualization remain cocktail, with an animation/narrative in the beginning but users are able to direct themselves back to any certain year to access detailed data. 

###Feedback 

The feedback to this visualization is that the connection is simply not clear enough and there are still too much information (User 1). All of the users tested are confused about what I am trying to show despite having all the encodings (User 1, 2). So I redid the graph again to a simplier version. 

##Draft 3 (Final Draft)

The final draft of my project is another dual-y-axis graph with a author centered narrative, instead of a cocktail one. The goal of this graph is just to show that the 2008 crisis reduced airport delay significantly, that's it. So it is much simplier than previous versions. 

The time is encoded on the x axis. The delay percentage is encoded on the y axis on the left because it is the most important information. The GDP growth is encoded on the y axies on the right as secondary information. 

There are four trend lines accorss the graph to display information. The steelblue opaque line represent actual delay changes within the duration, but becuase it is too volatile and difficult to identify actual trends, I have also added a line represent the annual mean of the trend, coded in solid steelblue. The solid red line represent GDP changes in all those years by quarter, while the dashed horizontal line represent the natural rate of growth of GDP to aid reader understanding. 

There is also another verical black line illustrating the start of the financial recession of 2007-2008 to further aid reader understanding. Finally, I understand that both Y axis has uneven scales, but after user testing this is the best way to aid understanding without crowding all the lines together. As a compensation, I coded everything related to delay steelblue and everything related to GDP red. 

###Final Feedback and Adjustments

User 1 suggested adding more labels on the graph, which led to the adding of the two trend lines to aid further understanding

User 2 suggested seperating the red and steelblue line (they used to be together) for clearer comparison

User 3 suggested having a unified color for trendline label, and axis representing both GDP and flight delays for more clear understanding. 

Per Pervious Review, An tooltip was added to enable interaction with users. The labels were changed and two footnotes were added to clearify some confusing variables. 

##Resources

D3 API
http://www.multpl.com/us-gdp-growth-rate/table/by-quarter
http://www.transtats.bts.gov/OT_Delay/OT_DelayCause1.asp


