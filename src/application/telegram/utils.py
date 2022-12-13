def escape(string):
    """
    Экранирование спецсимволов для Markdown разметки телеграм
    :param string: Строка для экранирования
    :return: Экранированная строка
    """

    chars = ['*', '_', '[', '`']
    for i in chars:
        string = string.replace(i, '\\' + i)

    return string
