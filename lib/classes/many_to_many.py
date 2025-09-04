#!/usr/bin/env python3

class Author:
    def __init__(self, name):
        if isinstance(name, str) and len(name) > 0:
            self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Name should not be changeable after instantiation
        if hasattr(self, '_name'):
            pass  # Do nothing - immutable property

    def articles(self):
        """Returns a list of all articles the author has written"""
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        """Returns a unique list of magazines for which the author has contributed"""
        magazines_list = []
        for article in self.articles():
            if article.magazine not in magazines_list:
                magazines_list.append(article.magazine)
        return magazines_list

    def add_article(self, magazine, title):
        """Creates and returns a new Article instance"""
        return Article(self, magazine, title)

    def topic_areas(self):
        """Returns a unique list of categories of magazines the author has contributed to"""
        if not self.articles():
            return None
        
        categories = []
        for magazine in self.magazines():
            if magazine.category not in categories:
                categories.append(magazine.category)
        return categories


class Magazine:
    all = []  # Class variable to store all magazine instances

    def __init__(self, name, category):
        if isinstance(name, str) and 2 <= len(name) <= 16:
            self._name = name
        if isinstance(category, str) and len(category) > 0:
            self._category = category
        Magazine.all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._category = value

    def articles(self):
        """Returns a list of all articles the magazine has published"""
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        """Returns a unique list of authors who have written for this magazine"""
        authors_list = []
        for article in self.articles():
            if article.author not in authors_list:
                authors_list.append(article.author)
        return authors_list

    def article_titles(self):
        """Returns a list of titles of all articles written for this magazine"""
        articles = self.articles()
        if not articles:
            return None
        return [article.title for article in articles]

    def contributing_authors(self):
        """Returns authors who have written more than 2 articles for the magazine"""
        authors = self.contributors()
        if not authors:
            return None
        
        contributing_authors = []
        for author in authors:
            author_articles_count = len([article for article in self.articles() if article.author == author])
            if author_articles_count > 2:
                contributing_authors.append(author)
        
        return contributing_authors if contributing_authors else None

    @classmethod
    def top_publisher(cls):
        """Returns the Magazine instance with the most articles"""
        if not cls.all:
            return None
        
        max_articles = 0
        top_magazine = None
        
        for magazine in cls.all:
            article_count = len(magazine.articles())
            if article_count > max_articles:
                max_articles = article_count
                top_magazine = magazine
        
        return top_magazine if max_articles > 0 else None


class Article:
    all = []  # Class variable to store all article instances

    def __init__(self, author, magazine, title):
        if isinstance(author, Author):
            self._author = author
        if isinstance(magazine, Magazine):
            self._magazine = magazine
        if isinstance(title, str) and 5 <= len(title) <= 50:
            self._title = title
        Article.all.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        # Title should not be changeable after instantiation
        if hasattr(self, '_title'):
            pass  # Do nothing - immutable property

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if isinstance(value, Author):
            self._author = value

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        if isinstance(value, Magazine):
            self._magazine = value


# Testing code - you can run this to test your implementation
if __name__ == '__main__':
    # Clear any existing data for testing
    Article.all.clear()
    Magazine.all.clear()
    
    # Create some test instances
    print("Creating test instances...")
    
    author1 = Author("Carry Bradshaw")
    author2 = Author("Nathaniel Hawthorne")
    author3 = Author("Jane Doe")
    
    magazine1 = Magazine("Vogue", "Fashion")
    magazine2 = Magazine("AD", "Architecture")
    magazine3 = Magazine("Tech Today", "Technology")
    
    # Create articles
    article1 = Article(author1, magazine1, "How to wear a tutu with style")
    article2 = Article(author1, magazine2, "Dating life in NYC")
    article3 = Article(author2, magazine2, "Emerging trends in the NYC housing market")
    article4 = Article(author1, magazine1, "Fashion trends for spring")
    article5 = Article(author1, magazine1, "Summer fashion guide")
    article6 = Article(author1, magazine1, "Winter wardrobe essentials")
    
    # Test immutability - should fail silently
    print(f"\nTesting immutability...")
    print(f"Article1 title before: {article1.title}")
    article1.title = 500  # This should fail silently
    print(f"Article1 title after: {article1.title}")
    
    # Test some methods
    print(f"\nAuthor1 articles count: {len(author1.articles())}")
    print(f"Author1 magazines: {[mag.name for mag in author1.magazines()]}")
    print(f"Author1 topic areas: {author1.topic_areas()}")
    
    print(f"\nMagazine1 articles count: {len(magazine1.articles())}")
    print(f"Magazine1 contributors: {[author.name for author in magazine1.contributors()]}")
    print(f"Magazine1 contributing authors (>2 articles): {[author.name for author in magazine1.contributing_authors()] if magazine1.contributing_authors() else 'None'}")
    
    print(f"\nTop publisher: {Magazine.top_publisher().name if Magazine.top_publisher() else 'None'}")
    
    print("\nAll tests completed successfully!")