"""
Utility to parse RSS feeds and return a random headline.
"""

from gc import collect
from random import randint
from urllib.urequest import urlopen

from check_mem import check_mem


def read_until(stream, char):
    result = b""
    while True:
        c = stream.read(1)
        if c == char:
            return result
        result += c


def discard_until(stream, c):
    while stream.read(1) != c:
        pass


def parse_xml_stream(s, accept_tags, group_by, max_items=3):
    text = b""
    count = 0
    current = {}
    check_mem('Start parse')
    while True:
        char = s.read(1)
        if len(char) == 0:
            break

        if char == b"<":
            next_char = s.read(1)

            # Discard stuff like <?xml vers...
            if next_char == b"?":
                discard_until(s, b">")
                continue

            # Detect <![CDATA
            elif next_char == b"!":
                s.read(1)  # Discard [
                discard_until(s, b"[")  # Discard CDATA[
                text = read_until(s, b"]")
                discard_until(s, b">")  # Discard ]>
                collect()

            elif next_char == b"/":
                current_tag = read_until(s, b">")

                # Populate our result dict
                if current_tag in accept_tags:
                    current[current_tag.decode("utf-8")] = text.decode("utf-8")
                    collect()
                    print('{}: {}'.format(current_tag.decode("utf-8"), text.decode("utf-8")))
                    # check_mem('Accept tag')

                # If we've found a group of items, yield the dict
                elif current_tag == group_by:
                    yield current
                    current = {}
                    count += 1
                    if count == max_items:
                        return
                text = b""
                collect()
                continue

            else:
                current_tag = read_until(s, b">")
                text = b""
                collect()

        else:
            text += char
            
    
def get_random_headline(url, max_items=10):
    try:
        check_mem('Open stream')
        stream = urlopen(url)
        check_mem('After stream')
        output = list(parse_xml_stream(stream, [b"title", b"link"], b"item", max_items))
        check_mem('After parse')
        stream.close()
        check_mem('After close stream')
        for item in output:
            print(item)
        collect()
        rand_i = randint(0, len(output)-1)
        print('Random index: {}'.format(rand_i))
        return output[rand_i]['title'], output[rand_i]['link']

    except OSError as e:
        print(e)
        return False, False