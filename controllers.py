from models import users, contacts
from views import contacts_view, contacts_edit_view


def show_contact_list(user, sorting='name'):
    if sorting == 'name':
        contact_list = contacts.select().where(contacts.user == user).order_by(contacts.name)
    elif sorting == 'email':
        contact_list = contacts.select().where(contacts.user == user).order_by(contacts.email)
    else:
        return
    return contacts_view(contact_list, user.username)


def show_contacts_edit(contact_id):
    contact = contacts.get_or_none(id=contact_id)
    if contact is None:
        return
    return contacts_edit_view(contact)


def do_register(username, password):
    if users.get_or_none(username=username) is None:
        return users.create(username=username, password=password)


def do_login(username, password):
    user = users.get_or_none(username=username)
    if user and password == user.password:
        return user


def do_delete_contact(contact_id):
    contact = contacts.get_or_none(id=contact_id)
    if contact is not None:
        contact.delete_instance()


def do_add_contact(user, name, email, phone):
    contacts.create(user=user, name=name, email=email, phone=phone)


def do_edit_contact(contact_id, name, email, phone):
    contact = contacts.get_or_none(id=contact_id)
    if contact:
        contact.name = name
        contact.email = email
        contact.phone = phone
        contact.save()
