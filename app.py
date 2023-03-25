"""A encourage bot working on slack, which stores data on google sheets."""

import os
import sys
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError
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
    logger.debug(f'Parsed Request: {source} to {target}')


    # filter out the bot/source and replace the user id with real name in the message
    real_target = []
    real_target_names = []
    for user in target:
        try:
            identity = app.client.users_info(user=user)
        except SlackApiError as e:
            logger.error(f"Error getting user info: {e}")
            continue

        text = text.replace(id_reparthenese(user), identity['user']['real_name'])
        if identity['user']['is_bot'] or user == source:
            continue
        
        real_target.append(user)
        real_target_names.append(identity['user']['real_name'])

    if len(real_target) > 0:
        logger.debug(f'User {source} to {real_target}: {real_target_names}')
        try:
            source_ideneity = app.client.users_info(user=source)
            source_name = source_ideneity['user']['real_name']
        except SlackApiError as e:
            logger.error(f"Error getting user info: {e}")
            return

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
        
        # send a completion message to the source
        try:
            result = app.client.chat_postMessage(channel=source, text=f"Your thank-you message to {', '.join(real_target_names)} has been recorded in {config['share_link']}")
            logger.debug(result)
            for user in real_target:
                result = app.client.chat_postMessage(channel=user, text=f"You just received a thank-you message from <@{source}>, details in {config['share_link']}")
                logger.debug(result)
        except SlackApiError as e:
            logger.error(f"Error posting message: {e}")
    else:
        try:
            result = app.client.chat_postMessage(channel=source, text=f"It seems you didn't mention any other user in the thank-you message. If this is a bug, please contact the bot developer.")
            logger.debug(result)
        except SlackApiError as e:
            logger.error(f"Error posting message: {e}")

if __name__ == "__main__":
    # parse config path
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
        config = parse_cfg(config_path)
    else:
        config = parse_cfg()

    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
