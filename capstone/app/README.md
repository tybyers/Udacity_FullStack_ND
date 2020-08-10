# Race Schedules API

This API is submitted as my *student's choice* implementation to satisfy the requirements of the Capstone for the Udacity [Full Stack nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044).

## About the API

The API is written in Flask in Python. Code and instructions for interaction with the API can be found in the [backend](./backend) directory. The [frontend](./frontend) was not required for this Capstone project and remains a work in progress.

## Motivation

In my free time away from work, I enjoy wheelchair racing. I have raced competitively since I was about 9 years old (almost 30 years!), including about 70 marathons and countless shorter races. I have also raced internationally, representing the USA at high-profile events.

I have long wished for a better way to share information about my past and upcoming races as well perhaps provide a bit of a social network to do the same for my peers. There just aren't many good options out there for sharing the information I want in the way I want.

This API is a first step toward possibly realizing that dream, and allowed me the opportunity to play with some of the ideas (and, oh yeah, this will be a lot harder to do than I imagined).  

## Database Schema

At this time, the API simply interacts with two Postgres database tables:

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
patch:race       | Update website details for a race |   | x | x |
patch:distance   | Update distance information in db |   |   | x |
post:race        | Add a race to the schedule        |   | x | x |
post:distance    | Add a new distance to the db      |   |   | x |
delete:race      | Delete a race from the db         |   |   | x |
delete:distance  | Delete a distance from the db     |   |   | x |

## Endpoints

Below is the documentation for the endpoints.

### get:race 

Get upcoming/past race list

#### Parameters

#### Response Body

#### Example  

### get:distance 

Get distances available

#### Parameters

#### Response Body

#### Example  

### get:race-details 

Get details about a specific race

#### Parameters

#### Response Body

#### Example  

### patch:race     

Update website details for a race 

#### Parameters

#### Response Body

#### Example  

### patch:distance 

Update distance information in db 

#### Parameters

#### Response Body

#### Example  

### post:race       

Add a race to the schedule   

#### Parameters

#### Response Body

#### Example  

### post:distance   

Add a new distance to the db 

#### Parameters

#### Response Body

#### Example  

### delete:race    

Delete a race from the db  

### delete:distance 

Delete a distance from the db

