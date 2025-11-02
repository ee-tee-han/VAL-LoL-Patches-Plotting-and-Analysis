import pandas as pd
import re
import matplotlib.pyplot as plt
import statistics
import numpy as np
from scipy.stats import pearsonr
#==================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
#cleaning valpatch.csv

input_filename = 'valpatch.csv'
output_filename = 'valpatch1.csv'

#"on_bad_lines='skip'" skips lines with errors
df = pd.read_csv(input_filename, on_bad_lines="skip")
df.drop(df.head(3).index, inplace=True) # drops first 3 lines
df.drop(df.index[97:125], inplace=True) # drops lines 97-125
df.to_csv(output_filename, index=False)
print(df)

file_valpatch = open("valpatch1.csv", "r")
data = file_valpatch.readlines()
file_valpatch.close()
print(data)

total_items = 0
for item in data:
    total_items +=1
print(total_items)
counter = 0

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
#finding the frequency
month_counts = {month: [0] * 5 for month in months} # [0] * 5 creates lists containing 5 zeros, and curly brackets store them into a dictionary

for year in range(2020, 2025): #iterates through each year
    for item in data: #iterates through data
        for month in months: #iterates through each month and searches for the number of occurences happening that year (index 0-5)
            pattern = re.compile(rf'{month}\s+\d{{1,2}}(st|nd|rd|th)?,?\s+{year}', re.IGNORECASE) # compile creates a separate function to call back to using pattern.search
            # "?" makes it optional, {1,2} allows for 1 or 2 digit dates and (st|nd|rd|th) for suffixes
            if pattern.search(item): #if that item is found, the list is incremented by 1
                month_counts[month][year - 2020] += 1 # in month ___ in year ___ 1 is added)
                print(f"Match found in: {item}")
                counter +=1
                
#this loop goes through the range of 2020 - 2025 and for every item in data, for the index and every month, it searches for the month selected and the year - and if it it found, the counter will be incrememnted by one.
                #month_counts[months][year-2020] += 1 gets the index for the month (eg jan = 0) and the year - 2020 (that specific year) and increments it by 1.


list_timeline = []
#the goal of the code is to sort all of the items into chronological order
#the index position (0) of an item within counts, a separate item within the dictionary of month_counts, is found, and the item (month_frequency) is appended to the list.
#the index now at (0),  will prompt the system to find the 1st frequency for each month in 2020
#the index now at (1), which will prompt the system to find the second frequency for each month in 2021
for index in range(5):
    month_frequency = [counts[index] for month, counts in month_counts.items()] 
    for item in month_frequency:
        list_timeline.append(item)
print('Overall occurrences:')
print(f'Total: {counter} occurrences')
print('Month-wise occurrences:')
for month, counts in month_counts.items():
    print(f'{month}: {counts} occurrences')
timeline = ["Jan 2020", "Feb 2020", "Mar 2020", "Apr 2020", "May 2020", "Jun 2020", "Jul 2020", "Aug 2020", "Sep 2020", "Oct 2020", "Nov 2020", "Dec 2020","Jan 2021", "Feb 2021", "Mar 2021", "Apr 2021", "May 2021", "Jun 2021", "Jul 2021", "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022", "Feb 2022", "Mar 2022", "Apr 2022", "May 2022", "Jun 2022", "Jul 2022", "Aug 2022", "Sep 2022", "Oct 2022", "Nov 2022", "Dec 2022","Jan 2023", "Feb 2023", "Mar 2023", "Apr 2023", "May 2023", "Jun 2023", "Jul 2023", "Aug 2023", "Sep 2023", "Oct 2023", "Nov 2023", "Dec 2023","Jan 2024", "Feb 2024", "Mar 2024", "Apr 2024", "May 2024", "Jun 2024", "Jul 2024", "Aug 2024", "Sep 2024", "Oct 2024", "Nov 2024", "Dec 2024"]
cleaned_timeline = timeline[5:-11] # there are extra months in here that the playerbase data does not have
cleanedfrequencies_permonth = list_timeline[5:-11]
#print(cleaned_timeline, "\n", list_timeline)

#==================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
#Graphing the timeline and patches
datetime_timeline = pd.to_datetime(cleaned_timeline, format="%b %Y")#converts the cleaned timeline to datetime format of month and year (eg: Jan 2020 -> 

plt.plot(datetime_timeline, cleanedfrequencies_permonth)
plt.legend(["Number of Patches"])
plt.xlabel("Date")
plt.ylabel("Frequency/Player Count")
plt.title("Frequency of Patches per Month Affects Growth of Playerbase")
plt.show()

