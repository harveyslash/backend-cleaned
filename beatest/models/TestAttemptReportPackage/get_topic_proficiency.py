def get_topic_proficiency(test_attempt_query, topic):
    analytical_metric_scores = []
    difficulty_scores = []
    was_correct_vals = []
    for section_attempt in test_attempt_query['section_attempts']:
        for question_attempt in section_attempt['question_attempts']:

            question = question_attempt['question']
            tags = question['tags']

            anal_value = None
            difficulty_score = None

            for tag in tags:

                tag_name = tag['name']

                if tag_name == topic:
                    anal_value = 1

                    try:
                        anal_value = float(anal_value)
                    except ValueError:
                        anal_value = None
                        pass

                if tag_name[:4] == "f-12":
                    difficulty_score = tag_name.split("-")[-1]

                    try:
                        difficulty_score = float(difficulty_score)
                    except:
                        difficulty_score = None
                        pass

            difficulty_scores.append(difficulty_score)
            analytical_metric_scores.append(anal_value)

            was_correct = question_attempt['was_correct']
            was_correct_vals.append(was_correct)

    total_possible_score = 0

    weighted_user_score = 0

    for anal_value, difficulty_score, was_correct in zip(
            analytical_metric_scores, difficulty_scores, was_correct_vals):

        # print(anal_value)
        # print(difficulty_score)
        # print(was_correct)

        if anal_value is None or difficulty_score is None:
            continue

        total_possible_score += anal_value * difficulty_score

        if was_correct:
            weighted_user_score += anal_value * difficulty_score

    if total_possible_score != 0:
        return weighted_user_score / total_possible_score
