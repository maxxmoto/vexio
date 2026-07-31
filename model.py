import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
tf.get_logger().setLevel('ERROR')
import numpy as np
from PIL import Image
import io

IMG_SIZE = 224

# ImageNet synset ID ranges for dogs and cats (hyponyms in WordNet)
DOG_SYNSETS = {
    # Dog breeds: n02085620 (Chihuahua) to n02113978 (Mexican hairless)
    'n02085620', 'n02085782', 'n02085936', 'n02086079', 'n02086240',
    'n02086646', 'n02086910', 'n02087046', 'n02087394', 'n02088094',
    'n02088238', 'n02088364', 'n02088466', 'n02088632', 'n02089078',
    'n02089867', 'n02089973', 'n02090379', 'n02090622', 'n02090721',
    'n02091032', 'n02091134', 'n02091244', 'n02091467', 'n02091635',
    'n02092002', 'n02092339', 'n02093256', 'n02093428', 'n02093647',
    'n02093754', 'n02093859', 'n02093991', 'n02094114', 'n02094258',
    'n02094433', 'n02095314', 'n02095570', 'n02095889', 'n02096051',
    'n02096177', 'n02096294', 'n02096437', 'n02096585', 'n02097047',
    'n02097130', 'n02097209', 'n02097298', 'n02097474', 'n02097658',
    'n02098105', 'n02098286', 'n02098413', 'n02099267', 'n02099429',
    'n02099601', 'n02099712', 'n02099849', 'n02100236', 'n02100583',
    'n02100735', 'n02100877', 'n02101006', 'n02101388', 'n02101556',
    'n02102040', 'n02102177', 'n02102318', 'n02102480', 'n02102973',
    'n02104029', 'n02104365', 'n02105056', 'n02105162', 'n02105251',
    'n02105412', 'n02105505', 'n02105641', 'n02105855', 'n02106030',
    'n02106166', 'n02106382', 'n02106550', 'n02106662', 'n02107142',
    'n02107312', 'n02107574', 'n02107683', 'n02107908', 'n02108000',
    'n02108089', 'n02108422', 'n02108551', 'n02108915', 'n02109047',
    'n02109525', 'n02109961', 'n02110063', 'n02110185', 'n02110341',
    'n02110627', 'n02110806', 'n02110958', 'n02111129', 'n02111277',
    'n02111500', 'n02111889', 'n02112018', 'n02112137', 'n02112350',
    'n02112706', 'n02113023', 'n02113186', 'n02113624', 'n02113712',
    'n02113799', 'n02113978',
    # Wolves, coyotes, foxes, etc. (canids)
    'n02114367', 'n02114548', 'n02114712', 'n02114855', 'n02115641',
    'n02115913', 'n02116738', 'n02117135', 'n02119022', 'n02119789',
}

CAT_SYNSETS = {
    # Domestic cats
    'n02123045', 'n02123159', 'n02123394', 'n02123597', 'n02124075',
    # Wild cats (big cats)
    'n02125311', 'n02127052', 'n02128385', 'n02128757', 'n02128925',
    'n02129165', 'n02129604', 'n02130308',
}


class CatDogClassifier:
    def __init__(self, model_path=None):
        self.model = None
        self._load_model(model_path)

    def _load_model(self, model_path=None):
        if model_path and os.path.exists(model_path):
            self.model = tf.keras.models.load_model(model_path)
        else:
            self.model = tf.keras.applications.MobileNetV2(
                weights='imagenet',
                input_shape=(IMG_SIZE, IMG_SIZE, 3),
                include_top=True
            )

    def predict(self, image_bytes):
        img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        img = img.resize((IMG_SIZE, IMG_SIZE))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)

        predictions = self.model.predict(img_array, verbose=0)
        decoded = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=10)[0]

        cat_score = 0.0
        dog_score = 0.0
        best_cat = 0.0
        best_dog = 0.0
        details = []

        for synset, class_name, score in decoded:
            s = float(score)
            details.append({"label": class_name, "confidence": round(s * 100, 2)})

            is_cat = synset in CAT_SYNSETS
            is_dog = synset in DOG_SYNSETS

            if is_cat:
                cat_score += s
                best_cat = max(best_cat, s)
            if is_dog:
                dog_score += s
                best_dog = max(best_dog, s)

        both_cat_dog = cat_score > 0.15 and dog_score > 0.15 and best_cat > 0.05 and best_dog > 0.05

        if both_cat_dog:
            conf = round(max(cat_score, dog_score) * 100, 1)
            return {
                "label": "Кошка и собака",
                "icon": "🐱🐶",
                "description": "На фото обнаружены и кошка, и собака.",
                "confidence": conf,
                "details": details
            }
        elif cat_score > dog_score and best_cat > 0.15:
            conf = round(cat_score * 100, 1)
            return {
                "label": "Кошка",
                "icon": "🐱",
                "description": "Наши алгоритмы обнаружили характерные черты семейства кошачьих.",
                "confidence": conf,
                "details": details
            }
        elif dog_score > cat_score and best_dog > 0.15:
            conf = round(dog_score * 100, 1)
            return {
                "label": "Собака",
                "icon": "🐶",
                "description": "Структура морды и пропорции указывают на то, что это собака.",
                "confidence": conf,
                "details": details
            }
        else:
            best = max(best_cat, best_dog)
            conf = round(best * 100, 1)
            if best > 0.05:
                if cat_score > dog_score:
                    label, icon, desc = "Возможно кошка", "🐱", "Обнаружены некоторые черты кошачьих, но уверенность недостаточна."
                else:
                    label, icon, desc = "Возможно собака", "🐶", "Обнаружены некоторые черты собак, но уверенность недостаточна."
            else:
                label, icon, desc = "Не определено", "❓", "Не удалось точно определить животное на фото. Попробуйте другое изображение."
            return {"label": label, "icon": icon, "description": desc, "confidence": conf, "details": details}


