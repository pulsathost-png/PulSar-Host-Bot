PLANS = {
    "START": {
        "price": 50,
        "ram": "2 GB",
        "cpu": "1 ядро"
    },

    "PRO": {
        "price": 100,
        "ram": "4 GB",
        "cpu": "2 ядра"
    },

    "ULTRA": {
        "price": 500,
        "ram": "8 GB",
        "cpu": "4 ядра"
    }
}


def get_plan(name):
    return PLANS.get(name)
