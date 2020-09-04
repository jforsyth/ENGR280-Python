from util import generate_random_int_list


#Diagnostic #1: Complete the methods student_min, student_max, and runner_up

# write a function to determine the minimum value in the list
# Don't use the min() function. That's too easy :)
def student_min(nums):
    ##### Your code here #####
    return


# write a function to determine the maximum value in the list
# Don't use the max() function. That's too easy :)
def student_max(nums):
    ##### Your code here #####
    return


# write a function that determines the 2nd highest value in the list. Not #1, but the runner up :)
def runner_up(nums):
    ##### Your code here #####
    return


if __name__ == "__main__":
    print('Welcome to the program!')

    print('Now generating a random length list of random integers....')
    rands = generate_random_int_list(10, 100)

    print('Random List is:')
    print(rands)

    print('Now running your code to determine the minimum value...')
    print('Maximum value is ' + str(student_max(rands)))
    print('Minimum value is ' + str(student_min(rands)))
    print('Second Highest value is ' + str(runner_up(rands)))

    print('All done!')
