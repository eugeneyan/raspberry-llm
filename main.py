from gc import collect

from inky_frame import BLACK, BLUE, GREEN, ORANGE, RED, WHITE, YELLOW
from machine import reset
from picographics import DISPLAY_INKY_FRAME_4 as DISPLAY  # 4.0"
from picographics import PicoGraphics
from utime import sleep

import inky_helper as ih
from check_mem import check_mem

# A short delay to give USB chance to initialise
sleep(1)

app_name = None

def launcher():
    
    check_mem('Before setting up graphics at top of launcher.')
    graphics = PicoGraphics(DISPLAY)
    WIDTH, HEIGHT = graphics.get_bounds()
    graphics.set_font("bitmap8")
    check_mem('After setting up graphics at top of launcher.')
    
    # Apply an offset for the Inky Frame 5.7".
    if HEIGHT == 448:
        y_offset = 20
    # Inky Frame 7.3"
    elif HEIGHT == 480:
        y_offset = 35
    # Inky Frame 4"
    else:
        y_offset = 0

    # Draws the menu
    graphics.set_pen(WHITE)
    graphics.clear()
    graphics.set_pen(BLACK)

    graphics.set_pen(YELLOW)
    graphics.rectangle(0, 0, WIDTH, 50)
    graphics.set_pen(BLACK)
    title = "Launch an App!"
    title_len = graphics.measure_text(title, 4) // 2
    graphics.text(title, (WIDTH // 2 - title_len), 10, WIDTH, 4)

    graphics.set_pen(RED)
    graphics.rectangle(30, HEIGHT - (340 + y_offset), WIDTH - 100, 50)
    graphics.set_pen(WHITE)
    graphics.text("A. WSJ News - Fake Quotes & Views", 35, HEIGHT - (325 + y_offset), 600, 3)

    graphics.set_pen(ORANGE)
    graphics.rectangle(30, HEIGHT - (280 + y_offset), WIDTH - 150, 50)
    graphics.set_pen(WHITE)
    graphics.text("B. WSJ News - Told by Dr. Seuss", 35, HEIGHT - (265 + y_offset), 600, 3)

    graphics.set_pen(GREEN)
    graphics.rectangle(30, HEIGHT - (220 + y_offset), WIDTH - 200, 50)
    graphics.set_pen(WHITE)
    graphics.text("C. Get the Time in a Rhyme", 35, HEIGHT - (205 + y_offset), 600, 3)

    graphics.set_pen(BLUE)
    graphics.rectangle(30, HEIGHT - (160 + y_offset), WIDTH - 250, 50)
    graphics.set_pen(WHITE)
    graphics.text("D. Hacker News - Trolls", 35, HEIGHT - (145 + y_offset), 600, 3)

    graphics.set_pen(BLACK)
    graphics.rectangle(30, HEIGHT - (100 + y_offset), WIDTH - 300, 50)
    graphics.set_pen(WHITE)
    graphics.text("E. Rotate Randomly!", 35, HEIGHT - (85 + y_offset), 600, 3)

    graphics.set_pen(graphics.create_pen(220, 220, 220))
    graphics.rectangle(WIDTH - 100, HEIGHT - (340 + y_offset), 70, 50)
    graphics.rectangle(WIDTH - 150, HEIGHT - (280 + y_offset), 120, 50)
    graphics.rectangle(WIDTH - 200, HEIGHT - (220 + y_offset), 170, 50)
    graphics.rectangle(WIDTH - 250, HEIGHT - (160 + y_offset), 220, 50)
    graphics.rectangle(WIDTH - 300, HEIGHT - (100 + y_offset), 270, 50)

    graphics.set_pen(0)
    note = "Hold A + E, then press Reset, to return to the Launcher"
    note_len = graphics.measure_text(note, 2) // 2
    graphics.text(note, (WIDTH // 2 - note_len), HEIGHT - 30, 600, 2)

    ih.led_warn.on()
    graphics.update()
    ih.led_warn.off()

    # Now we've drawn the menu to the screen, we wait here for the user to select an app.
    # Then once an app is selected, we set that as the current app and reset the device and load into it.

    # You can replace any of the included examples with one of your own,
    # just replace the name of the app in the line "ih.update_last_app("nasa_apod")"

    while True:
        if ih.button_a.read():
            ih.button_a.led_on()
            ih.update_state("headline_quote")
            sleep(0.5)
            reset()
        if ih.button_b.read():
            ih.button_b.led_on()
            ih.update_state("headline_seuss")
            sleep(0.5)
            reset()
        if ih.button_c.read():
            ih.button_c.led_on()
            ih.update_state("clock")
            sleep(0.5)
            reset()
        if ih.button_d.read():
            ih.button_d.led_on()
            ih.update_state("hackernews")
            sleep(0.5)
            reset()
        if ih.button_e.read():
            ih.button_e.led_on()
            ih.update_state("random_app")
            sleep(0.5)
            reset()


# Turn any LEDs off that may still be on from last run.
ih.clear_button_leds()
ih.led_warn.off()

if ih.button_a.read() and ih.button_e.read():
    launcher()

ih.clear_button_leds()

if ih.file_exists("state.json"):
    # Loads the JSON and launches the app
    ih.load_state()
    app_name = ih.state['run']
    ih.launch_app(app_name)
    print('Loaded app: {}'.format(app_name))

    # Passes the the graphics object from the launcher to the app
    print('Setting up graphics in main.')
    
    check_mem('Before setting up graphics in state.')
    graphics = PicoGraphics(DISPLAY)
    WIDTH, HEIGHT = graphics.get_bounds()
    graphics.set_font("bitmap8")
    check_mem('After setting up graphics in state.')
    
    ih.app.graphics = graphics
    ih.app.WIDTH = WIDTH
    ih.app.HEIGHT = HEIGHT
        
    collect()
else:
    launcher()

try:
    from secrets import WIFI_PASSWORD, WIFI_SSID
    ih.network_connect(WIFI_SSID, WIFI_PASSWORD)
    print('Connected to WiFi: {}'.format(WIFI_SSID))
except ImportError:
    print("Create secrets.py with your WiFi credentials")

# Get some memory back, we really need it!
collect()

check_mem('Before main while loop')


def main():
    ih.led_warn.on()
    try:
        ih.app.update()
        ih.app.draw(ih.app.graphics)
        ih.led_warn.off()
    except:
        ih.led_warn.off()
        ih.button_e.led_on()
        
    # Disconnect network
    ih.network_disconnect()
    ih.stop_network_led()
    
    # Go to sleep
    print('Going to sleep for {} secs'.format(ih.app.UPDATE_INTERVAL))
    ih.sleep(ih.app.UPDATE_INTERVAL)
    print('Woken up from sleep!')
    collect()

main()
reset()