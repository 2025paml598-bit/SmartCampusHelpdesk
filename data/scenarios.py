SCENARIOS = {
    "Scenario A: Critical Classroom Failure": {
        "ticket_id": "TKT-101",
        "title": "Classroom 302 Projector Dead Before Lecture",
        "description": "The main projector in Lecture Hall 302 will not power on. A class of 120 students starts in 10 minutes.",
        "category": "AV / Classroom Hardware",
        "location": "Lecture Hall 302",
        "affected_users": 120,
        "minutes_until_event": 10,
        "report_completeness": 0.95,
        "has_workaround": False,
        "service_name": "AV_LectureHall_302",
        "reporter_role": "Faculty"
    },
    "Scenario B: Normal Single-User Issue": {
        "ticket_id": "TKT-102",
        "title": "MATLAB Installation Error on Personal Laptop",
        "description": "Student getting license activation error code -9 when installing MATLAB on Windows 11 personal laptop.",
        "category": "Software / Licensing",
        "location": "Dormitory / Off-Campus",
        "affected_users": 1,
        "minutes_until_event": 1440,
        "report_completeness": 0.90,
        "has_workaround": True,
        "service_name": "Campus_Software_Portal",
        "reporter_role": "Student"
    },
    "Scenario C: Ambiguous Campus Wi-Fi Outage": {
        "ticket_id": "TKT-103",
        "title": "Wi-Fi Down in Engineering Building?",
        "description": "Three tickets arrived saying 'internet not working' in Science & Engineering Hall. No room numbers or error codes provided.",
        "category": "Network / Wi-Fi",
        "location": "Science & Engineering Hall",
        "affected_users": 45,
        "minutes_until_event": 30,
        "report_completeness": 0.35,
        "has_workaround": False,
        "service_name": "Eduroam_Eng_Building",
        "reporter_role": "Multiple Students"
    }
}
