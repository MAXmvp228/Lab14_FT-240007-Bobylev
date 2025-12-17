import os
import logging
from datetime import datetime

"""Базовая настройка системы логирования"""
# Создаем форматер с датой, временем, уровнем и сообщением
formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)-8s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')

# Настраиваем основной логгер
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Очищаем существующие обработчики (чтобы избежать дублирования)
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# Файловый обработчик
file_handler = logging.FileHandler('program.log', encoding='utf-8', mode='a')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

# Добавляем обработчики к логгеру
logger.addHandler(file_handler)

def log_program_start():
    """Логирование начала работы программы"""
    logger.info("=" * 50)
    logger.info("ПРОГРАММА ЗАПУЩЕНА")
    logger.info(f"Время запуска: {datetime.now()}")
    logger.info("=" * 50)

def log_program_end():
    """Логирование завершения работы программы"""
    logger.info("=" * 50)
    logger.info("ПРОГРАММА ЗАВЕРШЕНА")
    logger.info(f"Время завершения: {datetime.now()}")
    logger.info("=" * 50)

def log_user_input(input_type, value):
    """Логирование ввода пользователя"""
    logger.info(f"ВВОД [{input_type}]: {value}")

def log_program_output(output_type, value):
    """Логирование вывода программы"""
    logger.info(f"ВЫВОД [{output_type}]: {value}")

def log_operation(operation, details):
    """Логирование операций программы"""
    logger.info(f"ОПЕРАЦИЯ [{operation}]: {details}")

def log_error(error_msg, context=""):
    """Логирование ошибок"""
    logger.error(f"ОШИБКА [{context}]: {error_msg}")


log_program_start()
# Загружаем тест
filename = "test.txt"
"""Загружает тест из файла"""
if not os.path.exists(filename):
    print(f"Файл {filename} не найден!")
else:
    with open(filename, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    if len(lines) < 6:
        print("Неверный формат файла!")
        log_error("Неверный формат файла!","Файл содержит недостаточно данных для тестирования")

    try:
        # Читаем количество вопросов
        total_questions = int(lines[0])
        test_data = []
        idx = 1

        for i in range(total_questions):
            if idx >= len(lines):
                break

            question = lines[idx]
            idx += 1
            log_operation('Запись данных теста из файла', f"Вопрос: {question}")
            if idx >= len(lines):
                break

            n_answers = int(lines[idx])
            idx += 1
            log_operation('Запись данных теста из файла', f"Количество ответов: {n_answers}")
            if idx >= len(lines):
                break

            correct_answer = int(lines[idx]) - 1  # переводим в 0-индекс
            idx += 1
            log_operation('Запись данных теста из файла', f"Правильный ответ: {correct_answer}")

            answers = []
            for j in range(n_answers):
                if idx >= len(lines):
                    break
                answers.append(lines[idx])
                log_operation('Запись данных теста из файла', f"Вариант ответа: {lines[idx]}")
                idx += 1

            test_data.append({'question': question,'answers': answers,'correct': correct_answer})

    except (ValueError, IndexError) as e:
        print(f"Ошибка при чтении файла: {e}")
        log_error(f"Ошибка при чтении файла: {e}","Файл содержит не соответствующие данные")

    """Запускает тестирование"""
    correct_count = 0

    for i, q in enumerate(test_data, 1):
        print(f"{q['question']}")
        log_program_output("Вопрос",f"{q['question']}")

        # Выводим варианты ответов
        for j, answer in enumerate(q['answers'], 1):
            print(f"  {j}){answer}")
            log_program_output("Вариант ответа", f"  {j}){answer}")

        # Запрашиваем ответ
        while True:
            try:
                user_answer = input(f"Введите номер ответа (1-{len(q['answers'])}): ").strip()
                log_program_output("Запрос ответа у пользователя", f"Введите номер ответа (1-{len(q['answers'])}): ")
                log_user_input("Ответ пользователя",user_answer)
                if not user_answer:
                    print("Пожалуйста, введите номер ответа")
                    log_error("Пожалуйста, введите номер ответа.",f"Ввод неверных данных: {user_answer}")
                    continue

                user_choice = int(user_answer) - 1  # переводим в 0-индекс

                if 0 <= user_choice < len(q['answers']):
                    break
                else:
                    print(f"Введите число от 1 до {len(q['answers'])}")
                    log_error(f"Введите число от 1 до {len(q['answers'])}", f"Ввод неверных данных: {user_answer}")
            except ValueError:
                print("Пожалуйста, введите число.")
                log_error("Пожалуйста, введите число.", f"Ввод неверных данных: {user_answer}")

        # Проверяем ответ
        if user_choice == q['correct']:
            print("Правильно!")
            log_program_output("Проверка ответа пользователя","Правильно!")
            correct_count += 1
            log_operation("Увеличение количества правильных ответов",correct_count)
        else:
            print(f"Неправильно. Правильный ответ: {q['correct'] + 1}){q['answers'][q['correct']]}")
            log_program_output("Проверка ответа пользователя",f"Неправильно. Правильный ответ: {q['correct'] + 1}){q['answers'][q['correct']]}")
        print()

    # Выводим итоги
    print("ТЕСТ ЗАВЕРШЕН")
    log_program_output("Подведение итогов","ТЕСТ ЗАВЕРШЕН")
    print(f"Количество правильных ответов: {correct_count} из {total_questions}")
    log_program_output("Подведение итогов", f"Количество правильных ответов: {correct_count} из {total_questions}")
    print(f"Процент выполнения: {int((correct_count / total_questions) * 100)}%")
    log_program_output("Подведение итогов", f"Процент выполнения: {int((correct_count / total_questions) * 100)}%")

    log_program_end()