from gc import collect
from random import choice

collect()

app_name = None
UPDATE_INTERVAL = 300

def update():
    global app_name
    app_name = choice(['headline_quote', 'headline_seuss', 'clock', 'hackernews'])
    print('Randomly chosen app: {}'.format(app_name))
    if app_name == 'headline_quote':
        from headline_quote import update as headline_quote_update
        collect()
        headline_quote_update()
    elif app_name == 'headline_seuss':
        from headline_seuss import update as headline_seuss_update
        collect()
        headline_seuss_update()
    elif app_name == 'clock':
        from clock import update as clock_update
        collect()
        clock_update()
    elif app_name == 'hackernews':
        from hackernews import update as hackernews_update
        collect()
        hackernews_update()
    elif app_name == 'nasa_apod':
        from nasa_apod import update as nasa_apod_update
        collect()
        nasa_apod_update()
    collect()

        
def draw(graphics):
    global app_name
    print('Drawing app: {}'.format(app_name))
    if app_name == 'headline_quote':
        from headline_quote import draw as headline_quote_draw
        collect()
        headline_quote_draw(graphics)
    elif app_name == 'headline_seuss':
        from headline_seuss import draw as headline_seuss_draw
        collect()
        headline_seuss_draw(graphics)
    elif app_name == 'clock':
        from clock import draw as clock_draw
        collect()
        clock_draw(graphics)
    elif app_name == 'hackernews':
        from hackernews import draw as hackernews_draw
        collect()
        hackernews_draw(graphics)
    elif app_name == 'nasa_apod':
        from nasa_apod import draw as nasa_apod_draw
        collect()
        nasa_apod_draw(graphics)
    collect()