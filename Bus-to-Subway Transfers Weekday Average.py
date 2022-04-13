import pandas as pd

# Read linked trips csv
linked_df = pd.read_csv(r'nyc-travel-surveys-Linkedcsv.csv')

# Print sample of data 
linked_df.head()

# Remove unnecessary columns to speed up runtime
# Filter values are based on the information found in the final report https://new.mta.info/document/28971
columns = ['hhid',
          'personid',
          'tripid',
           'daynum',
           'tripnum',
           'traveldate',
           'traveldate_dow',
           'mode1',
           'mode2',
           'mode3',
           'mode4',
           'mode5',
           'mode6',
           'mode7',
           'mode8',
           'mode9',
           'mode10',
           'modeflag_transit',
           'mode_g5', # == 2 If the trip includes both an NYC Subway leg and an NYC Bus leg 
           'numlegs',
           'num_transit_legs',
           'transit_system_1',
           'transit_system_2',
           'transit_system_3',
           'transit_system_4',
           'transit_system_5',
           'transit_system_6',
           'transit_system_7',
           'transit_system_8',
           'route_id_1',
           'route_id_2',
           'route_id_3',
           'route_id_4',
           'route_id_5',
           'route_id_6',
           'route_id_7',
           'route_id_8',
           'transfer_stop_id_1',
           'transfer_stop_name_1',
           'transfer_stop_id_2',
           'transfer_stop_name_2',
           'transfer_stop_id_3',
           'transfer_stop_name_3',
           'transfer_stop_id_4',
           'transfer_stop_name_4',
           'transfer_stop_id_5',
           'transfer_stop_name_5',
           'transfer_stop_id_6',
           'transfer_stop_name_6',
           'transfer_stop_id_7',
           'transfer_stop_name_7',
           'subway_board_stop_id',
           'subway_board_stop_name',
           'hhsize',
           'per_weight_wd_trips_rsadj',
           'per_weight_sat_rsadj',
           'per_weight_sun_rsadj']

linkedtrips_df = linked_df[columns]

# Filter only by trips during the week and using both bus and subway
weekday = ['Monday','Tuesday','Wednesday','Thursday','Friday']
weekdaytrips = linkedtrips_df[(linkedtrips_df['traveldate_dow'].isin(weekday)) & (linkedtrips_df['mode_g5'] == 'Subway + Bus')]

def checkorder(listofvalues, val1, val2): # Function to check whether value 1 comes before value 2. 0 == False, 1 == True 
    if val1 not in listofvalues or val2 not in listofvalues:
        return 0
    else:
        i = listofvalues.index(val1)
        flag = 0
        if val2 in listofvalues[i:]:
            flag = 1
        return flag        

# Write filtered dataframe to dictionary for iterating
wkdaytrips_dict = weekdaytrips.to_dict('records')

# Run checkorder function on all rows
for row in wkdaytrips_dict:
    # Create the columns list (mode1, mode2, etc.)
    columnstocheck = ['mode' + str(n) for n in range(1,11)]
    tocheck = [row[c] for c in columnstocheck]
    # For every row, indicate whether it was a bus to subway transfer by writing 0 or 1 in a new column
    row['BusToSubwayTransfer'] = checkorder(tocheck, 'NY or MTA Bus','NYC Subway')

# Write the dictionary to a DataFrame
wkdaytransfer_df = pd.DataFrame.from_dict(wkdaytrips_dict)

# Filter trips to only bus to subway transfers
filteredtrips_df = wkdaytransfer_df[wkdaytransfer_df['BusToSubwayTransfer'] == 1]

subwayboardingsfrombus = filteredtrips_df.groupby('subway_board_stop_name')['per_weight_wd_trips_rsadj'].sum()

totalweekday = subwayboardingsfrombus.reset_index()
totalweekday['averageboardings_wkday'] = totalweekday['per_weight_wd_trips_rsadj']/5

outputname = 'Average_Weekday_Boardings_From_Bus_To_Subway.csv'
totalweekday.to_csv(outputname)
