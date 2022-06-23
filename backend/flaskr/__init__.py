
import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_page = questions[start:end]
    return current_page

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    setting up CORS Allow '*' for origins. 
    """
    cors = CORS(app, resources={r'/api/*':{'origins':'*'}})

    """
    setting up Access-Control-Allow for headers and methods
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')

        response.headers.add('Acess-Control-Allow-Methods','GET,POST,PATCH,DELETE,OPTIONS')

        return response

    """
    endpoint to handle GET requests
    for all available categories.
    """
    @cross_origin
    @app.route('/api/v1.0/categories')
    def retrieve_categories():

        try:
            category_query = Category.query.order_by(Category.id).all()

            if request.method == 'DELETE':
                abort(405)

            categories = {category.id:category.type for category in category_query}

            return jsonify({
                'success' : True,
                'categories' : categories
            })
        
        except:
            print(sys.exc_info())
            abort(500)


    """
    endpoint to handle GET requests for questions,
    including pagination.
    the endpoint return a list of questions,
    number of total questions, and all categories.

    """
    @cross_origin
    @app.route('/api/v1.0/questions')
    def retrieve_questions():

        try:
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)
            category_query = Category.query.order_by(Category.id).all()
            categories =  { category.id:category.type for category in category_query}

            if len(current_questions) == 0:
                abort(404)

            return jsonify({
                'success' : True,
                'questions' : current_questions,
                'totalQuestions' : len(Question.query.all()),
                'categories' : categories,
                'currentCategory' : ''
            })
        
        except:
            print(sys.exc_info())
            abort(500)


    """
    endpoint that DELETEs questions using a question ID

    """
    @cross_origin
    @app.route('/api/v1.0/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                'success' : True,
                'deleted' : question_id
            })
        
        except:
            print(sys.exc_info())
            abort(400)


    """
    This endpoint either POSTs (creates) a new question, or searches for a question depending on whether or not a search term is included in the request body.

    """
    @cross_origin
    @app.route('/api/v1.0/questions', methods=['POST'])
    def create_new_question():
        
        try:
            body = request.get_json()

            new_question = body.get('question', None)
            new_answer = body.get('answer', None)
            new_difficulty = body.get('difficulty', None)
            new_category = body.get('category', None)
            search = body.get('searchTerm', None)

            if search:
                selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)))
                questions_found = paginate_questions(request, selection)

                return jsonify({
                    'success' : True,
                    'questions' : questions_found,
                    'total_questions' : len(selection.all())

                })

            elif (search is None and new_question is None and new_answer is None):
                abort(400)

            else:
            
                question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)

                question.insert()

                return jsonify({
                    'success' : True,
                    'created' : question.id 
                })
        
        except:
            print(sys.exc_info())
            abort(500)
    
    """

    This endpoint gets questions based on category.
    
    """
    @cross_origin
    @app.route('/api/v1.0/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        
        try:
            category = Category.query.filter(Category.id == category_id).one_or_none()

            if category:
                selection = Question.query.order_by(Question.id).filter(Question.category == category_id).all()
                questions = paginate_questions(request, selection)

                return jsonify({
                    'success' : True,
                    'questions' : questions, 
                    'totalQuestions' : len(selection),
                    'currentCategory' : category.type
                })
            
        except:
            print(sys.exc_info())
            abort(404)
        

    """
    this POST endpoint gets questions to play the quiz.
    it takes category and previous question parameters
    and returns a random questions within the given category, that is not one of the previous questions.

    """
    @cross_origin
    @app.route('/api/v1.0/quizzes', methods=['POST'])
    def get_quiz_question():
        
        try:
            body = request.get_json()
            if not ('previous_questions' in body and 'quiz_category' in body):
                abort(400)

            quiz_category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')
            
            if quiz_category.get('id') == 0:
                all_questions = Question.query.all()

                questions = [question for question in all_questions if question.id not in previous_questions]

            else:
                category_questions = Question.query.filter(Question.category == quiz_category.get('id')).all()


                questions = [ question for question in category_questions if question.id not in previous_questions]

            if questions:
                # conditional to check if there are still available questions and return an empty object otherwise thereby ending the game
                question_chosen = random.choice(questions).format()

            else: 
                question_chosen = {}
            
            

            return jsonify({
                'success' : True,
                'question' : question_chosen
            })
        
        except:
            abort(500)


    """
    Common error handlers for all expected errors.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error' : 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def Unprocessable(error):
        return jsonify({
            'success': False,
            'error' : 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error' : 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error' : 500,
            'message': 'internal server error'
        }), 500

    @app.errorhandler(405)
    def bad_request(error):
        return jsonify({
            'success' : False,
            'error' : 405,
            'message' : 'method not allowed'
        }), 405

    return app

