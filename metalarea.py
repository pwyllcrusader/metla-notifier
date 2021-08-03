def login(username, password):
    ...


def go_to_releases_tab():
    ...


def switch_to_hot_releases_view():
    ...


def get_release_links():
    ...


def parse_release():
    ...


def get_releases_list(username, password):
    login(username, password)
    go_to_releases_tab()
    switch_to_hot_releases_view()
    links = get_release_links()
    return [parse_release(link) for link in links]
