from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.crud import (
    cancel_registration,
    check_user_registration,
    create_new_event,
    delete_event_by_id,
    get_attendees_contact_info,
    get_event_by_id,
    get_event_organizer_info,
    get_public_events,
    get_user_events,
    is_current_user_event,
    number_of_attendees,
    register_user_for_event,
    update_event,
)
from app.file_utils import save_file
from app.forms.event import EventForm, EventIdForm, RegistrationForm

event_routes = Blueprint("event", __name__)


@event_routes.route("/public_events", methods=["GET"])
def public_events():
    """
    Handle displaying public events.
    """
    search_query = request.args.get("search", "")
    date_filter = request.args.get("date", "")

    public_events_list = get_public_events(search_query, date_filter)

    return render_template("./event/public_events.html", public_events_list=public_events_list)


@event_routes.route("/event/create", methods=["GET", "POST"])
@login_required  # Requires the user to be logged in
def create_event():
    """
    Handle event creation.
    """
    form = EventForm()

    if request.method == "POST":
        if form.validate_on_submit():
            image_path = save_file(form.image.data) if form.image.data else None
            create_new_event(current_user.id, form, image_path)
            flash("Event created successfully!", "success")
            return redirect(url_for("event.my_events"))

    return render_template("./event/create_event.html", form=form)


@event_routes.route("/event/edit_event/<int:event_id>", methods=["GET", "POST"])
@login_required
def edit_event(event_id):
    """
    Handle event editing.
    """

    if not is_current_user_event(current_user.id, event_id):
        flash("Invalid event ID or you don't have permission to delete this event.", "danger")
        return redirect(url_for("event.my_events"))

    event_info = get_event_by_id(event_id)
    if not event_info:
        flash("Event not found.", "danger")
        return redirect(url_for("event.my_events"))

    if request.method == "POST":
        form = EventForm()
        if form.validate_on_submit():
            image_path = save_file(form.image.data) if form.image.data else None
            update_event(event_id, form, image_path)
            flash("Event updated successfully!", "success")
            return redirect(url_for("event.my_events"))

    else:
        form = EventForm(obj=event_info)

    return render_template("./event/edit_event.html", form=form, event_info=event_info)


@event_routes.route("/event/my_events", methods=["GET"])
@login_required
def my_events():
    """
    Handle displaying user's events.
    """
    my_events_list = get_user_events(current_user.id)
    return render_template("./event/my_events.html", my_events_list=my_events_list)


@event_routes.route("/event/my_events/<int:event_id>", methods=["GET", "POST"])
@login_required
def my_event_details(event_id):
    """
    Handle event details and registration.
    """
    # Check if the event belongs to the current user
    if not is_current_user_event(current_user.id, event_id):
        flash("Invalid event ID", "danger")
        return redirect(url_for("event.my_events"))

    event_info = get_event_by_id(event_id)
    attendees_count = number_of_attendees(event_id)
    attendees_contact_info = get_attendees_contact_info(event_id)
    organizer_info = get_event_organizer_info(event_id)

    form = EventIdForm()

    return render_template(
        "./event/my_event_details.html",
        form=form,
        event_info=event_info,
        organizer_info=organizer_info,
        attendees_count=attendees_count,
        attendees_contact_info=attendees_contact_info,
    )


@event_routes.route("/event/delete_event/<int:event_id>", methods=["POST"])
@login_required
def delete_event(event_id):
    """
    Handle event deletion.
    """

    form = EventIdForm()

    if not form.validate_on_submit():
        flash("Form validation failed. Please check your inputs.", "danger")
        return redirect(url_for("event.my_event_details", event_id=event_id))

    if not is_current_user_event(current_user.id, event_id):
        flash("Invalid event ID or you don't have permission to delete this event.", "danger")
        return redirect(url_for("event.my_events"))

    result = delete_event_by_id(event_id)

    if not result:
        flash("Event deletion failed.", "danger")
    else:
        flash("Event deleted successfully.", "success")

    return redirect(url_for("event.my_events"))


@event_routes.route("/event/<int:event_id>", methods=["GET", "POST"])
@login_required
def event_details(event_id):
    """
    Handle event details and registration.
    """

    registration_form = RegistrationForm()

    event_info = get_event_by_id(event_id)
    attendees_count = number_of_attendees(event_id)
    organizer_info = get_event_organizer_info(event_id)

    return render_template(
        "./event/event_details.html",
        event_info=event_info,
        organizer_info=organizer_info,
        attendees_count=attendees_count,
        registration_form=registration_form,
    )


@event_routes.route("/event/register_for_event/<int:event_id>", methods=["POST"])
@login_required
def register_for_event(event_id):
    """
    Handle user registration for an event.
    """
    registration_form = RegistrationForm()

    if not registration_form.validate_on_submit():
        flash("Form validation failed. Please check your inputs.", "error")
        return redirect(url_for("event.event_details", event_id=event_id))

    if check_user_registration(current_user.id, event_id):
        flash("You are already registered for this event.", "error")
        return redirect(url_for("event.event_details", event_id=event_id))

    registration = register_user_for_event(current_user.id, event_id)

    if not registration:
        flash("Failed to join the event.", "error")
        return redirect(url_for("event.event_details", event_id=event_id))

    flash("Successfully joined the event!", "success")
    return redirect(url_for("event.event_details", event_id=event_id))


@event_routes.route("/event/cancel_registration/<int:event_id>", methods=["POST"])
@login_required
def cancel_registration_for_event(event_id):
    """
    Handle user un-registration from an event.
    """
    form = RegistrationForm()

    if not form.validate_on_submit():
        flash("Form validation failed. Please check your inputs.", "error")
        return redirect(url_for("event.event_details", event_id=event_id))

    if not check_user_registration(current_user.id, event_id):
        flash("You are not registered for this event.", "error")
        return redirect(url_for("event.event_details", event_id=event_id))

    registration = cancel_registration(current_user.id, event_id)

    if not registration:
        flash("Failed to leave the event.", "error")
        return redirect(url_for("event.event_details", event_id=event_id))

    flash("Successfully left the event!", "success")
    return redirect(url_for("event.event_details", event_id=event_id))
