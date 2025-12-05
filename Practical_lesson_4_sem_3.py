import tensorflow as tf
from keras import Sequential
from keras.callbacks import EarlyStopping
from keras.layers import Embedding, LSTM, Dense, Dropout
import ssl
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

ssl._create_default_https_context = ssl._create_unverified_context


def load_and_preprocess_imdb(num_words=10000, maxlen=500):
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.imdb.load_data(num_words=num_words)
    
    x_train = tf.keras.preprocessing.sequence.pad_sequences(x_train, maxlen=maxlen)
    x_test = tf.keras.preprocessing.sequence.pad_sequences(x_test, maxlen=maxlen)
    
    x_val = x_train[:5000]
    y_val = y_train[:5000]
    x_train_final = x_train[5000:]
    y_train_final = y_train[5000:]
    
    return (x_train_final, y_train_final), (x_val, y_val), (x_test, y_test)


def create_lstm_model(use_dropout=False, dropout_rate=0.2, recurrent_dropout=0.2, embedding_dim=128, lstm_units=64):
    model = Sequential()
    model.add(Embedding(10000, embedding_dim, input_length=500))
    
    if use_dropout:
        model.add(LSTM(lstm_units, dropout=dropout_rate, recurrent_dropout=recurrent_dropout))
    else:
        model.add(LSTM(lstm_units))
    
    if use_dropout:
        model.add(Dropout(dropout_rate))
    
    model.add(Dense(1, activation='sigmoid'))
    
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    return model


def train_model(model, x_train, y_train, x_val, y_val, epochs=20):
    early_stop = EarlyStopping(
        monitor='val_accuracy',
        patience=5,
        restore_best_weights=True,
        verbose=1
    )
    
    history = model.fit(
        x_train, y_train,
        epochs=epochs,
        batch_size=128,
        validation_data=(x_val, y_val),
        callbacks=[early_stop],
        verbose=1
    )
    
    return history


