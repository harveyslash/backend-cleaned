def get_algorithmic_sense(test_attempt_query):
    algo_metric_scores = []
    difficulty_scores = []
    was_correct_vals = []
    coding_scores = []
    max_coding_scores = []

    for section_attempt in test_attempt_query['section_attempts']:
        for question_attempt in section_attempt['question_attempts']:

            question = question_attempt['question']
            tags = question['tags']

            algo_value = None
            difficulty_score = None

            for tag in tags:
                tag_name = tag['name']

                if tag_name[:4] == "f-13":
                    algo_value = tag_name.split("-")[-1]

                    try:
                        algo_value = float(algo_value)
                    except ValueError:
                        algo_value = None
                        pass

                if tag_name[:4] == "f-12":
                    difficulty_score = tag_name.split("-")[-1]

                    try:
                        difficulty_score = float(difficulty_score)
                    except:
                        difficulty_score = None
                        pass

            algo_metric_scores.append(algo_value)
            difficulty_scores.append(difficulty_score)

            ques_type = question['type']
            was_correct = question_attempt['was_correct']

            if ques_type == "CODING":
                coding_score = question_attempt['score']
                max_coding_score = question['points_correct']
                try:
                    coding_score = float(coding_score)
                except:
                    coding_score = None
                    pass

                coding_scores.append(coding_score)

                try:
                    max_coding_score = float(max_coding_score)
                except:
                    max_coding_score = None
                    pass

                max_coding_scores.append(max_coding_score)
                was_correct_vals.append(True)          # There is no right or wrong for coding ques
            else:
                coding_scores.append(None)
                max_coding_scores.append(None)
                was_correct_vals.append(was_correct)

    total_possible_score = 0

    weighted_user_score = 0

    for algo_value, difficulty_score, coding_score, max_coding_score, was_correct in zip(
            algo_metric_scores, difficulty_scores, coding_scores, max_coding_scores, was_correct_vals):

        if algo_value is None or difficulty_score is None:
            continue

        if coding_score is None or max_coding_score is None:
            coding_score = 1
            max_coding_score = 1

        total_possible_score += algo_value * difficulty_score * max_coding_score

        if was_correct:
            weighted_user_score += algo_value * difficulty_score * coding_score

    if total_possible_score != 0:
        return weighted_user_score / total_possible_score
