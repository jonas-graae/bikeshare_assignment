import time
import datetime as dt
import pandas as pd
import numpy as np

filters = {
    'CITY_DATA': {
            'chicago': 'chicago.csv',
            'new york city': 'new_york_city.csv',
            'washington': 'washington.csv' 
    }, 
    'months': ['january', 'february', 'march', 'april', 'may', 'june' ],
    'days': ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'],
    'filter_choice': False,
    'filter_by_month': False,
    'filter_by_day' : False
}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    month = 'all'
    day = 'all'
    
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        choose_city = input("Would you like to see data for Chicago, New York, or Washington? \n").lower()
        if choose_city in filters['CITY_DATA']:
            city = choose_city
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        filter_choice = input("\nWould you like to filter the data by month, day, both or not at all? Type 'none' for no time filter. \n").lower()
        filters['filter_choice'] = filter_choice
        if filter_choice == "both":
            filters['filter_by_month'] = True
            filters['filter_by_day'] = True
            break
        elif filter_choice == "month":
            filters['filter_by_month'] = True
            break
        elif filter_choice == 'day':
            filters['filter_by_day'] = True
            break
        elif filter_choice == 'none':
            break

    if filters['filter_by_month']:
        while True:
            choose_month = input("\nWhich month? January, February, March, April, May or June? \n").lower()
            if choose_month in filters['months']:
                month = choose_month
                break
    
    if filters['filter_by_day']:
        while True:
            try:
                choose_day = int(input("\nWhich day? Please type your response as an integer (e.g., 1=Sunday)\n"))
                if choose_day in range(1,8):
                    day = choose_day  
                    break
            except:
                pass

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
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
    df = pd.read_csv(filters['CITY_DATA'][city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    ### Month
    # Create column with month number
    df['month'] = df['Start Time'].dt.month

    if month != 'all':
        # get month number of chosen number
        month = filters['months'].index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    ### Weekday
    # Create column with weekday
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if day != 'all':
        # filter by day to create new DataFrame
        df = df[df['day_of_week'] == filters['days'][day-1].title()]
        
    return df

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # TO DO: display the most common month
    if filters['filter_by_month'] == False:
        popular_month = df['month'].mode()[0]
        popular_month_count = df['month'].value_counts().iloc[0]
        print(f"Most popular month:{filters['months'][popular_month-1]}, Count:{popular_month_count}, Filter:{filters['filter_choice']}")

    # TO DO: display the most common day of week
    if filters['filter_by_day'] == False:
        popular_day = df['day_of_week'].mode()[0]
        popular_day_count = df['day_of_week'].value_counts().iloc[0]
        print(f"Most popular day: {popular_day}, Count: {popular_day_count}, Filter: {filters['filter_choice']}")

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    popular_hour_count = df['hour'].value_counts().iloc[0]

    #print Hour
    print(f"Most popular hour:{popular_hour}, Count:{popular_hour_count}, Filter:{filters['filter_choice']}")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    top_start_station = df['Start Station'].mode()[0]
    top_start_station_count = df['Start Station'].value_counts()[0]
    print(f"Most popular start station: {top_start_station}, Count: {top_start_station_count}, Filter: {filters['filter_choice']}")

    # TO DO: display most commonly used end station
    top_end_station = df['End Station'].mode()[0]
    top_end_station_count = df['End Station'].value_counts()[0]
    print(f"Most popular end station: {top_end_station}, Count: {top_end_station_count}, Filter: {filters['filter_choice']}")

    # TO DO: display most frequent combination of start station and end station trip
    df['travel'] = df['Start Station'] + " - " + df['End Station'] 
    top_trip = df['travel'].mode()[0]
    top_trip_count = df['travel'].value_counts()[0]
    print(f"The most common trip is: {top_trip}, trip-count: {top_trip_count}, Filter: {filters['filter_choice']}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    #Print both mean and total travel time in one line
    print(f"Total travel time: {total_travel_time} seconds, mean travel time: {mean_travel_time} seconds")
    print(f"Total travel time: {total_travel_time / 60} minutes, mean travel time: {mean_travel_time / 60} minutes")
    print(f"Total travel time: {total_travel_time / 60 / 60} hours, mean travel time: {mean_travel_time / 60 /60} hours")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    total_rows = len(df.index)
    print(total_rows)
    print(df.shape)
    print(df.size)

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    subscribers = df['User Type'].value_counts()['Subscriber']
    customers = df['User Type'].value_counts()['Customer']
    print(f"Subscribers: {subscribers}, Customers: {customers}, Filter: {filters['filter_choice']}")

    # Washington missing gender and birth column
    if city != 'washington':
        # TO DO: Display counts of gender
        males = df['Gender'].value_counts()['Male']
        females = df['Gender'].value_counts()['Female']
        gender_unknown = total_rows - males - females
        print(f"Male: {males}, Female: {females}, Gender Unknown: {gender_unknown}, Filter: {filters['filter_choice']}")
        

        # TO DO: Display earliest, most recent, and most common year of birth
        birth_years = df['Birth Year']
        earliest_birth = int(birth_years.min())
        latest_birth = int(birth_years.max())
        common_birth_year = int(birth_years.mode()[0])
        print(f"Ealiest Birth year: {earliest_birth}, latest birth year: {latest_birth}, Most common birth year: {common_birth_year}, Filter: {filters['filter_choice']}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(data):
    start_loc = 0
    while True:
        get_raw_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no.\n').lower()
        if get_raw_data != 'yes':
            break
        print(data.iloc[start_loc:start_loc + 5])
        start_loc += 5

def main():
    while True:
        #Ask user for City, month, day
        city, month, day = get_filters()

        # Load city data with applied filters
        df = load_data(city, month, day)

        # Get stats on time
        time_stats(df, month, day)

        # Get stats on stations and trips
        station_stats(df)

        # get stats on time used by consumers
        trip_duration_stats(df)
        
        # get stats about the users
        user_stats(df, city)

        # Ask user to see five rows of raw data
        display_raw_data(df)

        # Ask user to restart game
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()