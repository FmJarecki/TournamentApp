import webbrowser


def open_maps(latitude: float, longitude: float):
    url = f"geo:{latitude},{longitude}?q={latitude},{longitude}(Location)" # for mobile
    url = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}" # temporary for pc
    webbrowser.open(url)
