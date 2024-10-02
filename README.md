# my-jira-automation
Automate my JIRA issue creation

## First Draft Architecture
![2 My jira automation.png](docs/img/architecture_jira_automation.png)

## Description
This project automates the creation of JIRA issues and logs time to Tempo. It leverages an LLM (Large Language Model) to
generate titles and descriptions for the tickets, creating a streamlined workflow to save time.

## Steps
1. Request LLM to generate a title/description for tickets.
2. Log the ticket to JIRA.
3. Log time to Tempo.
4. Enjoy 15 minutes of my time saved every working week 😂

## Prerequisites
Ensure you have the following installed:

- Python 3.10.11
- Packages: PyYAML, pip, requests, wheel

## Installation
1. Clone the repository:
    ```sh
    git clone <your-repo-url>
    cd my-jira-automation
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. Configure your JIRA and Tempo API settings in a configuration file inside `resources/config.yaml`
2. Run the main script to start the automation process:
    ```sh
    python main.py
    ```

## TODO
- ~~Use LLM to generate prompt to log JIRA ticket with summary and description~~
- ~~Use Tempo API to log time on ticket created~~
- ~~Create JIRA ticket~~
- ~~Create Tempo for the current week~~
- Add Skipping holiday
- add more comments docstring

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.