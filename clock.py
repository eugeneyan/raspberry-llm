"""
A clock that tells the time in a rhyme.
"""
from gc import collect

import ntptime
from inky_frame import BLACK, WHITE
from machine import RTC

from check_mem import check_mem
from inky_helper import button_c
from llm import call_openai

# Time variables
UPDATE_INTERVAL = 180
TIMEZONE_OFFSET = -7

# Prompt to tell the time
PROMPT = "Write a couplet with the time {}. Write numbers as numerals instead of spelling them. For example, 15 instead of fifteen."
# PROMPT = "Write a couplet with the time {}."

rhyme = ""

collect()


def update():
    check_mem('Start update in Clock')
    global rhyme
    
    try:
        ntptime.settime()
        print('Set NTP time')
    except OSError:
        print('Unable to contact NTP server')
    rtc = RTC()
    print("RTC time: {0}-{1}-{2} - {4:02d}:{5:02d}".format(*rtc.datetime()))
    
    # Using RTC time
    _time = rtc.datetime()
    hour = (_time[4] + TIMEZONE_OFFSET + 24) % 24
    minute = _time[5]
    timestring = "{:02d}:{:02d}".format(hour, minute)
    if hour < 12:
        timestring += "am"
    
    print(PROMPT.format(timestring))
    check_mem('Before calling API in AI clock')
    rhyme = call_openai(PROMPT.format(timestring))
    check_mem('After calling API in AI clock')
    print(rhyme)
        
    collect()

def draw(graphics):
    check_mem('Start draw in Clock')
    WIDTH, _ = graphics.get_bounds()
    
    graphics.set_pen(WHITE)
    graphics.clear()
    graphics.set_pen(BLACK)
    graphics.set_font("bitmap8")
    if len(rhyme) < 80:
        graphics.text(rhyme, 0, 0, WIDTH-20, 8)
    else:
        graphics.text(rhyme, 0, 0, WIDTH-20, 7)
    graphics.update()

    collect()

    check_mem('End draw in Clock')
    
    # button_c.led_on()