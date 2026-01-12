import csv
import json
from datetime import datetime

def add_expense(expenses_list):
    category = input('Введите категорию расходов: ')
    date_input = input('Введите дату расходов (дд.мм.гггг) или нажмите Enter для текущей даты: ')
    if date_input:
        date = date_input
    else:
        date = datetime.now().strftime('%d.%m.%Y')
    
    while True:
        amount_of_expenses = input('Введите сумму расходов: ')
        try:
            amount_of_expenses = float(amount_of_expenses)
            break
        except ValueError:
            print('Ошибка! Введите число для суммы расходов.')
    
    new_expense = [category, amount_of_expenses, date]
    expenses_list.append(new_expense)
    
    exprence = input('Продолжить ввод данных? (Да/Нет): ').lower()
    if exprence in ['нет', 'no', 'н']:
        return expenses_list
    
    return expenses_list


def show_expenses(expenses_list):
    if not expenses_list:
        print('Нет данных о расходах')
        return
    
    print('\nКак отсортировать расходы?')
    print('1. По дате (новые сверху)')
    print('2. По сумме (от больших к меньшим)')
    print('3. По категории (алфавит)')
    print('4. Без сортировки')
    
    choice = input('Выберите вариант (1-4): ')
    
    sorted_expenses = expenses_list.copy()
    
    if choice == '1':
        try:
            sorted_expenses.sort(key=lambda x: datetime.strptime(x[2], '%d.%m.%Y'), reverse=True)
            print('\n=== Расходы (сортировка по дате, новые сверху) ===')
        except ValueError as e:
            print(f'Ошибка в данных: {e}. Показываю без сортировки.')
    
    elif choice == '2':
        sorted_expenses.sort(key=lambda x: x[1], reverse=True)
        print('\n=== Расходы (сортировка по сумме, от больших) ===')
    
    elif choice == '3':
        sorted_expenses.sort(key=lambda x: x[0].lower())
        print('\n=== Расходы (сортировка по категории, А-Я) ===')
    
    elif choice == '4':
        print('\n=== Все расходы (без сортировки) ===')
    
    else:
        print('Неверный выбор. Показываю без сортировки.')
        print('\n=== Все расходы ===')
    
    print(f'{"№":<3} | {"Категория":<15} | {"Сумма":>10} | {"Дата":<10}')
    print('-' * 50)
    
    for i, expense in enumerate(sorted_expenses, 1):
        print(f'{i:<3} | {expense[0]:<15} | {expense[1]:>10.2f} | {expense[2]:<10}')
  
    print('-' * 50)
    total = sum(expense[1] for expense in sorted_expenses)
    print(f'Всего записей: {len(sorted_expenses)}')
    print(f'Общая сумма: {total:.2f}')

def show_expenses_by_date(expenses_list):
    if not expenses_list:
        print('Нет данных о расходах.')
        return
    date = input('Введите дату расходов (дд.мм.гггг) или нажмите Enter для текущей даты: ')
    if date == '':
        date = datetime.now().strftime('%d.%m.%Y')
    
    print(f'=== Расходы за {date} ===')
    found = False
    for expense in expenses_list:
        if expense[2] == date:
            print(f'{expense[0]:<15} | {expense[1]:>10.2f}')
            found = True
    
    if not found:
        print('Расходы за указанную дату не найдены.')

def show_total_statistics(expenses_list):
    if not expenses_list:
        print('Нет данных о расходах.')
        return
    
    total = 0
    for expense in expenses_list:
        total += expense[1]
    
    print('=== Общая статистика ===')
    print(f'Всего расходов: {len(expenses_list)} записей')
    print(f'Общая сумма: {total:.2f}')
    print(f'Средний расход на запись: {total/len(expenses_list):.2f}')

def load_from_file():
    try:
        with open('expense.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            data = []
            for row in reader:
                if len(row) >= 3:
                    row[1] = float(row[1])
                    data.append(row)
            return data
    except FileNotFoundError:
        return []
    except StopIteration:
        return []

def save_to_file(expenses_list):
    try:
        with open('expense.csv', 'r', newline='', encoding='utf-8') as file:
            file_exists = True
    except FileNotFoundError:
        file_exists = False
    
    with open('expense.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Категория', 'Сумма', 'Дата'])
        writer.writerows(expenses_list)
    with open('expense.json', 'w', encoding='utf-8') as file:
        json.dump(expenses_list, file, ensure_ascii=False)

def show_file_data():
    try:
        with open('expense.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            print('Данные из файла expense.csv:')
            print(f'{header[0]:<15} | {header[1]:>10}')
            print('-' * 30)
            
            total = 0
            count = 0
            for row in reader:
                print(f'{row[0]:<15} | {row[1]:>10}')
                total += float(row[1])
                count += 1
            
            print('-' * 30)
            print(f'Всего записей: {count}')
            print(f'Общая сумма: {total:.2f}')
    except FileNotFoundError:
        print('Файл expense.csv не найден.')
    except StopIteration:
        print('Файл пустой или содержит только заголовок.')

def show_category_statistics(expenses_list):
    if not expenses_list:
        print('Нет данных о расходах.')
        return
    print('\n=== Простая статистика по категориям ===')
    category_count = {}
    category_total = {}

    for expense in expenses_list:
        category = expense[0]
        amount = expense[1]

        if category in category_count:
            category_count[category] += 1
            category_total[category] += amount
        else:
            category_count[category] = 1
            category_total[category] = amount
    
    print('\n1. Категории по количеству записей:')
    for category, counts in category_count.items():
        print(f'{category:<15}: {counts:>10} записей')
    print('\n2. Категории по сумме расходов:')

    for category, total in category_total.items():
        print(f'{category:<15}: {total:>10.2f}руб.')

    if category_count:
        most_common = max(category_count, key=category_count.get)
        print(f'\n3. Самая частая категория: {most_common} ({category_count[most_common]} записей)')

    if category_total:
        most_expensive = max(category_total, key=category_total.get)
        print(f'4. Самая затратная категория: {most_expensive} ({category_total[most_expensive]:.2f} руб.)')
    


data = load_from_file()

while True:
    print('\n=== Менеджер расходов ===')
    print('1. Добавить расход')
    print('2. Показать все расходы')
    print('3. Статистика за день')
    print('4. Общая статистика')
    print('5. Сохранить и выйти')
    print('6. Показать данные из файла')
    print('7. Статистика по категориям')
    
    choice = input('Выберите пункт меню: ')
    
    if choice == '1':
        data = add_expense(data)
    elif choice == '2':
        show_expenses(data)
    elif choice == '3':
        show_expenses_by_date(data)
    elif choice == '4':
        show_total_statistics(data)
    elif choice == '5':
        save_to_file(data)
        print(f'Данные сохранены в файлы expense.csv и expense.json.')
        break
    elif choice == '6':
        show_file_data()
    elif choice == '7':
        show_category_statistics(data) 
    else:
        print('Неверный выбор. Пожалуйста, выберите пункт меню.')