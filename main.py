import requests
import csv
from datetime import datetime
import time
import chardet

# Detect encoding
with open('games_list.txt', 'rb') as file:
    result = chardet.detect(file.read())
    encoding = result['encoding']
    print(f"Detected encoding: {encoding}")

# Load the list of game names using the detected encoding
games = []
bad_lines = []

with open('games_list.txt', 'r', encoding=encoding, errors='strict') as file:
    for line_number, line in enumerate(file, start=1):
        try:
            clean_line = line.strip().replace('™', '')
            if clean_line:
                games.append(clean_line)
        except UnicodeDecodeError as e:
            print(f"Error decoding line {line_number}: {e}")
            bad_lines.append((line_number, line))

# Output bad lines if any
if bad_lines:
    print("\nProblematic lines:")
    for line_number, line in bad_lines:
        print(f"Line {line_number}: {line}")
else:
    print("All lines decoded successfully.")

no_page = []
possible_page = []
exact_page = []
errors = []

for game in games:
    while True:
        print(f"Fetching data for {game}...")
        response = requests.get(f'https://www.speedrun.com/api/v1/games?name={game}')
        if response.status_code == 200:
            break
        elif response.status_code == 420:
            print(f"Rate limit reached for {game}, waiting 5 seconds...")
            time.sleep(5)
        else:
            print(f"Error fetching data for {game}: {response.status_code}")
            errors.append([game, response.status_code, response.text])
            break

    if response.status_code != 200:
        continue

    data = response.json().get('data', [])

    if not data:
        no_page.append([game])
        continue

    exact_match = False
    for entry in data:
        names = entry['names']
        if game in [names['international'], names.get('japanese'), names.get('twitch')]:
            leaderboard_link = next((link['uri'] for link in entry['links'] if link['rel'] == 'leaderboard'), None)
            if leaderboard_link:
                leaderboard_response = requests.get(leaderboard_link)
                if leaderboard_response.status_code != 200:
                    print(f"Error fetching leaderboard for {game}: {leaderboard_response.status_code}")
                    errors.append([game, leaderboard_response.status_code, leaderboard_response.text])
                    continue

                runs = leaderboard_response.json().get('data', {}).get('runs', [])
                num_runners = len(runs)
                latest_run_date = None
                best_time = None

                for run in runs:
                    run_date = datetime.fromisoformat(run['run']['date']) if run['run']['date'] else None
                    if latest_run_date is None or (run_date and run_date > latest_run_date):
                        latest_run_date = run_date
                        best_time = run['run']['times']['primary']

                exact_page.append([game, num_runners, best_time, latest_run_date])
            exact_match = True
            break

    if not exact_match:
        possible_page.append([game])

# Write to CSV files
with open('output/no_speedrun_page.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Game Name'])
    writer.writerows(no_page)

with open('output/possible_speedrun_page.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Game Name'])
    writer.writerows(possible_page)

with open('output/exact_speedrun_page.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Game Name', 'Number of Runners', 'Best Time', 'Latest Run Date'])
    writer.writerows(exact_page)

with open('output/errors.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Game Name', 'Error Code', 'Response'])
    writer.writerows(errors)

print("CSV files created successfully.")
