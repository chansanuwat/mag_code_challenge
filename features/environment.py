from lib.tag_management import TagManager
from behave.fixture import fixture, use_fixture

def before_tag(context, tag):
    if tag == "fixture.tag.management":
        use_fixture(tag_management, context)
    if tag == "clear.all.tags":
        # This works in a controlled environment with a small dataset,
        # but would need a better solution to guarantee accuracy in a larger, uncontrolled env
        context.tag_manager.clear_all_tags()

@fixture
def tag_management(context):
    context.tag_manager = TagManager(context.config.userdata["host"])
    yield
    context.tag_manager.delete_new_tags()