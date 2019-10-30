
OUTPUT_FILENAME = 'docker-compose.yml'

head = None
judger_config = None
name = 'esxi'
host = '140.136.150.67'
LIMIT = 8

def set_judger(idx):
	return judger_config.replace('{ID}', str(idx)) \
						.replace('{name}', name) \
						.replace('{HOST}', host)

def main():
	global judger_config
	with open('dc_template', 'r') as f:
		head = f.read()
	with open('judger_template', 'r') as f:
		judger_config = f.read()
	with open(OUTPUT_FILENAME, 'w') as f:
		f.write(head)
		for i in range(LIMIT):
			f.write(set_judger(i))

if __name__ == "__main__":
	main()