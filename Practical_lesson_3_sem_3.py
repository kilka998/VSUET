import tensorflow as tf
from keras import Sequential, Input
from keras.callbacks import EarlyStopping
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
import ssl
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

ssl._create_default_https_context = ssl._create_unverified_context


def load_and_preprocess_cifar10():
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
    
    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0
    
    x_val = x_train[:5000]
    y_val = y_train[:5000]
    x_train_final = x_train[5000:]
    y_train_final = y_train[5000:]
    
    return (x_train_final, y_train_final), (x_val, y_val), (x_test, y_test)


def create_cnn_model(use_dropout=False, dropout_rate=0.5):
    model = Sequential()
    model.add(Input(shape=(32, 32, 3)))
    
    model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D((2, 2)))
    if use_dropout:
        model.add(Dropout(dropout_rate))
    
    model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D((2, 2)))
    if use_dropout:
        model.add(Dropout(dropout_rate))
    
    model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D((2, 2)))
    if use_dropout:
        model.add(Dropout(dropout_rate))
    
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(BatchNormalization())
    if use_dropout:
        model.add(Dropout(dropout_rate))
    model.add(Dense(128, activation='relu'))
    model.add(BatchNormalization())
    if use_dropout:
        model.add(Dropout(dropout_rate))
    model.add(Dense(10, activation='softmax'))
    
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model


def train_model(model, x_train, y_train, x_val, y_val, epochs=20):
    early_stop = EarlyStopping(
        monitor='val_accuracy',
        patience=10,
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
    print("Практическая работа №3")
    print("Исследование сверточной нейронной сети для классификации CIFAR-10\n")
    
    print("Загрузка данных CIFAR-10...")
    (x_train, y_train), (x_val, y_val), (x_test, y_test) = load_and_preprocess_cifar10()
    
    print(f"Размер обучающей выборки: {x_train.shape}")
    print(f"Размер валидационной выборки: {x_val.shape}")
    print(f"Размер тестовой выборки: {x_test.shape}\n")
    
    print("Эксперимент 1: Обучение модели БЕЗ Dropout")
    model_no_dropout = create_cnn_model(use_dropout=False)
    print("\nАрхитектура модели:")
    model_no_dropout.summary()
    
    history_no_dropout = train_model(
        model_no_dropout, x_train, y_train, x_val, y_val, epochs=20
    )
    
    _, test_acc_no_dropout = model_no_dropout.evaluate(
        x_test, y_test, verbose=0
    )
    print(f"\nТочность на тестовой выборке (без Dropout): {test_acc_no_dropout * 100:.2f}%")
    
    dropout_rates = [0.25, 0.5, 0.75]
    results_with_dropout = {}
    
    print("Эксперимент 2: Обучение модели С Dropout")    
    for dropout_rate in dropout_rates:
        print(f"\n--- Обучение с Dropout rate = {dropout_rate} ---")
        model_with_dropout = create_cnn_model(use_dropout=True, dropout_rate=dropout_rate)
        
        history_with_dropout = train_model(
            model_with_dropout, x_train, y_train, x_val, y_val, epochs=20
        )
        
        _, test_acc = model_with_dropout.evaluate(x_test, y_test, verbose=0)
        results_with_dropout[dropout_rate] = {
            'model': model_with_dropout,
            'history': history_with_dropout,
            'test_accuracy': test_acc
        }
        print(f"Точность на тестовой выборке (Dropout={dropout_rate}): {test_acc * 100:.2f}%")
    
    print("СРАВНЕНИЕ РЕЗУЛЬТАТОВ")
    print(f"Без Dropout: {test_acc_no_dropout * 100:.2f}%")
    for rate, result in results_with_dropout.items():
        print(f"С Dropout (rate={rate}): {result['test_accuracy'] * 100:.2f}%")
    
    all_results = [('Без Dropout', test_acc_no_dropout)]
    all_results.extend([(f'Dropout={rate}', result['test_accuracy']) 
                       for rate, result in results_with_dropout.items()])
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
    for rate, result in results_with_dropout.items():
        plt.plot(result['history'].history['val_accuracy'], 
                label=f'Dropout={rate}', linewidth=2)
    plt.title('Сравнение точности на валидации')
    plt.xlabel('Эпохи')
    plt.ylabel('Точность на валидации')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(2, 2, 4)
    configs = ['Без Dropout'] + [f'Dropout={rate}' for rate in dropout_rates]
    accuracies = [test_acc_no_dropout] + [results_with_dropout[rate]['test_accuracy'] 
                                          for rate in dropout_rates]
    colors = ['red' if acc < 0.92 else 'green' for acc in accuracies]
    bars = plt.bar(configs, [acc * 100 for acc in accuracies], color=colors, alpha=0.7)
    plt.axhline(y=92, color='black', linestyle='--', label='Целевая точность (92%)')
    plt.title('Точность на тестовой выборке')
    plt.ylabel('Точность (%)')
    plt.xticks(rotation=45, ha='right')
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
        print("В данном случае Dropout не улучил результаты. Возможно, модель не страдала от переобучения")
    
    print("\nОптимальный коэффициент Dropout:")
    best_dropout_rate = max(results_with_dropout.items(), 
                           key=lambda x: x[1]['test_accuracy'])[0]
    print(f"Лучший коэффициент: {best_dropout_rate}")
    print(f"Точность с этим коэффициентом: "
          f"{results_with_dropout[best_dropout_rate]['test_accuracy'] * 100:.2f}%")
    
    print("\nДостижение целевой точности (92%):")
    if best_acc >= 0.92:
        print(f"Целевая точность достигнута! ({best_acc * 100:.2f}%)")
    else:
        print(f"Целевая точность не достигнута. Лучший результат: {best_acc * 100:.2f}%")
        print("Рекомендации:")
        print("1) Увеличить количество эпох обучения\n2) Добавить data augmentation\n3) Увеличить глубину сети или количество фильтров\n4) Попробовать другие оптимизаторы (например, Adam с learning rate decay)")


if __name__ == "__main__":
    main()

