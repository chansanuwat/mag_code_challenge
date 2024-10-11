import requests

class TagManager:
    def __init__(self, host):
        self.host = f"{host}/config/tags"
        self.session = requests.Session()
        self.session.headers['Accept'] = 'application/json'
        self.created_tags = []
        self.name_map = {}

    def clear_all_tags(self):
        for tag in self.get_all_tags().keys():
            self.delete_tag(tag)

    def create_tags(self, tags):
        for tag in tags:
            response = self.session.post(self.host, json = tag).json()
            self.created_tags.append(response)
            self.name_map[tag["name"]] = response["id"]

    def delete_tag(self, tag_id):
        self.session.delete(f"{self.host}/{tag_id}")

    def delete_new_tags(self):
        for tag in self.created_tags:
            self.delete_tag(tag['id'])

    def get_all_tags(self):
        return self.session.get(self.host).json()

    def tag_id_by_name(self, name):
        return self.name_map[name]