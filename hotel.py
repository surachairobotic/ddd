import sys

if __name__ == '__main__':  
  #print('Number of arguments: ' + str(len(sys.argv)))
  #print('Argument List: ' + str(sys.argv))

  price = [30, 5, 80, 15, 25, 70]
  y = [0, 0, 0, 0, 0, 0]
  if len(sys.argv) == 7:
    for i in range(1, len(sys.argv)):
      k = int(sys.argv[i])
      y[i-1] = k*price[i-1]
      print(str(k) + "\tx\t" + str(price[i-1]) + "\t=\t" + str(y[i-1]))
    print("-----------------")
    print("\t\t\t" + str(sum(y)))
  else:
    print(price)

