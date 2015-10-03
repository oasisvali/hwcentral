from core.data_models.question import build_question_part_from_data
from core.utils.json import HWCentralJsonResponse
from croupier.croupier_api import deal_subpart
from croupier.data_models import SubpartVariableConstraints


def croupier_failure_response(message):
    return HWCentralJsonResponse({
        'success': False,
        'message': message
    })


def croupier_success_response(data):
    return HWCentralJsonResponse({
        'success': True,
        'payload': data
    })


def deal_subpart_post(request):
    if 'subpart' not in request.POST:
        return croupier_failure_response('No subpart data provided')

    subpart_data = request.POST['subpart']

    try:
        subpart = build_question_part_from_data(subpart_data)
    except Exception, e:
        return croupier_failure_response('Malformed subpart data: %s' % e)

    try:
        variable_constraints = SubpartVariableConstraints(subpart_data.get('variable_constraints'))
    except Exception, e:
        return croupier_failure_response('Malformed variable constraints data: %s' % e)

    try:
        dealt_subpart = deal_subpart(subpart, variable_constraints)
    except Exception, e:
        return croupier_failure_response('Dealing error: %s' % e)

    return croupier_success_response(dealt_subpart)
