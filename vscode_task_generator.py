from typing import Literal
from path import Path
from dataclasses import dataclass
import json

ROOT = Path(__file__).parent

@dataclass
class Data:
    year: str
    day: str
    script_type: Literal['1', '2', 'example'] = '1'

    def as_vscode_task(self):
        return {
            'label': f'{self.year} {self.day} {self.script_type}',
            'type': 'shell',
            'command': 'python',
            'args': [f'{self.year}/{self.day}/solution.py']
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

tasks = [task.as_vscode_task() for task in tasks]
output['tasks'] = tasks

ROOT.joinpath('.vscode').makedirs_p()

with open(ROOT.joinpath('.vscode', 'tasks.json'), 'w') as f:
    json.dump(output, f, indent=4)