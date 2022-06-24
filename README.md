# API Development and Documentation Final Project

## Trivia App

This project is a trivia API app, that allows users to add, search and delete questions and play a fun quizz to see who can get the highest score. It is a part of the Fullstack Nanodegree, and serves as a practice module for lessons from Course 2: API Development and Documentation. The project enabled we the students to display our newly learnt skills with regard to structuring and implementing well formatted API endpoints that leverage knowledge of HTTP and API development best practices.

All backend code follows [PEP8 style guidelines.](https://peps.python.org/pep-0008/)

## Getting Started

### Pre-requisites and Local Development

Developers using this App should already have Python3, pip and node installed on their local machines. 

### Backend

The instructions given in this section are for developers using windows 10 or higher and gitbash as their command line tool. Mac and Linux users can check [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/) for subtle differences in the commands.

open gitbash and clone the project repository, `cd` into the backend folder and run the following commands to create and activate a virtual environment and install all dependencies.

```sh
python3 -m venv venv 
source venv/Scripts/activate
python3 -m pip install pip --upgrade
python3 -m pip install requirements.txt
```
To run the application run the following commands:

```sh
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made.

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration.

### Frontend

From the frontend folder, run the following commands to start the client:

```sh
npm install // only once to install dependencies
npm start //everytime you want to start the client
```
By default, the frontend will run on ```localhost:3000```. Please ensure that the backend is running before proceeding to start or use the client.

## Tests

In order to run tests, navigate to the backend folder and run ```psql -h localhost -U <database_username>``` to enter the psql shell.
Then run the following commands to create the test database:

```pgsql
DROP DATABASE IF EXISTS trivia_test;
CREATE DATABASE trivia_test;
\i test_trivia.psql
\q
```
And then run the following command to run the tests:

```sh
python3 test_flaskr.py
```
these commands are for developers using windows 10 or higher and gitbash as their command line tool.
All tests are kept in that file and should be maintained as updates are made to app functionality.

# API Reference

## Getting Started

Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, ```http://127.0.0.1:5000/```, which is set as a proxy in the frontend configuration.
Authentication: This version of the application does not require authentication or API keys.

## Error Handling

Errors are returned as JSON objects in the following format:

```javascript
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return five error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Unprocessable
- 500: Internal Server Error

## Endpoints
### GET /api/v1.0/categories

- General:
    - Returns a categories object and  a success value.

- Sample: 
```sh
curl http://127.0.0.1:5000/api/v1.0/categories
```

```javascript
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

### GET /api/v1.0/questions

- General:
    - Returns a list of question objects, the total number of questions, a categories object and  a success value.
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

- Sample: 
```sh
curl http://127.0.0.1:5000/api/v1.0/questions?page=2
```

```javascript
{
  "questions": [
    {
      "id": 1,
      "question": "Who scored the last goal in the 2011 champions league final?",
      "answer": "David Villa",
      "difficulty": 3,
      "category": 6
    },
    {
      "id": 2,
      "question": "What is the largest organ in the human body?",
      "answer": "The liver",
      "difficulty": 4,
      "category": 1
    }
  ],
  "totalQuestions": 20,
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

### DELETE /api/v1.0/questions/{question_id}

- General:
    - Deletes the question of the given ID if it exists and returns the id of the deleted question and a success value.

- Sample: 
```sh
curl -X DELETE http://127.0.0.1:5000/api/v1.0/questions/2
```

```javascript
{
 "deleted": 2,
  "success": true
}
```

### POST /api/v1.0/questions

- General:
- This endpoint either POSTs (creates) a new question, or searches for a question depending on whether or not a search term is included in the request body.

 #### Search questions
 - If a search term is included in the request body, it returns a list of question objects, the total number of questions, and  a success value.
 - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
 - The search term is a substring of the question and could be either in upper or lower case.
 
 - Sample: 
 ```sh
 curl -X POST http://127.0.0.1:5000/api/v1.0/questions -H 'Content-type:application/json' -d '{"searchTerm":"champions"}'
 ```

```javascript
{
  "questions": [
    {
      "id": 1,
      "question": "Who scored the last goal in the 2011 champions league final?",
      "answer": "David Villa",
      "difficulty": 3,
      "category": 6
    },
    {
      "id": 10,
      "question": "Who scored the first goal in the 2006 champions league final?",
      "answer": "Sol Campbell",
      "difficulty": 4,
      "category": 6
    }
  ],
  "totalQuestions": 2,
  "success": true
}
```
#### Create question
 - If there is no search term included in the request body, it is expected that a question, an answer, a difficulty and a category are included in the request. These would then be used to create a new question.
 - It would then return a success message and the id of the newly created question.

 - Sample: 
  ```sh 
 -curl -X POST http://127.0.0.1:5000/api/v1.0/questions -H 'Content-type:application/json' -d '{"question":"What is the name of the second largest city in Africa", "answer":"Ibadan", "difficulty": "5", "category": "3"}' 
 ```
  
  ```javascript
  {
    "created": 21,
    "success": true
  }
  ```
  
  ### GET /api/v1.0/categories/{category_id}/questions

- General: 
    - Returns a list of question objects of a particular category, the total number of questions of that category, the category chosen and  a success value.
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
    - The endpoint expects a category id in the request body.

- Sample: 
```sh
curl http://127.0.0.1:5000/api/v1.0/categories/6/questions
```

```javascript
{
  "questions": [
    {
      "id": 1,
      "question": "Who scored the last goal in the 2011 champions league final?",
      "answer": "David Villa",
      "difficulty": 3,
      "category": 6
    },
    {
     "id": 10,
      "question": "Who scored the first goal in the 2006 champions league final?",
      "answer": "Sol Campbell",
      "difficulty": 4,
      "category": 6
    }
  ],
  "totalQuestions": 2,
  "currentCategory": "Sports",
  "success": true
}
```

### POST /api/v1.0/quizzes

- General:
    - This endpoint is used to play the trivia game. It returns a question chosen at random from a particular category (if a category is chosen by the user) or a question chosen at random from all categories if the user selects all the categories as well as a success value.
    - The endpoint expects a category id and list of previous questions in the request body. A category id of 0 is provided if the user selects all categories rather than a particular category, in which case a random question is selected from all questions provided it is not in the list of previous questions chosen. 
    - If a aprticular category is chosen, then a random question is chosen from that category provided it is not in the list of previous questions.
    - The game ends and the score is displayed to the player when the player has attempted five questions or when there are no more questions available (i.e. all the questions in that category are already in the previous questions list, meaning there were not up to five questions in that particular category).

- Sample: 
```sh
curl -X POST http://127.0.0.1:5000/api/v1.0/quizzes -d '{"previous_questions": [], "quiz_category": {"id":"6", "type":"Sports"}}'
```

```javascript
{
  "question": 
    {
      "id": 1,
      "question": "Who scored the last goal in the 2011 champions league final?",
      "answer": "David Villa",
      "difficulty": 3,
      "category": 6
    }
  "success": true
}
```
 
## Deployment N/A

## Author

Owolabi Adeyemi

## Acknowledgements 

Coach Caryn McCarthy (Tutor)

Sunday Ajiroghene (Connect sessions lead)

Emmanuel Agbavwe (Friend and Accountability buddy)

