import random

def gen_pleasing_fn(max_fn_length, start_with_vowel=False, fn_forbidden=[]):
	"""Generates an aesthetically-pleasing filename by alternating consonants
	   and vowels."""

	# Feed this function forbidden filenames in fn_forbidden and it won't pick
	# those names when it generates a filename.

	filename = ''
	consonants = 'bcdfghjklmnpqrstvwxyz'
	vowels = 'aeiou'
	last_was_constant = start_with_vowel

	fn_is_forbidden = True
	while fn_is_forbidden:
		while len(filename) < max_fn_length:
			if last_was_constant:
				filename += random.choice(vowels)
			else:
				filename += random.choice(consonants)
			last_was_constant = not last_was_constant
		fn_is_forbidden = filename in fn_forbidden
	return filename

def fn_split(fn):
	"""Breaks a filename into the name and extension parts.""" 
	split_fn = fn.split('.')
	parts = len(split_fn)
	name = '.'.join(split_fn[:-1])
	ext = split_fn[len(split_fn) - 1]
	return name, ext

if __name__ == '__main__':
	max_fn_length = 6 # 1,157,625 uniques with alternating consonant-vowels
	print gen_pleasing_fn(max_fn_length)
	print gen_pleasing_fn(max_fn_length, start_with_vowel=True)
	print fn_split('test.jpg')
	print fn_split('martin.gale.dots.png')
	name, ext = fn_split('this.is_ugly.silly_amount_of.dots.bmp')
	print name
	print ext