#==================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
#Cleaning valpop.csv
input_filename = 'valpop.csv'
output_filename = 'valpop1.csv'

df = pd.read_csv(input_filename, on_bad_lines='skip')
df = df[["Date", "Players Count"]]
df["Players Count"] = pd.to_numeric(df["Players Count"].str.replace(",", ""), errors="coerce") #converts all the string numbers to integers.
print(df)
df['Date'] = pd.to_datetime(df['Date'], format="%b-%y") #converts the column of date to a date-time format.
df.to_csv(output_filename, index=False)


#==================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
#Graphing all data
fig, axis1 = plt.subplots()

axis1.plot(df["Date"], df["Players Count"], color="blue", label="Players Count")
axis1.set_xlabel("Date")
axis1.set_ylabel("Players Count", color="blue")
axis1.tick_params("y", colors="blue") #makes the indicators blue on the y axis

axis2 = axis1.twinx() # creates a second y axis on the right
axis2.plot(datetime_timeline, cleanedfrequencies_permonth, color="red", label="Number of Patches")
axis2.set_ylabel("Number of Patches", color="red")
axis2.tick_params("y", colors="red") #makes the indicators red on the y axis

plt.title("Frequency of Patches per Month Affects Growth of Val Playerbase (2020-2024)")
plt.show()
#==================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
#Analysis
#finding the mean, median and mode for patches

#mean of frequencies per month
average_frequency = statistics.mean(cleanedfrequencies_permonth)
print("Average Frequency =", average_frequency)

#median of frequencies per month
cleanedfrequencies_permonth.sort()
if len(cleanedfrequencies_permonth) % 2 == 0: #if even
    middlePlusOne = len(cleanedfrequencies_permonth) // 2
    median = (cleanedfrequencies_permonth[middlePlusOne -1] + cleanedfrequencies_permonth[middlePlusOne]) /2
else:
    middle = len(cleanedfrequencies_permonth) // 2 #when odd
    median = cleanedfrequencies_permonth[middle]
print("Median Frequency = ", median)

#mode of frequencies per month
frequency_mode = statistics.mode(cleanedfrequencies_permonth)
print("Most frequent frequency per month = ", frequency_mode)

#player counts

#mean of player counts
average_playercount = statistics.mean(df["Players Count"])
print("Average Player count =", average_playercount)

#median of player counts
df["Players Count"] = df["Players Count"].sort_values()
if len(df["Players Count"]) % 2 == 0:
    middlePlusOne = len(df["Players Count"]) // 2
    median = (df["Players Count"][middlePlusOne -1] + df["Players Count"][middlePlusOne]) /2
else:
    middle = len(df["Players Count"]) // 2
    median = df["Players Count"][middle]
print("Median Player Count = ", median)

#mode of player counts
frequency_playercount = statistics.mode(df["Players Count"])
print("Most frequent player count = ", frequency_playercount)

#correlation coefficient
corr_coeffval1 = np.corrcoef(cleanedfrequencies_permonth, df["Players Count"])[0, 1]
print(f"Correlation Coefficient: {corr_coeffval1}")

std_player_count = df["Players Count"].std()
covariance = np.cov(cleanedfrequencies_permonth, df["Players Count"])[0, 1]
corr_coeffval2 = covariance / (np.std(cleanedfrequencies_permonth) * std_player_count)
print(f"Correlation Coefficient: {corr_coeffval2}")

corr_coeffval3, _ = pearsonr(df["Players Count"], cleanedfrequencies_permonth)
print(f"Correlation Coefficient: {corr_coeffval3}")

corr_coeffvalaverage = (corr_coeffval1+corr_coeffval2+corr_coeffval3)/3
print("The average correlation coefficient for valorant is:", corr_coeffvalaverage)
#Conclusion, in large scale, it has little, if not negative, correlation to the player growth, however, visually there are some spikes in player growth that could correspond to the frequency of patches.
#==================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
#league of legends comparison
#==================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
#cleaning lolpatch.csv

input_filename = 'lolpatch.csv'
output_filename = 'lolpatch1.csv'

df = pd.read_csv(input_filename, on_bad_lines='skip')
df = df[["Release Date", "Patch"]]
df.to_csv(output_filename, index=False)
print(df)
counter = 0

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
#finding the frequency
month_counts = {month: [0] * 5 for month in months} # [0] * 5 creates lists containing 5 zeros, and curly brackets store them into a dictionary

