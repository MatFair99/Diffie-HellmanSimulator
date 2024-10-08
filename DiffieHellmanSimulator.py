# Title: Diffie-Hellman Simulator 
# Author: Mat Fairchild 
# Version 2.0

''' CHANGELOG:
    * Wrote independent script for generating prime numbers more efficiently and accurately.
    * Wrote "main" function for better code organization/convention compliance.
    * Included call from PrimeGen to allow direct access of a primes list.
        - Creates more overhead, especially once max_size is greater than 5,000
        - next subversion will include option to import files generated by PrimeGen.py
        - May eventually write PrimeGen in a compiled language for better efficiency
    * Removed p_choice function, as it is unnecessary with a larger pool, and better defined "safe primes".
    * More descriptive comments to increase usability as a teaching tool.
    * Increased minimum for range
    * Misunderstood that a and b had to be prime as well. This is incorrect and has been removed.
    * Loaded the dice, so to speak, to avoid Alice and Bob from having the same private key


'''

from random import randint, choice
from PrimeGen import prime_gen, safe_prime_gen
from time import sleep

def main():
    while True:
        try:
            max_size = int(input("Select a maximum range from 10 to 5,000: ").replace(",", "").strip()) # remove commas and leading/trailing whitespace
            if 5000 >= max_size >= 10: # anything larger than 5,000 greatly increases overhead
                break
            else:
                raise TypeError
        except(ValueError, TypeError):
            print("Range must be between 10 and 5,000.")
    
    primes = prime_gen(max_size)
    safe_primes = safe_prime_gen(primes)
    
    # Generate a "random" prime, "p", and a primitive root of it, "g."
    # These numbers are shared by the two parties performing DH,
    # and are necessary for the calculations to work correctly.
    p = choice(safe_primes)
    g = g_calc(p)
    
    # This is a safety loop. It *shouldn't* be necessary, but wanted to catch edge cases.
    # This loop just ensures that the derived "shared" key is, in fact, equal.
    while True:       
        alice_secret = secret_choice(p)
        bob_secret = secret_choice(p)
        a = g**alice_secret % p
        b = g**bob_secret % p
        alice_s = b**a % p
        bob_s = a**b % p
        if (
            bob_s == alice_s and
            bob_secret != alice_secret and
            bob_s != 1 # we don't want a secret key of 1. It's technically valid, but cryptographically very weak
            ):
            break
    
    # Little scnario to illustrate how Diffie-Hellman produces a shared secret key.
    # Notice that Alice never interacts with Bob's Key and vice versa.
    # Mallory is a malicious actor who has eavesdropped into the conversation
    print('Alice says, "Hey Bob, I want to talk to you in private."')
    sleep(0.5)
    print('Bob says, "Sure. Let\'s make a cipher. \nWe can use Diffie-Hellman to generate a secret key to decode our cipher."')
    sleep(0.5)
    print('Mallory whispers, "Secrets? Ciphers? Oh, boy, I bet I could have some fun with these two."')
    sleep(0.5)
    print('Alice says, "Okay! We\'ll need to come up with a special prime number, called \'p\' and a second number that\'s a primitive root, \'g\'."')
    sleep(0.5)
    print('Bob says, "Primitive roots are neat. \nWhen you raise it to every power from 0 to that prime minus 1, and then divide by that prime number, ')
    print('the remainders of that division, or modulos, will include every integer from 1 to one less than that prime.')
    sleep(0.5)
    print('Alice says, "That\'s right! On the count of three, let\'s come up with p and g."')
    sleep(0.5)
    print("1...")
    sleep(1)
    print("2...")
    sleep(1)
    print("3!")
    sleep(1)
    print(f'Alice and Bob say, "p = {p}, g = {g}."')
    sleep(0.5)
    print(f'Alice says, "A = {a}."')
    sleep(0.5)
    print(f"Alice's secret key is {alice_secret}.") ### included Alice's Secret Key
    sleep(0.5)
    print(f'Bob says, "B = {b}."')
    sleep(0.5)
    print(f"Bob's secret key is {bob_secret}.") ### also included Bob's
    sleep(0.5)
    print('Alice and Bob say, "We know our secret key."')
    sleep(0.5)
    print('Mallory says, "I have no idea what you\'re talking about."')
    sleep(0.5)
    print(f'The secret key is {bob_s}.')



# In order to get the variable g for our equation, we must select a number that is a primitive root of p, where p is the safe prime we selected.
# A primitive root is a number that, when we iterate through every power from 0 to p-1, will give a remainder (modulus) that encompasses every integer from 1 through p.
# There's no specific formula for this, so I use a pseudo random number, and try it until I find one that works.
def g_calc(p):
    g = randint(1, p - 1)
    prim_rt = []
    c = 0 # Counter to iterate through each exponent from 0 to one less than "p"
    while True: # Loop through this function until "broken", in this case, by a return call
        if len(prim_rt) == p - 1:
            return g
        elif (g**c % p) not in prim_rt:
            prim_rt.append(g**c % p)
            c += 1
        else:
            g = randint(1, p - 1)
            c = 0
            prim_rt = []


# each party's secret number must also be smaller than p.
def secret_choice(p):
    while True:
        sc = randint(1, p - 1)
        if sc < p:
            return sc
    
if __name__ == "__main__":
    main()


