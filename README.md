# cdnms

This is essentially codenames because we had a hard time making the game

## Architecture

Single server (multiple rooms)

## Models

Cards
    - There could be a lot of these
    - These could probably be preloaded from a file into the database?

Rooms
    - Users (temporary) (max 10?)
    - All pull from the same card pool (Really only requires 25 cards per game at a time which should limit memory usage)
      - Hold everything in a redis database (?)
        - There won't be that many people on this thing anyways so assume we have a lot of memory
    - Spymaster
      - Self selection or randomization

Sessions
    - Since we aren't storing any data really, 
