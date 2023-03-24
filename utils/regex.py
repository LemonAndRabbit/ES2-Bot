"""A regular experssion base."""
import re

match_user = re.compile(r'<@([0-9a-zA-Z]+)>')
match_message = re.compile(r'[Tt]hanks?.*<@[0-9a-zA-Z]+>')
