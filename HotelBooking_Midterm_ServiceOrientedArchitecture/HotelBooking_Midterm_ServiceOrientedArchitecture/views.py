"""
Routes and views for the flask application.
"""

from HotelBooking_Midterm_ServiceOrientedArchitecture import app
from datetime import datetime
import os
from flask import Flask, render_template, redirect, url_for, request, session, g
from flask.helpers import flash, url_for
from werkzeug.wrappers import UserAgentMixin
from wtforms import Form, BooleanField, StringField, PasswordField, validators, DateField, IntegerField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL

#config Mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'HOTELDB'
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor' #this config line returns queries we execute as dictionaries, default is to return as a tuple; ex. User Login 

#
mysql = MySQL(app)


class SearchHotelForm(Form):
    check_in = DateField('Check-In Date', [validators.required()], format='%m-%d-%Y')
    check_out = DateField('Check-Out Date', [validators.required()], format='%m-%d-%Y')
    extra_bed = IntegerField('Number of extrabed', [validators.required()], Length(min=0, max=2, message= None))

class ReservationInfo():
    extra_bed=0         #number of extra_bed to reserve
    room_nums=None      #room info
    check_in=None       #check-in date
    check_out=None      #check-out date
    num_days=0          #length of stay
    cost=0              #total cost
    #### SQL ####
    hotels_avail=None

res = None

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


"""
Dashboard
"""
@app.route('/dashboard')
def dashboard():
    upcoming=None
    
    cur = mysql.connection.cursor()
    result = cur.execute("""SELECT DISTINCT p.TenPhong, p.DonGia, p.idPhong FROM phong as p 
                             WHERE p.status = 0""")
    if result>0:
        upcoming=cur.fetchall()
        
    
    return render_template('dashboard.html', upcoming=upcoming)
    
    cur.close()
    #fdgdgf
# STEP 1 - Search for Available Rooms
@app.route('/search_room', methods=['GET','POST'])
def search_room():
    search_form = SearchHotelForm(request.form)
    
    cur = mysql.connection.cursor()
    search_result = cur.execute("""SELECT DISTINCT TenPhong 
                                    FROM phong 
                                    WHERE status = 0""")
    hotels_avail = cur.fetchall()
    cur.close()

    if request.method=='POST' and search_form.validate():
        check_in = search_form.check_in.data
        check_out = search_form.check_out.data
        extra_bed = search_form.extra_bed.data

        if extra_bed<0:
            flash("Must reserve atleast 1 or 0 room", 'danger')
            return render_template('1_search_room.html', form=search_form)
        
        if check_in<datetime.date.today():
            flash("Check-In Date must be today or later", 'danger')
            return render_template('1_search_room.html', form=search_form)
        
        if check_out<=check_in:
            flash("Check-Out Date must be at least one day later than Check-In Date", 'danger')
            return render_template('1_search_room.html', form=search_form)


        cur = mysql.connection.cursor()
        search_result = cur.execute("""SELECT DISTINCT p.TenPhong, p.idPhong 
                                    FROM phong AS p 
                                    LEFT JOIN phieuthue as pt
                                        ON p.idPhong = pt.idPhong
                                            AND (pt.Date_in <= %s OR pt.Date_out >= %s)
                                    WHERE status = 0
                                    ORDER BY p.TenPhong;""", (check_in, check_out))
        hotels_avail = cur.fetchall()
        cur.close()
        
        if search_result==0:
            flash("No Rooms Available, try different search", 'danger')
            return render_template('1_search_room.html', form=search_form)

        count=0
        new_hotels_avail = dict()
        for room in hotels_avail:
            if not room['idPhong'] in new_hotels_avail:
                new_hotels_avail['Available']=list()
                count+=1
            new_hotels_avail['Available'].append(room)
                
        if count==0:
            flash("Not enough rooms available, try different search", 'danger')
            return render_template('1_search_room.html', form=search_form, loc=locations)

        global res 
        res = ReservationInfo()
        res.check_in = check_in
        res.check_out = check_out
        res.num_days = (check_out-check_in).days
        res.hotels_avail=new_hotels_avail

        return redirect(url_for('pick_room'))
    return render_template('1_search_room.html', form=search_form)
