from datetime import datetime

from flask import session, request

PING_DURATION = 30
PING_TOLERANCE = .5

PING_WARNING_GRACE = 30  # in seconds. if the diff is less than this, but more than
# normal ping diff, warning count will go up

PING_WARNING_COUNTS = 10
# max number of warnings before raising error

PING_GRACE = 10

PENALTY = PING_DURATION

PING_TIME_FAIL_CODE = "PF666"
PING_FAIL_TRY_AGAIN = "PF6969"

PING_ALREADY_MOVED_ON = "PF0253"


def get_string_from_data(test_id, section_id, jumps_allowed, time_of_ping,
                         warn_count):
    assert test_id
    assert section_id
    assert time_of_ping
    assert warn_count >= 0

    return f"{test_id}-{section_id}-{jumps_allowed}-{time_of_ping}-{warn_count}"


def split_pinger_string():
    return request.headers['ping'].split("-")

    return session['ping'].split("-")


def validate_ping_time():
    data = split_pinger_string()

    data[0] = int(data[0])
    data[1] = int(data[1])
    data[2] = data[2] == "True"
    data[3] = float(data[3])
    data[4] = int(data[4])
    # print(data)

    _, _, _, time, _ = data

    time = float(time)

    diff = (datetime.now() - datetime.fromtimestamp(time)).total_seconds()

    # print("DIFF")
    # print(diff)

    # return data

    if diff > PING_DURATION + PING_DURATION * PING_TOLERANCE:
        # print("encountered")
        # print("diff")
        # print(diff)

        # outside ping duration but inside warning grace
        if diff < PING_WARNING_GRACE:
            # print("got here")

            # if there number of warnings are less than max allowed warnings
            if data[4] <= PING_WARNING_COUNTS:
                data[4] += 1
                return data
            else:
                raise ValueError

        raise ValueError

    return data


def push_data_to_session(string):
    return
    session['ping'] = string


def push_data_from_data(test_id, section_id, jumps_allowed, time_of_ping,
                        warn_count):
    string = get_string_from_data(test_id, section_id, jumps_allowed,
                                  time_of_ping, warn_count)
    # print("pushing this data")
    # print(string)
    push_data_to_session(string)

    return string
