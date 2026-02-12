ARTICLE = 'AR'
NEWS = 'NE'

AUTHOR_CHOICES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость')
]
# sports = 'sports'
# politics = 'politics'
# education = 'education'
# humor = 'humor'
#
#
# POSITIONS = [
#     (sports, 'спорт'),
#     (politics, 'Политика'),
#     (education, 'Образование'),
#     (humor, 'Юмор')
# ]

# Author.objects.filter(age__lt=25)
# Author.objects.filter(age=32).values("name")