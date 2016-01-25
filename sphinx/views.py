import json

from core.data_models.question import build_question_subpart_from_data
from core.utils.json import HWCentralJsonResponse
from croupier.constraints import SubpartVariableConstraints
from croupier.croupier_api import deal_subpart


def sphinx_failure_response(message):
    return HWCentralJsonResponse({
        'success': False,
        'message': message
    })


def sphinx_success_response(data):
    return HWCentralJsonResponse({
        'success': True,
        'payload': data
    })


# TODO: this should actually be a GET?
def deal_subpart_post(request):
    request_data = json.loads(request.body)  # ajax post data has to be accessed here instead of request.POST

    if 'subpart' not in request_data:
        return sphinx_failure_response('No subpart data provided')

    subpart_data = request_data['subpart']

    try:
        subpart = build_question_subpart_from_data(subpart_data)
    except Exception, e:
        return sphinx_failure_response('Malformed subpart data: %s' % e)

    variable_constraints_data = subpart_data.get('variable_constraints')

    try:
        variable_constraints = SubpartVariableConstraints(variable_constraints_data)
    except Exception, e:
        return sphinx_failure_response('Malformed variable constraints data: %s' % e)

    try:
        dealt_subpart = deal_subpart(subpart, variable_constraints)
    except Exception, e:
        return sphinx_failure_response('Dealing error: %s' % e)

    # return in form useful for sphinx users
    if variable_constraints_data is not None:
        setattr(dealt_subpart, 'variable_constraints', variable_constraints_data)

    return sphinx_success_response(dealt_subpart)
