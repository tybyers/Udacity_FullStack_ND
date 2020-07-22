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