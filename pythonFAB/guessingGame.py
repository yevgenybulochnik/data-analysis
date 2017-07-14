import random

print("I'm thinking of a number 1-100 can you guess it?")

start = 1
end = 100
usr_response = ""
valid_response = ["Lower", "Higher", "Correct!"]


while usr_response != "Correct!":
    print("Im guessing your number")
    comp_guess = random.randint(start, end)
    print("Is your number %s" %(comp_guess))
    print("Please respond with Lower , Higher or Correct!")
    usr_response = input()
    if usr_response not in valid_response:
        print("\nPlease Enter a valid response")
        print("Lets try again...\n")
        continue
    if usr_response == "Lower":
        end = comp_guess
    if usr_response == "Higher":
        start = comp_guess
