import time


startTime = time.time() # start

a = ['123','1222','1','1234','11551155']
b = '124'

if b in a:
    print(True)
else:
    print(False)

print("Exec in %s seconds" % (time.time() - startTime)) # end time
