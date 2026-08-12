#!/usr/bin/python3
from Crypto.Hash import SHA256
import random
import os 

jurrasic = os.getenv("ANACONDA")

forest = """
/~~~~~~~~~-----
\\~~~~~~~~~~~<#:>-<
"""

random.seed(','.join(jurrasic.split('A')))

def bypass_them_all(user_input):
    input_arr = user_input.split(',')
    if len(input_arr) != 0x64:
        print("Oops! Your input is shorter than a T-Rex's arms. Make it exactly 0x64 in length!")
        return None

    print("[+] Level 1/4 PASSED! You've made it past the ancient ruins!")

    story_data = open("story.txt").read()

    try:
        int_arr = []
        non_int_arr = []
        for i in input_arr:
            if i.isdigit():
                if 0 <= int(i) < len(story_data):
                    int_arr.append(int(i))
            else:
                try:
                    non_int_arr.append(i)
                    int_arr.append(ord(i))
                except Exception as e:
                    print("Value is based on single character or a any number.")

        if non_int_arr:
            r = random.randrange(0, len(non_int_arr))
            if (r % 2):
                print(f"Looks like we've got some non-integers: {non_int_arr}.")
                print("We'll convert these to integers using their ord() values to use them as an index.")
                
                for i in range(len(non_int_arr)):
                    random_non_int = non_int_arr[random.randrange(0,len(non_int_arr))]
                    print(f"For example: {random_non_int} to {ord(random_non_int)}")
    except ValueError:
        print("Oops! Something went wrong. Please make sure your input is valid.")
        return False

    print("[+] Level 2/4 PASSED! You've dodged the quicksand!")

    user_input = ''.join([story_data[i] for i in int_arr])

    secret = ''.join([chr(rnd) for rnd in [random.randrange(0, 0x64) for _ in range(random.randrange(0, 0x64))]])
    sha256hash = SHA256.new(secret.encode()).hexdigest()

    try:
        if sha256hash != user_input[:0x40]:
            print("SHA256 mismatch! The temple doors remain sealed shut!")
            print(user_input)
            return False
        
        print("[+] Level 3/4 PASSED! The ancient script aligns!")

        charset_check = [x == y for (x, y) in zip(forest, user_input[0x40:])]
    except IndexError:
        print("Hold up! Some of these numbers are practically comets—too big to handle right now!")
        return False

    if not all(charset_check):
        print("We can't see the snake... Are we blind, or did it just slither past us?")
        return False

    print("[+] Level 4/4 PASSED! You've unlocked the final chamber!")

    return True


if __name__ == '__main__':
    print("Swing through the jungle of filters to snatch the flag!")  
    print("Feed me a list of values separated by commas, and let's see if you make it out alive!")

    for i in range(5):
        if not bypass_them_all(input().strip()):
            print(f"Try again, explorer! You have {4 - i} attempts left.")
        else:
            print(open("flag.txt").read())
            break