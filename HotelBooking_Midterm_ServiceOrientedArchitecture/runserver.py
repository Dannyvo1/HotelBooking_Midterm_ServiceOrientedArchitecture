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







if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
