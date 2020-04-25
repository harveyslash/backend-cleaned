def get_metric_from_tag(tag_string):
    assert 'metric' in tag_string
    return float(tag_string.split("-")[-1])
