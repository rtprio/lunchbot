import os, re, random
import time
from slackclient import SlackClient

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">:"
EXAMPLE_COMMAND = "do"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def handle_command(command, channel):
    """
    Receives commands directed at the bot and determines if they
    are valid commands. If so, then acts on the commands. If not,
    returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"
        slack_client.api_call("chat.postMessage", channel=channel,
                              text=response, as_user=True)
        

def parse_slack_output(slack_rtm_output):
    """
    The Slack Real Time Messaging API is an events firehose.
    this parsing function returns None unless a message is
    directed at the Bot, based on its ID.
    """

    foods = ['apple', 'bento', 'bread', 'burrito', 'cake', 'cheese_wedge',
            'curry', 'egg', 'fried_shrimp', 'fries', 'hotdog', 'icecream',
             'pizza', 'poultry_leg', 'ramen', 'spaghetti', 'sushi', 'taco']

    burritos = [
        'Chopollos Burrito',
        'Carnitas Burrito',
        'Carne Asada Burrito',
        'Pastor Burrito',
        'Chicken Burrito',
        'All Meat Burrito',
        'Red Chile Burrito',
        'Green Chile Burrito',
        'Machaca Burrito',
        'Beef, Bean & Cheese Burrito',
        'Chicken Fajita Burrito',
        'Steak Fajita Burrito',
        'Ground Beef Burrito',
        'Trio Fajita Burrito',
        'Steak Potato Burrito',
        'Veggie Fajita Burrito',
        'Chile Relleno Burrito',
        'Veggie Burrito',
        'Low Fat Burrito',
        'Rice, Bean & Cheese Burrito',
        'Bean & Cheese Burrito',
        'Veggie Potato Burrito',
        'Tofu Burrito',
        'Breakfast Burrito',
        'Breakfast Machaca Burrito',
        'Steak Potato Breakfast Burrito']

    f = random.choice(foods)
    pattern = re.compile(r'.*lunch.*', re.I)
    
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                    output['channel']
            if output and 'text' in output and pattern.match(output['text']):
                slack_client.api_call("reactions.add", name=f, channel=output['channel'], timestamp= output['ts'] )
            if output and 'text' in output and re.search(':burrito:',output['text']):
                msg = "I recomend a _{0}_.".format(random.choice(burritos))
                slack_client.api_call("chat.postMessage", channel=output['channel'], text=msg, as_user=True, link_names=1)

    return None, None
        

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
                time.sleep(READ_WEBSOCKET_DELAY)
        else:
            print("Connection failed. Invalid Slack token or bot ID?")
