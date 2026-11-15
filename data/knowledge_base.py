KNOWN_FIXES = {
    "AV / Classroom Hardware": {
        "fix_id": "KB-401",
        "solution": "Check master wall power switch, cycle HDMI matrix switcher, or deploy portable backup projector.",
        "avg_resolution_mins": 12
    },
    "Software / Licensing": {
        "fix_id": "KB-112",
        "solution": "Connect to Campus VPN before launching MATLAB installer and select 'Campus Concurrent License'.",
        "avg_resolution_mins": 15
    },
    "Network / Wi-Fi": {
        "fix_id": "KB-305",
        "solution": "Check core distribution switch in IDF closet; reboot PoE access points if controller shows heartbeat loss.",
        "avg_resolution_mins": 40
    }
}

SERVICE_STATUS = {
    "AV_LectureHall_302": {"status": "DEGRADED", "last_checked": "2 mins ago", "active_alerts": 1},
    "Campus_Software_Portal": {"status": "OPERATIONAL", "last_checked": "1 min ago", "active_alerts": 0},
    "Eduroam_Eng_Building": {"status": "WARNING - HIGH PACKET LOSS", "last_checked": "Just now", "active_alerts": 4}
}

SUPPORT_POLICIES = {
    "P1 - Critical": "SLA: 15 mins. Immediate dispatch to Field Support / Tier-2 Engineering. Mandatory if active class is disrupted.",
    "P2 - High": "SLA: 1 hour. Assign to Tier-2 Network/Systems queue. Request missing diagnostics if report completeness < 50%.",
    "P3 - Normal": "SLA: 24 hours. Assign to Tier-1 Helpdesk or send self-service Knowledge Base article."
}