try:
    finetuned_path = os.path.join(os.path.dirname(__file__), 'models', 'cat_dog_finetuned.keras')
    if os.path.exists(finetuned_path):
        classifier = CatDogClassifier(model_path=finetuned_path)
    else:
        classifier = CatDogClassifier()
except Exception:
    classifier = CatDogClassifier()

IMAGE_CAPTION_CLASSES_RU = {
    'tiger_cat': 'тигровая кошка', 'Persian_cat': 'персидская кошка', 'Siamese_cat': 'сиамская кошка',
    'Egyptian_cat': 'египетская кошка', 'cougar': 'пума', 'lynx': 'рысь',
    'leopard': 'леопард', 'snow_leopard': 'снежный барс', 'jaguar': 'ягуар',
    'lion': 'лев', 'tiger': 'тигр', 'cheetah': 'гепард',
    'Chihuahua': 'чихуахуа', 'beagle': 'бигль', 'collie': 'колли',
    'pug': 'мопс', 'boxer': 'боксёр', 'Rottweiler': 'ротвейлер', 'Doberman': 'доберман',
    'Great_Dane': 'дог', 'German_shepherd': 'немецкая овчарка', 'Siberian_husky': 'хаски',
    'golden_retriever': 'золотистый ретривер', 'Labrador_retriever': 'лабрадор',
    'poodle': 'пудель', 'dalmatian': 'далматинец', 'bulldog': 'бульдог',
    'chow': 'чау-чау', 'Pomeranian': 'шпиц', 'Samoyed': 'самоед',
    'horse': 'лошадь', 'zebra': 'зебра', 'cow': 'корова', 'sheep': 'овца',
    'goat': 'коза', 'pig': 'свинья', 'elephant': 'слон', 'giraffe': 'жираф',
    'bear': 'медведь', 'monkey': 'обезьяна', 'rabbit': 'кролик',
    'bird': 'птица', 'owl': 'сова', 'eagle': 'орёл', 'penguin': 'пингвин',
    'car': 'автомобиль', 'bus': 'автобус', 'train': 'поезд', 'airplane': 'самолёт',
    'boat': 'лодка', 'bicycle': 'велосипед', 'motorcycle': 'мотоцикл',
    'house': 'дом', 'building': 'здание', 'bridge': 'мост', 'tower': 'башня',
    'tree': 'дерево', 'flower': 'цветок', 'mountain': 'гора', 'beach': 'пляж',
    'pizza': 'пицца', 'hamburger': 'гамбургер', 'apple': 'яблоко', 'banana': 'банан',
    'guitar': 'гитара', 'piano': 'пианино', 'television': 'телевизор', 'laptop': 'ноутбук',
    'book': 'книга', 'umbrella': 'зонт', 'backpack': 'рюкзак', 'suitcase': 'чемодан',
    'sunglasses': 'очки', 'hat': 'шляпа', 'shoe': 'обувь', 'watch': 'часы',
    'person': 'человек', 'face': 'лицо', 'child': 'ребёнок', 'man': 'мужчина', 'woman': 'женщина',
    'soccer_ball': 'футбольный мяч', 'tennis_ball': 'теннисный мяч',
    'desk': 'письменный стол', 'chair': 'стул', 'bed': 'кровать',
    'cat': 'кот', 'dog': 'собака',
}

classifier = CatDogClassifier()


def predict_raw(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize((IMG_SIZE, IMG_SIZE))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)

    predictions = classifier.model.predict(img_array, verbose=0)
    decoded = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=10)[0]

    details = []
    for synset, class_name, score in decoded:
        ru = IMAGE_CAPTION_CLASSES_RU.get(class_name, class_name.lower().replace('_', ' '))
        details.append({
            'label': class_name,
            'name_ru': ru,
            'confidence': round(float(score) * 100, 2)
        })

    # Build description in Russian
    top3 = [(d['name_ru'], d['confidence']) for d in details[:3]]
    desc_parts = []
    for name, conf in top3:
        desc_parts.append(f'{name} ({conf}%)')
    description = 'На изображении вероятнее всего: ' + ', '.join(desc_parts) + '.'

    return {
        'description': description,
        'details': details
    }


def predict_image(image_bytes):
    return classifier.predict(image_bytes)
