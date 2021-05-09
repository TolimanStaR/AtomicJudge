n = int(input())

for d in range(10**(n-1), 10**n):
	p = True
	for i in range(2, int(d**.5)+1):
		if not d % i:
			p = False
			break
	if p:
		print(d)
		exit(0)