for year in range(2020, 2025): #iterates through each year
    for item in df["Release Date"]: #iterates through data
        for month in months: #iterates through each month and searches for the number of occurences happening that year (index 0-5)
            pattern = re.compile(fr'{month}\s+\d{{1,2}}(st|nd|rd|th)?,?\s+{year}', re.IGNORECASE) # compile creates a separate function to call back to using pattern.search
            # "?" makes it optional, {1,2} allows for 1 or 2 digit dates and (st|nd|rd|th) for suffixes
            if pattern.search(item): #if that item is found, the list is incremented by 1
                month_counts[month][year - 2020] += 1 # in month ___ in year ___ 1 is added)
                print(f"Match found in: {item}")
                
#this loop goes through the range of 2020 - 2025 and for every item in data, for the index and every month, it searches for the month selected and the year - and if it it found, the counter will be incrememnted by one.
                #month_counts[months][year-2020] += 1 gets the index for the month (eg jan = 0) and the year - 2020 (that specific year) and increments it by 1.


list_timeline = []
#the goal of the code is to sort all of the items into chronological order
#the index position (0) of an item within counts, a separate item within the dictionary of month_counts, is found, and the item (month_frequency) is appended to the list.
#the index now at (0),  will prompt the system to find the 1st frequency for each month in 2020
#the index now at (1), which will prompt the system to find the second frequency for each month in 2021
for index in range(5):
    month_frequency = [counts[index] for month, counts in month_counts.items()] 
    for item in month_frequency:
        list_timeline.append(item)
print('Overall occurrences:')
print(f'Total: {counter} occurrences')
print('Month-wise occurrences:')
for month, counts in month_counts.items():
    print(f'{month}: {counts} occurrences')
timeline = ["Jan 2020", "Feb 2020", "Mar 2020", "Apr 2020", "May 2020", "Jun 2020", "Jul 2020", "Aug 2020", "Sep 2020", "Oct 2020", "Nov 2020", "Dec 2020","Jan 2021", "Feb 2021", "Mar 2021", "Apr 2021", "May 2021", "Jun 2021", "Jul 2021", "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022", "Feb 2022", "Mar 2022", "Apr 2022", "May 2022", "Jun 2022", "Jul 2022", "Aug 2022", "Sep 2022", "Oct 2022", "Nov 2022", "Dec 2022","Jan 2023", "Feb 2023", "Mar 2023", "Apr 2023", "May 2023", "Jun 2023", "Jul 2023", "Aug 2023", "Sep 2023", "Oct 2023", "Nov 2023", "Dec 2023","Jan 2024", "Feb 2024", "Mar 2024", "Apr 2024", "May 2024", "Jun 2024", "Jul 2024", "Aug 2024", "Sep 2024", "Oct 2024", "Nov 2024", "Dec 2024"]
cleaned_timeline = timeline[3:-11] # there are extra months in here that the playerbase data does not have
cleanedfrequencies_permonth = list_timeline[3:-11]
print(cleanedfrequencies_permonth)
for item in cleanedfrequencies_permonth:
    counter +=1


#==================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
#Graphing the timeline and patches
df['Release Date'] = pd.to_datetime(df['Release Date'], format="%B %d, %Y")
datetime_timeline = pd.to_datetime(cleaned_timeline, format="%b %Y")#converts the cleaned timeline to datetime format of month and year (eg: Jan 2020 -> 

plt.plot(datetime_timeline, cleanedfrequencies_permonth)
plt.legend(["Number of Patches"])
plt.xlabel("Date")
plt.ylabel("Frequency/Player Count")
plt.title("Frequency of Patches per Month Affects Growth of Playerbase")
plt.show()

#==================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
#Cleaning lolpop.csv
input_filename = 'lolpop.csv'
output_filename = 'lolpop1.csv'
counter = 0
df = pd.read_csv(input_filename, on_bad_lines='skip')
df = df[["Month", "Average Monthly Players"]]
df["Average Monthly Players"] = pd.to_numeric(df["Average Monthly Players"].str.replace(",", ""), errors="coerce") #converts all the string numbers to integers.
print(df)
df["Month"] = pd.to_datetime(df['Month'], format="%b-%y", errors='coerce') #converts the column of date to a date-time format.
df.to_csv(output_filename, index=False)
df["Month"] = df["Month"][:-2]
df["Average Monthly Players"] = df["Average Monthly Players"][:-2]
for item in df["Average Monthly Players"]:
    counter+=1

#==================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
#Graphing all data
fig, axis1 = plt.subplots()

axis1.plot(df['Month'], df["Average Monthly Players"], color="blue", label="Average Monthly Players")
axis1.set_xlabel("Month")
axis1.set_ylabel("Average Monthly Players", color="blue")
axis1.tick_params("y", colors="blue") #makes the indicators blue on the y axis

