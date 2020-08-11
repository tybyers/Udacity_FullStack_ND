
# Race Schedule Backend

This API may be downloaded and run locally; it is also available for a short time via Heroku.

## Getting Started -- Local

The following instructions are for local machine setup.

### Dependencies

From the `backend` directory:

* Python 3.7  
* Virtual Environment (we like conda)  
* `pip` dependencies: 
```bash
conda install pip
pip install -r requirements.txt
```

### Database Setup

To set up the database locally, with postgres running, run the following:

```bash
source setup.sh                        # loads env variables
createdb raceschedule                  # create the db
flask db migrate                       # use Flask-Migrate to migrate the db
psql raceschedule                      # open db
```

After opening the database, seed with the following default data:
```psql
INSERT INTO distance (name, distance_km, distance_mi)
VALUES 
  ('Marathon', 42.195, 26.22),
  ('25K', 25, 15.53),
  ('12K', 12, 7.46);

INSERT INTO race (name, city, state, website, distance_id, date)
VALUES
  ('Bloomsday', 'Spokane', 'WA', 'https://www.bloomsdayrun.org/', 3, '2020-09-20'),
  ('MTC Marathon', 'Minneapolis', 'MN', 'https://www.tcmevents.org/', 1, '2020-10-05'),
  ('Riverbank Run', 'Grand Rapids', 'MI', 'https://amwayriverbankrun.com/', 2, '2020-10-18'),
  ('LA Marathon', 'Los Angeles', 'CA', 'https://www.lamarathon.com/', 1, '2019-03-05');
```

*Alternatively*, rather than running `flask db migrate` and seeding the data yourself, you may use the following command to set up the database:
```bash
psql raceschedule < raceschedule.psql
```

### Role-Based Access Control

To obtain tokens for the Role-Based Access Control (RBAC), visit https://udacity-tbyers.auth0.com/authorize?audience=ByersRaceSchedule&&response_type=token&client_id=IvmBCu8E2t5O6iNrMcDFc4yXqyapArw6&redirect_uri=http://localhost:8080/login-results 

The role names and passwords are provided to the Udacity project grader in a separate email.

## Heroku

We have successfully deployed the API to [heroku](https://www.heroku.com/). **Our API url is: https://udacity-raceschedule.herokuapp.com**. The only public endpoint available from the web is the `races` endpoint. Other endpoints are RBAC protected and may be accessed via `curl` (see the [Endpoints](#endpoints) section for more details).  

## Database Schema

At this time, the API interacts with two Postgres database tables:

  * A `race` table. It holds information about upcoming and past races. The table schema is:

```psql
   column_name |     data_type     
-------------+-------------------
 id          | integer
 name        | character varying
 city        | character varying
 state       | character varying
 website     | character varying
 distance_id | integer
 date        | date
```

  * A `distance` table. It contains information about the various distances  available:

```psql
 column_name |     data_type     
-------------+-------------------
 id          | integer
 name        | character varying
 distance_km | double precision
 distance_mi | double precision
(4 rows)
```

## Roles

We have defined two RBAC "roles" for this API, in addition to the "public" persona.

* Public -- Anyone who interacts with the API. Can only get the list of upcoming and past races.  
* Member -- We would allow people to apply to be members of our API and/or website. They would be able to add and change some basic information about races (for instance, they might be a race director), and they could also see more detail on distances and specific upcoming races.  
* Admin -- A few admin members would be "super" users, able to access any of the available endpoints.  

Below is a table of the endpoints and which roles may interact with each endpoint. 

endpoint  | description | public | members | admin |
----------|-------------|---------|-------|--------|
get:race  | Get upcoming/past race list | x | x | x |
get:distance | Get distances available |   | x | x |
get:race-details | Get details about a specific race |   | x | x |
post:race        | Add a race to the schedule        |   | x | x |
post:distance    | Add a new distance to the db      |   |   | x |
patch:race       | Update website details for a race |   | x | x |
patch:distance   | Update distance information in db |   |   | x |
delete:race      | Delete a race from the db         |   |   | x |
delete:distance  | Delete a distance from the db     |   |   | x |

## Endpoints

For each of the endpoints below with a `<rbac-token>` (eg `<member-token`>), you must have obtained a RBAC token via instructions provided from the author of this package.

Also, for these examples we use the Heroku web URL; for running locally replace the URL with `http://127.0.0:5000/`. 

### get:race 

Get upcoming/past race list.

#### Parameters

None

#### Response Body

```
{
    'races':
    {
        'past': { # races before today
            'id': <int> # db id
            {
                'name': <str> # race name
                'city': <str> # city
                'state': <str> # state
                'distance': <str> # distance name
                'km': <dbl>  # race distance (km)
                'miles': <dbl> # race distance (miles)
                'date': <datetime> # date of race
                'website': <str> # race website
            }
            
        },
        'upcoming': { # races today or after
            # same format as "past"
        }
    },
    'success": <bool>
}
```

#### Example  

This is a public endpoint, so no RBAC token needed.

```bash
(fsnd) backend % curl https://udacity-raceschedule.herokuapp.com/races

{"races":{"past":{"4":{"city":"Los Angeles","date":"Tue, 05 Mar 2019 00:00:00 GMT","distance":"Marathon","km":42.2,"miles":26.22,"name":"LA Marathon","state":"CA","website":"https://www.lamarathon.com/"}},"upcoming":{"1":{"city":"Spokane","date":"Sun, 20 Sep 2020 00:00:00 GMT","distance":"12K","km":12.0,"miles":7.46,"name":"Bloomsday","state":"WA","website":"https://www.bloomsdayrun.org/"}}},"success":true}
```

### get:distance 

Get distances available. 

#### Parameters

None

#### Response Body

```
{
    'distances':
    {
        'id': <int> # db id
        {
            'name': <str> # name of race
            'distance_km': <dbl> # race distance in km
            'distance_mi': <dbl> # race distance in miles
        }
    },
    'success': <bool>
}
```

#### Example  

```bash
curl https://udacity-raceschedule.herokuapp.com/distances -H "Authorization: Bearer <member-token>"

{"distances":{"1":{"distance_km":42.195,"distance_mi":26.22,"name":"Marathon"},"2":{"distance_km":25.0,"distance_mi":15.53,"name":"25K"},"3":{"distance_km":12.0,"distance_mi":7.46,"name":"12K"}},"success":true}
```

### get:race-details 

Get details about a specific race.

#### Parameters

\<int:race-id\>: Race primary key

#### Response Body

```
{
    'race': {
        'name': <str> # race name
        'city': <str> # city
        'state': <str> # state
        'distance_id': <int> # primary key of distance
        'distance': <str> # distance name
        'km': <dbl>  # race distance (km)
        'miles': <dbl> # race distance (miles)
        'date': <datetime> # date of race
        'website': <str> # race website
    },
    'success': <bool>
}
```

#### Example  

```bash
curl https://udacity-raceschedule.herokuapp.com/races-detail/1 -H "Authorization: Bearer <member-token>"

{"race":{"city":"Spokane","date":"Sun, 20 Sep 2020 00:00:00 GMT","distance_id":3,"distance_km":12.0,"distance_mi":7.46,"distance_name":"12K","name":"Bloomsday","race_id":1,"state":"WA","website":"https://www.bloomsdayrun.org/"},"success":true}
```

### post:race       

Add a race to the schedule.

#### Parameters

```
{
    "name": <str>         # race name
    "city": <str>         # city location of race
    "state": <str>        # state location of race
    "website": <str>      # race website
    "distance_id": <int>  # primary key of distance type
    "date": <datetime>    # YYYY-mm-dd for race
}
```

#### Response Body

```
{
    "success": <bool>
}
```

#### Example  

```bash
curl https://udacity-raceschedule.herokuapp.com/races -X POST -H "Content-Type: application/json" -d '{"name": "MTC Marathon", "city": "Minneapolis", "state": "MN", "website": "https://www.mtecresults.com/race/leaderboard/5829/2017_Medtronic_Twin_Cities_Marathon-Wheelchair", "distance_id": 1, "date": "2017-10-01"}' -H "Authorization: Bearer <member-token>"

{"success":true}
```

### post:distance   

Add a new distance to the db. 

#### Parameters

For the `distance` parameters, you only need to specify either `distance_km` or `distance_mi`, not both. If both are provided, the `distance_km` parameter is treated as "truth".

```
{
    'name': <str> Name of race,
    'distance_km': <dbl> Distance in km,
    `distance_mi': <dbl> Distance in miles
}
```

#### Response Body

```
{
    'success': <bool>
}
```

#### Example  

```bash
curl https://udacity-raceschedule.herokuapp.com/distances -X POST -H "Content-Type: application/json" -d '{"name": "5 Miler", "distance_mi": 5.0}' -H "Authorization: Bearer <admin-token>"

