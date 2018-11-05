class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address

    def __repr__(self):
        return "User: {name} - Email: {email} - Books read: {nb}".format(name=self.name, email=self.email, nb=len(self.books))

    def __eq__(self, other_user):
        if other_user is User:
            return self.name == other_user.name and self.email == other_user.email
        else:
            return False

    def read_book(self, book, rating=None):
        self.books[book] = rating

    def get_average_rating(self):
        return sum([x if isinstance(x, int) else 0 for x in self.books.values()]) / len(self.books)

class Book(object):
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print("The ISBN of the book {title} has been updated to {isbn}".format(title=self.title, isbn=self.isbn))

    def add_rating(self, rating):
        if isinstance(rating, int):
            self.ratings.append(rating) if 0 <= rating <= 4 else print ("Invalid Rating")

    def __eq__(self, other):
        return self.title == other.title and self.isbn == other.isbn

    def get_average_rating(self):
        return sum(self.ratings) / len(self.ratings)

    def __hash__(self):
        return hash((self.title, self.isbn))

class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title=self.title, author=self.author)

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title=self.title, level=self.level, subject=self.subject)

class TomeRater(object):
    def __init__(self):
        self.users = {}
        self.books = {}

    def create_book(self, title, isbn):
        return Book(title, isbn)

    def create_novel(self, title, author, isbn):
        return Fiction(title, author, isbn)

    def create_non_fiction(self, title, subject, level, isbn):
        return Non_Fiction(title, subject, level, isbn)

    def add_book_to_user(self, book, email, rating=None):
        user = self.users.get(email)
        if user == None:
            print("No user with email: {email}".format(email=email))
            return
        else:
            user.read_book(book, rating)
            book.add_rating(rating)
        if book in self.books:
            self.books[book] += 1
        else:
            for b in self.books.keys():
                if b.get_isbn() == book.isbn:
                    print("A book already holds this ISBN.")
                    return
            self.books[book] = 1

    def add_user(self, name, email, user_books=None):
        for u in self.users.values():
            if email == u.get_email():
                print("A user with email '{email}' already exists.".format(email=email))
                return
        if email.count('@') == 1 and email[-4:] in [".com", ".org", ".edu"]:
            self.users[email] = User(name, email)
        else:
            print("Email must have the format: 'xxxx@xxxx[.com][.edu][.org]'")
            return
        if user_books != None:
            for b in user_books:
                self.add_book_to_user(b, email)

    def print_catalog(self):
        for b in self.books.keys():
            print(b)

    def print_users(self):
        for u in self.users:
            print(u)

    def most_read_book(self):
        return max(self.books, key=self.books.get)

    def highest_rated_book(self):
        return max(self.books, key=lambda x: x.get_average_rating())

    def most_positive_user(self):
        return max(self.users.values(), key=lambda x: x.get_average_rating())
