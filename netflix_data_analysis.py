import pandas as pd
import matplotlib.pyplot as plt

def plot_bar_chart(data, x_label, y_label, title, figsize=(12, 6), rotation=90, bar_width=0.8):
    plt.figure(figsize=figsize)
    data.plot(kind='bar', width=bar_width)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=rotation)
    plt.show()

def plot_comparison_chart(dataframe, category_col, value_col, category1, category2, title='Comparison Chart', figsize=(15, 8), rotation=90, bar_width=0.8):
    category1_df = dataframe[dataframe[category_col] == category1]
    category2_df = dataframe[dataframe[category_col] == category2]

    category1_per_value = category1_df[value_col].value_counts().sort_index()
    category2_per_value = category2_df[value_col].value_counts().sort_index()

    comparison_df = pd.DataFrame({
        category1: category1_per_value,
        category2: category2_per_value
    }).fillna(0)

    comparison_df.plot(kind='bar', figsize=figsize, width=bar_width)
    plt.title(title)
    plt.xlabel(value_col.capitalize())
    plt.ylabel('Number of Releases')
    plt.xticks(rotation=rotation)
    plt.legend(title=category_col.capitalize())
    plt.show()

def get_actor_director_counts(df, category, top_n=10):
    filtered_df = df[df['type'] == category]
    actors = filtered_df['cast'].str.split(', ').explode()
    directors = filtered_df['director'].str.split(', ').explode()
    actor_counts = actors.value_counts().head(top_n)
    director_counts = directors.value_counts().head(top_n)
    return actor_counts, director_counts

def plot_top_countries(df, top_n=10):
    countries = df['country'].str.split(', ').explode()
    country_counts = countries.value_counts().head(top_n)
    plot_bar_chart(country_counts, x_label='Country', y_label='Number of Titles', title=f'Top {top_n} Countries by Number of Titles', rotation=45, figsize=(15, 8))

df = pd.read_csv('./netflix.csv')

df['month_added'] = df['date_added'].str.split(' ').str[0]
movies_per_year = df[df['type'] == 'Movie']['release_year'].value_counts().sort_index()
month_with_most_releases = df['month_added'].value_counts().idxmax()
top_n = 10
movie_actors, movie_directors = get_actor_director_counts(df, 'Movie', top_n)
tv_show_actors, tv_show_directors = get_actor_director_counts(df, 'TV Show', top_n)
recent_years = df[df['release_year'] >= 2015]
movies_recent_years = recent_years[recent_years['type'] == 'Movie']['release_year'].value_counts().sort_index()
tv_shows_recent_years = recent_years[recent_years['type'] == 'TV Show']['release_year'].value_counts().sort_index()
recent_years_comparison_df = pd.DataFrame({
    'Movies': movies_recent_years,
    'TV Shows': tv_shows_recent_years
}).fillna(0)

plot_bar_chart(movies_per_year, x_label='Year', y_label='Number of Movies', title='Number of Movies Released Per Year', rotation=90, figsize=(15, 8))
plot_comparison_chart(df, category_col='type', value_col='release_year', category1='Movie', category2='TV Show', title='Comparison of Movies and TV Shows Released Per Year')
print(f'The month with most releases is {month_with_most_releases}')
plot_bar_chart(movie_actors, x_label='Actor', y_label='Number of Movies', title=f'Top {top_n} Actors in Movies', rotation=45, figsize=(15, 8))
plot_bar_chart(tv_show_actors, x_label='Actor', y_label='Number of TV Shows', title=f'Top {top_n} Actors in TV Shows', rotation=45, figsize=(15, 8))
plot_bar_chart(movie_directors, x_label='Director', y_label='Number of Movies', title=f'Top {top_n} Directors in Movies', rotation=45, figsize=(15, 8))
plot_bar_chart(tv_show_directors, x_label='Director', y_label='Number of TV Shows', title=f'Top {top_n} Directors in TV Shows', rotation=45, figsize=(15, 8))
plot_bar_chart(recent_years_comparison_df, x_label='Year', y_label='Number of Releases', title='Comparison of Movies and TV Shows Released in Recent Years (Since 2015)', rotation=0, figsize=(15, 8))

plot_top_countries(df, top_n=10)
