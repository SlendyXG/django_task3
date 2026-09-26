from django.core.exceptions import ObjectDoesNotExist

from datacenter.models import Mark, Chastisement, Schoolkid, Lesson, Commendation


def fix_marks(schoolkid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except ObjectDoesNotExist:
        print(f'Ученик по запросу {schoolkid_name!r} не найден.')
        return
    except Schoolkid.MultipleObjectsReturned:
        print(f'По запросу {schoolkid_name!r} найдено несколько учеников, '
              f'уточните имя.')
        return

    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    for mark in bad_marks:
        mark.points = 5
        mark.save()


def remove_chastisements(schoolkid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except ObjectDoesNotExist:
        print(f'Ученик по запросу {schoolkid_name!r} не найден.')
        return
    except Schoolkid.MultipleObjectsReturned:
        print(f'По запросу {schoolkid_name!r} найдено несколько учеников, '
              f'уточните имя.')
        return

    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(schoolkid_name, subject_title):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except ObjectDoesNotExist:
        print(f'Ученик по запросу {schoolkid_name!r} не найден.')
        return
    except Schoolkid.MultipleObjectsReturned:
        print(f'По запросу {schoolkid_name!r} найдено несколько учеников, '
              f'уточните имя.')
        return

    lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject_title,
    ).order_by('-date').first()

    if lesson is None:
        print(f'Урок по предмету {subject_title!r} для {schoolkid} не найден.')
        return

    Commendation.objects.create(
        text='Хвалю!',
        created=lesson.date,
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher,
    )