def main():
    print("Практическая работа №4")
    print("Исследование рекуррентной нейронной сети для классификации отзывов IMDB\n")
    
    print("Загрузка данных IMDB...")
    (x_train, y_train), (x_val, y_val), (x_test, y_test) = load_and_preprocess_imdb()
    
    print(f"Размер обучающей выборки: {x_train.shape}")
    print(f"Размер валидационной выборки: {x_val.shape}")
    print(f"Размер тестовой выборки: {x_test.shape}\n")
    
    print("Эксперимент 1: Обучение модели БЕЗ Dropout")
    model_no_dropout = create_lstm_model(use_dropout=False)
    print("\nАрхитектура модели:")
    model_no_dropout.summary()
    
    history_no_dropout = train_model(
        model_no_dropout, x_train, y_train, x_val, y_val, epochs=20
    )
    
    _, test_acc_no_dropout = model_no_dropout.evaluate(
        x_test, y_test, verbose=0
    )
    print(f"\nТочность на тестовой выборке (без Dropout): {test_acc_no_dropout * 100:.2f}%")
    
    dropout_configs = [
        {'dropout': 0.2, 'recurrent_dropout': 0.0},
        {'dropout': 0.3, 'recurrent_dropout': 0.2},
        {'dropout': 0.4, 'recurrent_dropout': 0.3},
        {'dropout': 0.5, 'recurrent_dropout': 0.3},
    ]
    results_with_dropout = {}
    
    print("Эксперимент 2: Обучение модели С Dropout")
    for i, config in enumerate(dropout_configs, 1):
        print(f"\n--- Обучение с Dropout={config['dropout']}, RecurrentDropout={config['recurrent_dropout']} ---")
        model_with_dropout = create_lstm_model(
            use_dropout=True, 
            dropout_rate=config['dropout'],
            recurrent_dropout=config['recurrent_dropout']
        )
        
        history_with_dropout = train_model(
            model_with_dropout, x_train, y_train, x_val, y_val, epochs=20
        )
        
        _, test_acc = model_with_dropout.evaluate(x_test, y_test, verbose=0)
        config_key = f"dropout={config['dropout']}, rec_dropout={config['recurrent_dropout']}"
        results_with_dropout[config_key] = {
            'model': model_with_dropout,
            'history': history_with_dropout,
            'test_accuracy': test_acc,
            'dropout': config['dropout'],
            'recurrent_dropout': config['recurrent_dropout']
        }
        print(f"Точность на тестовой выборке ({config_key}): {test_acc * 100:.2f}%")
    
    print("СРАВНЕНИЕ РЕЗУЛЬТАТОВ")
    print(f"Без Dropout: {test_acc_no_dropout * 100:.2f}%")
    for config_key, result in results_with_dropout.items():
        print(f"С Dropout ({config_key}): {result['test_accuracy'] * 100:.2f}%")
    
    all_results = [('Без Dropout', test_acc_no_dropout)]
    all_results.extend([(config_key, result['test_accuracy']) 
                       for config_key, result in results_with_dropout.items()])
    best_config, best_acc = max(all_results, key=lambda x: x[1])
    
    print(f"\nЛучший результат: {best_config} - {best_acc * 100:.2f}%")
    
    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 2, 1)
    plt.plot(history_no_dropout.history['accuracy'], label='Обучение (без Dropout)')
    plt.plot(history_no_dropout.history['val_accuracy'], label='Валидация (без Dropout)')
    plt.title('Точность: модель без Dropout')
    plt.xlabel('Эпохи')
    plt.ylabel('Точность')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(2, 2, 2)
    plt.plot(history_no_dropout.history['loss'], label='Обучение (без Dropout)')
    plt.plot(history_no_dropout.history['val_loss'], label='Валидация (без Dropout)')
    plt.title('Потери: модель без Dropout')
    plt.xlabel('Эпохи')
    plt.ylabel('Потери')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(2, 2, 3)
    plt.plot(history_no_dropout.history['val_accuracy'], label='Без Dropout', linewidth=2)
    for config_key, result in results_with_dropout.items():
        plt.plot(result['history'].history['val_accuracy'], 
                label=config_key, linewidth=2)
    plt.title('Сравнение точности на валидации')
    plt.xlabel('Эпохи')
    plt.ylabel('Точность на валидации')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(2, 2, 4)
    configs = ['Без Dropout'] + list(results_with_dropout.keys())
    accuracies = [test_acc_no_dropout] + [results_with_dropout[key]['test_accuracy'] 
                                          for key in results_with_dropout.keys()]
    colors = ['red' if acc < 0.85 else 'green' for acc in accuracies]
    bars = plt.bar(range(len(configs)), [acc * 100 for acc in accuracies], color=colors, alpha=0.7)
    plt.axhline(y=85, color='black', linestyle='--', label='Целевая точность (85%)')
    plt.title('Точность на тестовой выборке')
    plt.ylabel('Точность (%)')
    plt.xticks(range(len(configs)), configs, rotation=45, ha='right')
    plt.legend()
    plt.grid(True, axis='y')
    
    for bar, acc in zip(bars, accuracies):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{acc*100:.2f}%',
                ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()
    
    print("АНАЛИЗ РЕЗУЛЬТАТОВ")
    print("\nЭффект Dropout:")
    if test_acc_no_dropout < max([r['test_accuracy'] for r in results_with_dropout.values()]):
        print("Dropout улучшил обобщающую способность модели. Это указывает на то, что модель без Dropout переобучалась")
    else:
        print("В данном случае Dropout не улучшил результаты. Возможно, модель не страдала от переобучения")
    
    print("\nОптимальный коэффициент Dropout:")
    best_dropout_config = max(results_with_dropout.items(), 
                           key=lambda x: x[1]['test_accuracy'])
    print(f"Лучшая конфигурация: {best_dropout_config[0]}")
    print(f"Точность с этой конфигурацией: "
          f"{best_dropout_config[1]['test_accuracy'] * 100:.2f}%")
    
    print("\nДостижение целевой точности (85%):")
    if best_acc >= 0.85:
        print(f"Целевая точность достигнута! ({best_acc * 100:.2f}%)")
    else:
        print(f"Целевая точность не достигнута. Лучший результат: {best_acc * 100:.2f}%")
        print("Рекомендации:")
        print("1) Увеличить количество эпох обучения\n2) Увеличить размер embedding или количество LSTM units\n3) Добавить больше LSTM слоев\n4) Попробовать другие оптимизаторы (например, Adam с learning rate decay)\n5) Увеличить размер словаря или maxlen последовательностей")


if __name__ == "__main__":
    main()

