lst = [1,1,2,2,3,4,4,5,6]
rec =[]
output=[]
for i in lst:
    if i not in rec:
        rec.append(i)
        output.append((i,lst.count(i)))

print(output)