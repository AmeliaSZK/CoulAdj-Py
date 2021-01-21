import sys

print("\nSTARTING hello.py")

name = sys.argv[1] if len(sys.argv) > 1  else "World"
print("Hello {}!".format(name))