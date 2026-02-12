from django.contrib.auth.models import Group

def get_group(name):
    current_group, created = Group.objects.get_or_create(name= name) # get_or_create если естьгруппа, то добавляет, если группы такой нет создает ее, чтобы приложение не упало в случае отсутсвия таковой группы.
    return current_group
