from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category, PostCategory


class Command(BaseCommand):

    help = 'Удаляет все посты из категории'
    missing_args_message = 'Не указана категория !'

    def add_arguments(self, parser):

        parser.add_argument('category', type=str)

    def handle(self, *args, **options):

        ctg_name = options["category"].lower()

        self.stdout.write(f'Вы действительно хотите удалить посты в категории {ctg_name.title()}? Введите да/нет')
        answer = input()

        if answer == 'Да' or answer == 'да':

            try:
                ctg = Category.objects.get(name=ctg_name)

                Post.objects.filter(categories__id=ctg.id).delete()

                self.stdout.write(self.style.SUCCESS('Посты успешно удалены'))
                return

            except Category.DoesNotExist:
                self.stdout.write(
                    f'Не найдена категория {ctg_name.title()}')

        else:
            self.stdout.write(self.style.ERROR('Удаление не выполнено'))
            return
