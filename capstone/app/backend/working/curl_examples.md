# GETs

## Good

### Distances

curl http://127.0.0.1:5000/distances  

### Races

curl http://127.0.0.1:5000/races  

## Fail

curl http://127.0.0.1:5000/racetypo  

# POSTs

## Good

### Distances

curl http://127.0.0.1:5000/distances  -X POST -H "Content-Type: application/json" -d '{"name": "5 Miler", "distance_mi": 5.0}'

curl http://127.0.0.1:5000/distances  -X POST -H "Content-Type: application/json" -d '{"name": "5K", "distance_km": 5.0}'

### Races

curl http://127.0.0.1:5000/races  -X POST -H "Content-Type: application/json" -d '{"name": "MTC Marathon", "city": "Minneapolis", "state": "MN", "website": "https://www.mtecresults.com/race/leaderboard/5829/2017_Medtronic_Twin_Cities_Marathon-Wheelchair", "distance_id": 1, "date": "2017-10-01"}'

## Fail

### Distances

curl http://127.0.0.1:5000/distances  -X POST -H "Content-Type: application/json" -d '{"name": "5 Miler", "distance_typo": "5.0"}'

### Races

Invalid Distance ID
curl http://127.0.0.1:5000/races  -X POST -H "Content-Type: application/json" -d '{"name": "MTC Marathon", "city": "Minneapolis", "state": "MN", "website": "https://www.mtecresults.com/race/leaderboard/5829/2017_Medtronic_Twin_Cities_Marathon-Wheelchair", "distance_id": 999999, "date": "2017-10-01"}'

# DELETEs

Note the "good ones" are only good if done after creating

## Good

### Distances

curl -X "DELETE" http://127.0.0.1:5000/distances/4

### Races

curl -X "DELETE" http://127.0.0.1:5000/races/7

## Bad

### Distances

curl -X "DELETE" http://127.0.0.1:5000/distances/99

### Races

curl -X "DELETE" http://127.0.0.1:5000/races/99


# PATCH

## Good

### Distances

curl http://127.0.0.1:5000/distances/5  -X PATCH -H "Content-Type: application/json" -d '{"name": "5K Race (upd)", "distance_km": 5.1}'

### Races

curl http://127.0.0.1:5000/races/6  -X PATCH -H "Content-Type: application/json" -d '{"website": "http://raceresults.com"}'

## Bad

### Distances




### Races

curl http://127.0.0.1:5000/races/6  -X PATCH -H "Content-Type: application/json" -d '{"unknown": "ignored"}'