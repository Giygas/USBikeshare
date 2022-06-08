import time
import pandas as pd
import numpy as np
from os import system, name


def clrscr():
    """Method for clearing the screen"""
    # for windows os
    if name == 'nt': 
        _ = system('cls') 
    
    # for mac and linux os(The name is posix)
    else: 
        _ = system('clear') 


CITY_DATA = {'chicago': 'data/chicago.csv',
                'new york city': 'data/new_york_city.csv',
                'washington': 'data/washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # if there's no input, no filters will be applied
    month = "all"
    day = "all"
    # a list containing the differents input possibilities for city
    cities = ['chicago', 'new', 'new york', 'new york city','washington', 'c', 'n', 'w']
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        clrscr()
        print('Hello! Let\'s explore some US bikeshare data!')
        print('-'*40)
        try:
            city = input("You want to see data from wich city? (Chicago, New York City, Washington): ").lower()
            # if the input is in the list of valid options, standarize the name of the city
            if city in cities:
                if  city == 'c':
                    city = 'chicago'
                elif city == 'new' or city == 'new york' or city == 'n':
                    city = 'new york city'
                elif city == 'w':
                    city = 'washington'
                break
            else:
                print("Sorry, you must input a valid city, try again ")
                time.sleep(2)
        except:
            print("Sorry, that's an invalid option, try again")
            time.sleep(2)
    
    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        clrscr()
        print('Hello! Let\'s explore some US bikeshare data!')
        print('City selected: ',city.title())
        print('-'*40)
        print("You can choose ", months)
        try:
            month = input("Your choice: ").lower()
            if month not in months:
                print("Sorry, you must input a valid month, try again")
                time.sleep(2)
            else:
                break
        except:
            print("Sorry, that's an invalid option, try again")
            time.sleep(2)
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        clrscr()
        print('Hello! Let\'s explore some US bikeshare data!')
        print('City selected: ',city.title())
        print("Month selected: ", month.title())
        print('-'*40)
        print("You can choose ", days)
        try:
            day = input("Your choice: ").lower()
            if day not in days:
                print("Sorry, you must input a valid day, try again")
                time.sleep(2)
            else:
                break
        except:
            print("Sorry, that's an invalid option, try again")
            time.sleep(2)
        
    
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
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
        
    # convert the Times columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
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

    print('\nCalculating The Most Frequent Times of Travel...')
    print('-'*20)
    start_time = time.time()

    # display the most common month
    print("The most commont month is: ", df['month'].mode()[0])
    print('-'*20)
    # display the most common day of week
    print("The most common day of the week is: ", df['day_of_week'].mode()[0])
    print('-'*20)
    # display the most common start hour
    start_hour = df['Start Time'].dt.hour
    print("The most common Start hour is: ", start_hour.mode()[0])
    print('-'*20)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...')
    print('-'*20)
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station is: ", df.mode()['Start Station'][0])
    # display most commonly used end station
    print("The most commonly used end station is: ", df.mode()['End Station'][0])
    # display most frequent combination of start station and end station trip
    combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("The most common combination of starting and ending station are: ", combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    
    print('\nCalculating Trip Duration...')
    print('-'*20)
    start_time = time.time()

    # display total travel time
    df['diff_min'] = (df['End Time'] - df['Start Time'])
    total_travel_time = df['diff_min'].sum()
    print("Total travel time: ", total_travel_time)
    print('-'*20)
    # display mean travel time
    mean_travel_time = df['diff_min'].mean()
    print("Mean travel time: ", mean_travel_time)
    print('-'*20)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    
    print('\nCalculating User Stats...')
    print('-'*20)
    start_time = time.time()
    
    # Display counts of user types
    print("Differents user types and its count:\n")
    print(df['User Type'].value_counts().to_frame().T)
    print('-'*20)
    
    # Display counts of gender
    print("Differents genders and its count:\n")
    print(df['Gender'].value_counts().to_frame().T)   
    print('-'*20)

    
    # Display earliest, most recent, and most common year of birth
    print("Earliest year of birth :", df['Birth Year'].min().astype(int))
    print("Most recent year of birth :", df['Birth Year'].max())
    print("Most common year of birth :", df['Birth Year'].mode()[0])
    print('-'*20)

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        if city != 'washington':
            user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
