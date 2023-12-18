""" Uses template.py to create a new file for today's date. """

import datetime

from pathlib import Path


def main(day=None, *, year=None, date=None):
    if day and year and date:
        raise RuntimeError('Cannot specify all 3 params, choose either day+year or date!')

    now = datetime.datetime.now()
    if day and year:
        date = datetime.date(year, 12, day)
    elif day:
        date = datetime.date(now.year, 12, day)
    elif year:
        raise RuntimeError('It is ambiguous if you do not specify the date!')

    date = date or datetime.date.today()  # Otherwise today

    today_str = date.strftime('%Y/%d')

    if (new_file := Path(__file__).parent / f'{today_str}.py').exists():
        print(f'Target file already exists: {new_file.as_uri()}')
        return

    template = Path(__file__).parent / 'template.py'

    with template.open() as f:
        template_contents = f.read()

    new_contents = (template_contents
                    .replace('<YYYY>', str(date.year))
                    .replace('<D>', str(date.day))
                    .replace('<DD>', str(date.day).zfill(2)))

    if not new_file.parent.exists():
        new_file.parent.mkdir(parents=True)
        print(f'Created dir {new_file.parent.as_uri()}')

    with new_file.open('w') as f:
        f.write(new_contents)

    print(f'Created {new_file.as_uri()}')


if __name__ == '__main__':
    main()
