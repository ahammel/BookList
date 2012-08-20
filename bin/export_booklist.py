import booklist
import sys

list_file = sys.argv[1]
output_file = sys.argv[2]

def main():
    blist = booklist.read_book_list(list_file)
    export_goodreads(blist, output_file)

if __name__ == "__main__":
    main()
