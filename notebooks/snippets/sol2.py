if os.path.isfile(shape_path) == True:
    print('File found.')

else:
    print('Please enter a valid file path.')

# In python, we can omit the == True, as the os.path.isfile() method evaluates to a boolean, and python understands this to mean if true is retrned. Similarly, we can use the 
# not logical operator

if not os.path.isfile(shape_path):
    print('Please enter a valid file path.')

else:
    print('File found.')
