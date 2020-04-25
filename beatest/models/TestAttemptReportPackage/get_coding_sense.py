import lizard


def get_coding_sense(test_attempt_query):
    avg_cyclomatic_complexity = []
    difficulty_scores = []
    for section_attempt in test_attempt_query['section_attempts']:
        for question_attempt in section_attempt['question_attempts']:

            question = question_attempt['question']
            ques_type = question['type']
            if ques_type == "CODING":
                if question_attempt['long_answer'] is None:
                    avg_cyc = None
                    continue
                tags = question['tags']
                difficulty_score = None

                for tag in tags:
                    tag_name = tag['name']

                    if tag_name[:4] == "f-12":
                        difficulty_score = tag_name.split("-")[-1]

                        try:
                            difficulty_score = float(difficulty_score)
                        except:
                            difficulty_score = None
                            pass
                difficulty_scores.append(difficulty_score)

                #fixme support all languages
                i = lizard.analyze_file.analyze_source_code("AllTests.java", question_attempt['long_answer'])
                avg_cyc = i.average_cyclomatic_complexity
                avg_cyclomatic_complexity.append(avg_cyc)

    total_possible_score = 0

    weighted_user_score = 0

    for avg_cyc, difficulty_score in zip(
            avg_cyclomatic_complexity, difficulty_scores):

        if avg_cyc is None or difficulty_score is None:
            continue

        weighted_user_score += (1 / (avg_cyc * difficulty_score))
        total_possible_score += (1 / difficulty_score)

    if total_possible_score != 0:
        return weighted_user_score / total_possible_score
