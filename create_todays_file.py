""" Uses template.py to create a new file for today's date. """

import datetime

from pathlib import Path


def main():
    today = datetime.date.today()
    today_str = today.strftime('%Y/%d')

    if (new_file := Path(__file__).parent / f'{today_str}.py').exists():
        print(f'Target file already exists: {new_file.as_uri()}')
        return

    template = Path(__file__).parent / 'template.py'

    with template.open() as f:
        template_contents = f.read()

    new_contents = (template_contents
                    .replace('<YYYY>', str(today.year))
                    .replace('<D>', str(today.day))
                    .replace('<DD>', str(today.day).zfill(2)))

    if not new_file.parent.exists():
        new_file.parent.mkdir(parents=True)
        print(f'Created dir {new_file.parent.as_uri()}')

    with new_file.open('w') as f:
        f.write(new_contents)

    print(f'Created {new_file.as_uri()}')


if __name__ == '__main__':
    main()
