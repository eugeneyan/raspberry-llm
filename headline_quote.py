"""
Pulls a random headline from the Wall Street Journal and makes up a fake quote from it.
"""
from gc import collect

from inky_frame import BLACK, ORANGE

from check_mem import check_mem
from inky_helper import button_a
from llm import call_openai
from qr_code import code, draw_qr_code
from rss import get_random_headline

URL = "https://feeds.a.dj.com/rss/RSSWSJD.xml"

UPDATE_INTERVAL = 300
MAX_TITLE_LEN = 90

# Prompt for a funny story
PROMPT = 'Write a funny quote from the headline in less than 50 words: "{}". Include the name of who said it.'

title = None
link = None
story = ''

collect()


def update():
    check_mem('Start update in Headline Quote')
    global title, story, link
    # Gets Feed Data
    title, link = get_random_headline(URL, 20)
    print(PROMPT.format(title))
    story = call_openai(PROMPT.format(title))
    print(story)
    collect()


def draw(graphics):
    check_mem('Start draw in Headline Quote')
    global title, story, link
    WIDTH, HEIGHT = graphics.get_bounds()
    graphics.set_font("bitmap8")

    # Clear the screen
    graphics.set_pen(1)
    graphics.clear()
    graphics.set_pen(0)

    # Draws 2 articles from the feed if they're available.
    if title:

        # Title
        if len(title) > MAX_TITLE_LEN:
            title = title[:MAX_TITLE_LEN] + '...'
        graphics.set_pen(BLACK)
        graphics.text('WSJ: {}'.format(title), 10, 10, WIDTH-140, 4 if len(title) < 50 else 3)

        # QR Code
        code.set_text(link)
        draw_qr_code(WIDTH-100, 5, 100, code, graphics)
        
        # Separator
        graphics.set_pen(ORANGE)
        graphics.rectangle(0, 105, WIDTH, 10)

        # Story
        graphics.set_pen(BLACK)
        graphics.text('FAKE QUOTE: {}'.format(story), 10, 125, WIDTH-50, 6 if len(story) < 80 else 5)
        
    else:
        graphics.set_pen(4)
        graphics.rectangle(0, (HEIGHT // 2) - 20, WIDTH, 40)
        graphics.set_pen(1)
        graphics.text("Unable to display news feed!", 5, (HEIGHT // 2) - 15, WIDTH, 2)
        graphics.text("Check your network settings in secrets.py", 5, (HEIGHT // 2) + 2, WIDTH, 2)

    graphics.update()

    collect()

    check_mem('End draw in Headline Quote')
    
    # button_a.led_on()