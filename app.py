"""A encourage bot working on slack, which stores data on google sheets."""

import os
import sys
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from utils.logging import logger
from utils import regex
from google_sheet.io import append_to_sheet, get_from_sheet
from utils.compose import compose_onetoall, id_reparthenese, compose_formatted_time
from utils.parse_cfg import parse_cfg

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


@app.event("app_mention")
def handle_app_mention_events(body, say):
    """Deaful message event handler"""
    # parse the message
    logger.debug(body)
    text = body['event']['text']
    source = body['event']['user']
    target = regex.match_user.findall(text)
    logger.debug(f'User {source} to {target}')


    # filter out the bot/source and replace the user id with real name in the message
    real_target = []
    real_target_names = []
    for user in target:
        identity = app.client.users_info(user=user)
        text = text.replace(id_reparthenese(user), identity['user']['real_name'])
        if identity['user']['is_bot'] or user == source:
            continue
        
        real_target.append(user)
        real_target_names.append(identity['user']['real_name'])
    if len(real_target) > 0:
        logger.debug(f'User {source} to {real_target}: {real_target_names}')
        source_ideneity = app.client.users_info(user=source)
        source_name = source_ideneity['user']['real_name']

        # set the constants
        time = compose_formatted_time(body['event_time'], config['timezone'])
        constants = [time, text]
        values = compose_onetoall(source_name, real_target_names, constants)

        # append to the details sheet
        append_to_sheet(config['spreadsheet_id'], config['sheet_name']+'!A1:A1', values)

        # check the summary sheet
        summary_names = get_from_sheet(config['spreadsheet_id'], config['summary_name']+'!A2:A')
        summary_names = [name[0] for name in summary_names]
        for name in real_target_names+[source_name,]:
            if name not in summary_names:
                append_to_sheet(config['spreadsheet_id'], config['summary_name']+'!A1:A1', 
                            [[name, f'=COUNTIF({config["sheet_name"]}!A:A, "{name}")', f'=COUNTIF({config["sheet_name"]}!B:B, "{name}")']],
                            value_input_option='USER_ENTERED')
    else:
        say(f"Hi <@{source}>! It seems you didn't mention any other user. If this is a bug, please contact the bot developer.")

if __name__ == "__main__":
    # parse config path
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
        config = parse_cfg(config_path)
    else:
        config = parse_cfg()

    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
