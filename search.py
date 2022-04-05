from Model import BooleanIRSystem
import time
from wild_card import matchwildcard

if __name__ == "__main__":
    model = BooleanIRSystem("./corpus/*")
    start_time = time.time()
    """ Accepting query as input from the user and splitting
    the query into boolean words (&,|,~) and
    query words """
    num = input("Enter 0 for normal query and 1 for wildcard query:")
    if num == "0":
        print(model.query(input("Search Query:")))
    elif num=="1":
        print(matchwildcard(input("Search WildcardQuery:")))

    # print(model.query(input("Search Query:")))
    end_time = time.time()
    total_time = end_time - start_time
    print("Total Time: ", total_time)