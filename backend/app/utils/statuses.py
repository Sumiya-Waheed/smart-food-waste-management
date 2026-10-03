DONATION_STATUSES = {
    "available",
    "reserved",
    "collection_confirmed",
    "collected",
    "completed",
    "cancelled",
    "expired",
}


DONATION_REQUEST_STATUSES = {
    "pending",
    "accepted",
    "rejected",
    "cancelled",
    "collection_confirmed",
    "collected",
    "completed",
}


DONATION_STATUS_TRANSITIONS = {
    "available": [
        "reserved",
        "cancelled",
        "expired",
    ],
    "reserved": [
        "collection_confirmed",
        "cancelled",
    ],
    "collection_confirmed": [
        "collected",
        "cancelled",
    ],
    "collected": [
        "completed",
    ],
    "completed": [],
    "cancelled": [],
    "expired": [],
}


DONATION_REQUEST_STATUS_TRANSITIONS = {
    "pending": [
        "accepted",
        "rejected",
        "cancelled",
    ],
    "accepted": [
        "collection_confirmed",
        "cancelled",
    ],
    "collection_confirmed": [
        "collected",
        "cancelled",
    ],
    "collected": [
        "completed",
    ],
    "rejected": [],
    "cancelled": [],
    "completed": [],
}