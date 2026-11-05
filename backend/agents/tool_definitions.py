TRAVEL_TOOLS = [

    {
        "type": "function",
        "function": {
            "name": "search_destination",
            "description": "Find destination information, attractions and estimated activity costs.",
            "parameters": {
                "type": "object",
                "properties": {
                    "destination": {
                        "type": "string"
                    }
                },
                "required": ["destination"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "search_hotels",
            "description": "Find accommodation matching the user's preference.",
            "parameters": {
                "type": "object",
                "properties": {
                    "destination": {
                        "type": "string"
                    },
                    "preference": {
                        "type": "string",
                        "enum": ["budget", "comfortable", "luxury"]
                    }
                },
                "required": ["destination", "preference"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "search_transport",
            "description": "Find estimated round-trip transport costs per person.",
            "parameters": {
                "type": "object",
                "properties": {
                    "destination": {
                        "type": "string"
                    },
                    "origin": {
                        "type": "string"
                    },
                    "travelers": {
                        "type": "integer"
                    }
                },
                "required": [
                    "destination",
                    "origin",
                    "travelers"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "calculate_budget",
            "description": "Calculate the complete estimated trip budget using the retrieved costs.",
            "parameters": {
                "type": "object",
                "properties": {
                    "hotel_price_per_night": {
                        "type": "number"
                    },
                    "duration_days": {
                        "type": "integer"
                    },
                    "travelers": {
                        "type": "integer"
                    },
                    "transport_per_person": {
                        "type": "number"
                    },
                    "food_per_person_per_day": {
                        "type": "number"
                    },
                    "activities_per_person": {
                        "type": "number"
                    },
                    "local_transport": {
                        "type": "number"
                    }
                },
                "required": [
                    "hotel_price_per_night",
                    "duration_days",
                    "travelers",
                    "transport_per_person",
                    "food_per_person_per_day",
                    "activities_per_person",
                    "local_transport"
                ]
            }
        }
    },

{
    "type": "function",
    "function": {
        "name": "search_travel_knowledge",
        "description": (
            "Search the travel knowledge base for destination guides, "
            "travel policies, hotel rules, availability limitations "
            "and other travel information."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The travel information to search for."
                },
                "top_k": {
                    "type": "integer",
                    "description": "Number of relevant document chunks to retrieve."
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
}

]