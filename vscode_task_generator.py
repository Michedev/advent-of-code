"""
Run this script to generate the .vscode/tasks.json file.
This will create a task for each day of each year, solving the first part, the second part, the example and the example for the second part of the problem.
"""


from typing import Iterable, Literal, Optional
from path import Path
from dataclasses import dataclass
import json

ROOT = Path(__file__).parent

@dataclass
class Data:
    year: str
    day: str
    script_type: Literal['1', '2', 'example', 'example-2', 'custom', 'custom-2', 'doctest'] = '1'
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

    def as_vscode_launch(self):
        args = [f'-y', f'{self.year}', f'-d', f'{self.day.replace("day", "")}', '${input:verbose}']
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
        elif self.script_type == 'doctest':
            args = [ '-v', f'{self.year}/{self.day}/{self.custom_fname}']
        custom_fname_str = f'{self.custom_fname}' if self.custom_fname is not None else ''
        
        result = {
            'name': ('Doctest ' if self.script_type == 'doctest' else '') + f'{self.year} {self.day} {self.script_type} {custom_fname_str}',
            "type": "python",
            "request": "launch",
            "program": "run",
            'args': args,
            "env": {
                "PYTHONPATH": f"{self.year}/{self.day}:./"
            },
            "justMyCode": True
        }
        # if doctest, remove program and replace with module doctest
        if self.script_type == 'doctest':
            del result['program']
            result['module'] = 'doctest'
        return result

inputs = [
        {
            "id": "year",
            "type": "promptString",
            "description": "Year",
        },
        {
            "id": "day",
            "type": "promptString",
            "description": "Day",
        },
        {
            "id": "solutiontype",
            "type": "pickString",
            "options": [
                "",
                "-2"
            ],
            "description": "Solve problem 1 or 2",
        },
        {
            "id": "is_example",
            "type": "pickString",
            "options": [
                "",
                "-e"
            ],
            "description": "Use example input or not"
        },
    {
    'id': 'verbose',
    'description': 'Set verbose mode (default: false)',
    'type': 'pickString',
    'options': ['', '--verbose']
}
]
tasks_json = {
  "version": "2.0.0",
  "inputs": inputs,
}

launch_json = {
        "version": "0.2.0",
    "configurations": [
        {
            "name": "Launch solution advent of code",
            "type": "python",
            "request": "launch",
            "program": "run",
            "args": [
                "-y", "${input:year}",
                "-d", "${input:day}",
                "${input:solutiontype}",
                "${input:is_example}"
            ],
            "justMyCode": True
        }
    ],
    "inputs": inputs

}

def iter_python_scripts() -> Iterable[Path]:
    for folder_year in ROOT.dirs():
        if folder_year.name.startswith("20"):
            for folder_day in folder_year.dirs():
                if folder_day.name.startswith("day"):
                    if folder_day.joinpath('solution.py').exists():
                        yield from folder_day.files('*.py')  # this part doesn't support subdirs yet

def find_doctestable_scripts():
    for script in iter_python_scripts():
        with open(script, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if '>>> ' in line:
                    yield script
                    break
                    


def find_all_aoc_scripts():
    vscode_aoc_scripts = []
    for folder_year in ROOT.dirs():
        if folder_year.name.startswith("20"):
            for folder_day in folder_year.dirs():
                if folder_day.name.startswith("day"):
                    if folder_day.joinpath('solution.py').exists():
                        print(f'python {folder_day.joinpath("solution.py")}')
                        vscode_aoc_scripts.append(Data(folder_year.name, folder_day.name, '1'))
                        vscode_aoc_scripts.append(Data(folder_year.name, folder_day.name, '2'))
                        vscode_aoc_scripts.append(Data(folder_year.name, folder_day.name, 'example'))
                        vscode_aoc_scripts.append(Data(folder_year.name, folder_day.name, 'example-2'))
                        for custom_txt_path in folder_day.files('*.txt'):
                            if custom_txt_path.basename() not in ('input.txt', 'input_example.txt') and "input" in custom_txt_path.basename():
                                vscode_aoc_scripts.append(Data(folder_year.name, folder_day.name, 'custom', custom_txt_path.basename()))
                                vscode_aoc_scripts.append(Data(folder_year.name, folder_day.name, 'custom-2', custom_txt_path.basename()))
    return vscode_aoc_scripts

vscode_aoc_scripts = find_all_aoc_scripts()



tasks_json['tasks'] = [task.as_vscode_task() for task in vscode_aoc_scripts] + [
    {
        'label': 'generate tasks',
        'type': 'shell',
        'command': 'python',
        'args': ['vscode_task_generator.py'],
    }
]

launch_json['configurations'] = [task.as_vscode_launch() for task in vscode_aoc_scripts] + [
        {
            "name": "Launch solution advent of code",
            "type": "python",
            "request": "launch",
            "program": "run",
            "args": [
                "-y", "${input:year}",
                "-d", "${input:day}",
                "${input:solutiontype}",
                "${input:is_example}",
                "${input:verbose}"
            ],
            "justMyCode": True
        },
        {
            "name": "Generate tasks",
            "type": "python",
            "request": "launch",
            "program": "vscode_task_generator.py",
            "justMyCode": True
        } 
    ]

doctestable_scripts = [Data(script_path.parent.parent.name, script_path.parent.name, 'doctest', script_path.basename()) for script_path in find_doctestable_scripts()]

launch_json['configurations'] += [task.as_vscode_launch() for task in doctestable_scripts]

ROOT.joinpath('.vscode').makedirs_p()

with open(ROOT.joinpath('.vscode', 'tasks.json'), 'w') as f:
    json.dump(tasks_json, f, indent=4)
with open(ROOT.joinpath('.vscode', 'launch.json'), 'w') as f:
    json.dump(launch_json, f, indent=4)