"""
Run this script to generate the .vscode/tasks.json file.
This will create a task for each day of each year, solving the first part, the second part, the example and the example for the second part of the problem.
"""


from typing import Literal
from path import Path
from dataclasses import dataclass
import json

ROOT = Path(__file__).parent

@dataclass
class Data:
    year: str
    day: str
    script_type: Literal['1', '2', 'example', 'example-2'] = '1'

    def as_vscode_task(self):
        args = [f'{self.year}/{self.day}/solution.py']
        if self.script_type == 'example':
            args.append('--example')
        elif self.script_type == '2':
            args.append('--solution2')
        elif self.script_type == 'example-2':
            args.append('--example')
            args.append('--solution2')
        return {
            'label': f'{self.year} {self.day} {self.script_type}',
            'type': 'shell',
            'command': 'python',
            'args': args,
            "options": {
                "env": {
                    "PYTHONPATH": f"{self.year}/{self.day}:./"
                }
            }

        }

tasks = []
output = {
  "version": "2.0.0",
}
for folder_year in ROOT.dirs():
    if folder_year.name.startswith("20"):
        for folder_day in folder_year.dirs():
            if folder_day.name.startswith("day"):
                if folder_day.joinpath('solution.py').exists():
                    print(f'python {folder_day.joinpath("solution.py")}')
                    tasks.append(Data(folder_year.name, folder_day.name, '1'))
                    tasks.append(Data(folder_year.name, folder_day.name, '2'))
                    tasks.append(Data(folder_year.name, folder_day.name, 'example'))
                    tasks.append(Data(folder_year.name, folder_day.name, 'example-2'))


tasks = [task.as_vscode_task() for task in tasks]
tasks.append({
    'label': 'generate tasks',
    'type': 'shell',
    'command': 'python',
    'args': ['vscode_task_generator.py'],
})

output['tasks'] = tasks

ROOT.joinpath('.vscode').makedirs_p()

with open(ROOT.joinpath('.vscode', 'tasks.json'), 'w') as f:
    json.dump(output, f, indent=4)