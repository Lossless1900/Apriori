==================
Dataset Selection:
==================
We use two datasets to get an integrated dataset. One dataset is the Restaurant Inspection Results and the other is Parking Facilities.

==================
Data preprocess:
==================
For the Restaurant Inspection Results dataset, each violation of a restaurant will result in a row. Key fields include the cuisine code, inspection date, violation code, current grade, zipcode and action code. One inspection may have multiple corresponding rows. To handle this problem, we group the dataset by inspection date and concatenate the violation code at one inspection. In addition, we remove the address and restaurant name in the dataset because these two fields are not likely to reach the minimun support rate. We only consider the inspection data over 2013 due to the data volume. Around 75000 records will be generated in the first dataset. Note that some of the features have very long descriptions and we use its code instead in mining association rules.
For the Parking Facilities, one record is corresponded to one parklot, including its License Number, Entity Name, Trade Name, Address Zip Code, Telephone Number and	Number of Spaces. We only sconsider the total number of spaces within a region which has the same zipcode.
To join the dataset, we use the zipcode of restaurant and parklot as the join filed. Since the total number of spaces are integers, if we use these numbers as items, it is unlikely to get interesting rules. So we classify them into five categories according to the percentile statistics, accordingly PARK_SPACE='Very High','High','Medium','Low' and 'Very Low'. The same trick is used to classify the total number of restaurants and average inspection score (the lower the better) within the same region.

==================
Interesting Rules:
==================
We set the minimum support rate to 0.05 and the minimum confidence rate 0.6. Some of the interesting rules are listed below.
1. ['ACTIONCODE=D'] => ['GRADE=A']   0.960632427844
['GRADE=A'] => ['ACTIONCODE=D']   0.918464660129
This rule indicates that if a restaurant is required to take action D after the violation, it is still likely to get the grade A in the inspection. From the description we can know that the actioncode D denotes 'Violations were cited in the following area(s)', which seems not so severe.

2.['VIOCODE=08A', 'ACTIONCODE=D'] => ['GRADE=A']   0.987778049377349 
['VIOCODE=06D', 'ACTIONCODE=D'] => ['GRADE=A']   0.995268463279
These two rules are between the violation code and grade of one inspection. The violation code 08A denotes 'Facility not vermin proof. Harborage or conditions conducive to attracting vermin to the premises and/or allowing vermin to exist'. The violation code 06D denotes 'Personal cleanliness inadequate. Outer garment soiled with possible contaminant.  Effective hair restraint not worn in an area where food is prepared'. It seems that these two rule are usually violated by the restaurant and are not that critical.

3.['GRADE=B'] => ['ACTIONCODE=U']  0.936857142857
This rule indicates that for a restaurant whose grade is B, it is likely to be required to take action 'U'. However, the description of actioncode 'U' and 'D' is actually the same. We can get the sense that even the description is the same, the action 'U' seems more severe than the action 'D'.

4.['PARK_SPACE=Very High'] => ['RESTAURANT_VOLUME=Very High']  0.883788164177
This rule shows that if the parking slots in a region is really large, it is likely that there are many restaurants in this region. This rule is expected and reasonable.

5.['VIOCODE=10F', 'VIOCODE=04L'] => ['VIOCODE=08A']   0.842159277504
['VIOCODE=08A'] => frozenset(['VIOCODE=04L'])   0.657733787759
This rule indicates the correalation between several violations. The violation code 10F denotes Non-food contact surface improperly constructed. Unacceptable material used. Non-food contact surface or equipment improperly maintained and/or not properly sealed, raised, spaced or movable to allow accessibility for cleaning on all sides, above and underneath the unit. 04L denotes Evidence of mice or live mice present in facility's food and/or non-food areas." It is obvious that these three violations are highly related and tend to appear at the same time.

6. If we decrease the support rate, more rules regarding with the cuisine code and grade will be generated. While at the same time, some trivial rules with confidence 100% will also be generated.

==================
Run Directions
==================
The apriori.py takes three mandatory parameters csv_file, min_support, min_confidence and one optional parameter max_confidence.
python apriori.py <csv_file> <min_support> <min_confidence> [max_confidence]
