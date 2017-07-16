import random

print("Pick a number 1-100 and I will guess it.\n")

start = 1
end = 100
usr_response = ""
valid_response = ["Lower", "Higher", "Correct!"]
tries = 0


while usr_response != "Correct!":
    print("Im guessing your number")
    comp_guess = random.randint(start, end)
    tries += 1
    print("Is your number %s" %(comp_guess))
    print("Please respond with Lower , Higher or Correct!")
    usr_response = input()
    if usr_response not in valid_response:
        print("\nPlease Enter a valid response")
        print("Lets try again...\n")
        continue
    if usr_response == "Lower":
        comp_guess -= 1
        end = comp_guess
    if usr_response == "Higher":
        comp_guess += 1
        start = comp_guess
    if usr_response == "Correct!":
        print("\nI guessed your number in %s tries" %(tries))
