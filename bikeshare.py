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
    #List of cities to check against user input
    cities=['chicago', 'new york city', 'washington']
    #Ask user to enter name of city they wish to explore its data
    city=input("would you like to see data for Chicago, New York City or Washington?:\n").lower()
    while city not in cities:
        city=input("Please enter correct city name (Chicago, New York City or Washington):\n").lower()
    print("You have chosen={}".format(city))

    #List of first 6 months of 2017 (january, february, ... , june,all) to check against user input
    months=['january', 'february', 'march', 'april', 'may', 'june','all']
    #Ask user to input month name (january, february, ... , june,all) or choose all to filter by month
    month=input("Enter a month name (January - June) to filter the data by spacific month or enter 'all':\n").lower()
    while month not in months:
        month=input("Please enter correct month name (January - June) or enter 'all':\n").lower()
    print("You have chosen={}".format(month))

    #List of days (saturday, sunday, ... friday,all) to check against user input
    days=['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday','all']
    #Ask user to input day of week or choose all to filter by day
    day=input("Enter day name to filter by day or enter 'all':\n").lower()
    while day not in days:
        day=input("Please enter correct day name or enter 'all':\n").lower()
    print("You have chosen={}".format(day))


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    #Load data of the chosen city by the user
    df=pd.read_csv(CITY_DATA[city])

    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #Format Start Time values from String to Datetime
    df['Start Time']=pd.to_datetime(df['Start Time'])
    #Create month column from Start Time column date
    df['month']=df['Start Time'].dt.month
    #Create weekday column from Start Time Coloumn date
    df['day_of_week']=df['Start Time'].dt.weekday_name

    #Add hour and ST & End station combination column for upcoming analysis
    #Create hour column from Start Time column
    df['hour']=df['Start Time'].dt.hour
    #Create ST & End station combination column from Start Station and End Station columns
    df['ST End Stations']=df['Start Station'] + "+" + df['End Station']

    #Filter data table based on user chosen month/s
    if month !='all':
        months=['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df=df[df['month']==month]
    #Filter data table based on user chosen day/s
    if day !='all':
        df=df[df['day_of_week']==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Calculate the most common month
    common_month=df['month'].mode()[0]
    print("The most common month is={}".format(common_month))
    # Calculate the most common day of week
    common_dow=df['day_of_week'].mode()[0]
    print("The most common day of week is={}".format(common_dow))
     # Calculate the most common start hour
    common_st_hr=df['hour'].mode()[0]
    print("The most common start hour is={}".format(common_st_hr))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_st_station=df['Start Station'].mode()[0]
    print("The most common start station is={}".format(common_st_station))
    # Display most commonly used end station
    common_end_station=df['End Station'].mode()[0]
    print("The most common end station is={}".format(common_end_station))
    # Display most frequent combination of start station and end station trip
    common_combination=df['ST End Stations'].mode()[0]
    print("The most frequant combination of trips is={}".format(common_combination))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Calculate total travel time in seconds
    total_travel_time=df['Trip Duration'].sum()
    print("Total travel time in seconds is= {} seconds".format(total_travel_time))
    # Calculate total travel time in minutes
    ttt_in_minutes=total_travel_time/60
    ttt_in_minutes=format(ttt_in_minutes, ".2f")
    print("Total travel time in minutes is= {} minutes".format(ttt_in_minutes))
    # Calculate mean travel time in seconds
    mean_travel_time=df['Trip Duration'].mean()
    mean_travel_time=format(mean_travel_time, ".2f")
    print("Mean travel time in seconds is= {} seconds".format(mean_travel_time))
    # Calculate mean travel time in minutes
    mean_travel_time=float(mean_travel_time)
    mean_travel_time_min=mean_travel_time/60
    print("Mean Travel time in minutes is=",format(mean_travel_time_min, ".2f"),"minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Calculate counts of user types (Subscriber, Customer and Dependent)
    user_types=df['User Type'].value_counts()
    print("Type of users distributed as=\n",user_types)
    # Calculate counts of gender (Male and Female) for Chicago and New York City
    if 'Gender' in df.columns:
        genders=df['Gender'].value_counts()
        print("Users genders distributed as=\n",genders)
    else:
        print("No gender details available for this city.")

    #Display earliest, most recent, and most common year of birth for Chicago and New York City
    #Display earliest year of birth(oldest customer)
    if 'Birth Year' in df.columns:
        eldest=df['Birth Year'].min()
        print("Earliset year of birth=",int(eldest))
    #Display most recent birth year (youngest customer)
        youngest=df['Birth Year'].max()
        print("Most recent year of birth=",int(youngest))
    #Display most common year of birth
        common_year=df['Birth Year'].mode()[0]
        print("Most common year of birth=",int(common_year))
    else:
        print("No birth year information available for this city.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    answer=""
    i=0
    while answer != "yes" or answer != "no":
        answer=input("Do you want to see 5 rows of raw data?(yes or no):\n").lower()
        if answer=="yes":
            print(df.iloc[i:i+5])
            i+=5
        elif answer=="no":
            print("End of program, thank you.")
            break
        else:
            print("wrong input, only (yes, no)..")
            continue


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
