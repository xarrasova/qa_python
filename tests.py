import pytest
from main import BooksCollector

@pytest.fixture
def collector():
    return BooksCollector()

class TestBooksCollector:

    #добавляем две новые книги в словарь без указания жанра
    def test_add_new_book_add_two_books(self, collector):
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    #одну и ту же книгу можно добавить только один раз
    def test_add_new_book_duplicate_not_added(self, collector):
        collector.add_new_book('Код даВинчи')
        collector.add_new_book('Код даВинчи')
        assert len(collector.get_books_genre()) == 1

    #название книги может содержать максимум 40 символов
    def test_add_new_book_long_name_not_added(self, collector):
        long_name = 'ABCD' * 11
        collector.add_new_book(long_name)
        assert len(collector.get_books_genre()) == 0

    #создаем параметризированный тест: устанавливаем жанр книги, если книга есть в словаре books_genre, и её жанр входит в список genre
    @pytest.mark.parametrize(
        'book_name, genre, expected_genre', 
        [
        ('Аленький цветочек', 'Мультфильмы', 'Мультфильмы'),
        ('Аленький цветочек', 'Сказка', ''),
        ('Код даВинчи', 'Детективы', 'Детективы')
        ]
    )
    def test_set_book_genre_parametrized(self, collector, book_name, genre, expected_genre):
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.get_book_genre(book_name) == expected_genre
    
    #проверяем, что если книги нет в словаре, то и жанр не установится - не к чему
    def test_set_book_genre_missing_book(self, collector):
        collector.set_book_genre('Потерянная книга', 'Фантастика')
        assert len(collector.get_books_genre()) == 0

    #выводим жанр книги по её имени
    def test_get_book_genre_existing(self, collector):
        collector.add_new_book('Пила')
        collector.set_book_genre('Пила', 'Ужасы')
        assert collector.get_book_genre('Пила') == 'Ужасы'

    #создаем параметризированный тест: выводим список книг с определённым жанром
    @pytest.mark.parametrize(
        'genre, expected_books', 
        [
        ('Фантастика', ['Властелин колец']),
        ('Комедии', ['Кавказская пленница']),
        ('Детективы', ['Тело'])
        ]
    )
    def test_get_books_with_specific_genre_parametrized(self, collector, genre, expected_books):
        book_name = expected_books[0]
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.get_books_with_specific_genre(genre) == expected_books

    #выводим текущий словарь books_genre
    def test_get_books_genre(self, collector):
        collector.add_new_book('Над пропастью во ржи')
        collector.set_book_genre('Над пропастью во ржи', 'Детективы')
        collector.add_new_book('Ночь нежна')
        collector.set_book_genre('Ночь нежна', 'Роман')
        expected_dictionary = {'Над пропастью во ржи': 'Детективы', 'Ночь нежна': ''}
        assert collector.get_books_genre() == expected_dictionary

    #возвращаем книги, которые подходят детям
    def test_get_books_for_children_allowed_genre(self, collector):
        collector.add_new_book('Три поросенка')
        collector.set_book_genre('Три поросенка', 'Мультфильмы')
        children_books = collector.get_books_for_children()
        assert 'Три поросенка' in children_books

    def test_get_books_for_children_restricted_genre(self, collector):
        collector.add_new_book('Пила')
        collector.set_book_genre('Пила', 'Ужасы')
        children_books = collector.get_books_for_children()
        assert 'Пила' not in children_books

    #добавляем книгу в избранное. Книга должна находиться в словаре books_genre. Повторно добавить книгу в избранное нельзя
    def test_add_book_in_favorites_success(self, collector):
        collector.add_new_book('Властелин колец')
        collector.add_book_in_favorites('Властелин колец')
        collector.add_book_in_favorites('Властелин колец')
        favorites = collector.get_list_of_favorites_books()
        assert len(favorites) == 1
        assert favorites[0] == 'Властелин колец'

    #удаляем книгу из избранного
    def test_delete_book_from_favorites_success(self, collector):
        collector.add_new_book('Ночь нежна')
        collector.add_book_in_favorites('Ночь нежна')
        assert ['Ночь нежна'] == collector.get_list_of_favorites_books()
        collector.delete_book_from_favorites('Ночь нежна')
        assert ['Ночь нежна'] != collector.get_list_of_favorites_books()

    #получаем список избранных книг
    def test_get_list_of_favorites_books(self, collector):
        collector.add_new_book('1+1')
        collector.add_book_in_favorites('1+1')
        collector.add_new_book('2+1')
        collector.add_book_in_favorites('2+1')
        assert ['1+1', '2+1'] == collector.get_list_of_favorites_books()
