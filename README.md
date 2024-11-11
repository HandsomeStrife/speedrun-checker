# Speedrun.com Game Checker

This project is a Python script that checks if games in a list exist on [speedrun.com](https://www.speedrun.com) and outputs the results to CSV files. It categorizes the results into three CSV files:
1. **Games with no speedrun.com page**
2. **Games with possible matches but no exact name match**
3. **Games with exact matches, including details about the number of runners, the best time, and the latest run date**

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/HandsomeStrife/speedrun-checker.git
   cd speedrun-checker
   ```

2. **Set up a Python environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use: venv\Scripts\activate
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## Generating the `games_list.txt` File

To use this script, you need a list of game names in a text file called `games_list.txt`. Follow these steps to generate this file:

1. **Find Your Steam ID**:
   - Go to [steamid.io](https://steamid.io/) and enter your Steam profile URL or username to find your 64-bit Steam ID.

2. **Export Your Steam Games**:
   - Visit [steam.tools/games](https://steam.tools/games/).
   - Enter your Steam ID to load your library.
   - Export your game list to a text file by copying and pasting it into `games_list.txt`.

> **Note**: Ensure the game names are formatted with one game per line, and the script will remove any trademark symbols (e.g., `™`) automatically.

## Usage

1. **Run the script**:
   ```bash
   python speedrun_checker.py
   ```

2. **Output**:
   The script will create the following CSV files:
   - `no_speedrun_page.csv` - Contains game names with no page found on speedrun.com.
   - `possible_speedrun_page.csv` - Contains game names where a page might exist but with no exact match.
   - `exact_speedrun_page.csv` - Contains game names with an exact match, number of runners, the best time, and the latest run date.
   - `errors.csv` - Contains any errors encountered during the execution with game name, error code, and response.

## Troubleshooting

- If you encounter a `420` error, the script will automatically wait for 5 seconds and retry the request.
- For other errors, check `errors.csv` for more details.

## License
This project is licensed under the MIT License.

## Contributions
Contributions are welcome! Please feel free to submit a pull request or report issues.

---

Enjoy checking your game library against speedrun.com and discovering new challenges!