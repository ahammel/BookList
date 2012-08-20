from booklist import parsers, exporters
import sys

list_file = sys.argv[1]
output_file = sys.argv[2]

def main():
    blist = parsers.read_book_list(list_file)
    exporters.export_goodreads(blist, output_file)

if __name__ == "__main__":
    main()
