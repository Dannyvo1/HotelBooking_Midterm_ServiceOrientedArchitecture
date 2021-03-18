"""
This script runs the HotelBooking_Midterm_ServiceOrientedArchitecture application using a development server.
"""
import os
from os import environ
from HotelBooking_Midterm_ServiceOrientedArchitecture import app
from flask_marshmallow import Marshmallow
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
from datetime import datetime
from flask import render_template, Flask, redirect, url_for, request, session
from flask_wtf import FlaskForm
from flask_restful import Api, Resource
from HotelBooking_Midterm_ServiceOrientedArchitecture.database import db
from HotelBooking_Midterm_ServiceOrientedArchitecture.response import response_with
import HotelBooking_Midterm_ServiceOrientedArchitecture.response as resp
from HotelBooking_Midterm_ServiceOrientedArchitecture.config.config import DevelopmentConfig, TestingConfig, ProductionConfig




app.config['SECRET_KEY']='Thisissupposedtobesecret!!'
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format( os.path.join(os.path.dirname(__file__), 'bookingdb.db'))

#if os.environ.get('WORK_ENV') == 'PROD':
#    app_config = ProductionConfig
#elif os.environ.get('WORK_ENV') == 'TEST':
#    app_config = TestingConfig
#else:
#    app_config = DevelopmentConfig
#app.config.from_object(app_config)

def create_app(config):
    app.config.from_object(config)
    
    db.init_app(app)
    with app.app_context():
        db.create_all()

    @app.after_request
    def add_header(response):
        return response
    
    @app.errorhandler(400)
    def bad_request(e):
        logging.error(e)
        return response_with(resp.BAD_REQUEST_400)
    
    @app.errorhandler(500)
    def server_error(e):
        logging.error(e)
        return response_with(resp.SERVER_ERROR_500)
    
    @app.errorhandler(404)
    def not_found(e):
        logging.error(e)
        return response_with(resp. SERVER_ERROR_404)
    
    
    return app





if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
