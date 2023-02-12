from vk_api import VkApi


def _parse_wall_id(link: str) -> str:
    """ Достает id поста из ссылки link """
    return link[link.find('wall') + 4:]


# TODO: сделать красивее
def get_vk_session(params: tuple) -> VkApi:
    """ Возвращает объект сессии ВК. Параметрами служат сервисный токен или
        логин и пароль пользователя ВК.
    """
    if len(params) == 1:
        return VkApi(token=params[0])
    if len(params) == 2:
        session = VkApi(*params)
        session.auth()
        return session
    ValueError(f'Expected 1 or 2 params, got {len(params)}')


def get_vk_tracks(session: VkApi, link: str) -> dict | None:
    """ Возвращает список аудиозаписей из поста по ссылке. Если в посте нет
        аудиозаписей или не был получен пост, то возвращает None.
        Параметрами служат сессия ВК session и ссылка на пост link.
    """
    vk = session.get_api()
    post = vk.wall.getById(posts=_parse_wall_id(link))

    if not post or 'attachments' not in post[0]:
        return None

    tracks = dict()
    for d in post[0]['attachments']:
        try:
            tracks[d['audio']['title']] = d['audio']['artist']
        except KeyError:
            continue
    return tracks if tracks else None
