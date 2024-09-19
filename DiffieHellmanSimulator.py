# Title: Diffie-Hellman Simulator 
# Author: Mat Fairchild 
# Version 1.0


from random import randint, choice

# Diffie-Hellman requires "safe primes to function correctly".
# A safe prime is any prime that can be expressed as 2n+1, where n is also a prime.
# This generates a small number of safe primes.
# In a real DH, these numbers would be MUCH bigger.
def prime_gen():
    safe_primes = [3, 5, 7]

    for n in safe_primes:
        y = 2 * n + 1
        prime = True
        for _ in safe_primes:
            if y % _ == 0:
                prime = False
        if prime == True and y not in safe_primes:
            safe_primes.append(y)
            
    return safe_primes

safe_primes = prime_gen()

# In order to get the variable g for our equation, we must select a number that is a primitive root of p, where p is the safe prime we selected.
# A primitive root is a number that, when we iterate through every power from 0 to p-1, will give a remainder (modulus) that encompasses every integer from 1 through p.
# There's no specific formula for this, so I use a pseudo random number, and try it until I find one that works.

def g_calc(n):
    g = randint(1, n - 1)
    prim_rt = []
    c = 0
    while True:
        if len(prim_rt) == n - 1:
            return g
        elif (g**c % n) not in prim_rt:
            prim_rt.append(g**c % n)
            c += 1
        else:
            g = randint(1, n - 1)
            c = 0
            prim_rt = []

# To make things interesting, I made sure p was larger than 7.

def p_choice(s):
    while True:
        p = choice(s)
        if (
            p != 3 and
            p != 5 and
            p != 7
        ):
            return p    

# each party's secret number must also be a prime number, and smaller than p.

def secret_choice(s, p):
    while True:
        sc = choice(s)
        if sc <= p:
            return sc
    
# this iterates through until the two parties have a shared secret number.
# notice that alice never interacts with bob's secret number and vice versa.
while True:       
    p = p_choice(safe_primes)
    g = g_calc(p)
    
    alice_secret = secret_choice(safe_primes, p)
    bob_secret = secret_choice(safe_primes, p)
    a = g**alice_secret % p
    b = g**bob_secret % p
    alice_s = b**a % p
    bob_s = a**b % p
    if bob_s == alice_s and bob_s != 1:
        break

# This is just for flavor. Mallory would have a tough time guessing any of the secret numbers.
print(f'Alice and Bob say, "p = {p}, g = {g}."')
print(f'Alice says, "A = {a}."')
print(f'Bob says, "B = {b}."')
print('Alice and Bob say, "We know our secret key."')
print('Mallory says, "I have no idea what you\'re talking about."')
print(f'The secret key is {bob_s}.')