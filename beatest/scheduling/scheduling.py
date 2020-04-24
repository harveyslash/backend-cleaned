from datetime import timedelta

scheduling_config = {

    "testing": {
        "schedule": timedelta(seconds=10000),
        "task": "controllers.apiv01.routes.add_numer",
        "args": ()
    },

    "boo": {
        "schedule": timedelta(seconds=300),
        "task": "schedules.update_college_test_table.update_college_tests",
        "args": ()
    },

}
