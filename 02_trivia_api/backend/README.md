# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Endpoints

### GET '/questions'

Get all questions available in the database.

#### Parameters

Default: None

May add the `page` argument to choose a page number, starting from 1. Results are paginated in groups of 10.

#### Response Body

```
{
    'success': <bool>,
    'questions': <list>,  #default paginated list of 10
    'total_questions': <int>, # total number of questions
    'categories': <dict> # available categories
}
```

#### Example 

Basic query:
```
(fsnd) backend $ curl http://127.0.0.1:5000/questions
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ], 
  "success": true, 
  "total_questions": 18
}
```

To get a paginated list add the `page` parameter:
```
(fsnd) backend $ curl http://127.0.0.1:5000/questions?page=2
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
... (continued)
```

### GET '/categories'

Get all available categories for questions in the database. 

#### Parameters

None

#### Response Body

```
{
    'success': <bool>,
    'categories': <dict>  available categories
}
```

#### Example 

```
(fsnd) backend $ curl http://127.0.0.1:5000/categories
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

### GET '/categories/\<int:category_id\>/questions'

Get a list of questions given the category ID

#### Parameters

\<int:category_id\>: Category primary key

May add the `page` argument to choose a page number, starting from 1. Results are paginated in groups of 10.

#### Response Body

```
{
    'success': <bool>,
    'questions': <list>,  #default paginated list of 10
    'total_questions': <int>, # total number of questions
    'categories': <dict> # available categories
}
```

#### Example 

```
(fsnd) backend $ curl http://127.0.0.1:5000/categories/1/questions
{
  "current_category": 1, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "adf", 
      "category": 1, 
      "difficulty": 1, 
      "id": 24, 
      "question": "test science difficulty 1"
    }
  ], 
  "success": true, 
  "total_questions": 4
}
```

### DELETE '/questions/\<int:question_id\>'

Deletes a question from the database, given the question id.

#### Parameters

\<int:question_id\>: Primary key of the question to be deleted.

#### Response Body

```
{
    "success": <bool>
}
```

#### Example 

```
(fsnd) backend $ curl -X DELETE http://127.0.0.1:5000/questions/24
{
  "success": true
}
```

### POST '/questions'

Submit a new question to the database.

#### Parameters

{
    "question": <str>, # question
    "answer": <str>, "answer
    "category": <int>, # primary key of category
    "difficulty": <int> # difficulty on 1-5 scale
}

#### Response Body

```
{
    "success": <bool>
}
```

#### Example 

```
(fsnd) backend $ curl -X POST -H "Content-Type: application/json" -d '{"question": "sample", "answer": "made up", "category": "2", "difficulty": "2"}' http://127.0.0.1:5000/questions
{
  "success": true
}
```

### POST '/questions/search'

Search question text for a given string, done from the Search box in the List tab

#### Parameters

```
{
    "searchTerm": <str>
}
```

#### Response Body

```
{
    'success': <bool>,
    'questions': <list>,  #default paginated list of 10
    'total_questions': <int>, # total number of questions
    'categories': <dict> # available categories
}
```

#### Example 

```
(fsnd) backend $ curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "Tom"}' http://127.0.0.1:5000/questions/search
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```

### POST '/quizzes'

Play the quiz game. After user chooses a category, chooses a question from that category (or ALL), which hasn't been shown to the user before. If there are no more unseen questions remaining, the game ends.



#### Parameters

#### Response Body

```
{
    "question": {
        "question": <str>,
        "answer": <str>,
        "category": <int> # primary key of category,
        "id": <int> # primary key of question,
        "difficulty": <int> difficulty, scale 1-5
    },
    "success": <bool>
}
```

#### Example 

```
(fsnd) backend $ curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category": {"id": "1", "type": "Science", "previous_questions": []}}'
{
  "question": {
    "answer": "Alexander Fleming", 
    "category": 1, 
    "difficulty": 3, 
    "id": 21, 
    "question": "Who discovered penicillin?"
  }, 
  "success": true
}
```

## Error Handling

Error are returned as JSON objects in the following format:

``` 
{
    "success": False,
    "error"  : 404,
    "message": "Cannot find resource"
}
```

The API currently returns the following error types when requests fail:

* 400: Bad Request  
* 404: Cannot find resource  
* 405: Method not allowed  
* 422: Cannot process  

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```