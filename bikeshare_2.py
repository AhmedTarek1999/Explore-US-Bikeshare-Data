import time
import pandas as pd
import numpy as np

City_Data = {'Chicago': 'chicago.csv',
             'New York': 'new_york_city.csv',
             'Washington': 'washington.csv'}


def get_filters():
    """
    This function is for asking user to specify a city, month, and day to analyze.

    Returns:
        city: name of the city to analyze
        month: name of the month to filter by, or "all" to apply no month filter
        day: name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello friend!')
    print('Let\'s explore some US bikeshare data together!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Which city of those you would like to see its data?  (Chicago - New York - Washington) ').title()
    while city not in City_Data.keys():  # Loop to handle invalid input from user
        print('SORRY! You entered an invalid city name. Please enter a city name from choices!')
        city = input('Which city of those would you like to see its data?  (Chicago - New York - Washington) ').title()

    # get user input for month (all, january, february, ... , june)
    months = ['All', 'January', 'February', 'March', 'April', 'May', 'June']
    while True:
        month = input(
            'Please choose from the valid months! (January - February - March - April - May - June - All) ').title()
        if month in months:
            print('Alright! here we go')
            break  # Break the while loop and get out of the list when user enter a valid month
        print('SORRY! You entered an invalid month name. Please enter month from choices!')  # else, print this

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['All', 'Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    while True:
        day = input('Please choose from the valid days (Saturday - Sunday - Monday - Tuesday - Wednesday - Thursday - '
                    'Friday - All) ').title()
        if day in days:
            print('Alright! here we go')
            break  # Break when user enter valid day
        print('SORRY! You entered an invalid day name. Please enter day from choices!')  # else, print this

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    This function is for Loading data for the specified city and filters by month and day if applicable.

    Args:
        city: name of the city to analyze
        month: name of the month to filter by, or "all" to apply no month filter
        day: name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df: Pandas DataFrame containing city data filtered by month and day
    """
    # Load data from file into the dataframe
    df = pd.read_csv(City_Data[city])

    # Creating new dataframe from Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extracting month and day from Start Time column
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_name()

    # filtering by month
    if month != 'All':
        # using the index of the months list to get the corresponding integer
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        # filtering by month to create new dataframe
        df = df[df['month'] == month]

    # filtering by day
    if day != 'All':
        # filtering by day to create new dataframe
        df = df[df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Displaying the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    month = df['month'].mode()[0]
    print("The most common month is : {}".format(months[month - 1]))    # (-1): bec. I added 1 in list index before

    # Displaying the most common day of week
    day = df['day'].mode()[0]
    print("The most common day is : {}".format(day))

    # Displaying the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour  # Extracting hour from Start Time to create new columns
    hour = df['start_hour'].mode()[0]
    print("The most common start hour is : {}".format(hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displaying statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Displaying the most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print("The most common start station is: {}".format(start_station))

    # Displaying the most commonly used end station
    end_station = df['End Station'].mode()[0]
    print("The most common end station is: {}".format(end_station))

    # Displaying the most frequent combination of start station and end station trip
    # Concatenating start station column with end station column
    common_trip = (df['Start Station'] + ' ---> ' + df['End Station']).mode()[0]
    print("The most common trip is: {}".format(common_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """This function is for displaying statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time : {}".format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time : {}".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """This function is displaying statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displaying counts of user types
    user_counts = df['User Type'].value_counts()
    print("Counts of user types: {}".format(user_counts))

    # Displaying counts of gender
    # Washington datasheet doesn't contain gender column
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("Counts of gender: {}".format(gender_counts))

    # Display earliest, most recent, and most common year of birth
    # Washington datasheet doesn't contain Birth Year column
    if 'Birth Year' in df.columns:
        year = df['Birth Year'].fillna(0).astype('int64')       # Because of NaN values and type of data
        print('The earliest birth year is: {}'.format(year.min()))
        print('The most recent birth year is: {}'.format(year.max()))
        print('The most common birth year is: {}'.format(year.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def show_data(df):
    """Asking user if he wants to see 5 rows of the data at time"""
    print("\nData is obtainable to review if you want")
    data = input("Would you like to show the first 5 rows of data?  [Yes - No]").title()
    if data != 'Yes':
        print("Thank you for your time!")
    else:
        i = 0
        while data == "Yes":            
            print(df.iloc[i : i + 5])       # show row with index = 0 to row with index = 4
            i += 5          # For adding the next 5 rows
            check = input('Would you like to display the next 5 raws? [Yes - No]').title()
            if check != 'Yes':
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

var = np.arange(5) == np.arange(5).astype(str)  # For FutureWarning
