=========
Partners:
=========
Xingyu Wang xw2303
Muyuan Liu ml3569

===============
Submitted Files
===============
./proj3/
./proj3/ddl_inspection.sql
./proj3/INTEGRATED-DATASET
./proj3/apriori.py
./proj3/ddl_parking.sql
./proj3/example-run.txt
./proj3/export.sql
./proj3/README.md

==================
Dataset Selection:
==================
We use two datasets to get an integrated dataset. One dataset is the Restaurant Inspection Results and the other is Parking Facilities.

===========================
High Level Data Preprocess:
===========================
For the Restaurant Inspection Results dataset, each violation of a restaurant will result in a row. Key fields include the cuisine code, inspection date, violation code, current grade, zipcode and action code. One inspection may have multiple corresponding rows. To handle this problem, we group the dataset by inspection date and concatenate the violation code at one inspection. In addition, we remove the address and restaurant name in the dataset because these two fields are not likely to reach the minimun support rate. We only consider the inspection data over 2013 due to the data volume. Around 75000 records will be generated in the first dataset. Note that some of the features have very long descriptions and we use its code instead in mining association rules.
For the Parking Facilities, one record is corresponded to one parklot, including its License Number, Entity Name, Trade Name, Address Zip Code, Telephone Number and	Number of Spaces. We only sconsider the total number of spaces within a region which has the same zipcode.
To join the dataset, we use the zipcode of restaurant and parklot as the join filed. Since the total number of spaces are integers, if we use these numbers as items, it is unlikely to get interesting rules. So we classify them into five categories according to the percentile statistics, accordingly PARK_SPACE='Very High','High','Medium','Low' and 'Very Low'. The same trick is used to classify the total number of restaurants and average inspection score (the lower the better) within the same region.
The operations illustrated above involves loading data into Mysql database and outputing csv file as the input of association rules. Related import and export scripts are also submitted.

==============================
Reason of choosing the dataset
==============================
Recently one of the restaurant near the school was closed. We explore the relation between the violations and restaurant inspection grade to see if there is any correaltion between violation rules or geological locations and how the restaurant will react to these violations. In addition, one related information about the restaurant is the parking spaces nearby. We want to verify that if one region has many parking lots, it tends to have lots of restaurants.
To reconstruct the dataset, Mysql is needed to run  ddl_inspection.sql, ddl_parking.sql and export.sql. Before running ddl_parking.sql, csv file should be prepocessed and remove address and entity name column. Each record should occupy one line. Before running the ddl_inspection.sql, four csvs need to be downloaded from Restaurant Inspection Results dataset.

==============
Run Directions
==============
The apriori.py takes three mandatory parameters csv_file, min_support, min_confidence and one optional parameter max_confidence.
python apriori.py <csv_file> <min_support> <min_confidence> [max_confidence]

e.g: python apriori.py INTEGRATED-DATASET 0.05 0.7 1

==================
Interesting Rules:
==================
We set the minimum support rate to 0.05 and the minimum confidence rate 0.7. Some of the interesting rules are listed below.
1.[ACTIONCODE=D] => [GRADE=A] (Conf: 96.1106803249%, Supp: 37%)
[GRADE=A] => [ACTIONCODE=D] (Conf: 91.7020365251%, Supp: 37%)
This rule indicates that if a restaurant is required to take action D after the violation, it is still likely to get the grade A in the inspection. From the description we can know that the actioncode D denotes 'Violations were cited in the following area(s)', which seems not so severe.

2.[VIOCODE=02G,ACTIONCODE=D] => [GRADE=A] (Conf: 99.8678646934%, Supp: 5%)
[VIOCODE=06D,ACTIONCODE=D] => [GRADE=A] (Conf: 99.5673076923%, Supp: 6%)
[VIOCODE=08A,ACTIONCODE=D] => [GRADE=A] (Conf: 98.7688864018%, Supp: 5%)
These rules are between the violation code and grade of one inspection. The violation code 08A denotes 'Facility not vermin proof. Harborage or conditions conducive to attracting vermin to the premises and/or allowing vermin to exist'. The violation code 06D denotes 'Personal cleanliness inadequate. Outer garment soiled with possible contaminant.  Effective hair restraint not worn in an area where food is prepared'. It seems that these rules are usually violated by the restaurant and are not that critical.

3.[GRADE=B] => [ACTIONCODE=U] (Conf: 93.4927606963%, Supp: 9%)
This rule indicates that for a restaurant whose grade is B, it is likely to be required to take action 'U'. However, the description of actioncode 'U' and 'D' is actually the same. We can get the sense that even the description is the same, the action 'U' seems more severe than the action 'D'.

4.[PARK_SPACE=Very High] => [RESTAURANT_VOLUME=Very High] (Conf: 88.3672039243%, Supp: 31%)
This rule shows that if the parking slots in a region is really large, it is likely that there are many restaurants in this region. This rule is expected and reasonable.

5.[VIOCODE=10F,VIOCODE=04L] => [VIOCODE=08A] (Conf: 84.2354053415%, Supp: 5%)
[VIOCODE=04L] => [VIOCODE=08A] (Conf: 79.8218612876%, Supp: 19%)
This rule indicates the correalation between several violations. The violation code 10F denotes Non-food contact surface improperly constructed. Unacceptable material used. Non-food contact surface or equipment improperly maintained and/or not properly sealed, raised, spaced or movable to allow accessibility for cleaning on all sides, above and underneath the unit. 04L denotes Evidence of mice or live mice present in facility's food and/or non-food areas." It is obvious that these three violations are highly related and tend to appear at the same time.

6. If we decrease the support rate, more rules regarding with the cuisine code and grade will be generated. While at the same time, some trivial rules with confidence 100% will also be generated.