axis2 = axis1.twinx() # creates a second y axis on the right
axis2.plot(datetime_timeline, cleanedfrequencies_permonth, color="red", label="Number of Patches")
axis2.set_ylabel("Number of Patches", color="red")
axis2.tick_params("y", colors="red") #makes the indicators red on the y axis

plt.title("Frequency of Patches per Month Affects Growth of LoL Playerbase (2020-2024")
plt.show()
#==================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
#Analysis
#finding the mean, median and mode for patches
average_frequency = statistics.mean(cleanedfrequencies_permonth)
print("Average Frequency =", average_frequency)
cleanedfrequencies_permonth.sort()
if len(cleanedfrequencies_permonth) % 2 == 0: #if even
    middlePlusOne = len(cleanedfrequencies_permonth) // 2
    median = (cleanedfrequencies_permonth[middlePlusOne -1] + cleanedfrequencies_permonth[middlePlusOne]) /2
else:
    middle = len(cleanedfrequencies_permonth) // 2 #when odd
    median = cleanedfrequencies_permonth[middle]
print("Median Frequency = ", median)

frequency_mode = statistics.mode(cleanedfrequencies_permonth)
print("Most frequent frequency per month = ", frequency_mode)

#player count
average_playercount = statistics.mean(df["Average Monthly Players"])
print("Average Player count =", average_playercount)
df["Average Monthly Players"] = df["Average Monthly Players"].sort_values()
if len(df["Average Monthly Players"]) % 2 == 0:
    middlePlusOne = len(df["Average Monthly Players"]) // 2
    median = (df["Average Monthly Players"][middlePlusOne -1] + df["Average Monthly Players"][middlePlusOne]) /2
else:
    middle = len(df["Average Monthly Players"]) // 2
    median = df["Average Monthly Players"][middle]
print("Median Player Count = ", median)
frequency_playercount = statistics.mode(df["Average Monthly Players"])
print("Most frequent player count = ", frequency_playercount)

#correlation coefficient
print(df["Average Monthly Players"])
df = df.dropna()
corr_coefflol1 = np.corrcoef(cleanedfrequencies_permonth, df["Average Monthly Players"])[0, 1]
print(f"Correlation Coefficient: {corr_coefflol1}")

std_player_count = df["Average Monthly Players"].std()
covariance = np.cov(cleanedfrequencies_permonth, df["Average Monthly Players"])[0, 1]
corr_coefflol2 = covariance / (np.std(cleanedfrequencies_permonth) * std_player_count)
print(f"Correlation Coefficient: {corr_coefflol2}")

corr_coefflol3, _ = pearsonr(df["Average Monthly Players"], cleanedfrequencies_permonth)
print(f"Correlation Coefficient: {corr_coefflol3}")
#Conclusion, comparing the correlation coefficient seen between the Average Monthly Players and Frequency of Patches per month for League Of Legends and Valorant, we can see there is a negative correlation.

corr_coefflolaverage = (corr_coefflol1+corr_coefflol2+corr_coefflol3)/3
print("The average of the league of legends correlation coefficients is :", corr_coefflolaverage)

#comparison
corr_coefflolvalaverage = (corr_coefflolaverage+corr_coeffvalaverage)/2
print("Comparing the two coefficients, we see there is no positive correlation between the two variables (", corr_coefflolaverage, corr_coeffvalaverage, "average =", corr_coefflolvalaverage, ") and there seems to even be a negative correlation between them.")






















'''plt.plot(datetime_timeline, list_timeline)
plt.legend(["Number of Patches"])
plt.xlabel("Date")
plt.ylabel("Frequency/Player Count")
plt.title("Frequency of Patches per Month Affects Growth of Playerbase")
plt.plot(df["Players Count"])
plt.show()

df.to_csv(output_filename, index=False)
plt.plot(df)
plt.show()'''

'''for month, counts in month_counts.items():
    plt.bar(month, counts)
    print(f'{month}: {counts} occurrences')'''
'''while counter < 48:
    for counts in month_counts.items():
        list_timeline.append(counts[0])
    counter +=1
    index+=1'''
'''for month, counts in month_counts.items():
    plt.bar([f'{month} - {year}' for year in range(2020, 2025)], counts, label=month)

plt.xlabel('Year')
plt.ylabel('Occurrences')
plt.title('Monthly Occurrences Over 5 Years')
plt.legend()
plt.show()'''

'''matpat.legend(months)
'''


