import json
import re


# Remove words in a list, return the removed result
def remove_words(words):
	remove_list = ['vehicle', 'is', 'includes', 'controlling', 'apparatus', 'having', \
		'10', 'comprises', 'driving', 'a', 'for', 'providing', 'supplies', 'used', \
		'operates', '20', 'the', 'device', 'control', 'controls', 'fuel', 'heat', 'includes']
	words_split = re.split('[ ().,-]', words)

	words_removed  = [word for word in words_split if word.lower() not in remove_list and not word.isdigit()]
	words_result = ' '.join(words_removed)

	return words_result


def main():
	input_file = "patents_sub.json"
	output_file = "patents_removed_sub.json"

	with open(input_file, 'r') as f:
		data = json.load(f)

	for item in data:
		item['title'] = remove_words(item['title'])
		item['snippet'] = remove_words(item['snippet'])

	with open(output_file, 'w') as f:
		f.write(json.dumps(data))


if __name__ == '__main__':
	main()
