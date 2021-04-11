import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'Nyc': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    # This function interacts with the user and asks for the required user entries. The values are used to filter the data.

    print('\n--- Hello! Let\'s explore some US bikeshare data! ---')
    print('\nWhich city would you like to explore? \nThis database has data from: Chicago, New York City and Washington.')
    city=input("\nPlease enter the name of the city. (For New York City please write NYC): ").lower().title()
    while city not in {'Chicago', 'Nyc', 'Washington'}:
        print('Sorry. Your input doesn\'t match the aforementioned cities.\nTry again.')
        city=input('\nPlease enter: Chicago, NYC (for New York City) or Washington\nYour choice: ').lower().title()
    else:
        print('\nThank you! The city you would like to explore is {}.\n'.format(city))

    x = input('Do you want to filter the data by month, day or not at all? (type month, day or non): ').lower().title()
    while x not in {'Month', 'Day', 'Non'}:
        print('Sorry. Your input doesn\'t match the mentioned criteria (month,day,non) .\nTry again.')
        x = input('Do you want to filter the data by month, day or not at all? (type month, day or non): ')
    else:
        print('\nYou have chosen [ {} ].\n'.format(x))

    if x in {'month', 'Month', 'MONTH'}:
        print('Please enter a month that you would like to filter by.\nPlease follow this scheme:')
        print('January = 1, February = 2, March = 3, April = 4, May = 5, June = 6 ... December = 12')
        month_dic={1: 'january', 2: 'febuary', 3: 'march', 4: 'april', 5: 'may', 6: 'june', 7: 'july', 8: 'august', 9: 'september', 10: 'october', 11: 'november', 12: 'december'}
        month=int(input('Please enter the number here: '))
        while month > 12 or month == 0:
            print('Your input {} is invalid. Please try again.'.format(month))
            month=int(input('Please enter a number from 1 to 12 for the corresponding month: '))
        else:
            print('Thank you. You have chosen {}.\nLets move on.'.format(month_dic[month].capitalize()))
        day=0
    elif x in {'day', 'Day', 'DAY'}:
        print('Please enter a day following this scheme:\n1= Monday, 2= Tuesday, 3= Wednesday, 4= Thursday, 5= Friday, 6= Saturday, 7= Sunday')
        weekday_dic={1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
        day=int(input('Please enter the number for the day of the week: '))
        while day > 7 or day == 0:
            print('Your input {} is invalid. Please try again.'.format(day))
            day=int(input('Please enter the number for the day of the week: '))
        else:
            print('Thank you. You have chosen {}.'.format(weekday_dic[day]))
        month=0
    else:
        print('Ok, so you dont want any filter.')
        month=0
        day=0

    return(city,month,day)
    print('-'*40)

def load_data(city, month, day):
    # This function loads the file for the selected city and filters for the values entered by the user. It also generates the variable x which is used in time_stats.

    # Loads the file based on the filter
    df=pd.read_csv(CITY_DATA[city])

    # Converts the Start time to datetime
    df['Start Time']=pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # Filters for the value passed on by the user
    if month != 0:
        df_m = df[df['month'] == month]
        df=df_m
        x = 'Month'

    if day != 0:
        weekday_dic={1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
        day=weekday_dic[day]
        df_d = df[df['day_of_week'] == day.title()]
        df=df_d
        x = 'Day'

    if month == 0 and day == 0:
        df=df
        x = 'Non'

    return df, x



def time_stats(df, x, city, month, day):
    # This function calculates the statistics based on the dataframe which is generated above.

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if x == 'Month':
        # This condition is met when a month is selected
        month_dic={1: 'January', 2: 'Febuary', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
        print('Here are the statistics for the year: 2017, month: {}, city: {}:'.format(month_dic[month], city))
        popular_dow=df['day_of_week'].mode()
        print('WEEKDAY: The most common day of the week was: {}.'.format(popular_dow[0]))
        common_hour=df['Start Time'].dt.hour.mode()
        print('HOUR: The most common starting hour was: {}:00.'.format(common_hour[0]))

    elif x == 'Day':
        weekday_dic={1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
        day=weekday_dic[day]
        print('Here are the statistics for the weekday: {}, year: 2017, city: {}:'.format(day, city))
        common_hour=df['Start Time'].dt.hour.mode()
        print('HOUR: The most common starting hour was: {}:00.'.format(common_hour[0]))

    elif x == 'Non':
        print('Here are the statistics for the year: 2017, city: {}:'.format(city))
        popular_month=df['month'].mode()
        month_dic={1: 'January', 2: 'Febuary', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
        print('\nMONTH: The most popular month in 2017 was: {}.'.format(month_dic[popular_month[0]]))
        popular_dow=df['day_of_week'].mode()
        print('WEEKDAY: The most common day of the week was: {}.'.format(popular_dow[0]))
        common_hour=df['Start Time'].dt.hour.mode()
        print('HOUR: The most common starting hour was: {}:00.'.format(common_hour[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, x, city, month, day):
    # This function calculates the statistics concerning the stations.

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    if x == 'Month':
        most_used=df['Start Station'].mode()
        print('START STATION: the most used station was: {}'.format(most_used[0]))
        most_used_es=df['End Station'].mode()
        print('END STATION: The most commonly used end station was: {}'.format(most_used_es[0]))
        fre_com=df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False)
        print('COMBINATION: The most frequent combination of Start and End station was: {} and {}'.format(fre_com.index[0][0],fre_com.index[0][1]))

    elif x == 'Day':
        most_used=df['Start Station'].mode()
        print('START STATION: the most used station was: {}'.format(most_used[0]))
        most_used_es=df['End Station'].mode()
        print('END STATION: The most commonly used end station was: {}'.format(most_used_es[0]))
        fre_com=df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False)
        print('COMBINATION: The most frequent combination of Start and End station was: {} and {}'.format(fre_com.index[0][0],fre_com.index[0][1]))

    elif x == 'Non':
        most_used=df['Start Station'].mode()
        print('START STATION: The most commonly used start station was: {}'.format(most_used[0]))
        most_used_es=df['End Station'].mode()
        print('END STATION: The most commonly used end station was: {}'.format(most_used_es[0]))
        fre_com=df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False)
        print('COMBINATION: The most frequent combination of Start and End station was: {} and {}'.format(fre_com.index[0][0],fre_com.index[0][1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    # This function calculates the trip duration.

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['End Time']=pd.to_datetime(df['End Time'])
    df['Total Travetime']=df['End Time']-df['Start Time']
    td=df['Total Travetime'].sum()
    td=td.components
    print('The total travel time was: {} days, {} hours, {} minutes, {} seconds.'.format(td[0],td[1],td[2],td[3]))

    tdm=df['Total Travetime'].mean()
    tdm=tdm.components
    print('The mean travel time was: {} days, {} hours, {} minutes, {} seconds.'.format(tdm[0],tdm[1],tdm[2],tdm[3]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    # Since Washington has no gender and birth year data, the function needs an if condition.

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    count=df['User Type'].value_counts()
    count_nan=df['User Type'].isnull().sum()
    print('Subscribers: {}'.format(count[0]))
    print('Customer: {}'.format(count[1]))
    print('There have been {} unregistered users.'.format(count_nan))

    if 'Gender' in df.columns:
        count_gender=df['Gender'].value_counts()
        no_gen=df['Gender'].isnull().sum()
        print('\nMale User: {}'.format(count_gender[0]))
        print('Female User: {}'.format(count_gender[1]))
        print('There are {} users of which we don\'t have any gender data.'.format(no_gen))
    else:
        print('Ther are no gender data available.')

    if 'Birth Year' in df.columns:
        df['Birth Day_n']=df['Birth Year'].fillna(0)
        recent=df['Birth Day_n'].max().astype(int)
        print('The most recent year of birth was: {}'.format(recent))
        early=df['Birth Year'].min().astype(int)
        print('The earliest year of birth was: {}'.format(early))
        common=df['Birth Year'].mode()
        print('The most common year of birth was: {}'.format(common[0].astype(int)))
    else:
        print('There are no birth year data available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df, x, month, day):
# This function filters for the first 5 rows of raw data. The user is then recurrently asked if he wants to see 5 more rows.
# The 5 lines are only displayed if filter is non (all data). If filter settings are day or month, only the lines that match the filter condition will be displyed.
    start_time = time.time()
    i=4

    choice=input('\nWould you like to see 5 lines of raw data? (enter yes / no):\n').lower()
    while choice.lower() == 'yes':

        if x == 'Month':
            print('\nCalculating raw data...\n')
            month_dic={1: 'January', 2: 'Febuary', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
            print('Here is the result for the rows that contain data for {} :\n'.format(month_dic[month]))
            print(df.loc[0:i,:])
            choice=input('\nWould you like to see the result for the next 5 rows? (enter yes / no):\n').lower()
            while choice not in {'yes', 'no'}:
                print('Invalid entry. Try again.')
                choice=input('\nWould you like to see the result for the next 5 rows? (enter yes / no:\n').lower()
            else:
                if choice == 'yes':
                    i += 5

        if x == 'Day':
            print('\nCalculating raw data...\n')
            weekday_dic={1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
            print('Here is the result for the rows that contain data for {} :\n'.format(weekday_dic[day]))
            print(df.loc[0:i,:])
            choice=input('\nWould you like to see the result for the next 5 rows? (enter yes / no):\n').lower()
            while choice not in {'yes', 'no'}:
                print('Invalid entry. Try again.')
                choice=input('\nWould you like to see the result for the next 5 rows? (enter yes / no:\n').lower()
            else:
                if choice == 'yes':
                    i += 5

        if x == 'Non':
            print('\nCalculating raw data...\n')
            print('Here are the first 5 rows of the raw data:\n')
            print(df.loc[0:i,:])
            choice=input('\nWould you like to see the next 5 rows? (enter yes / no):\n').lower()
            while choice not in {'yes', 'no'}:
                print('Invalid entry. Try again.')
                choice=input('\nWould you like to see the next 5 rows? (enter yes / no:\n').lower()
            else:
                if choice == 'yes':
                    i += 5

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():

    while True:
        city, month, day = get_filters()
        df, x = load_data(city, month, day)

        time_stats(df, x, city, month, day)
        station_stats(df, x, city, month, day)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df, x, month, day)

        restart = input('\nWould you like to restart? (enter yes / no):\n')
        if restart.lower() != 'yes':
            print('\nGood Bye!\n')
            break


if __name__ == "__main__":
	main()
