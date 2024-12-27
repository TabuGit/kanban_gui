n = [1, 2, -3, 0, 2, 5, 7, 6, 4, -5]
for i in range(len(n)):
    for j in range(len(n)-1):
        if n[j] > n[j+1]:
            n[j], n[j+1] = n[j+1], n[j]
print(n)

family = ['praprapradedushka', 'mama', 'papa', 'sestra', 'bratishka', 'dedushka']

for i in range(len(family)):
    for j in range(len(family) - 1):
        if len(family[j]) > len(family[j+1]):
            family[j], family[j+1] = family[j+1], family[j]

print(family)

nums = [-1, -4, -2, -6, 0, 1, 2, 3, 4, 5, 7, 6, 3, 3, 4, 2]

for i in range(len(nums)):
    for j in range(len(nums) - 1):
        if nums[j] < nums[j+1]:
            nums[j], nums[j+1] = nums[j+1], nums[j]

print(nums)