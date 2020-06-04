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
    print('Hello! Let\'s explore some US bikeshare data! \n')

    city_dict = {
        "ch": "chicago",
        "ny": "new york city",
        "dc": "washington"
    }

    city = input("Please choose a city you would like to explore the data from: \n write CH for Chicago, NY for New York and DC for Washington: ")
    while city.lower() not in city_dict.keys():
        print("\n Please enter valid input!")
        city = input("Please choose a city you would like to explore the data from: \n write CH for Chicago, NY for New York and DC for Washington: ")
    else:
        city = city_dict[city.lower()]


    date_filter = input("Would you like to filter by month or day? ")
    while date_filter.lower() not in ('month', 'day'):
        print("\n Please enter valid input!")
        date_filter = input("Would you like to filter by month or day? ")
    else:
        if date_filter.lower() == 'month':
            month = input("Which month between January to June would you like to get the data from? ")
            while month.lower() not in ('january', 'february', 'march', 'april', 'may', 'june'):
                print("\n Sorry, we don't have data for this month, please type a month between January to June.")
                month = input("Which month between January to June would you like to get the data from? ")
            else:
                month = month.lower()
                day = 'all'

        else:
            day = input("Which day would you like to get the data from?")
            while day.lower() not in ('monday', 'tuesday', 'wendsday', 'thursday', 'friday', 'saturday', 'sunday'):
                print("\n please enter a valid day!")
                day = input("Which day would you like to get the data from?")
            else:
                month = 'all'


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
        df - Pandas DataFrame containing city data filtered by month and day, the filtered month and day
    """

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        df = df[df['month'].str.lower() == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df, month, day

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if month == 'all':
        popular_month = df.month.mode()[0]
        print("The most popular month is: {}".format(popular_month))

    if day == 'all':
        popular_day = df.day_of_week.mode()[0]
        print("The most popular day is: {}".format(popular_day))

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df.hour.mode()[0]
    print("The most popular hour of the day is: {}".format(popular_hour))

    print_duration(start_time)

    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popluar_start_station = df['Start Station'].mode()[0]
    print("The most popular starting station is: {}".format(popluar_start_station))

    popluar_end_station = df['End Station'].mode()[0]
    print("The most popular ending station is: {}".format(popluar_end_station))

    popular_comb = counts = df.groupby(['Start Station','End Station']).size().sort_values(ascending=False)
    print("The most common requent combination of start station and end station trip is: {}".format(counts.index[0]))

    print_duration(start_time)
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print("The total trip duration for the chosen period is: {} minutes.".format(sum(df['Trip Duration'])/60))

    print("The average trip duration for the chosen period is: {} minutes.".format(df['Trip Duration'].mean()/60))

    print_duration(start_time)
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print(user_types)

    print("\nThis is the count of our user typs: \n")
    user_types = df.groupby(['User Type'])['User Type'].count()
    print(user_types)

    try:
        print("\nThis is the count of our users gender: \n")
        gender = df.groupby(['Gender'])['Gender'].count()
        print(gender)
    except KeyError:
        print("Sorry, no data for your chosen filter\n")

    try:
        print("Here some data about our users year of birth: \n")
        print("\nThe earliest year of birth is: {}. \n".format(int(df['Birth Year'].min())))
        print("The most recent year of birth is: {}. \n".format(int(df['Birth Year'].max())))
        print("The most common year of birth is: {}.\n".format(int(df['Birth Year'].mode())))
    except KeyError:
        print("Sorry, no data for your chosen filter\n")

    print_duration(start_time)
    print('-'*40)

def print_duration(start_time):
    print("\nThis took %s seconds." % (time.time() - start_time))


def main():

    while True:
        month = None
        answer = None

        while True:
            if month == None:
                city, month, day = get_filters()
                df, month, day = load_data(city, month, day)
            elif day == 'all':
                answer = input('\nWould you like to filter by day? Enter yes or no.\n')

                if answer.lower() == "yes":
                    day = input("Which day would you like to get the data from?")

                    while day.lower() not in ('monday', 'tuesday', 'wendsday', 'thursday', 'friday', 'saturday', 'sunday'):
                        print("\n please enter a valid day!")
                        day = input("Which day would you like to get the data from?")

                    df, month, day = load_data(city, month, day)
                else:
                    break
            else:
                break

            time_stats(df, month, day)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

            if answer != None:
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Bye Bye!")
            break


if __name__ == "__main__":
	main()
