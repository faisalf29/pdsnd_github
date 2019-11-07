"""
In this project, I will use data provided by Motivate (a bike share system provider for many major
cities in the United States), to uncover bike share usage patterns. I will compare the system usage
between three large cities: Chicago, New York City and Washington, DC.


Faisal Fayyaz
"""

# Import time, pandas and numpy libraries
import time
import pandas as pd
import numpy as np

# Dictionary defining city names to city data files
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
        city = input('\nWhich city would you like to filter by: Chicago, New York City or Washington?: ')
        if city.lower() not in ('chicago', 'new york city', 'washington'):
            print("Input Error: Please enter Chicago, New York City or Washington only. Try again.")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('\nWhich month would you like to filter by: January, February, March, April, May, June or type all if you do not have any preference: ')
        if month.lower() not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print("Input Error: Please enter correct month or 'all'. Try again.")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\nWhich day would you like to filter by: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or type all if you do not have any preference: ')
        if day.lower() not in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'):
            print("Sorry, I didn't catch that. Try again.")
            continue
        else:
            break

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
    # load the city data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list below to get the corresponding int of month
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print("The most common month is: ", popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("The most common day of week is: ", popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("The most common start hour is: ", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station is: ", start_station)

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print("The most commonly used end station is: ", end_station)

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + " AND " + df['End Station']
    frequent_trip = df['trip'].mode()[0]
    print("The most frequent combination of start station and end station trip is: ", frequent_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = sum(df['Trip Duration'])
    print("Total travel time is ", total_travel_time/86400, " days.")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time is ", mean_travel_time/60, " minutes.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of User Types:\n", user_types)

    # Display counts of gender
    try:
        gender_types = df['Gender'].value_counts()
        print("\nCounts of Gender Types:\n", gender_types)
    except KeyError:
        print("\nCounts of Gender Types:\nNo data available for this month.")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year = df['Birth Year'].min()
        print("\nEarliest Year of Birth:", earliest_year)
    except KeyError:
        print("\nEarliest Year of Birth:\nNo data available for this month.")

    try:
        most_recent_year = df['Birth Year'].max()
        print("\nMost Recent Year of Birth:", most_recent_year)
    except KeyError:
        print("\nMost Recent Year of Birth:\nNo data available for this month.")

    try:
        most_common_year = df['Birth Year'].value_counts().idxmax()
        print("\nMost Common Year of Birth:", most_common_year)
    except KeyError:
        print("\nMost Common Year of Birth:\nNo data available for this month.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(city, month, day):
    """ Display the contents of the CSV file 5 rows at a time """

    start_row = 0
    end_row = 5

    # Ask user if they would like to see the raw data from the CSV file
    show_raw_data = input('Would you like to see the raw data 5 rows at a time? (yes/no): ')
    if show_raw_data.lower() == 'yes':
        # Load the dataframe with raw data from CSV file
        df = load_data(city, month, day)
        # Loop through the dataframe 5 rows at a time
        while end_row <= df.shape[0] -1:
            print(df.iloc[start_row:end_row, :])
            start_row += 5
            end_row += 5
            stop_raw_data = input('Would you like to continue? (yes/no): ')
            if stop_raw_data.lower() == 'no':
                break


def main():
    # Use a while loop to call the functions and get user input
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(city, month, day)

        # Ask user if they would like to start another analysis
        restart = input('\nWould you like to restart? (yes/no): ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