'''years = ["2020", "2021", "2022", "2023", "2024"]
for item in data:
    for i, month in enumerate(months): #enumerate gets both the index and the month during the loop
        if re.search(fr'{month}\s+\d{{1,2}}(st|nd|rd|th)?,?\s+2020', item, re.IGNORECASE):
            counter += 1
            april_2020 += 1
            month_counts[i] += 1
            print(f'Match found in: {item}')

print(f'April 2020 occurrences: {april_2020}')
print('Month-wise occurrences:')
for month, count in zip(months, month_counts): #iterates over both month_counts and months simultaneously
    print(f'{month}: {count} occurrences')
'''
'''for item in data:
    if re.search(r'{for month in months}\s+\d{1,2}(st|nd|rd|th)?,?\s+2020', item, re.IGNORECASE): # "?" makes it optional, {1,2} allows for 1 or 2 digit dates and (st|nd|rd|th) for suffixes
            counter += 1
            index = months.index[month]
            month_counts.append(counter)

            
            print(f'Match found in: {item}')
print(month_counts)'''
'''for item in data:
    for i, month in enumerate(months):
        if re.search(fr'{month}\s+\d{{1,2}}(st|nd|rd|th)?,?\s+2020', item, re.IGNORECASE):
            counter += 1
            april_2020 += 1
            month_counts[i] += 1
            print(f'Match found in: {item}')'''
'''for item in data:
    if re.search(r'April\s+\d{1,2}(st|nd|rd|th)?,?\s+2020', item): # "?" makes it optional, {1,2} allows for 1 or 2 digit dates and (st|nd|rd|th) for suffixes
        april_2020 += 1
        print(f'Match found in: {item}')
    if re.search(r'May\s+\d{1,2}(st|nd|rd|th)?,?\s+2020', item): # "?" makes it optional, {1,2} allows for 1 or 2 digit dates and (st|nd|rd|th) for suffixes
        april_2020 += 1
        print(f'Match found in: {item}')'''







'''while counter < total_items:
    for item in data:
        if re.search('April', item):
            april_2020 += 1
            print(april_2020, "yes")
            counter += 1
        else:
            counter += 1'''
#        if "April" and "2020" in item:
#            april_2020 += 1











#df = pd.read_csv(input_filename, quotechar='"')

# Replace non-alphanumeric characters in the entire DataFrame
#df = df.replace(to_replace=r'[^a-zA-Z0-9 ]', value='', regex=True)
'''df = pd.read_csv(input_filename, error_bad_lines=False)

condition = df['Estimated patch release time'] == '14:00-18:00 UTC'
df_filtered = df[~condition]
df_filtered.to_csv(output_filename, index=False)
print(df)'''
'''for item in patch_list:
    if item == "Act 1":
        index1 = patch_list.index(item)
        patch_list.pop(index1)
        print(index1)'''

#patch_list = [item.replace("\n", "") for item in patch_list]
#patch_list = data.split("\n")
#patch_list = data.split('"')
'''print(patch_list)
file_newvalpatch = open("valpatch1.csv", "w")
for item in patch_list:
    file_newvalpatch.write(str(item) + ",") # this ignores the square brackets
file_newvalpatch.close()
'''
#act 1, items are shifted to the right

#patch_list = split("\n")
#goal - remove Stage, Reguib, Affected shards, estimated patch release time
#remove index 2 and 3
#add how many times a patch appears per month - create a code that can be used for other docs
'''counter = 0
for item in patch_list:
    if item == "v Â· d Â· eVALORANT":
        index1 = patch_list.index(item) 
        print(index1)
counter = index1
while counter <=4:
    patch_list.pop(counter)
    counter +=1
print(patch_list)
item_amount = 0
for item in patch_list:
    item_amount +=1
print(item_amount)

for item in patch_list:
    if item == "v Â· d Â· eVALORANT":
        index1 = patch_list.index(item) 
        print(index1)
counter = index1
while counter <= item_amount:
    patch_list.pop(counter)
    counter +=1
    if counter == 235:
        break
print(patch_list)'''
'''for item in patch_list:
    counter +=1
    if item == "Stage" or "Region" or "Affected shards" or "Estimated patch release time" or "Stage 1" or "Stage 2" or "Stage 3" or "Americas" or "APAC" or "Asia" or "Europe" or "Brazil" or "EMEA" or "14:00-18:00 UTC" or "21:00-23:00 UTC" or "02:00-05:00 UTC":
        patch_list.remove(item)
print(counter)
print(patch_list)'''
#valpatch_df = pd.read_csv("valpatch.csv", on_bad_lines='warn') #encoding = "latin-1")
'''print("Nr. rows", len(valpatch_df))
print("Shape (rows, cols)", valpatch_df.shape)
'''
