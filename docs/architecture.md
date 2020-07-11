# System Design

## Database

- No database. Game state should be held in memory unless this becomes a problem. Remember to design datastore resource interfaces properly
- Redis (Do we even need this?)

## Experiment Time

Lets try using the redis datastore

- Client contains cookie (session id)
- Client should delete this when the session is dead