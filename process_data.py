import json
import csv


def build_event_row(event):
    """
    Takes event object from json and returns a dict of fields to upload.
    """
    if event:
        return {
            "id": event.get("id"),
            "contact_id": event.get("contact"),
            "sponsor_id": event.get("sponsor"),
            "location": event.get("location"),
            "title": event.get("title"),
            "description": event.get("description"),
            "featured_image_url": event.get("featured_image_url"),
            "high_priority": event.get("high_priority"),
            "timeslots": event.get("timeslots"),
            "location": event.get("location"),
            "timezone": event.get("timezone"),
            "event_type": event.get("event_type"),
            "browser_url": event.get("browser_url"),
            "visibility": event.get("visibility"),
            "address_visibility": event.get("address_visibility"),
            "created_by_volunteer_host": event.get("created_by_volunteer_host"),
            "is_virtual": event.get("is_virtual"),
            "virtual_action_url": event.get("virtual_action_url"),
            "accessibility_status": event.get("accessibility_status"),
            "accessibility_notes": event.get("accessibility_notes"),
            "tags": event.get("tags"),
            "approval_status": event.get("approval_status"),
            "event_campaign": event.get("event_campaign"),
            "instructions": event.get("instructions"),
            "created_date": event.get("created_date"),
            "modified_date": event.get("modified_date"),
        }


def build_timeslot_row(timeslot):
    """
    Takes a timeslot object from json and returns a dict of fields to upload.
    """
    if timeslot:
        return {
            "id": timeslot["id"],
            "start_date": timeslot["start_date"],
            "end_date": timeslot["end_date"],
            "is_full": timeslot["is_full"],
            "instructions": timeslot["instructions"],
        }

def build_people_row(person):
    """
    Takes a person object from json and returns a dict of fields to upload.

    This function is really just here to ensure a specific order of fields.
    """
    if person:
        return {
            "id": person["user_id"],
            "created_date": person["created_date"],
            "modified_date": person["modified_date"],
            "given_name": person["given_name"],
            "family_name": person["family_name"],
            "email_addresses": person["email_addresses"],
            "phone_numbers": person["phone_numbers"],
            "postal_addresses": person["postal_addresses"],
            "sms_opt_in_status": person["sms_opt_in_status"],
            "blocked_date": person["blocked_date"],
        }


def build_attendance_row(attendance):
    """
    Takes an attendance object from json and returns a dict of fields to upload.
    """
    if attendance:
        return {
            "id": attendance.get("id"),
            "created_date": attendance.get("created_date"),
            "modified_date": attendance.get("modified_date"),
            "person_id": attendance.get("person").get("id") if attendance.get("person") else None,
            "event_id": attendance.get("event").get("id") if attendance.get("event") else None,
            "timeslot_id": attendance.get("timeslot").get("id") if attendance.get("timeslot") else None,
            "sponsor_id": attendance.get("sponsor").get("id") if attendance.get("sponsor") else None,
            "status": attendance.get("status"),
            "attended": attendance.get("attended"),
            "referrer_id": attendance.get("referrer").get("id") if attendance.get("referrer") else None,
            "custom_signup_field_values": attendance.get("custom_signup_field_values"),
        }


attendances = {}
# Open attendances JSON file
with open("data/attendances.json") as f:
    attendances = json.loads(f.read())

# write events
with open("output/events.csv", "w") as event_file:
    writer = csv.writer(event_file)

    # write the header
    header = build_event_row(attendances[0]["event"]).keys()
    writer.writerow(header)

    for attendance in attendances:
        event_row = build_event_row(attendance.get("event"))

        # if there's an event in this attendance, write it
        if event_row is not None:
            writer.writerow(event_row.values())

# write timeslots
with open("output/timeslots.csv", "w") as timeslot_file:
    writer = csv.writer(timeslot_file)

    # write the header
    header = build_timeslot_row(attendances[0]["timeslot"]).keys()
    writer.writerow(header)

    for attendance in attendances:
        timeslot_row = build_timeslot_row(attendance.get("timeslot"))

        # if there's a timeslot in this attendance, write it
        if timeslot_row:
            writer.writerow(timeslot_row.values())

# write people
with open("output/people.csv", "w") as people_file:
    writer = csv.writer(people_file)

    # write the header
    header = build_people_row(attendances[0]["person"]).keys()
    writer.writerow(header)

    for attendance in attendances:
        person_row = build_people_row(attendance.get("person"))

        # if there's a people in this attendance, write it
        if person_row:
            writer.writerow(person_row.values())

# write people
with open("output/attendances.csv", "w") as people_file:
    writer = csv.writer(people_file)

    # write the header
    header = build_attendance_row(attendances[0]["person"]).keys()
    writer.writerow(header)

    for attendance in attendances:
        attendance_row = build_attendance_row(attendance)

        # if there's a people in this attendance, write it
        if attendance_row:
            writer.writerow(attendance_row.values())

print("processed", len(attendances), "attendances")
