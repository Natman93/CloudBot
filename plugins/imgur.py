import re
import json
from util import hook
import httplib2


http = httplib2.Http(disable_ssl_certificate_validation=True)
api_key = ""

@hook.command()
def imgur(inp, bot=None):
    global api_key
    api_key = bot.config.get("api_keys", {}).get("imgur_client_id", None)
    data = json.loads(request('https://api.imgur.com/3/gallery/search?q=' + inp))
    if data['success']:
        # hooray! it works!
        data = data['data'][0]
        print data
        data = betterWords(data)
        if str(data['is_album']) is "True": # https://api.imgur.com/models/gallery_album
            # Since the data is already in JSON form, we can just go right in and use the data like this.
            # Bold: \x02. Colored: \x03(color). End Colors: \x0f
            return ("Imgur Album: Title: {title}. Description: {description}. {views} views with \x033{ups}\x0f upvotes and \x034{downs}\x0f downvotes. {images_count} images: {link}").format(**data)
        else:
            # Just an image. https://api.imgur.com/models/gallery_image
            return ("Imgur Image: Title: {title}. Description: {description}. {views} views with \x033{ups}\x0f upvotes and \x034{downs}\x0f downvotes. Gif: {animated}. {link}").format(**data)
    else:
        print data
        return "An error occurred, HTTP response code %s was returned: %s - %s" % (data['status'], data['data']['error'], data['data']['request'])



def request(inp):
    result, content = http.request(inp, 'GET',
        headers={'Authorization': 'Client-ID ' + api_key})
    return content

def betterWords(inp):
    """ Replace some words that sound too 'programmy' in a one-layer json array, bold the words. """
    for e in inp:
        if type(e) is dict or str(e) is "id":
            #inp[e] = betterWords(e)
            continue
        elif inp[e] is None: # Null *is* "None" in python.
            inp[e] = "No " + e
        elif str(inp[e]) is "False":
            inp[e] = "No"
        elif str(inp[e]) is "True":
            inp[e] = "Yes"
        inp[e] = "\x02" + str(inp[e]) + "\x02"
    return inp
