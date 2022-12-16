my_str = 'hello'

my_list = ['apple', 'one', 'he']

if any(my_str.startswith(match := item) for item in my_list):
    # 👇️ this runs
    print('string starts with at least one of the elements from the list')

    print(match)  # 👉️ 'he'