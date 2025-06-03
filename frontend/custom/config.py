#!/usr/bin/env python3
import os

# Mandatory variables
DEFAULT_ROWS = int(os.environ.get("DEFAULT_ROWS", 20))

CORE_MAP = {
    # resource name -> solr core name
    "item": "casebooks",
}
facets = {
    "f1-astrologer": {
        "type": "terms",
        "field": "facet-astrologer",
        "limit": 20,
        "sort": {"index": "asc"},
        "nested": True,
        "max_depth": 1
    },
    "f1-date": {
        "type": "terms",
        "field": "facet-date",
        "limit": 20,
        "sort": {"index": "asc"},
        "nested": True,
        "max_depth": 3
    },
    "f1-document-type": {
        "type": "terms",
        "field": "facet-document-type",
        "limit": 20,
        "sort": {"index": "asc"},
        "nested": True,
        "max_depth": 3
    },
    "f1-entity-age-band": {
        "type": "terms",
        "field": "facet-entity-age-band",
        "limit": 20,
        "sort": {"index": "asc"},
        "nested": True,
        "max_depth": 1
    },
    "f1-entity-question-asked": {
        "type": "terms",
        "field": "facet-entity-question-asked",
        "limit": 20,
        "sort": {"index": "asc"},
        "nested": True,
        "max_depth": 3
    },
    "f1-how-did-it-take-place": {
        "type": "terms",
        "field": "facet-how-did-it-take-place",
        "limit": 20,
        "sort": {"index": "asc"},
        "nested": True,
        "max_depth": 1
    },
    "f1-identified-entity-role": {
        "type": "terms",
        "field": "facet-identified-entity-role",
        "limit": 20,
        "sort": {"index": "asc"},
        "nested": True,
        "max_depth": 3
    },
    "f1-info": {
        "type": "terms",
        "field": "facet-info",
        "limit": 20,
        "sort": {"index": "asc"},
        "nested": True,
        "max_depth": 3
    },
    "f1-occupation": {
        "type": "terms",
        "field": "facet-occupation",
        "limit": 20,
        "sort": {"index": "asc"},
        "nested": True,
        "max_depth": 2
    },
    "f1-patient-age-band": {
        "type": "terms",
        "field": "facet-patient-age-band",
        "limit": 20,
        "sort": {"index": "asc"},
        "nested": True,
        "max_depth": 1
    },
    "f1-practitioner": {
        "type": "terms",
        "field": "facet-practitioner",
        "limit": 20,
        "sort": {"index": "asc"},
        "nested": True,
        "max_depth": 1
    },
    "f1-querent-age-band": {
        "type": "terms",
        "field": "facet-querent-age-band",
        "limit": 20,
        "sort": {"index": "asc"},
        "nested": True,
        "max_depth": 1
    },
    "f1-question-asked": {
        "type": "terms",
        "field": "facet-question-asked",
        "limit": 20,
        "sort": {"index": "asc"},
        "nested": True,
        "max_depth": 3
    },
    "f1-residence": {
        "type": "terms",
        "field": "facet-residence",
        "limit": 20,
        "sort": {"index": "asc"},
        "nested": True,
        "max_depth": 4
    },
    "f1-time-of-day": {
        "type": "terms",
        "field": "facet-time-of-day",
        "limit": 20,
        "sort": {"index": "asc"},
        "nested": True,
        "max_depth": 2
    },
}
facet_query = {
    "facet": {
        "f1-document-type": {
            "type": "terms",
            "field": "facet-document-type",
            "limit": 10,
            "sort": {"index": "asc"}
        },
        "f1-author": {
            "type": "terms",
            "field": "facet-author",
            "limit": 5,
            "sort": {"count": "desc"}
        },
        "f1-addressee": {
            "type": "terms",
            "field": "facet-addressee",
            "limit": 5,
            "sort": {"count": "desc"}
        },
        "f1-correspondent": {
            "type": "terms",
            "field": "facet-correspondent",
            "limit": 5,
            "sort": {"count": "desc"}
        },
        "f1-repository": {
            "type": "terms",
            "field": "facet-repository",
            "limit": 5,
            "sort": {"index": "asc"}
        },
        "f1-contributor": {
            "type": "terms",
            "field": "facet-contributor",
            "limit": 99,
            "sort": {"index": "asc"}
        },
        ".env": {
            "type": "terms",
            "field": "facet-transcription-available",
            "limit": 5,
            "sort": {"index": "desc"}
        },
        "f1-cdl-images-linked": {
            "type": "terms",
            "field": "facet-cdl-images-linked",
            "limit": 5,
            "sort": {"index": "desc"}
        },
        "f1-astrologer": {
            "type": "terms",
            "field": "facet-astrologer",
            "limit": 20,
            "sort": {"index": "asc"},
            "nested": True,
            "max_depth": 1
        },
        "f1-decade": {
            "type": "terms",
            "field": "facet-decade",
            "limit": 100,
            "sort": {"index": "asc"},
            "facet": {
                "f1-decade-year": {
                    "type": "terms",
                    "field": "facet-decade-year",
                    "limit": 20,
                    "sort": {"index": "asc"},
                    "facet": {
                        "f1-decade-year-month": {
                            "type": "terms",
                            "field": "facet-decade-year-month",
                            "limit": 24,
                            "sort": {"index": "asc"},
                            "facet": {
                                "f1-decade-year-month-day": {
                                    "type": "terms",
                                    "field": "facet-decade-year-month-day",
                                    "limit": 62,
                                    "sort": {"index": "asc"}
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
