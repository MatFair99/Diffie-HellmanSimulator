# Title: Prime Number Generator 
# Author: Mat Fairchild 
# Version 1.0

def main():
    # Set max size of prime
    while True:
        try:
            max_size = int(input("Select a maximum range for the primes you want to generate: "))
            if max_size > 1:
                break
            else:
                raise TypeError
        except(ValueError, TypeError):
            print("Range must be a positive number greater than 1.")
    
    primes = prime_gen(max_size)
    safe_primes = safe_prime_gen(primes)
    
    c = 0
    while True:
        try:
            with open(f"primes_{max_size}.txt", 'x') as file:
                for n in primes:
                    file.write(str(n))
                    file.write("\n")
                file.close
            with open(f"safe_primes_{max_size}.txt", 'x') as file2:
                for n in safe_primes:
                    file2.write(str(n))
                    file2.write("\n")
                file2.close
            break
        except FileExistsError:
            c += 1
            break
    
    if c != 0:
        while True:
            try:
                with open(f"primes_{max_size}({c}).txt", 'x') as file:
                    for n in primes:
                        file.write(str(n))
                        file.write("\n")
                    file.close
                with open(f"safe_primes_{max_size}({c}).txt", 'x') as file2:
                    for n in safe_primes:
                        file2.write(str(n))
                        file2.write("\n")
                    file2.close
                break
            except FileExistsError:
                c += 1
    
    print("Text files have been saved in current directory.")     
            

# Seed primes with 2, since it is the only even prime, and also the only one that will not return 0 on a mod of p-1
# Iterate through every prime number less than or equal to half the candidate, if mod == 0, it can't be prime
def prime_gen(mx):
    primes = [2]
    prime_candidate = 3
    while prime_candidate <= mx:
        prime = True
        for n in primes:
            if n > int(round(prime_candidate / 2)):
                break 
            elif prime_candidate % n == 0:
                prime = False
                break
        if prime == True:
            primes.append(prime_candidate)
        prime_candidate += 1
    return primes

#TODO
def safe_prime_gen(p):
    safe_primes = []
    for n in p:
        if (n-1) / 2 in p:
            safe_primes.append(n)
    return safe_primes

if __name__ == "__main__":
    main()

