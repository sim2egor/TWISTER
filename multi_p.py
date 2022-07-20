import multiprocessing
import time


def worker(num, arr):
    num.value = 3.1415927
    for i in range(len(arr)):
        arr[i] = -arr[i]
    for i in range(1000) :
        num.value = i
        time.sleep(0.0001)
    print(arr[:])
    print(">>>>>>>>>>>>>>>>>>>>>")
    while arr[0]==0:
        print("hop! %s",num.value)
        num.value = num.value+1
        time.sleep(1)

if __name__ == '__main__':
    num = multiprocessing.Value('d', 0.0)
    arr = multiprocessing.Array('i', range(10))

    p = multiprocessing.Process(target=worker, name="Pr1", args=(num, arr))
    p.start()
    # for i in range(100):
    #     if i == 30:
    #         p.terminate()
    #     time.sleep(0.00015)
    #     print(" Живой ? {} {}".format(p.is_alive(),i))

    print(arr[:])
    print(p.is_alive())
    time.sleep(5)
    print("first step")
    print(arr[:])
    arr[0]=1
    p.join()
    print("---------------------------------------")
    print("Global {}".format(num.value))
    p.close()
    p = multiprocessing.Process(target=worker, name="Pr1", args=(num, arr))
    p.start()
    p.join()
