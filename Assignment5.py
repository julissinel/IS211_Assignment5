import argparse
import csv
import os



parser = argparse.ArgumentParser()
parser.add_argument("--url",help="Add URL",default=None)
parser.add_argument("--servers",type=int,help="Add Servers",default=None)
args = parser.parse_args()

#Queue Class
class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

class Server:
    def __init__(self):
        self.time_remaining = 0
        self.current_task = None

    def tick(self):
        self.current_task = None

    def busy(self):
        if self.current_task != None:
            return True
        else:
            return False

    def start_next(self,new_task):
        self.current_task = new_task
        self.time_remaining = new_task.get_time()

#class Request
class Request:
    def __init__(self, time, timeSpent):
        self.timestamp = time
        self.timespent = timeSpent

    def get_stamp(self):
        return self.timestamp

    def get_time(self):
        return self.timespent

    def wait_time(self):
        return self.timespent

#SimulateOneServer

def SimulateOneServer(inputData):

    server_queue = Queue()
    waiting_times = []
    server = Server()

    for row in inputData:
        time_value = int(inputData[row]['Time_Value'])
        time_spent = int(inputData[row]['Time_Spent'])
        request = Request(time_value,time_spent)
        server_queue.enqueue(request)

        if (not server.busy()) and (not server_queue.is_empty()):
            next_request = server_queue.dequeue()
            waiting_times.append(next_request.timespent)
            server.start_next(next_request)
        server.tick()
    results = sum(waiting_times)/len(waiting_times)
    return results

#Simulate multiple servers

def SimulateManyServers(inputData,servers):
    server_queue = Queue()
    waiting_times = []
    server = Server()

    server_list = []

    for x in range(servers):
        server_list.append(Server())

    for k in server_list:
        for row in inputData:
            time_value = int(inputData[row]['Time_Value'])
            time_spent = int(inputData[row]['Time_Spent'])

            request = Request(time_value, time_spent)

            server_queue.enqueue(request)

            if (not server.busy()) and (not server_queue.is_empty()):
                next_request = server_queue.dequeue()
                waiting_times.append(next_request.timespent)
                server.start_next(next_request)

            server.tick()

    results = sum(waiting_times) / len(waiting_times)
    return results

def main():
    database = {}
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    with open(BASE_DIR +'/Desktop/requests.csv') as data:
        reader = csv.reader(data, delimiter=',')
        for row, item in enumerate(reader):
            database [row] = {
                'Time_Value': item[0],
                'Time_Spent': item[2],
                'File': item[1]
             }

    servers = args.servers if args.servers else input("Enter # of servers: ")

    if int(servers)>1:
        response = SimulateManyServers(database,int(servers))
        print("Process Time for {0} servers is {1}".format(servers,response))
    else:
        response = SimulateOneServer(database)
        print("Process time for one server is {0}".format(response))

if __name__ == '__main__':
    main()