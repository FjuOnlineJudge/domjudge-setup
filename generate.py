
import argparse
import string
import random

parser = argparse.ArgumentParser(description='Compress problem folder', epilog='')
group = parser.add_mutually_exclusive_group()
group.add_argument('-j', '--judgehost', type = int, default = 1, help='the nmuber of judgehosts')
args = parser.parse_args()

head = None
judgerConfig = None
footer = None
outputFile = 'docker-compose.yml'
hostname = 'domserver'
judgerCount = args.judgehost
judgerPasswd = ''.join(random.choice(string.ascii_letters) for _ in range(17))

def set_judger(idx):
	return judgerConfig.replace('{ID}', f"{idx}") \
						.replace('{HOST}', hostname) \
						.replace('{PASSWD}', judgerPasswd)

def main():
	global judgerConfig
	with open('template/head_template', 'r') as f:
		head = f.read()
	with open('template/judger_template', 'r') as f:
		judgerConfig = f.read()
	with open('template/footer_template', 'r') as f:
		footer = f.read()
	with open(outputFile, 'w') as f:
		f.write(head)
		for i in range(judgerCount):
			f.write(set_judger(i))
		f.write(footer)

if __name__ == "__main__":
	main()