from sqlalchemy import or_
from src import db
from src import models
from src.libs.validation_file import phone_valid


def add_tag_notate(notate, tag):
    notate_tag = models.Notate(notate=notate, tag=tag)
    db.session.add(notate_tag)
    db.session.commit()


def show_all_notates():
    notates = db.session.query(models.Notate).all()
    return notates


def delete_notate(n_id):
    notates = db.session.query(models.Notate).filter(models.Notate.id==n_id).delete()
    db.session.commit()


def edit_notate(n_id, tag, notate):
    n = db.session.query(models.Notate).filter(models.Notate.id == n_id).first()
    n.notate = notate
    n.tag = tag
    db.session.commit()


def get_notate(id):
    n = db.session.query(models.Notate).filter(models.Notate.id == id).first()
    return n


def find_notate(tag):
    notates = db.session.query(models.Notate).filter(or_(
            models.Notate.id.ilike(tag),
            models.Notate.notate.ilike(tag),
            models.Notate.tag.ilike(tag))).all()
    return notates


def add_new_contact(name, phone, birthday, address, email):
    new_contact = models.Contact(user_name=name, email=email, birthday=birthday, address=address)
    db.session.add(new_contact)
    db.session.commit()
    phone = models.PhoneToContact(phone=phone, contact_id=new_contact.id)
    db.session.add(phone)
    db.session.commit()


def show_address_book():
    return db.session.query(models.Contact).all()


def show_phones_for_contact():
    return db.session.query(models.PhoneToContact).all()


def delete_contact(c_id):
    contact = db.session.query(models.Contact).filter(models.Contact.id==c_id).delete()
    db.session.commit()


def delete_contact_phones(n_id):
    contact = db.session.query(models.PhoneToContact).filter(models.PhoneToContact.contact_id==n_id).delete()
    db.session.commit()


def get_contact(c_id):
    return db.session.query(models.Contact).filter(models.Contact.id == c_id).one()


def get_contacts_phones(c_id):
    return db.session.query(models.PhoneToContact).filter(models.PhoneToContact.contact_id == c_id).all()


def edit_contact(c_id, name, birthday, address, email):
    c = db.session.query(models.Contact).filter(models.Contact.id == c_id).first()
    c.user_name = name
    c.birthday = birthday
    c.address = address
    c.email = email
    db.session.commit()


def add_new_phone(contact_id, phone):
    phones = db.session.query(models.PhoneToContact).all()
    for ph in phones:
        if ph.phone == phone_valid(phone):
            raise ValueError
    new_phone = models.PhoneToContact(phone=phone, contact_id=contact_id)
    db.session.add(new_phone)
    db.session.commit()
    return f'new phone added'

