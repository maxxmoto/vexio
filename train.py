"""
Дообучение (fine-tuning) модели на датасете кошек и собак.

Способ 1 (рекомендуемый): скачать подвыборку Cats vs Dogs через tensorflow-datasets
    pip install tensorflow-datasets
    python train.py --quick

Способ 2: скачать датасет с Kaggle вручную:
    https://www.kaggle.com/c/dogs-vs-cats/data
    Распаковать в data/cats_and_dogs/train/cats/ и data/cats_and_dogs/train/dogs/
    python train.py

После обучения модель сохраняется в models/cat_dog_finetuned.keras
и автоматически загружается app.py вместо предобученной ImageNet модели.
"""

import os, sys, argparse
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
tf.get_logger().setLevel('ERROR')

IMG_SIZE = 224
BATCH_SIZE = 16
EPOCHS = 3
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


def train_from_local(data_dir):
    ds_train = tf.keras.utils.image_dataset_from_directory(
        os.path.join(data_dir, 'train'),
        image_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        label_mode='binary'
    )
    val_dir = os.path.join(data_dir, 'val') if os.path.exists(os.path.join(data_dir, 'val')) else os.path.join(data_dir, 'train')
    ds_val = tf.keras.utils.image_dataset_from_directory(
        val_dir,
        image_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        label_mode='binary'
    )
    return ds_train, ds_val


def train_from_tfds(quick=True):
    import tensorflow_datasets as tfds
    split = 'train[:10%]' if quick else 'train[:80%]'
    val_split = 'train[10%:12%]' if quick else 'train[80%:]'

    ds = tfds.load('cats_vs_dogs', split={'train': split, 'val': val_split}, as_supervised=True)

    def preprocess(image, label):
        image = tf.image.resize(image, (IMG_SIZE, IMG_SIZE))
        image = tf.keras.applications.mobilenet_v2.preprocess_input(image)
        return image, label

    ds_train = ds['train'].map(preprocess).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
    ds_val = ds['val'].map(preprocess).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
    return ds_train, ds_val


def build_model():
    base = tf.keras.applications.MobileNetV2(
        weights='imagenet',
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        pooling='avg'
    )
    base.trainable = False

    model = tf.keras.Sequential([
        base,
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    return model


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--quick', action='store_true', help='Быстрое обучение на 10% данных')
    parser.add_argument('--data', help='Путь к локальному датасету')
    args = parser.parse_args()

    if args.data:
        print(f'Загрузка данных из {args.data}...')
        ds_train, ds_val = train_from_local(args.data)
    elif args.quick:
        print('Быстрое обучение на подвыборке Cats vs Dogs...')
        print('(Первый запуск скачает ~150 МБ данных)')
        ds_train, ds_val = train_from_tfds(quick=True)
    else:
        local = os.path.join(PROJECT_DIR, 'data', 'cats_and_dogs')
        if os.path.exists(local):
            ds_train, ds_val = train_from_local(local)
        else:
            print('Локальные данные не найдены.')
            print('Запустите: python train.py --quick')
            sys.exit(1)

    model = build_model()
    print('Начало обучения...')
    history = model.fit(ds_train, validation_data=ds_val, epochs=EPOCHS, verbose=1)

    acc = history.history['val_accuracy'][-1]
    print(f'\nТочность на валидации: {acc:.2%}')

    model_dir = os.path.join(PROJECT_DIR, 'models')
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, 'cat_dog_finetuned.keras')
    model.save(model_path)
    print(f'Модель сохранена: {model_path}')
    print('app.py автоматически загрузит её при следующем запуске.')
