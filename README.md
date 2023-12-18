### Список команд:

- **add [name] [phone]**: Додати новий контакт з іменем та телефонним номером.
- **change [name] [phone]**: Змінити телефонний номер для вказаного контакту.
- **phone [name]**: Показати телефонний номер для вказаного контакту.
- **all**: Показати всі контакти в адресній книзі.
- **add-birthday [name] [date]**: Додати дату народження для вказаного контакту.
- **show-birthday [name]**: Показати дату народження для вказаного контакту.
- **birthdays**: Показати дні народження, які відбудуться протягом наступного тижня.
- **hello**: Отримати вітання від бота.
- **close або exit**: Закрити програму.

### Обробка помилок:

#### Обробка ValueError
```
Enter a command: add Eugene
Invalid command format. Use '[name] [phone]' as command arguments.
Enter a command: change Anna
Invalid command format. Use '[name] [phone]' as command arguments.
Enter a command: add Eugene +380 987554115
Invalid command format. Use '[name] [phone]' as command arguments.
Enter a command: add Eugene +380987554115
Invalid phone number format. Use a 10-digit number.
Enter a command: add-birthday Eugene 1984.06.23
Invalid birthday format. Use DD.MM.YYYY.
```
#### Обробка KeyError
```
Enter a command: phone Tanya
Contact with the name 'Tanya' doesn't exists. Use 'add [name] [new_phone]' to add.
Enter a command: change John 0965354185
Contact with the name 'John' doesn't exists. Use 'add [name] [new_phone]' to add.
Enter a command: add-birthday Eric 10.11.2005
Contact with the name 'Eric' doesn't exists. Use 'add [name] [new_phone]' to add.
```

#### Обробка IndexError
```
Enter a command: phone
Invalid command format. Use 'phone [name]' to get contact number.
