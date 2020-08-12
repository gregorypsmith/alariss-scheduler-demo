from scheduler_app import zoom_client
from datetime import datetime
import json


def _generate_payload(interview_obj):
    time = int(interview_obj.client_selection)/1000
<<<<<<< HEAD
    time_payload = datetime.utcfromtimestamp(time).strftime('%Y-%m-%dT%H:%M:%S')
=======
    time_payload = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%S')
>>>>>>> 53db696b3b29ed75568c5ef8d889277a18ecaf73

    payload = {
        "topic": f"Interview for {interview_obj.position_name} {interview_obj.company_name}",
        "type": "2",
        "start_time": time_payload,
        "duration": "60",
        "timezone": "UTC",
        "password": "123",
        "agenda": f"Interview for {interview_obj.position_name} {interview_obj.company_name}",
        "settings": {
            "host_video": True,
            "participant_video": True,
            "join_before_host": True,
            "mute_upon_entry": True,
            "approval_type": 0
        }
    }

    return payload


def create_zoom_room(interview_obj):
    payload = _generate_payload(interview_obj)
    response = zoom_client.meeting.post_request("users/me/meetings", data=payload)
<<<<<<< HEAD
    print(json.loads(response.content))
=======
>>>>>>> 53db696b3b29ed75568c5ef8d889277a18ecaf73
    join_link = json.loads(response.content)["join_url"]
    return join_link