{"success":true}
```

### patch:race     

Update website details for a race. Only the website may be patched.

#### Parameters

\<int:race-id\>: Race primary key

```
{
    "website": <str> # new website
}
```

#### Response Body

```
{
    "success": <bool>
}
```

#### Example  

```bash
curl https://udacity-raceschedule.herokuapp.com/races/4 -X PATCH -H "Content-Type: application/json" -d '{"website": "http://raceresults.com"}' -H "Authorization: Bearer <admin-token>"

{"success":true}
```

### patch:distance 

Update distance information in db 

#### Parameters

As with the `POST` request, `distance_km` updates take precedence over `distance_mi` precedence. Neither needs to be supplied here, however. 

\<int:race-id\>: Distance primary key

```
{
    'name': <str> (Optional) Updated name of race,
    'distance_km': <dbl> (Optional) Updated distance in km,
    `distance_mi': <dbl> (Optional) Updated distance in miles
}
```

#### Response Body
```
{
    'success': <bool>
}
```
#### Example  

```bash
curl https://udacity-raceschedule.herokuapp.com/distances/4 -X PATCH -H "Content-Type: application/json" -d '{"name": "5K Race (upd)", "distance_km": 5.1}' -H "Authorization: Bearer <admin-token>"

{"success":true}
```

### delete:race    

Delete a race from the db.

#### Parameters

\<int:race-id\>: Race primary key

#### Response Body

```
{
    "success": <bool>
}
```

#### Example  

```
curl https://udacity-raceschedule.herokuapp.com/races/4 -X "DELETE"  -H "Authorization: Bearer <admin-token>

{"success":true}
```

### delete:distance 

Delete a distance from the db

#### Parameters

\<int:race-id\>: Distance primary key

#### Response Body

```
{
    "success": <bool>
}
```

#### Example  

```
curl https://udacity-raceschedule.herokuapp.com/distances/4 -X "DELETE"  -H "Authorization: Bearer <admin-token>

{"success":true}
```

## Testing

To run the unit tests locally, you must obtain valid RBAC tokens for the `races_member` and `races_admin` personas. Paste those updated values into the `setup.sh` script at the appropriate line. Then:

```bash
source test_setup.sh  # sets up the environment variables and database defaults
python test_api.py    # runs the tests
```