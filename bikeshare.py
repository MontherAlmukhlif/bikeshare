import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('What city do you want to know about? (chicago, new york city, washington): ').lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid city. Please choose from chicago, new york city, or washington.")
    

    # get user input for month (all, january, february, ... , june)

    # List of valid months
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Which month? ("all" to apply no filter, january, february....): ').lower()
        if month in months:
            break
        else:
            print("Invalid month. Please choose from: 'all' to apply no filter, january, february...")


    # get user input for day of week (all, monday, tuesday, ... sunday)

    days = ['all', 'saturday', 'sunday', 'monday', 'tuesday', 'thursday', 'friday','wednesday']

    while True:
        day = input('Which day? ("all" to apply no filter, monday, tuesday, ...): ').lower()
        if day in days:
            break
        else:
            print("Invalid day. Please choose from: 'all', monday, tuesday, ...")


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_week'] = df['Start Time'].dt.day_name()
    df['hours'] = df['Start Time'].dt.hour

    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
       
    if month != 'all':
       num = months.index(month) + 1
       df = df[df['month'] == num]

    if day != 'all':
        df = df[df['day_week'].str.lower() == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if len(df) == 0:
        print("No data for the selected filters.")
    else:
        months = ['january', 'february', 'march', 'april', 'may', 'june',
              'july', 'august', 'september', 'october', 'november', 'december']

        if not df['month'].empty:
            most_common_month_num = df['month'].mode().iloc[0]
            most_common_month = months[most_common_month_num - 1]  
            print("The most common month is: " + most_common_month)

        if not df['day_week'].empty:
            most_common_day = df['day_week'].mode().iloc[0]
            print("the most common day is: " + most_common_day)

        if not df['hours'].empty:
            most_common_hour = df['hours'].mode()[0]
            print("The most common start hour is: " + str(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    if len(df) == 0:
        print("No data for the selected filters.")
    else:
        if 'Start Station' in df and not df['Start Station'].empty:
            print('The most commonly used start station is: ',df['Start Station'].mode()[0])

        if 'End Station' in df and not df['End Station'].empty:
            print('The most commonly used end station is: ',df['End Station'].mode()[0])

        if 'Start Station' in df and 'End Station' in df:
            df['Station combination'] = df['Start Station'] + '-->' + df['End Station']
            if not df['Station combination'].empty:
                print('The most frequent combination of start & end station trip is:' , df['Station combination'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    if len(df) == 0 or 'Trip Duration' not in df:
        print("No trip duration data available!")
    else:
        totat_time = df["Trip Duration"].sum()
        print('Total travel time is',totat_time, 'seconds')

        mean = df["Trip Duration"].mean()
        print('Mean travel time is ', mean)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if len(df) == 0:
        print("No data for the selected filters.")
    else:
        if 'User Type' in df:
            print('Count of User types: ',df['User Type'].value_counts())

        if 'Gender' in df:
            print('Number of Genders is ',df['Gender'].value_counts())
        else:
            print('There is no gender')

        if 'Birth Year' in df:
            print('The earliest year of birth is ',df['Birth Year'].min())
            print('The most recent year of birth is ',df['Birth Year'].max())
            print('The most common year of birth is ',df['Birth Year'].mode()[0])
        else:
            print('Birth Year not available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    #Display raw data 5 rows at a time upon user request.
    if len(df) == 0:
        return
    i = 0
    pd.set_option('display.max_columns', None)
    while True:
        ans = input('Would you like to see 5 lines of raw data? (yes/no): ').strip().lower()
        if ans not in ('yes', 'y'):
            break
        print(df.iloc[i:i+5])
        i += 5
        if i >= len(df):
            print('End of data.')
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
