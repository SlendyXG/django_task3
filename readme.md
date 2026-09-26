# Скрипты для работы с электронным дневником

Набор вспомогательных функций для работы с базой данных электронного дневника через Django shell. Позволяют исправить плохие оценки, удалить замечания и добавить похвалу ученику.

## Требования

- Проект электронного дневника развёрнут и настроен (см. основной README).
- База данных создана (`python manage.py migrate`).
- Функции лежат в модуле `datacenter/scripts.py`.

## Как открыть shell

Из папки проекта, где лежит `manage.py`:

    python manage.py shell

## Импорт функций

    from datacenter.scripts import fix_marks, remove_chastisements, create_commendation

Если функции лежат в другом модуле — замените `datacenter.scripts` на путь к нему.

## Функции

### fix_marks(schoolkid_name)

Заменяет все оценки 2 и 3 указанного ученика на 5.

    fix_marks('Фролов Иван Григорьевич')

- schoolkid_name — часть ФИО ученика (поиск через full_name__contains).
- Если ученик не найден — печатает сообщение и завершается.
- Если найдено несколько учеников — печатает сообщение и завершается.

Примеры:

    >>> fix_marks('John')
    Ученик по запросу 'John' не найден.

    >>> fix_marks('Степан')
    По запросу 'Степан' найдено несколько учеников, уточните имя.

    >>> fix_marks('Фролов Иван Григорьевич')
    # без вывода — оценки исправлены

### remove_chastisements(schoolkid_name)

Удаляет все замечания указанного ученика.

    remove_chastisements('Фролов Иван Григорьевич')

Поведение при ненайденном или неоднозначном имени — как у fix_marks.

Примеры:

    >>> remove_chastisements('John')
    Ученик по запросу 'John' не найден.

    >>> remove_chastisements('Фролов Иван Григорьевич')
    # без вывода — замечания удалены

### create_commendation(schoolkid_name, subject_title)

Создаёт похвалу ученику по указанному предмету. Дата похвалы совпадает с датой последнего урока этого предмета у класса ученика. Автор и предмет берутся из того же урока.

    create_commendation('Фролов Иван Григорьевич', 'Музыка')

- schoolkid_name — часть ФИО ученика.
- subject_title — название предмета (Subject.title), например 'Музыка', 'Математика'.
- Если ученик не найден или найден не один — печатает сообщение и завершается.
- Если уроков по предмету у класса нет — печатает сообщение и завершается.

Примеры:

    >>> create_commendation('John', 'Музыка')
    Ученик по запросу 'John' не найден.

    >>> create_commendation('Фролов Иван Григорьевич', 'Астрономия')
    Урок по предмету 'Астрономия' для Фролов Иван Григорьевич 6А не найден.

    >>> create_commendation('Фролов Иван Григорьевич', 'Музыка')
    # без вывода — похвала создана

## Полный сценарий использования

    from datacenter.utils import fix_marks, remove_chastisements, create_commendation
    from datacenter.models import Mark, Chastisement, Schoolkid, Lesson, Commendation

    name = 'Фролов Иван Григорьевич'

    fix_marks(name)
    remove_chastisements(name)
    create_commendation(name, 'Музыка')

    schoolkid = Schoolkid.objects.get(full_name__contains=name)
    print('Двоек и троек:', Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).count())
    print('Замечаний:', Chastisement.objects.filter(schoolkid=schoolkid).count())
    print('Похвал:', Commendation.objects.filter(schoolkid=schoolkid).count())

Ожидаемый вывод:

    Двоек и троек: 0
    Замечаний: 0
    Похвал: 1

## Выход из shell

    exit()

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте Devman (https://dvmn.org).
