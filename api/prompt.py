import os

chat_language = os.getenv("INIT_LANGUAGE", default="zh")

MSG_LIST_LIMIT = int(os.getenv("MSG_LIST_LIMIT", default=20))
LANGUAGE_TABLE = {
    "zh": "哈囉！",
    "en": "Hello!"
}


class Prompt:
    def __init__(self):
        self.msg_list = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    def add_msg(self, role, content):
        if len(self.msg_list) >= MSG_LIST_LIMIT:
            self.remove_msg()
        new_msg = {"role": role, "content": content}
        self.msg_list.append(new_msg)

    def remove_msg(self):
        self.msg_list.pop(0)

    def generate_prompt(self):
        return '\n'.join(self.msg_list)
# import os
#
# chat_language = os.getenv("INIT_LANGUAGE", default = "zh")
#
# MSG_LIST_LIMIT = int(os.getenv("MSG_LIST_LIMIT", default = 20))
# LANGUAGE_TABLE = {
#   "zh": "哈囉！",
#   "en": "Hello!"
# }
#
# class Prompt:
#     def __init__(self):
#         self.msg_list = [
#             {"role": "system", "content": "You are a helpful assistant."}
#         ]
#
#     def add_msg(self, new_msg):
#         if len(self.msg_list) >= MSG_LIST_LIMIT:
#             self.remove_msg()
#         self.msg_list.append(new_msg)
#
#     def remove_msg(self):
#         self.msg_list.pop(0)
#
#     def generate_prompt(self):
#         return self.msg_list
#
#     def messages_container(self, role, content):
#         new_msg = {"role": role, "content": content}
#         self.msg_list.append(new_msg)
#
