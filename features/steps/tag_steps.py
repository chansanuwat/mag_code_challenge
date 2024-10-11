from lib.debug_request import DebugRequest
import requests

@given(u'tags exist with')
def step_impl(context):
    data = []
    for row in context.table:
        this_tag = {"name": row["name"]}
        if row["minutely_budget"]:
            this_tag["minutelyBudget"] = int(row["minutely_budget"])
        if row["allowed_countries"]:
            this_tag["allowedCountries"] = row["allowed_countries"].split(',')
        data.append(this_tag)
    context.tag_manager.create_tags(data)

@when(u'a request to debug is made with "{params}"')
def step_impl(context, params):
    context.debug_request = DebugRequest(context.config.userdata["host"])
    context.debug_request.get(params)

@when(u'the tags impression pixel is requested')
def step_impl(context):
    requests.get(context.debug_request.get_pixel_url())

@when(u'the tags impression pixel is requested again')
def step_impl(context):
    context.execute_steps(u"When the tags impression pixel is requested")


@then(u'tag "{name}" should be "{status}" in the debug response considered tags')
def step_impl(context, name, status):
    id = context.tag_manager.tag_id_by_name(name)
    assert id in context.debug_request.response_data['debug'].keys(), "Tag was not found as a considered tag"
    tag_status = context.debug_request.response_data['debug'][id]
    assert tag_status == status, f"Status expected to be '{status}', but was '{tag_status}'"

@then(u'the debug response should have no bid')
def step_impl(context):
    assert context.debug_request.response_data["nobid"], "Expected nobid to be true."