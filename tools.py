def create_tracks_answer_message(tracks):
    """ Создает ответное сообщение в зависимости от количества песен """
    if tracks is None:
        return 'В посте по ссылке нет аудиозаписей ¯\\_(ツ)_/¯'
    answer_message = 'Нашел песни:\n\n'
    i = 1
    for title in tracks:
        answer_message += f'{i}) {tracks[title]} — {title}\n'
        i += 1
    answer_message += '\nУже в Яндекс.Музыке (＾▽＾)'
    return answer_message
