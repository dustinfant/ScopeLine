def technique(tid):
    mapping = {
        "T1190": {
            "id": "T1190",
            "name": "Exploit Public-Facing Application"
        },
        "T1552": {
            "id": "T1552",
            "name": "Unsecured Credentials"
        },
        "T1046": {
            "id": "T1046",
            "name": "Network Service Discovery"
        }
    }
    return mapping.get(tid, {})

