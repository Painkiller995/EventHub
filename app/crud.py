from datetime import datetime, timedelta

from app import db
from app.models import Event, Registration, User


def create_new_event(user_id, form, image_url):
    """
    Create a new event in the database.
    """

    new_event = Event()

    new_event.user_id = user_id
    new_event.name = form.name.data
    new_event.description = form.description.data
    new_event.date = form.date.data
    new_event.location = form.location.data
    new_event.is_public = form.is_public.data
    new_event.image_url = image_url

    db.session.add(new_event)
    db.session.commit()

    return new_event


def update_event(event_id, form, image_url):
    """
    Update an existing event in the database.
    """
    event = Event.query.get(event_id)

    if event:
        event.name = form.name.data
        event.description = form.description.data
        event.date = form.date.data
        event.location = form.location.data
        event.is_public = form.is_public.data
        event.image_url = image_url if image_url else event.image_url

        db.session.commit()

    return event


def get_user_events(user_id):
    """
    Retrieve all events created by a user.
    """
    return Event.query.filter_by(user_id=user_id).order_by(Event.date.desc()).all()


def get_event_by_id(event_id):
    """
    Retrieve an event by its ID.
    """
    return Event.query.get(event_id)


def delete_event_by_id(event_id):
    """
    Delete an event by its ID.
    """
    event = Event.query.get(event_id)
    if event:
        db.session.delete(event)
        db.session.commit()
        return True
    return False


def get_event_organizer_info(event_id):
    """
    Get the organizer's information for an event.
    """
    event = Event.query.get(event_id)
    if event:
        return User.query.with_entities(User.name, User.email).join(Event).filter(Event.id == event_id).first()
    return None


def is_current_user_event(user_id, event_id):
    """
    Check if the event belongs to the current user.
    """
    event = Event.query.get(event_id)
    return event.user_id == user_id if event else False


def number_of_attendees(event_id):
    """
    Get the number of attendees for an event.
    """
    return Registration.query.filter_by(event_id=event_id).count()


def get_attendees_contact_info(event_id):
    """
    Get the contact information of attendees for an event.
    """
    registrations = (
        User.query.with_entities(User.name, User.email).join(Registration).filter(Registration.event_id == event_id).all()
    )

    return [{"name": name, "email": email} for name, email in registrations] if registrations else []


def get_public_events(search_query, date_filter):
    """
    Get all public events with search and filter functionality.
    """
    query = Event.query.filter_by(is_public=True)

    if search_query:
        query = query.filter(Event.name.ilike(f"%{search_query}%"))

    if date_filter == "today":
        query = query.filter(Event.date == datetime.today().date())

    elif date_filter == "tomorrow":
        query = query.filter(Event.date == (datetime.today() + timedelta(days=1)).date())

    elif date_filter == "week":
        start_of_week = datetime.today() - timedelta(days=datetime.today().weekday())
        end_of_week = start_of_week + timedelta(days=6)
        query = query.filter(Event.date.between(start_of_week.date(), end_of_week.date()))

    elif date_filter == "month":
        start_of_month = datetime.today().replace(day=1)
        end_of_month = start_of_month.replace(month=start_of_month.month % 12 + 1, day=1) - timedelta(days=1)
        query = query.filter(Event.date.between(start_of_month.date(), end_of_month.date()))

    return query.order_by(Event.date.desc()).all()


def check_user_registration(user_id, event_id):
    """
    Check if a user is already registered for an event.
    """
    registration = Registration.query.filter_by(user_id=user_id, event_id=event_id).first()
    return registration is not None


def register_user_for_event(user_id, event_id):
    """
    Register a user for an event.
    """
    registration = Registration()
    registration.user_id = user_id
    registration.event_id = event_id
    db.session.add(registration)
    db.session.commit()
    return registration


def cancel_registration(user_id, event_id):
    """
    Cancel a user's registration for an event.
    """
    registration = Registration.query.filter_by(user_id=user_id, event_id=event_id).first()
    if registration:
        db.session.delete(registration)
        db.session.commit()
        return True
    return False
