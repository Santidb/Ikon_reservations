"""
File: Run_periodic.py
--------------------
This file runs the main function from main.py periodically, according to the time set. The program stops when all
dates that are being reserved are confirmed.
"""

from main import *

def IkonBot():
    """
    Script that runs a bot at regular time intervals

    Args:
        Days: List containing all days to reserve
        Resort: Desired resort to reserve
        Username: Ikon Pass email for logging in
        Password: Ikon Pass password for logging in

    returns: None
    """
    username = "misslisachang@gmail.com"
    password = "GSBikon1!"
    resort = "Crystal Mountain"
    days = ["Sat Feb 20 2021", "Sun Feb 21 2021"]

    result = main(days, resort, username, password)

    return result

if __name__ == '__main__':

    # Count how many times we've run the script
    iteration = 0

    # Run the script until we break
    while True:

        # Count iterations
        iteration += 1
        print("-" * 50)
        print(f"Iteration number {iteration}")
        print("-" * 50)

        # Run the bot
        try:
            result = IkonBot()
        finally:
            # Wait periodic interval
            wait_time = 60 * 3
            time.sleep(wait_time)

        # If all dates have been reserved, stop the program
        if result == 'Complete':
            break