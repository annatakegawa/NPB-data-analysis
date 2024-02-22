import os
import requests
import pandas as pd
from bs4 import BeautifulSoup


# combined into function
def create_team_dict() -> dict:
    url = 'https://sp.baseball.findfriends.jp/?pid=db'
    player_page = requests.get(url)
    player_soup = BeautifulSoup(player_page.content, 'html.parser')
    team_ul_elements = player_soup.find_all('ul', class_ = 'db_team_select_box')

    team_dict = {}

    for team_ul in team_ul_elements:
        league_name = team_ul.find('li').text.strip()
        team_links = [a['href'] for a in team_ul.find_all('a')]
        team_names = [a.text for a in team_ul.find_all('a')]
    
        for link, name in zip(team_links, team_names):
            team_dict[name] = {
                'url': link,
                'league': 'セ' if league_name == 'セ･リーグ' else 'パ'
            }
    
    return team_dict


def create_player_data_df(url: str, team_name: str) -> pd.DataFrame:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', class_ = 'ResultTable02b')

    # get titles
    thead = table.find('thead')
    title_elements = thead.find_all('th')
    titles = [title.text.strip().replace('｜', 'ー') for title in title_elements]
    df = pd.DataFrame(columns = titles)
    
    # add rows
    tbody = table.find('tbody')
    column_data = tbody.find_all('tr')
    for row in column_data:
        row_data = row.find_all(['th', 'td'])
        individual_row_data = [data.text.strip() for data in row_data]
        # print(individual_row_data)
        length = len(df)
        df.loc[length] = individual_row_data

    # convert numeric columns' data types
    num_cols = df.columns[2:]
    df[num_cols] = df[num_cols].apply(pd.to_numeric, errors='coerce')

    df['チーム名'] = team_name

    return df


def get_salary_data(team_dict: dict, position: str):
    team_dfs = []
    for team_name, team_info in team_dict.items():
        team_url = team_info['url']
        url = f'https://sp.baseball.findfriends.jp{team_url}2023/{position}/'
        team_data = create_player_data_df(url, team_name)
        team_dfs.append(team_data)
    combined_df = pd.concat(team_dfs, ignore_index=True)
    save_path = os.path.join('data_collection/salaries/', f'{position}.csv')
    combined_df.to_csv(save_path)


if __name__ == '__main__':
    team_dict = create_team_dict()
    get_salary_data(team_dict, "batter")
