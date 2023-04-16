# Imports
import json
import sys
import os
import pandas      
import seaborn

# Variables
if(len(sys.argv) > 1):
  url = sys.argv[1]
else:
  url = 'http://localhost:3000'

# Variables
if(len(sys.argv) > 2):
  testName = sys.argv[2]
else:
  testName = 'default'

print('Running script on URL: ' + url)

# Creates the output directory if it doesn't exist
if not os.path.exists('./output'):
  os.mkdir('./output')

# Creates the new csv file and folder
if not os.path.exists(f'./output/{testName}'):
  os.mkdir(f'./output/{testName}')
 
file = open(f'./output/{testName}/performance.csv', 'w')
# Writes the headers to the csv file
file.write('index,Total Blocking Time,Performance Score\n')


# runs the action 50 times
for i in range(50):

  # Starts the lighthouse process
  os.system('lighthouse ' + url + ' --output json --output-path ./output/report.json')

  # Reads the json file
  file = open('./output/report.json', encoding='utf-8')
  data = json.load(file)

  # Gets the total blocking time and performance score
  total_blocking_time = data['audits']['total-blocking-time']['numericValue']
  performance_score = data['categories']['performance']['score']

  # Prints the results
  print('Total Blocking Time: ' + str(total_blocking_time))
  print('Performance Score: ' + str(performance_score))
  # Writes the results to the csv file
  file = open(f'./output/{testName}/performance.csv', 'a')
  file.write(str(i + 1) + ',' + str(total_blocking_time) + ',' + str(performance_score) + '\n')

# Removes the json file
os.remove('./output/report.json')

print(f'Script finished running. Check the output folder for the correct performance.csv file.')

# Analyze the results
print('Analyzing the results...')
dataset = pandas.read_csv(f'./output/{testName}/performance.csv')

# Plots the total blocking time 
plot = seaborn.lineplot(x='index', y='Total Blocking Time', data=dataset)
plot.set(xlabel='Index', ylabel='Total Blocking Time (ms)')
# Adds average line 
plot.axhline(dataset['Total Blocking Time'].mean(), color='r', linestyle='--')
plot.set_title(testName).get_figure().savefig(f'./output/{testName}/tbt-graph.png')   

# Save the average performance score
if not os.path.exists('./output/average_performance_score.csv'):
  file = open('./output/average_performance_score.csv', 'w')
  file.write('Name,Performance score\n')

average_performance_score = dataset['Performance Score'].mean()
print('Average Performance Score: ' + str(average_performance_score))
file = open('./output/average_performance_score.csv', 'a')
file.write(f'{testName},{str(average_performance_score)}\n')
file.close()

# Save the average total blocking time to a cvs file
if not os.path.exists('./output/average_total_blocking_time.csv'):
  file = open('./output/average_total_blocking_time.csv', 'w')
  file.write('Name,Total Blocking Time\n')

average_total_blocking_time = dataset['Total Blocking Time'].mean()
print('Average Total Blocking Time: ' + str(average_total_blocking_time))
file = open('./output/average_total_blocking_time.csv', 'a')
file.write(f'{testName},{str(average_total_blocking_time)}\n')
file.close()
