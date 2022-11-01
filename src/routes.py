from flask import render_template, request, flash, redirect, url_for, session, make_response
from werkzeug.utils import secure_filename
import pathlib
import uuid
from datetime import datetime, timedelta
from marshmallow import ValidationError

from . import app
from src.libs.validation_file import phone_valid
from src.repository import books_mathods
from src.libs.validation_schemas import  NewContactSchema




@app.route('/healthcheck')
def healthcheck():
    return 'I am working'


@app.route('/', strict_slashes=False)
def index():
    auth = True if 'username' in session else False
    return render_template('pages/index.html', title='Personal assistant', auth=auth)



@app.route('/new_notate', methods=['GET', 'POST'], strict_slashes=False)
def new_notate():
    if request.method == 'POST':
        notate = request.form.get('notate')
        tag = request.form.get('tag')
        books_mathods.add_tag_notate(notate,tag)
        print(notate, tag)
        flash('added successfully')
    return render_template('pages/new_notate.html')


@app.route('/show_notate_book', methods=['GET', 'POST'], strict_slashes=False)
def show_notate_book():
    if request.method == 'GET':
        notates = books_mathods.show_all_notates()
    return render_template('pages/show_notate_book.html', notates=notates)


@app.route('/show_notate_book/delete/<n_id>', methods=['GET', 'POST'], strict_slashes=False)
def delete_notate(n_id):
    if request.method == 'GET':
        books_mathods.delete_notate(n_id)
        flash('Deleted successfully!')
    return redirect(url_for('show_notate_book'))


@app.route('/show_notate_book/edit/<n_id>', methods=['GET', 'POST'], strict_slashes=False)
def edit_notate(n_id):
    notate = books_mathods.get_notate(n_id)
    if request.method == 'POST':
        notate = request.form.get('notate')
        tag = request.form.get('tag')
        books_mathods.edit_notate(n_id, tag, notate)
        flash('Changed successfully!')
    return render_template('pages/edit.html', notate=notate)


@app.route('/find_tag_notate', methods=['GET', 'POST'], strict_slashes=False)
def find_tag():
    if request.method == 'POST':
        tag = request.form.get('tag')
        notate = books_mathods.find_notate(tag)
        return render_template('pages/result_notate.html', notates=notate)
    return render_template('pages/find_tag_notate.html')


#  address book routes___________

@app.route('/new_contact', methods=['GET', 'POST'], strict_slashes=False)
def new_contact():
    if request.method == 'POST':
        try:
            NewContactSchema().load(request.form)
        except ValidationError as err:
            return render_template('pages/new_contact.html', messages=err.messages)
        name = request.form.get('name')
        phone = request.form.get('phone')
        birthday = request.form.get('birthday')
        address = request.form.get('address')
        email = request.form.get('email')
        if phone_valid(phone) is None:
            flash(f'Phone number is incorect\n'
                  f'Phone number must be 12 digits, and start with 380')
            return render_template('pages/new_contact.html')
        books_mathods.add_new_contact(name, phone_valid(phone), birthday, address, email)

        flash('added successfully')
    return render_template('pages/new_contact.html')


@app.route('/show_address_book', methods=['GET', 'POST'], strict_slashes=False)
def show_address_book():
    if request.method == 'GET':
        contacts = books_mathods.show_address_book()
        phones = books_mathods.show_phones_for_contact()
    return render_template('pages/show_address_book.html', contacts=contacts, phones=phones)


@app.route('/show_address_book/delete/<c_id>', methods=['GET', 'POST'], strict_slashes=False)
def delete_address_book(c_id):
    if request.method == 'GET':
        books_mathods.delete_contact(c_id)
        books_mathods.delete_contact_phones(c_id)
        flash('Deleted successfully!')
    return redirect(url_for('show_address_book'))


@app.route('/show_address_book/edit/<c_id>', methods=['GET', 'POST'], strict_slashes=False)
def edit_address_book(c_id):
    contact = books_mathods.get_contact(c_id)
    phones = books_mathods.get_contacts_phones(c_id)
    if request.method == 'POST':
        name = request.form.get('name')
        birthday = request.form.get('birthday')
        address = request.form.get('address')
        email = request.form.get('email')
        books_mathods.edit_contact(c_id, name, birthday, address, email)
        flash('Changed successfully!')
        return redirect(url_for('result_address_book'))
    return render_template('pages/edit_address_book.html', contact=contact, phones=phones)


@app.route('/find_address_book', methods=['GET', 'POST'], strict_slashes=False)
def find_address_book():
    if request.method == 'POST':
        symbol = request.form.get('symbol')
        contact = books_mathods.find_notate(symbol)
        return render_template('pages/result_address_book.html', contact=contact)
    return render_template('pages/find_address_book.html')



@app.route('/add_new_phone', methods=['GET', 'POST'], strict_slashes=False)
def add_new_phone():
    if request.method == 'POST':
        contact_id = request.form.get('user_id')
        phone = request.form.get('phone')
        if phone_valid(phone) is None:
            flash(f'Phone number is incorect\n'
                  f'Phone number must be 12 digits, and start with 380')
            return render_template('pages/add_new_phone.html')
        try:
            books_mathods.add_new_phone(contact_id, phone)
        except ValueError:
            flash('Phone already exist')
            return render_template('pages/add_new_phone.html')

        flash('added successfully')
    return render_template('pages/add_new_phone.html')


