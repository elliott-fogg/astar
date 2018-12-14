# 'w' means Write-Only (Existing file of the same name will be deleted)
# 'r' means Read-Only
# 'a' means Append (Write to an existing file)
# 'r+' means Read and Write

f = open('testfile','w')
f.write("This is a test\n")
f.write("This is ANOTHER test\n")
f.close

f = open('testfile','r')
print(f.readline(),end="")
print(f.readline(),end="")
