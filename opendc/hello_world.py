import os

# the calling, prints hello world
print("Hello, World!")

with open("hello-world.txt", "w") as f:
    f.write("Hello, World! Docker is working!\n")
