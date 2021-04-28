import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
selected_city = None
months = ['january', 'february', 'march', 'april', 'may', 'june']
days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def convert_time(time):
    """
    Converts the specified time (in seconds) to a value displayed in hours, minutes and seconds (as a string).

    Args:
        (int64) time - the value to convert to a formatted string

    Returns:
        (str) formatted_time - time formatted string

    """
    hours_value = (time // (60 * 60))
    minutes_value = (time - hours_value * (60 * 60)) // 60
    seconds_value = (time - hours_value * (60 * 60) - minutes_value * 60)

    return (str(hours_value) + ' hours, ' + str(minutes_value) + ' minutes, ' + str(seconds_value) + ' seconds.')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Includes some basic input error checking, including validity of specified city, month and day.
    
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please specify a city (chicago, new york city, washington): ").lower()
    while CITY_DATA.get(city) == None:
        city = input("Sorry! That is not a valid city... Please try and enter a city again (chicago, new york city, washington): ").lower()
    global selected_city
    selected_city = city

    # get user input for month (all, january, february, ... , june)
    month = input("Please enter a month (all, january, february, ... , june): ").lower()
    while month not in months and month != 'all':
        month = input("Sorry! That is not a valid month... Please try and enter a month again (all, january, february, ... , june): ").lower()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please enter a day of week: ").lower()
    while day not in days_of_week and day != 'all':
        day = input("Sorry! That is not a valid day... Please try and enter a day again (all, monday, tuesday, ..., sunday): ").lower()


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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA.get(city))

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
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

    # TO DO: display the most common month
    common_month_number = int(df['month'].mode())
    common_month = months[common_month_number-1]
    print("The most common month was: ", common_month)

    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print("The most common weekday was: ", common_day)

    # TO DO: display the most common start hour
    common_hour = int(df['hour'].mode())
    print("The most common start hour was: ", common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print("The most commonly used start station was: ", common_start)

    # TO DO: display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print("The most commonly used end station was: ", common_end)

    # TO DO: display most frequent combination of start station and end station trip
    df2 = df['Start Station'] + ' & ' + df['End Station']
    common_combination = df2.mode()[0]
    print("The most frequent combination of start station and end station trip was: ", common_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    total_time_formatted = convert_time(total_time)
    print("The total travel time was: ", str(total_time), " seconds, or ", total_time_formatted)

    # TO DO: display mean travel time
    mean_time = int(df['Trip Duration'].mean())
    mean_time_formatted = convert_time(mean_time)
    print("The mean travel time was: ", str(mean_time), " seconds, or ", mean_time_formatted)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Here is a display of the number of different user types:")
    for user_type in user_types.index:
        print(user_type, ": ", user_types[user_type])

    # TO DO: Display counts of gender
    if selected_city != 'washington':
        genders = df['Gender'].value_counts()
        print("\nHere is a display of the number of user genders:")
        for gender in genders.index:
            print(gender, ": ", genders[gender])

        # TO DO: Display earliest, most recent, and most common year of birth
        min_birth = int(df['Birth Year'].min())
        recent_birth = int(df['Birth Year'].max())
        common_birth = int(df['Birth Year'].mode())

        print("\nThe earliest year of birth was", min_birth)
        print("The most recent year of birth was", recent_birth)
        print("The most common year of birth was", common_birth)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data_query(df):
    """Asks the user whether or not they would like to see the raw dataset.
    If 'yes', print 5 rows of data at a time until there is no more data."""

    answer = input("Would you like to view the raw data? (yes/no)")
    if answer == 'yes':
        size = df.size
        lower_index = 0
        upper_index = 5
        while answer == 'yes' and upper_index <= size:
            print(df.iloc[lower_index:upper_index, :])
            lower_index += 5
            upper_index += 5
            if upper_index > size:
                print("You have run out of data to view.")
                break
            answer = input("Would you like to view another 5 rows? (yes/no)")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data_query(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
