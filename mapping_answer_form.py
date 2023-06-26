import json
def mapping_answer(data_payload):
    """
    result is:[
        {
            questions: string
            answer: string/integer
        }
    ]
    """
    questions_list = data_payload['view']['blocks']
    answer_objects = data_payload['view']['state']['values']
    result_answer = []
    for question in questions_list:
        id_question = question['block_id']
        action_id = question['element']['action_id']
        answer_object = answer_objects.get(id_question)
        answer_value = answer_object.get(action_id)
        if action_id == 'static_select-action':
            result_answer.append({question['label']['text']:answer_value['selected_option']['value']})
        else:
            result_answer.append({question['label']['text']:answer_value['value']})
    return result_answer

