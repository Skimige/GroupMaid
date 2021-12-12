from sys import version_info

__version__ = "0.0.2"

if version_info[:2] < (3, 6):
    # Verify Python 3.6+ is used
    print(
        "You're using Python {}.{},".format(*version_info[:2]),
        "but Python 3.6+ is required by this bot.",
    )
    quit()
