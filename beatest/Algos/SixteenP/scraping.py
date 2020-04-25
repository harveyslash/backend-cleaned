import json

from bs4 import BeautifulSoup

from Algos.SixteenP.questionIDto16Map import question_id_map
import requests

from requests.adapters import HTTPAdapter

from models import QuestionAttempt, Question


def prepare_data_for_16_p(answer_dict):
    """
    prepare data to be sent to 16p

    :param answer_dict: a dict in the form of
    {question_id:response_value}

    where response_value is the range -3,3 and can be null

    :return:
    """

    data_dict = {"questions": []}

    for key in answer_dict.keys():
        if key not in question_id_map:
            del key

    sorted_dict_by_values = sorted(question_id_map, key=question_id_map.get)

    for question_id in sorted_dict_by_values:
        data_dict['questions'].append({
            "text": "",
            "answer": answer_dict[question_id]
        })

    # for key, val in answer_dict.items():
    #     data_dict['questions'].append({
    #         "text": question_id_map[key],
    #         "answer": val
    #     })

    # print(data_dict)
    return data_dict


def prepare_data_from_question_attempts(question_attempts_array):
    response_dict = {}
    has_sixteen_p_questions = False

    for question_attempt in question_attempts_array:

        # question_attempt = QuestionAttempt(question_attempt)
        question = question_attempt.question

        if question_attempt.question_id in question_id_map:
            has_sixteen_p_questions = True
            value = None

            if question_attempt.choice_id is not None:

                sorted_choice_ids = list(
                        sorted(map(lambda x: x.id,
                                   question.choices)))

                index = sorted_choice_ids.index(question_attempt.choice_id)

                if index > -1:
                    value = index - 3
                    value = -1 * value

            response_dict[question.id] = value

    if not has_sixteen_p_questions:
        return None

    return response_dict


def scrape(question_attempts_array):
    prepared_from_attempts = prepare_data_from_question_attempts(
            question_attempts_array)

    if prepared_from_attempts is None:
        return None

    final_prepared_data = prepare_data_for_16_p(prepared_from_attempts)
    # print(final_prepared_data)
    # return

    output_dict = {}

    http_proxy = "socks5://13.234.194.19:9050"
    proxyDict = {
        "http": http_proxy,
        "https": http_proxy,
    }
    s = requests.session()
    s.proxies.update(proxyDict)
    s.mount('http://', HTTPAdapter(max_retries=10))
    s.mount('https://', HTTPAdapter(max_retries=10))

    s.keep_alive = False

    r = s.get("https://www.16personalities.com/free-personality-test")
    r = s.post(url="https://www.16personalities.com/test-results",

               headers={
                   "Content-Type": "application/json; charset=utf-8",
                   "User-Agent": "Mozilla/5.0"

               },

               data=json.dumps(final_prepared_data
                               ))

    r = s.get("https://www.16personalities.com/members-area")

    soup = BeautifulSoup(r.text, features='lxml')

    personality_type = role = strategy = None

    info = soup.find("table", {"class": "info-table"})
    rows = info.findAll("tr")

    for i, row in enumerate(rows):
        if i == 0:
            personality_type = row.find("a").text

        if i == 1:
            pass

        if i == 2:
            role = row.find("a").text

        if i == 3:
            strategy = row.find("a").text

    # print(personality_type, role, strategy)

    output_dict['personality_type'] = personality_type
    output_dict['role'] = role
    output_dict['strategy'] = strategy

    traits = soup.findAll("div", {"class": "trait-scales comp"})[0]

    for i, trait in enumerate(traits.findAll("div", {"class": "trait"})):

        caption = trait.find("div", {"class", "caption"}).text
        tagline = trait.find("div", {"class", "tagline"}).text
        percentage = trait.find("div", {"class", "percentage"}).text.replace(
                "%", "")
        left = trait.find("div", {"class", "left"}).text
        right = _get_right_element(trait).text
        explanation = trait.find("div", {"class", "explanation"}).text
        explanation = explanation.replace(" Read more", "")

        caption = caption.strip()
        tagline = tagline.strip()
        percentage = percentage.strip()
        left = left.strip()
        right = right.strip()
        explanation = explanation.strip()

        if i == 0:
            output_dict['mind_value'] = percentage
            output_dict['mind_text'] = explanation

        if i == 1:
            output_dict['energy_value'] = percentage
            output_dict['energy_text'] = explanation

        if i == 2:
            output_dict['nature_value'] = percentage
            output_dict['nature_text'] = explanation

        if i == 3:
            output_dict['tactics_value'] = percentage
            output_dict['tactics_text'] = explanation

        if i == 4:
            output_dict['identity_value'] = percentage
            output_dict['identity_text'] = explanation

    return output_dict


def _get_right_element(trait):
    right = trait.findAll("div", class_=["title"])

    for el in right:
        if "right" in el.get("class"):
            return el
