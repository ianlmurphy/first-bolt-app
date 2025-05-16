import random
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import logging
import threading
import http.server
import socketserver

logging.basicConfig(level=logging.DEBUG)

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")

# Start a dummy web server in a thread to keep Render happy
def run_dummy_server():
    PORT = 10000
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving dummy HTTP on port {PORT}")
        httpd.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

app = App(token=SLACK_BOT_TOKEN)

@app.command("/chore")
def handle_chore(ack, body, client, logger):
    ack()
    logger.info(f"Slash command triggered by user: {body['user_name']} in channel: {body['channel_id']}")

    names = ['Thomas', 'Myeonggon', 'Hunter', 'Ian', 'Madhurima', 'Simon', 'Sam']
    chores = [
        'Organize area around microscopes and remove clutter, clean microwave',
        'Order lab supplies, check shelves for low supplies',
        'Sweep the office and wetlab',
        'Sweep the microscope room',
        'Wipe wetlab surfaces and remove clutter, switch glass/plastic bins if full',
        'Clean the sink and surrounding area, refill bottles',
        'No chores for you freeloader'
    ]

    rand_chores = random.sample(chores, len(chores))
    combined = list(zip(names, rand_chores))

    message_lines = ["*Chore assignments:*", "```"]
    for name, chore in combined:
        message_lines.append(f"{name:<10} | {chore}")
    message_lines.append("```")
    message = "\n".join(message_lines)

    try:
        client.chat_postMessage(
            channel=body['channel_id'],
            text=message
        )
    except Exception as e:
        logger.error(f"Failed to post message: {e}")

if __name__ == "__main__":
    print("Starting Bolt app...")
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
