import time
import pandas as pd
#import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

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
        city = input("Would you like to see data for Chicago, New York City, or Washington?\n").lower()
        if city in CITY_DATA:
            city = city
            break
        else:
            city = input("Would you like to see data for Chicago, New York City, or Washington?\n").lower()
        
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month? (e.g., January)\n").lower()
        if month in months:
            month = month
            break
        else:
            month = input("Which month? (e.g., January)\n").lower()
            
    while True:
    # get user input for day of week (all, monday, tuesday, ... sunday)
        day = int(input("Which day? Please type your response as an integer (e.g., 1 = Sunday)\n"))
        if day > len(days):
            day = int(input("Which day? Please type your response as an integer (e.g., 1 = Sunday)\n"))
        else:
            day = days[day - 1]
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
    # load data file into dataframe
    df = pd.read_csv(CITY_DATA[city])
  
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
      
    # extract month and day ad the week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
      
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
        
    # filter by month to create the new dataframe
    #df = df[df['month'] == month]
        
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
        
    df.fillna(method='ffill')

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour

    # display the most common month
    common_month = df['month'].mode()[0]
    print("Common month: {}".format(common_month))

    # display the most common day of week
    common_dow = df['day_of_week'].mode()[0]
    print("Common day of week: {}".format(common_dow))
    
    # display the most common start hour
    common_hr = df['hour'].mode()[0]
    print("Common hour: {}".format(common_hr))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station is {}".format(popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("The most commonly use end station is {}".format(popular_end_station))

    # display most frequent combination of start station and end station trip
    #fq = df.groupby(['Start Station', 'End Station']).head(1)
    #fq = df.groupby(['Start Station','End Station']).agg(lambda x:x.value_counts())
    fq = df.groupby(['Start Station','End Station']).agg('max')
    #fq = fq.sort_values()
    print("Frequent combination: {}".format(fq))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    #df['Start Time'] = pd.to_datetime(df['Start Time'])
    #df['hour'] = df['Start Time'].dt.hour

    # display total travel time
    travel_time = df['hour'].sum()
    print("Total travel time {}".format(travel_time))

    # display mean travel time
    avg_travel_time = df['hour'].mean()
    print("Mean of total travel time {}".format(avg_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print(gender_count)
    else:
        print("No Gender data to display")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_yob = df['Birth Year'].min()
        recent_yob = df['Birth Year'].max()
        commom_yob = df['Birth Year'].mode()[0]
        
        print("Earliest year of birth: {}".format(earliest_yob))
        print("Recent year of birth: {}".format(recent_yob))
        print("Common year of birth: {}".format(commom_yob))
    else:
        print("No Birth Year data to display")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    
    start = 0
    ends = 5
    
    while True:
        answer = input("Would like to see more data? y or n : ")
        if answer.lower() == 'y':
            #print(df.head(count).to_dict('series'))
            #print(df.head(count).tolist())
            print(df.iloc[start:ends])
            start += 5
            ends += 5
        else:
            break
    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
