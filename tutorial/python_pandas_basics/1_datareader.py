from pandas_datareader import data


mylist = [1, 5, 6, 3, 36, 2, 6, 22, 9]

mylist2 = mylist
mylist3 = mylist.copy()
print(mylist, mylist2, mylist3)

len(mylist)

mylist[0]

mylist.append('new number')

mylist[-1]

mylist[0:2]

mylist.remove(6)

mylist.pop(0)



print(mylist, mylist2, mylist3)



mydict = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
len(mydict)

mydict['b']

mydict['f']=6

mydict.pop('a')

del mydict['b']

mydict['f']=8

mydict['g']=[1, 2, 3, 4, 5]

mydict['g'][0:2]

mydict['h']={'h1': 'x', 'h2': 'y', 'h3': 'z', 'h4': 'Z'}

mydict['h']['h1']=['xyz', {'key1': 10, 'key2': 20}, 'def']

mydict['h']

mydict['h']['h1']

mydict['h']['h1'][1]['key2']
