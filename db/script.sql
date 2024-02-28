CREATE TABLE User
(
    id INT PRIMARY KEY NOT NULL,
    name VARCHAR(100) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    mail VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL
);

CREATE TABLE Book
(
    id INT PRIMARY KEY NOT NULL,
    title VARCHAR(255) NOT NULL,
    type VARCHAR(100) NOT NULL,
    editor VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    release_year DOUBLE NOT NULL,
    borrowed BOOLEAN NOT NULL
);

CREATE TABLE Loan
(
    id INT PRIMARY KEY NOT NULL,
    user_id INT NOT NULL,
    book_id INT NOT NULL,
    date_start TIMESTAMP NOT NULL,
    date_end TIMESTAMP NOT NULL,
    price FLOAT NOT NULL,
    total_price FLOAT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (book_id) REFERENCES Book(id)
);