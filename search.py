from Model import BooleanIRSystem
import time

if __name__ == "__main__":
    model = BooleanIRSystem("./corpus/*")
    start_time = time.time()
    print(model.query(input("Search Query:  ")))
    end_time = time.time()
    total_time = end_time - start_time
    print("Entering Query + Searching Time: ",total_time)
        
    