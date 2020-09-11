#Krish Ganotra

def string_times(str, n):
  return str*n

def front_times(str, n):
  return str[:3]*n

def string_bits(str):
  return str[::2]

def string_splosion(str):
  return ''.join(str[:i] for i in range(len(str)+1))

def last2(str):
  return sum(str[i:i+2]==str[-2:] for i in range(len(str)-2))

def array_count9(nums):
  return nums.count(9)

def array_front9(nums):
  return 9 in nums[:4]

def array123(nums):
  return '1, 2, 3' in str(nums)

def string_match(a, b):
  return sum(a[i:i+2]==b[i:i+2] for i in range(len(a)-1))

def make_bricks(small, big, goal):
  return 5*min(big, goal//5)+small>=goal
  # return not(big*5+small<goal or goal%5>small)
  # return small>=goal%5 and big*5+small>=goal

def lone_sum(a, b, c):
  return sum(x for x in [a,b,c] if [a,b,c].count(x)<=1)

def lucky_sum(a, b, c):
  # return sum(x for i,x in enumerate([a,b,c]) if 13 not in [a,b,c][:i+1])
  return sum([a,b,c][i] for i in range(3) if 13 not in [a,b,c][:i+1])
  # return sum((y:=[a,b,c])[i] for i in range(3) if 13 not in y[:i+1])

def no_teen_sum(a, b, c):
  return sum(x for x in [a,b,c] if x not in[13,14,17,18,19])

def round_sum(a, b, c): #int and round seems stupid but maybe necessary
  return sum(int(round(x,-1)) for x in [a,b,c])

def close_far(a, b, c): # be better
  return (abs(a-b)<=1 and abs(b-c)>1 and abs(a-c)>1) or (abs(a-c)<=1 and abs(b-c)>1 and abs(a-b)>1)

def make_chocolate(small, big, goal): #be better -- shouldn't need walrus operator
  return ((val:=goal-5*min(goal//5, big)),-1)[small<val]
  # val = goal-5*min(goal//5, big)
  # return (val,-1)[small<val]
  #

def double_char(str):
  return ''.join(x*2 for x in str)

def count_hi(str):
  return str.count('hi')

def cat_dog(str):
  return str.count('cat')==str.count('dog')

def count_code(str): #range(len(str)-x) is bum
  return sum(str.count('co'+chr(k)+'e') for k in range(65,123))
  # return sum(str[i:i+2]=='co' and str[i+3]=='e' for i in range(len(str)-3))
  # return sum(str.count(f'co{chr(k)}e') for k in range(65,91))

def end_other(a, b):
  return a.lower()==b.lower()[-len(a)+0:] or b.lower()==a.lower()[-len(b)+0:]
  # return (a:=a.lower())==(b:=b.lower())[-len(a)+0:] or b==a[-len(b)+0:]
  # return a.lower()[-min(len(a),len(b))+0:]==b.lower()[-min(len(a), len(b))+0:]
  # return a.lower()[x:=-min(len(a),len(b))+0:]==b.lower()[x:]


#doesn't work when starts with xyz and ends with . e.g. 'xyzaaaaaa.'
#range(len(str)-x) is bum. True in is stupid (any function)?? be better
def xyz_there(str):
  return str.count('xyz')-str.count('.xyz')>0

def count_evens(nums):
  return sum(i%2==0 for i in nums)

def big_diff(nums):
  return max(nums)-min(nums)

def centered_average(nums):
  return sum(sorted(nums)[1:-1])/(len(nums)-2)

def sum13(nums):
  return sum(x for i,x in enumerate(nums) if x!=13 and (nums[i-1]!=13 or i==0))

def sum67(nums):
  return sum(x for i,x in enumerate(nums) if 6 not in nums[:i+1] or 7 in nums[[j for j,z in enumerate(nums) if z==6 and j<=i][-1]:i])

def has22(nums):
  return '2, 2' in str(nums)
