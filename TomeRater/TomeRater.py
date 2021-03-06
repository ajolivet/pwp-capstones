class User(object):
    '''
    User class, expects a name and email as strings, can build a dictionary
    (through read_book()) of the books read, with titles as keys and user
    ratings as values.
    '''
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
        try:
            rating = int(rating)
            if not 0 <= rating <= 4:
                raise ValueError
        except ValueError:
            raise
        except TypeError:
            self.books[book] = rating
        else:
            self.books[book] = rating

    def get_average_rating(self):
        # Returns an average of the ratings given by the user.
        return sum([x if isinstance(x, int) else 0 for x in self.books.values()]) / len(self.books)

class Book(object):
    '''
    Book class, expects a title and ISBN as strings, can build a list
    (through add_rating()) of the ratings received by users.
    '''
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
        try:
            rating = int(rating)
            if not 0 <= rating <= 4:
                raise ValueError
        except ValueError:
            raise
        except TypeError:
            pass
        else:
            self.ratings.append(rating)

    def __eq__(self, other):
        return self.title == other.title and self.isbn == other.isbn

    def get_average_rating(self):
        return sum(self.ratings) / len(self.ratings)

    def __hash__(self):
        # Books will be used as keys of a dictionary in the TomeRater class
        return hash((self.title, self.isbn))

class Fiction(Book):
    '''
    Inherits from Book, the only change is that it expects an author as string
    as well
    '''
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title=self.title, author=self.author)

class Non_Fiction(Book):
    '''
    Inherits from Book, the only change is that it expects a subject and a level
    as string as well
    '''
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
    '''
    Main class, it creates users and books and stores them in separate collections
    '''
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
        ''' Checks if the user exists, marks the book as read by the user, add
        the rating to the book and increment the number of readings for the
        book by one '''
        user = self.users.get(email)
        if user == None:
            print("No user with email: {email}".format(email=email))
            return
        else:
            try:
                user.read_book(book, rating)
                book.add_rating(rating)
            except ValueError:
                print("{} is not an acceptable rating, rating must be an integer between 0 and 4 included".format(rating))
        if book in self.books:
            self.books[book] += 1
        else:
            for b in self.books.keys():
                if b.get_isbn() == book.isbn:
                    print("A book already holds this ISBN.")
                    return
            self.books[book] = 1

    def add_user(self, name, email, user_books=None):
        ''' Checks the format of email, checks if email is already used by a user,
        then adds the user, then add the books to the user (add_book_user()) if
        provided '''
        try:
            self.check_email(email)
        except ValueError as err:
            print(err.args[0])
            return
        else:
            self.users[email] = User(name, email)
        if user_books != None:
            for b in user_books:
                self.add_book_to_user(b, email)

    def check_email(self, email):
        for u in self.users.values():
            if email == u.get_email():
                raise ValueError("A user with email '{email}' already exists.".format(email=email))
        if email.count('@') != 1 or email[-4:] not in [".com", ".org", ".edu"]:
            raise ValueError("Email must have the format: 'xxxx@xxxx[.com][.edu][.org]'")

    def print_catalog(self):
        for b in self.books.keys():
            print(b)

    def print_users(self):
        for u in self.users:
            print(u)

    def most_read_book(self):
        return max(self.books, key=self.books.get)

    def highest_rated_book(self):
        # returns the book which has the best average rating across all users
        return max(self.books, key=lambda x: x.get_average_rating())

    def most_positive_user(self):
        # returns the user who has the best average rating across all books
        return max(self.users.values(), key=lambda x: x.get_average_rating())
