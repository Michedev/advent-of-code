"""
Run this script to generate the .vscode/tasks.json file.
This will create a task for each day of each year, solving the first part, the second part, the example and the example for the second part of the problem.
"""


from typing import Literal, Optional
from path import Path
from dataclasses import dataclass
import json

ROOT = Path(__file__).parent

@dataclass
class Data:
    year: str
    day: str
    script_type: Literal['1', '2', 'example', 'example-2', 'custom', 'custom-2'] = '1'
    custom_fname: Optional[str] = None

    def as_vscode_task(self):
        args = [f'-y {self.year}', f'-d {self.day.replace("day", "")}']
        if self.script_type == 'example':
            args.append('--example')
        elif self.script_type == '2':
            args.append('--solution2')
        elif self.script_type == 'example-2':
            args.append('--example')
            args.append('--solution2')
        elif self.script_type == 'custom':
            assert self.custom_fname is not None
            args.append('--custom')
            args.append(self.custom_fname)
        elif self.script_type == 'custom-2':
            assert self.custom_fname is not None
            args.append('--custom')
            args.append(self.custom_fname)
            args.append('--solution2')
        args.append('${input:verbose}')
        custom_fname_str = f'{self.custom_fname}' if self.custom_fname is not None else ''
        return {
            'label': f'{self.year} {self.day} {self.script_type} {custom_fname_str}',
            'type': 'shell',
            'command': './run',
            'args': args,
            "options": {
                "env": {
                    "PYTHONPATH": f"{self.year}/{self.day}:./"
                }
            }

        }

tasks = []
inputs = []
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
                    for custom_txt_path in folder_day.files('*.txt'):
                        if custom_txt_path.basename() != 'input.txt' or custom_txt_path.basename() != 'input_example.txt':
                            tasks.append(Data(folder_year.name, folder_day.name, 'custom', custom_txt_path.basename()))
                            tasks.append(Data(folder_year.name, folder_day.name, 'custom-2', custom_txt_path.basename()))



tasks = [task.as_vscode_task() for task in tasks]
tasks.append({
    'label': 'generate tasks',
    'type': 'shell',
    'command': 'python',
    'args': ['vscode_task_generator.py'],
})
inputs.append({
    'id': 'verbose',
    'description': 'Set verbose mode (default: false)',
    'type': 'pickString',
    'options': ['', '--verbose']
})


output['tasks'] = tasks
output['inputs'] = inputs

ROOT.joinpath('.vscode').makedirs_p()

with open(ROOT.joinpath('.vscode', 'tasks.json'), 'w') as f:
    json.dump(output, f, indent=4)