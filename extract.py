from sample import core
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parsing book id & user credentials")
    parser.add_argument("book_id", type=str, help="O'Reilly book id")
    parser.add_argument("user_email", type=str, help="Safari Books Online user email")
    parser.add_argument("user_password", type=str, help="Safari Books Online user password")
    args = vars(parser.parse_args())
    BookGenerator = core.BookGeneration(args["book_id"], args["user_email"], args["user_password"])
    BookGenerator.create_book()
