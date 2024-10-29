import os
import dill
import json
import pandas as pd

# Путь к проекту
path = os.environ.get('PROJECT_PATH', '.')

def predict():
    # Загрузка обученной модели
    model_path = f'{path}/data/models'
    latest_model = sorted([f for f in os.listdir(model_path) if f.endswith('.pkl')])[-1]  # Последняя сохраненная модель
    with open(f'{model_path}/{latest_model}', 'rb') as file:
        model = dill.load(file)

    # Путь для загрузки тестовых данных и сохранения предсказаний
    test_data_path = f'{path}/data/test'
    predictions_path = f'{path}/data/predictions'
    os.makedirs(predictions_path, exist_ok=True)

    # Список для хранения предсказаний
    predictions_list = []

    # Обработка каждого JSON файла в папке data/test
    test_files = [f for f in os.listdir(test_data_path) if f.endswith('.json')]
    for file in test_files:
        file_path = os.path.join(test_data_path, file)
        
        try:
            # Загрузка данных из JSON
            with open(file_path, 'r') as f:
                car_data = json.load(f)
            
            # Создаем DataFrame для предсказания
            data = pd.DataFrame.from_dict([{
                'fuel': car_data.get('fuel'),
                'odometer': car_data.get('odometer'),
                'state': car_data.get('state'),
                'title_status': car_data.get('title_status'),
                'transmission': car_data.get('transmission'),
                'model': car_data.get('model'),
                'short_model': car_data.get('model', '').split(' ')[0],  # Берём первую часть модели как short_model
                'age_category': 'new' if car_data.get('year') > 2013 else ('old' if car_data.get('year') < 2006 else 'average'),
                'year': car_data.get('year')
            }])

            # Выполняем предсказание
            y_pred = model.predict(data)

            # Добавляем результаты в список
            predictions_list.append({
                'id': car_data.get('id'),
                'price': car_data.get('price'),
                'predicted_price_cat': y_pred[0]  # Предсказанная категория цены
            })

            print(f"Предсказания для {file} успешно выполнены.")

        except json.JSONDecodeError:
            print(f"Ошибка: файл {file} содержит некорректный JSON.")
        except ValueError as e:
            print(f"Ошибка при обработке файла {file}: {e}")

    # Объединение предсказаний в DataFrame и сохранение в CSV
    if predictions_list:
        all_predictions = pd.DataFrame(predictions_list)
        all_predictions.to_csv(f'{predictions_path}/predictions.csv', index=False)
        print("Все предсказания успешно сохранены в data/predictions/predictions.csv")

if __name__ == '__main__':
    predict()