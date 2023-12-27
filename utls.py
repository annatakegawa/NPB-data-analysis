import requests
import datetime


def get_json_from_url(url:str):
    """
    
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    

    response = requests.get(url) # , headers=headers)
    
    if response.status_code == 200:
        pass
    elif response.status_code == 401:
        raise ConnectionRefusedError(
            f'Could not connect. The connection was refused.\nHTTP Status Code 401.'
        )
    else:
        raise ConnectionError(
            f'Could not connect.\nHTTP Status code {response.status_code}'
        )

    json_data = response.json()

    return json_data


def convert_numeric(value: str):
    if '.' in value:
        try:
            return float(value)
        except ValueError as e:
            print(f"Error: {e}")
    else:
        try:
            return int(value)
        except ValueError as e:
            print(f"Error: {e}")


def get_latest_season_year():
    curr_date = datetime.datetime.now()
    curr_month = curr_date.month

    season_start_month = 3
    season_end_month = 10

    latest_season_year = curr_date.year if curr_month >= season_start_month else curr_date.year - 1

    return latest_season_year
