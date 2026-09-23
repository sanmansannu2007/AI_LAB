a=[10,20,30]
k=int(input("enter key"))
found=False
for i in range(len(a)):
    if a[i]==k:
        print("key found at position",i+1)
        found=True
        break
if not found:
    print("not found")
